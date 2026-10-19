#!/usr/bin/env python3
"""Structural + Agent Skills spec conformance validator for skills/*/SKILL.md.

Gate 1 of 2. Run from anywhere:

    python tests/validate_skill_inventory.py
    python tests/validate_skill_inventory.py --strict   # warnings also fail

Standard library only. PyYAML is used opportunistically as a cross-check when it
happens to be installed, but is never required.

Exit codes: 0 = pass, 1 = failure (errors, or warnings under --strict), 2 = harness error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------
# Configuration -- the repo's portability invariants, in one place.
# --------------------------------------------------------------------------------------

SKILLS_DIRNAME = "skills"
SKILL_FILENAME = "SKILL.md"

#: Top-level frontmatter keys permitted by the Agent Skills spec *as this repo uses it*.
#: Anything else is an error: non-OpenCode hosts silently ignore unknown keys, so an
#: unknown key is a key that does not work everywhere.
ALLOWED_TOP_LEVEL_KEYS = ("name", "description", "license", "compatibility", "metadata")

EXPECTED_LICENSE = "Apache-2.0"

#: metadata must be exactly these keys, in exactly this order, all string values.
EXPECTED_METADATA_KEYS = ("repo", "version", "updated", "keys-required")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

MAX_BODY_LINES = 500
DEFAULT_MAX_BODY_TOKENS = 5000
CHARS_PER_TOKEN = 4  # crude but conventional approximation

MAX_DESCRIPTION_CHARS = 1024
WARN_DESCRIPTION_CHARS = 300  # Codex budgets the whole skill list at 8,000 chars

REFERENCE_DIRNAME = "references"

#: Tokens that indicate the skill can complete its workflow on material the user already
#: has. Used for the zero-hard-dependency heuristic.
ZERO_DEPENDENCY_TOKENS = ("curl", "fetch", "web", "paste", "csv", "html", "url")

#: Phrases that would signal a hard dependency if found in an "inputs" position.
HARD_DEPENDENCY_HINTS = ("api key", "api-key", "apikey", "paid account", "requires a key")

#: Negators that turn a hard-dependency phrase into a disclaimer. "zero API keys" and
#: "no API keys" are the repo's own wording, not a dependency claim.
NEGATORS = ("no ", "not ", "zero ", "without ", "never ", "n't ", "free of ", "free from ")

FORBIDDEN_FRONTMATTER = (("context: fork", "context: fork"),)
FORBIDDEN_DIRS = ("hooks",)

LINK_RE = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")

ERROR, WARN = "ERROR", "WARN"


# --------------------------------------------------------------------------------------
# Minimal YAML-subset frontmatter parser
# --------------------------------------------------------------------------------------


class FrontmatterError(Exception):
    """Raised when the frontmatter block cannot be parsed as the supported subset."""


def _strip_inline_comment(value: str) -> str:
    """Drop a trailing ` # comment` from a plain scalar.

    Only whitespace-preceded `#` counts, so `https://x/#frag` and `C#` survive.
    """
    match = re.search(r"\s#", value)
    if match:
        return value[: match.start()].rstrip()
    return value.rstrip()


def _unquote(token: str) -> str:
    """Return (value, consumed_characters) for a quoted scalar starting at token[0]."""
    quote = token[0]
    if quote not in "\"'":
        return _strip_inline_comment(token), len(token)

    body: list[str] = []
    index = 1
    while index < len(token):
        char = token[index]
        if char == "\\" and quote == '"' and index + 1 < len(token):
            nxt = token[index + 1]
            body.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, nxt))
            index += 2
            continue
        if char == quote:
            if quote == "'" and index + 1 < len(token) and token[index + 1] == "'":
                body.append("'")  # '' is an escaped apostrophe
                index += 2
                continue
            return "".join(body), index + 1
        body.append(char)
        index += 1
    raise FrontmatterError("unterminated quoted string: %s..." % token[:40])


def _scalar(raw: str) -> str:
    value, _consumed = _unquote(raw.strip())
    return value


def _split_key_value(text: str) -> tuple[str, str]:
    """Split `key: value` on the first `:` that is followed by a space or end of line."""
    match = re.match(r"^([^:#]+?)\s*:\s*(.*)$", text)
    if not match:
        raise FrontmatterError("not a `key: value` line: %r" % text[:60])
    return match.group(1).strip(), match.group(2).strip()


def parse_frontmatter(text: str) -> tuple[dict, str, str | None]:
    """Parse the leading `---` fenced frontmatter block.

    Supports exactly what this repo's frontmatter uses: scalar keys, quoted or plain
    string scalars, and one level of nested string-to-string mapping (`metadata:`).

    Returns (data, body, error_message_or_None). `data` may be partially populated even
    when `error_message` is set, so callers can report as much as possible at once.
    """
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {}, text, "no frontmatter block (file must start with a `---` line)"

    try:
        end = next(
            (i for i in range(1, len(lines)) if lines[i].strip() == "---"),
            None,
        )
    except StopIteration:  # pragma: no cover - generator handles it
        end = None
    if end is None:
        return {}, text, "unterminated frontmatter block (no closing `---`)"

    block = lines[1:end]
    body = "\n".join(lines[end + 1 :])

    # Reject YAML constructs the minimal parser would otherwise mis-handle, BEFORE
    # parsing. Previously `description: {a: 1}` (flow mapping) and tab-indented
    # children parsed "successfully" into the wrong shape and the gate reported a
    # clean PASS. A conformance gate that false-passes malformed input is worse
    # than no gate, so unsupported syntax is an error, never a best-effort guess.
    for lineno, raw in enumerate(block, start=2):
        indent = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in indent:
            return {}, body, (
                "line %d: YAML forbids tabs in indentation. Use spaces." % lineno
            )
        stripped = raw.strip()
        if stripped.startswith("#"):
            continue
        if ":" in stripped:
            value = stripped.split(":", 1)[1].strip()
            if value[:1] in ("{", "["):
                return {}, body, (
                    "line %d: YAML flow style (%s) is not supported by the minimal "
                    "parser. Use block style." % (lineno, "mapping" if value[0] == "{" else "sequence")
                )
            if value[:1] in ("|", ">"):
                return {}, body, (
                    "line %d: YAML block scalars are not supported by the minimal "
                    "parser." % lineno
                )
            if value[:1] in ("&", "*"):
                return {}, body, (
                    "line %d: YAML anchors and aliases are not supported by the "
                    "minimal parser." % lineno
                )

    data: dict = {}
    current_map: dict | None = None

    try:
        return _parse_block(block, data, body)
    except FrontmatterError as exc:  # safety net: a finding, never a traceback
        return data, body, str(exc)


def _parse_block(block: list[str], data: dict, body: str):
    current_map: dict | None = None

    for lineno, raw in enumerate(block, start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_map is None:
                return data, body, "line %d: unexpected indentation" % lineno
            child = raw.strip()
            if child.startswith("- "):
                return data, body, (
                    "line %d: YAML sequences are not supported by the minimal parser "
                    "(and are not permitted in this repo's frontmatter)" % lineno
                )
            try:
                ckey, cval = _split_key_value(child)
            except FrontmatterError as exc:
                return data, body, "line %d: %s" % (lineno, exc)
            if cval == "":
                return data, body, "line %d: nested mappings deeper than one level are not supported" % lineno
            try:
                current_map[ckey] = _scalar(cval)
            except FrontmatterError as exc:
                return data, body, "line %d: %s" % (lineno, exc)
            continue

        try:
            key, value = _split_key_value(raw)
        except FrontmatterError as exc:
            return data, body, "line %d: %s" % (lineno, exc)

        if not key:
            return data, body, "line %d: empty key" % lineno

        if value == "":
            current_map = {}
            data[key] = current_map
        else:
            try:
                data[key] = _scalar(value)
            except FrontmatterError as exc:
                return data, body, "line %d: %s" % (lineno, exc)
            current_map = None

    # A trailing nested mapping with no children is almost always a mistake.
    for key, value in data.items():
        if isinstance(value, dict) and not value:
            return data, body, "key %r has no value" % key

    return data, body, None


def frontmatter_block(text: str) -> str:
    """Return the raw YAML between the `---` fences, or "" if there is none."""
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return ""
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return ""
    return "\n".join(lines[1:end])


def crosscheck_with_pyyaml(block: str, mine: dict) -> str | None:
    """If PyYAML is installed, compare its parse against the minimal parser.

    Opportunistic only: a disagreement means the minimal parser needs fixing, a PyYAML
    failure is reported as advisory.
    """
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    try:
        theirs = yaml.safe_load(block)
    except Exception as exc:  # pragma: no cover - depends on optional dep
        return "PyYAML failed to parse the frontmatter (%s); the minimal parser was used" % (
            str(exc).splitlines()[0]
        )
    if not isinstance(theirs, dict):
        return "PyYAML returned %s, not a mapping" % type(theirs).__name__
    if set(theirs) != set(mine):
        only_yaml = sorted(set(theirs) - set(mine))
        only_mine = sorted(set(mine) - set(theirs))
        return "parser disagreement (PyYAML only: %s / minimal only: %s)" % (
            only_yaml or "-",
            only_mine or "-",
        )
    for key in mine:
        if isinstance(mine[key], dict) and isinstance(theirs[key], dict):
            if set(mine[key]) != set(theirs[key]):
                return "parser disagreement inside `metadata`"
        elif str(mine[key]).strip() != str(theirs[key]).strip():
            return "parser disagreement on `%s`" % key
    return None


# --------------------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------------------


class Finding:
    __slots__ = ("level", "skill", "code", "message")

    def __init__(self, level: str, skill: str, code: str, message: str) -> None:
        self.level = level
        self.skill = skill
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return "%-5s [%s] %s: %s" % (self.level, self.code, self.skill, self.message)


class Report:
    def __init__(self, strict: bool) -> None:
        self.strict = strict
        self.findings: list[Finding] = []
        self.rows: list[tuple] = []

    def add(self, level: str, skill: str, code: str, message: str) -> None:
        self.findings.append(Finding(level, skill, code, message))

    def error(self, skill: str, code: str, message: str) -> None:
        self.add(ERROR, skill, code, message)

    def warn(self, skill: str, code: str, message: str) -> None:
        self.add(WARN, skill, code, message)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == WARN]

    @property
    def failed(self) -> bool:
        return bool(self.errors) or (self.strict and bool(self.warnings))


# --------------------------------------------------------------------------------------
# Section extraction (used by the zero-dependency heuristic)
# --------------------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def extract_section(body: str, wanted: str) -> str | None:
    """Return the text of the first heading whose title contains `wanted` (ci)."""
    lines = body.splitlines()
    wanted = wanted.lower()
    collected: list[str] = []
    capturing = False
    level = 0
    for line in lines:
        heading = _HEADING_RE.match(line)
        if heading:
            if capturing and len(heading.group(1)) <= level:
                break
            if wanted in heading.group(2).lower():
                capturing = True
                level = len(heading.group(1))
                continue
        if capturing:
            collected.append(line)
    return "\n".join(collected) if collected else None


# --------------------------------------------------------------------------------------
# Link checking
# --------------------------------------------------------------------------------------


def check_links(path: Path, skill_root: Path, report: Report, skill: str) -> tuple[int, int]:
    """Validate every relative markdown link in `path` against the skill root.

    Links are resolved relative to the *skill root*, not the containing file, so a
    reference file links to `references/FOO.md` rather than `../references/FOO.md`.
    Returns (checked, ok).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(skill, "read-failed", "%s: %s" % (path.name, exc))
        return (0, 0)

    where = path.relative_to(skill_root.parent).as_posix()
    checked = ok = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        # Skip fenced code blocks: example snippets may contain illustrative links.
        if line.lstrip().startswith("```"):
            continue
        for match in LINK_RE.finditer(line):
            target = match.group(1).strip()
            if not target or target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):  # http:, mailto:, tel:
                continue
            if target.startswith("/"):
                report.error(
                    skill,
                    "link-absolute",
                    "%s:%d: link is not skill-root relative: %s" % (where, lineno, target),
                )
                checked += 1
                continue
            if target.startswith("../"):
                report.error(
                    skill,
                    "link-parent",
                    "%s:%d: link escapes the skill root (%s); links must be relative to "
                    "the skill root, e.g. references/FOO.md" % (where, lineno, target),
                )
                checked += 1
                continue

            cleaned = target[2:] if target.startswith("./") else target
            path_part = cleaned.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue

            if path_part.startswith(REFERENCE_DIRNAME + "/"):
                remainder = path_part[len(REFERENCE_DIRNAME) + 1 :]
                if remainder.startswith(REFERENCE_DIRNAME + "/"):
                    report.error(
                        skill,
                        "link-double-prefix",
                        "%s:%d: doubled prefix %s" % (where, lineno, path_part),
                    )
                    checked += 1
                    continue

            checked += 1
            if (skill_root / path_part).is_file():
                ok += 1
            else:
                report.error(
                    skill,
                    "link-broken",
                    "%s:%d: link target does not exist: %s" % (where, lineno, path_part),
                )
    return checked, ok


# --------------------------------------------------------------------------------------
# Per-skill validation
# --------------------------------------------------------------------------------------


def validate_skill(skill_dir: Path, report: Report, max_body_tokens: int) -> None:
    name = skill_dir.name
    skill_md = skill_dir / SKILL_FILENAME

    if not skill_md.is_file():
        report.error(name, "no-skill-md", "directory %s/ contains no %s" % (name, SKILL_FILENAME))
        return

    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(name, "unreadable", "cannot read %s: %s" % (SKILL_FILENAME, exc))
        return

    data, body, parse_error = parse_frontmatter(text)
    if parse_error:
        report.error(name, "frontmatter", parse_error)
    else:
        # Opportunistic second opinion when PyYAML happens to be installed. A
        # disagreement means the minimal parser has a bug, not the skill.
        disagreement = crosscheck_with_pyyaml(frontmatter_block(text), data)
        if disagreement:
            report.warn(
                name,
                "parser-disagreement",
                "minimal YAML parser disagrees with PyYAML: %s" % disagreement,
            )

    # --- portabilty: no unknown top-level keys ---------------------------------------
    unknown = [k for k in data if k not in ALLOWED_TOP_LEVEL_KEYS]
    for key in unknown:
        report.error(
            name,
            "unknown-key",
            "frontmatter key `%s` is not in %s; non-OpenCode hosts ignore unknown keys"
            % (key, ", ".join(ALLOWED_TOP_LEVEL_KEYS)),
        )

    # --- name -----------------------------------------------------------------------
    front_name = data.get("name")
    if front_name is None:
        report.error(name, "name-missing", "frontmatter `name` is required")
    elif not isinstance(front_name, str):
        report.error(name, "name-type", "`name` must be a string")
    else:
        if not NAME_RE.match(front_name):
            report.error(
                name,
                "name-format",
                "`name: %s` does not match ^[a-z0-9]+(-[a-z0-9]+)*$" % front_name,
            )
        if front_name != name:
            report.error(
                name,
                "name-mismatch",
                "`name: %s` must equal the directory name `%s`" % (front_name, name),
            )

    # --- description ----------------------------------------------------------------
    description = data.get("description")
    if description is None:
        report.error(name, "desc-missing", "frontmatter `description` is required")
        desc_len = 0
    elif not isinstance(description, str) or not description.strip():
        report.error(name, "desc-type", "`description` must be a non-empty string")
        desc_len = 0
    else:
        desc_len = len(description)
        if desc_len > MAX_DESCRIPTION_CHARS:
            report.error(
                name,
                "desc-too-long",
                "`description` is %d chars; the spec caps it at %d"
                % (desc_len, MAX_DESCRIPTION_CHARS),
            )
        elif desc_len < 1:
            report.error(name, "desc-empty", "`description` is empty")
        elif desc_len > WARN_DESCRIPTION_CHARS:
            report.warn(
                name,
                "desc-long",
                "`description` is %d chars (>%d); Codex budgets the whole skill list at "
                "8,000 chars and truncates descriptions first"
                % (desc_len, WARN_DESCRIPTION_CHARS),
            )

    # --- license --------------------------------------------------------------------
    license_value = data.get("license")
    if license_value is None:
        report.error(name, "license-missing", "frontmatter `license` is required")
        license_ok = False
    elif license_value != EXPECTED_LICENSE:
        report.error(
            name,
            "license-value",
            "`license: %s` must be %s" % (license_value, EXPECTED_LICENSE),
        )
        license_ok = False
    else:
        license_ok = True

    # --- metadata -------------------------------------------------------------------
    metadata = data.get("metadata")
    meta_ok = False
    if metadata is None:
        report.error(name, "meta-missing", "frontmatter `metadata` is required")
    elif not isinstance(metadata, dict):
        report.error(name, "meta-type", "`metadata` must be a mapping")
    else:
        meta_ok = True
        keys = list(metadata.keys())
        if keys != list(EXPECTED_METADATA_KEYS):
            report.error(
                name,
                "meta-keys",
                "`metadata` keys are %s; expected exactly %s in that order"
                % (keys or "[]", list(EXPECTED_METADATA_KEYS)),
            )
            meta_ok = False
        for key in keys:
            if not isinstance(metadata[key], str):
                report.error(
                    name,
                    "meta-value-type",
                    "`metadata.%s` must be a string, got %s"
                    % (key, type(metadata[key]).__name__),
                )
                meta_ok = False
        updated = metadata.get("updated")
        if isinstance(updated, str):
            try:
                parsed = _dt.date.fromisoformat(updated)
            except ValueError:
                report.warn(
                    name,
                    "meta-updated-format",
                    "`metadata.updated: %s` is not an ISO YYYY-MM-DD date" % updated,
                )
            else:
                today = _dt.date.today()
                if parsed > today:
                    report.warn(
                        name,
                        "meta-updated-future",
                        "`metadata.updated: %s` is in the future" % updated,
                    )
        keys_required = metadata.get("keys-required")
        if isinstance(keys_required, str) and keys_required.strip().lower() not in (
            "none",
            "no",
            "false",
        ):
            report.error(
                name,
                "keys-required",
                "`metadata.keys-required: %s` violates the zero-required-API-keys rule"
                % keys_required,
            )
            meta_ok = False

    # --- frontmatter forbidden features ---------------------------------------------
    block_text = text.split("\n---", 1)[0]
    for needle, label in FORBIDDEN_FRONTMATTER:
        if needle in block_text:
            report.error(
                name,
                "context-fork",
                "`%s` in frontmatter is Claude Code only and breaks portability" % label,
            )

    # --- forbidden directories -------------------------------------------------------
    for dir_name in FORBIDDEN_DIRS:
        for found in sorted(skill_dir.rglob(dir_name)):
            if found.is_dir():
                report.error(
                    name,
                    "hooks-dir",
                    "`%s/` is a Claude Code only feature and breaks portability"
                    % found.relative_to(skill_dir.parent).as_posix(),
                )

    # --- body size -------------------------------------------------------------------
    body_lines = body.splitlines()
    n_lines = len(body_lines)
    n_chars = len(body)
    n_tokens = n_chars // CHARS_PER_TOKEN
    if n_lines > MAX_BODY_LINES:
        report.error(
            name,
            "body-lines",
            "body is %d lines (limit %d); move detail into references/" % (n_lines, MAX_BODY_LINES),
        )
    if n_tokens > max_body_tokens:
        report.error(
            name,
            "body-tokens",
            "body is ~%d tokens (~%d chars / %d); budget is %d; move detail into "
            "references/" % (n_tokens, n_chars, CHARS_PER_TOKEN, max_body_tokens),
        )

    # --- zero hard dependencies heuristic --------------------------------------------
    context = "\n".join(
        part
        for part in (extract_section(body, "when to use"), extract_section(body, "inputs"))
        if part
    )
    if not context.strip():
        context = body  # no explicit sections: fall back to the whole body
    haystack = context.lower()
    if not any(token in haystack for token in ZERO_DEPENDENCY_TOKENS):
        report.warn(
            name,
            "zero-dep",
            "no input-side artifact token (%s) found in the 'when to use'/'inputs' "
            "context; confirm this skill needs no API key to complete"
            % ", ".join(ZERO_DEPENDENCY_TOKENS),
        )
    if any(hint in haystack for hint in HARD_DEPENDENCY_HINTS):
        for hint in HARD_DEPENDENCY_HINTS:
            start = haystack.find(hint)
            while start != -1:
                lead = haystack[max(0, start - 24) : start]
                if not any(neg in lead for neg in NEGATORS):
                    report.warn(
                        name,
                        "zero-dep-hint",
                        "inputs context mentions %r without a negation; confirm it is not "
                        "a required credential" % hint,
                    )
                    break
                start = haystack.find(hint, start + 1)
            else:
                continue
            break

    # --- links -----------------------------------------------------------------------
    md_files = [skill_md] + sorted((skill_dir / REFERENCE_DIRNAME).glob("*.md"))
    links_checked = links_ok = 0
    for md in md_files:
        checked, ok = check_links(md, skill_dir, report, name)
        links_checked += checked
        links_ok += ok

    report.rows.append(
        (
            name,
            "ok" if parse_error is None and not unknown else "FAIL",
            front_name if isinstance(front_name, str) else "-",
            str(desc_len),
            "ok" if license_ok else "FAIL",
            "ok" if meta_ok else "FAIL",
            "%dL/%dt" % (n_lines, n_tokens),
            "%d/%d" % (links_ok, links_checked),
        )
    )


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def find_repo_root(start: Path) -> Path:
    """Walk up from `start` looking for a directory that contains `skills/`."""
    for candidate in [start, *start.parents]:
        if (candidate / SKILLS_DIRNAME).is_dir():
            return candidate
    return start


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="repository root (default: inferred from this script's location)",
    )
    parser.add_argument(
        "--max-body-tokens",
        type=int,
        default=DEFAULT_MAX_BODY_TOKENS,
        help="approximate body token budget per skill (default: %d)" % DEFAULT_MAX_BODY_TOKENS,
    )
    args = parser.parse_args(argv)

    # Windows consoles default to cp1252 and will raise UnicodeEncodeError on the
    # typography these documents use (em dashes, >= signs). Force UTF-8 with
    # replacement so a report is never lost to an encoding error.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover
            pass

    root = (args.root or find_repo_root(Path(__file__).resolve().parent)).resolve()
    skills_dir = root / SKILLS_DIRNAME

    if not skills_dir.is_dir():
        print("HARNESS ERROR: no %s/ directory under %s" % (SKILLS_DIRNAME, root), file=sys.stderr)
        return 2

    report = Report(strict=args.strict)

    skill_dirs = sorted(
        d
        for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_"))
    )

    # A gate that finds nothing to check must not report success. `skills/`
    # containing only dot-prefixed dirs (or an emptied tree) previously produced
    # "Checked 0 skill(s). RESULT: PASS", which is the worst possible failure
    # mode for a conformance gate: silently green while checking nothing.
    if not skill_dirs:
        present = sorted(p.name for p in skills_dir.iterdir())
        report.error(
            SKILLS_DIRNAME,
            "vacuous-pass",
            "no skill directories found under %s (contains: %s). Refusing to report PASS "
            "without checking anything."
            % (SKILLS_DIRNAME, ", ".join(present) if present else "empty"),
        )

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, report, args.max_body_tokens)

    # Files sitting loose in skills/ are not a skill and are almost always a mistake.
    for stray in sorted(p for p in skills_dir.iterdir() if p.is_file() and not p.name.startswith(".")):
        report.error(stray.name, "stray-file", "%s/%s is not a skill directory" % (SKILLS_DIRNAME, stray.name))

    # ---- output ---------------------------------------------------------------------
    print("Skill inventory validation -- %s" % root.as_posix())
    print("Mode: %s | body budget: %d est. tokens" % ("STRICT" if args.strict else "normal", args.max_body_tokens))
    print()

    headers = ("skill", "fm", "name", "desc", "lic", "meta", "body", "links")
    widths = [
        max(len(headers[i]), max((len(str(r[i])) for r in report.rows), default=0))
        for i in range(len(headers))
    ]
    fmt = "  ".join("{:<%d}" % w for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for row in report.rows:
        print(fmt.format(*row))
    print()

    if report.findings:
        print("Findings (%d error(s), %d warning(s)):" % (len(report.errors), len(report.warnings)))
        for finding in sorted(report.findings, key=lambda f: (f.level != ERROR, f.skill, f.code)):
            print("  " + str(finding))
        print()

    if not report.rows and not report.findings:
        print("No skills found under %s/." % SKILLS_DIRNAME)
        print()

    print("Checked %d skill(s)." % len(report.rows))
    if report.failed:
        print("RESULT: FAIL%s" % (" (strict: warnings are fatal)" if not report.errors else ""))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
