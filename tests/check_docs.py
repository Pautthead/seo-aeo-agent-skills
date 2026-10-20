#!/usr/bin/env python3
"""Documentation and shell gate: links, JSON, encoding, bash syntax, EN/ES parity.

Gate 3 of 3. Run from anywhere:

    python tests/check_docs.py                  # local checks only (no network)
    python tests/check_docs.py --strict         # warnings also fail
    python tests/check_docs.py --external       # also HEAD every external URL

Why this exists separately from Gate 1: Gate 1 checks the four skills against the
Agent Skills spec. It cannot see the README, the docs/ tree, the marketplace JSON,
or whether a `curl` command inside a reference file is even valid shell. Every
defect that survived to v1.0.2 lived in one of those blind spots.

Standard library only. `bash` and `shellcheck` are used when present and skipped
with a warning when absent; CI installs both so the skip never happens there.

Exit codes: 0 = pass, 1 = failure (errors, or warnings under --strict), 2 = harness error.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TEXT_SUFFIXES = (".md", ".json", ".yml", ".yaml", ".py", ".txt")
EXCLUDED_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".mypy_cache"}

MOJIBAKE_MARKERS = (
    "\ufffd",
    "\u00c3",
    "\u00c2",
    "\u00e2\u20ac",
    "\u00ef\u00bb\u00bf",
    "\u00c3\u00b3",
    "\u00c3\u00b1",
    "\u00c3\u00a1",
)

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([^\s`]*)")
LINK_RE = re.compile(r"(?<!!)\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?")
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?")
INLINE_CODE_RE = re.compile(r"`+[^`]*`+")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

BASH_INFO = {"bash", "sh", "shell", "console", "zsh"}

BADGE_HOST = "img.shields.io"

ERROR = "ERROR"
WARN = "WARN"


class Finding:
    def __init__(self, level: str, where: str, code: str, message: str) -> None:
        self.level = level
        self.where = where
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return "%s [%s] %s: %s" % (self.level, self.code, self.where, self.message)


class Report:
    def __init__(self, strict: bool) -> None:
        self.strict = strict
        self.findings: list[Finding] = []
        self.checked: dict[str, int] = {}

    def add(self, level: str, where: str, code: str, message: str) -> None:
        self.findings.append(Finding(level, where, code, message))

    def error(self, where: str, code: str, message: str) -> None:
        self.add(ERROR, where, code, message)

    def warn(self, where: str, code: str, message: str) -> None:
        self.add(WARN, where, code, message)

    def count(self, key: str, n: int = 1) -> None:
        self.checked[key] = self.checked.get(key, 0) + n

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == WARN]

    @property
    def failed(self) -> bool:
        return bool(self.errors) or (self.strict and bool(self.warnings))


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "skills").is_dir() and (candidate / "README.md").is_file():
            return candidate
    return start


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


# --------------------------------------------------------------------------------------
# Encoding
# --------------------------------------------------------------------------------------


def check_encoding(root: Path, report: Report) -> None:
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        report.count("files")
        if raw.startswith(b"\xef\xbb\xbf"):
            report.error(rel, "encoding-bom", "file starts with a UTF-8 BOM")
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            report.error(rel, "encoding-invalid", "not valid UTF-8: %s" % exc)
            continue
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                line = text[: text.index(marker)].count("\n") + 1
                report.error(
                    rel,
                    "mojibake",
                    "line %d contains %r, which is double-encoded text" % (line, marker),
                )
                break


# --------------------------------------------------------------------------------------
# Fenced code blocks
# --------------------------------------------------------------------------------------


def extract_fences(text: str):
    """Yield (start_line, info_string, body) for every fenced block."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = FENCE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        indent, fence, info = match.groups()
        start = i + 1
        body: list[str] = []
        i += 1
        while i < len(lines):
            close = re.match(r"^\s*(`{3,}|~{3,})\s*$", lines[i])
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= len(fence):
                break
            body.append(lines[i])
            i += 1
        yield start, info.strip().lower(), "\n".join(body)
        i += 1


def check_fences(path: Path, text: str, report: Report) -> None:
    rel = path.relative_to(report.root).as_posix() if hasattr(report, "root") else path.name
    lines = text.splitlines()
    depth = 0
    opened_at = 0
    for n, line in enumerate(lines, start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        if depth == 0:
            depth = 1
            opened_at = n
        else:
            closed = re.match(r"^\s*(`{3,}|~{3,})\s*$", line)
            if closed:
                depth = 0
    if depth:
        report.error(rel, "fence-unclosed", "code fence opened at line %d never closes" % opened_at)


def find_bash_exe() -> str | None:
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]
    found = shutil.which("bash")
    if found:
        candidates.append(found)
    for candidate in candidates:
        if not Path(candidate).is_file():
            continue
        # The WindowsApps shim is a WSL launcher: it exits 1 with a UTF-16 "no
        # distributions installed" message when WSL is absent. Probing is the only
        # reliable way to tell it apart from a real shell.
        if "WindowsApps" in candidate:
            continue
        try:
            probe = subprocess.run(
                [candidate, "--noprofile", "--norc", "-c", "printf ok"],
                capture_output=True,
                timeout=15,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if probe.returncode == 0 and probe.stdout.strip() == b"ok":
            return candidate
    return None


def run_bash_syntax(blocks, bash: str, report: Report) -> None:
    for where, body in blocks:
        try:
            result = subprocess.run(
                [bash, "-n", "-s"],
                input=(body + "\n").encode("utf-8"),
                capture_output=True,
                timeout=20,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            report.warn(where, "bash-unavailable", "could not run bash -n: %s" % exc)
            return
        report.count("bash-blocks")
        if result.returncode != 0:
            detail = (result.stderr or b"").decode("utf-8", "replace").strip()
            report.error(where, "bash-syntax", detail.splitlines()[0] if detail else "bash -n failed")


def run_shellcheck(blocks, shellcheck: str, report: Report) -> None:
    severity = "error" if not report.strict else "warning"
    # SC2016/SC2086/SC2034 etc. are excluded because these blocks are fragments:
    # $BASE is set in one block and used in the next, and quoting is deliberate in
    # the curl -A examples. Excluding them keeps the gate about correctness.
    for where, body in blocks:
        try:
            result = subprocess.run(
                [
                    shellcheck,
                    "-s",
                    "bash",
                    "-S",
                    severity,
                    "-e",
                    "SC2016,SC2086,SC1090,SC1091,SC2001,SC2034",
                    "-f",
                    "gcc",
                    "-",
                ],
                input=(body + "\n").encode("utf-8"),
                capture_output=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            report.warn(where, "shellcheck-unavailable", "could not run shellcheck: %s" % exc)
            return
        stdout = (result.stdout or b"").decode("utf-8", "replace").strip()
        if result.returncode != 0 and stdout:
            report.error(where, "shellcheck", stdout.splitlines()[0].replace("-:", "<block>:"))


def check_shell(blocks, report: Report, use_shellcheck: bool) -> None:
    if not blocks:
        return
    bash = find_bash_exe()
    if bash is None:
        report.warn("shell", "bash-missing", "bash not found; syntax check skipped (%d blocks)" % len(blocks))
    else:
        run_bash_syntax(blocks, bash, report)

    if not use_shellcheck:
        return
    shellcheck = shutil.which("shellcheck")
    if shellcheck is None:
        report.warn("shell", "shellcheck-missing", "shellcheck not installed; lint skipped")
        return
    run_shellcheck(blocks, shellcheck, report)


# --------------------------------------------------------------------------------------
# Links
# --------------------------------------------------------------------------------------


def mask_code(text: str) -> list[str]:
    """Return lines with fenced blocks and inline code blanked out, keeping line count."""
    out: list[str] = []
    in_fence = False
    fence_char = ""
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match and not in_fence:
            in_fence = True
            fence_char = match.group(2)[0]
            out.append("")
            continue
        if in_fence:
            if re.match(r"^\s*(`{3,}|~{3,})\s*$", line):
                in_fence = False
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return out


def check_links(root: Path, md_files, report: Report) -> set[str]:
    external: set[str] = set()
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        check_fences(path, text, report)
        for lineno, line in enumerate(mask_code(text), start=1):
            if line.lstrip().startswith("<!--"):
                continue
            targets = [m.group(1) for m in LINK_RE.finditer(line)]
            targets += [m.group(1) for m in IMAGE_RE.finditer(line)]
            ref = REF_DEF_RE.match(line)
            if ref:
                targets.append(ref.group(1))
            for target in targets:
                check_one_link(root, path, rel, lineno, target, external, report)
    return external


def check_one_link(root: Path, path: Path, rel: str, lineno: int, target: str, external: set, report: Report) -> None:
    target = target.strip()
    if not target or target.startswith("#"):
        return
    if target.startswith("mailto:") or target.startswith("tel:"):
        return
    if SCHEME_RE.match(target):
        if target.startswith(("http://", "https://")):
            external.add(target.split("#")[0])
        else:
            report.warn(rel, "link-scheme", "line %d: unsupported scheme in %s" % (lineno, target))
        return
    if target.startswith("/"):
        report.error(rel, "link-absolute", "line %d: absolute path %s" % (lineno, target))
        return

    report.count("relative-links")
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return
    resolved = (path.parent / clean).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        report.error(rel, "link-escapes-repo", "line %d: %s leaves the repository" % (lineno, target))
        return
    if not resolved.exists():
        report.error(rel, "link-broken", "line %d: %s does not exist" % (lineno, target))


def check_external(urls, report: Report, timeout: float, user_agent: str) -> None:
    headers = {"User-Agent": user_agent, "Accept": "*/*"}

    def probe(url: str):
        # GET only. A HEAD request is answered differently by several CDNs and
        # affiliate redirectors (HEAD 404, GET 200), which produced false failures
        # on real working links during development.
        request = urllib.request.Request(url, method="GET", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return url, response.status, None
        except urllib.error.HTTPError as exc:
            return url, exc.code, None
        except Exception as exc:  # noqa: BLE001 - a network failure is a finding, not a crash
            return url, None, str(exc)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for url, status, error in pool.map(probe, sorted(urls)):
            report.count("external-links")
            if error:
                report.warn(url, "external-unreachable", error.splitlines()[0][:160])
            elif status and status >= 400:
                level = WARN if status in (403, 429, 503) else ERROR
                report.add(level, url, "external-%d" % status, "HTTP %d" % status)


# --------------------------------------------------------------------------------------
# JSON and version consistency
# --------------------------------------------------------------------------------------


def load_version(text: str) -> str | None:
    match = re.search(r"^\s*version:\s*\"([^\"]+)\"", text, re.MULTILINE)
    return match.group(1) if match else None


def check_json_and_versions(root: Path, report: Report) -> None:
    marketplace = root / ".claude-plugin" / "marketplace.json"
    if not marketplace.is_file():
        report.error("marketplace", "missing", ".claude-plugin/marketplace.json not found")
        return
    try:
        data = json.loads(marketplace.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error("marketplace", "json-invalid", str(exc))
        return
    report.count("json")

    for key in ("name", "owner", "metadata", "plugins"):
        if key not in data:
            report.error("marketplace", "json-missing-key", "top-level key %r is missing" % key)
    version = (data.get("metadata") or {}).get("version")
    if not version:
        report.error("marketplace", "json-missing-key", "metadata.version is missing")
        return

    plugins = data.get("plugins") or []
    if not plugins:
        report.error("marketplace", "json-no-plugins", "plugins[] is empty")
    skills_dir = root / "skills"
    declared = set()
    for plugin in plugins:
        for entry in plugin.get("skills") or []:
            declared.add(Path(entry).name)
            if not (root / entry / "SKILL.md").is_file():
                report.error("marketplace", "json-bad-skill-path", "%s has no SKILL.md" % entry)

    actual = {p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")}
    for name in sorted(actual - declared):
        report.error("marketplace", "json-skill-undeclared", "%s exists in skills/ but is not in plugins[].skills" % name)
    for name in sorted(declared - actual):
        report.error("marketplace", "json-skill-missing", "%s is declared but absent from skills/" % name)

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skill_version = load_version(skill_md.read_text(encoding="utf-8"))
        if skill_version != version:
            report.error(
                skill_md.parent.name,
                "version-drift",
                "metadata.version is %s but marketplace.json says %s" % (skill_version, version),
            )

    readme = root / "README.md"
    if readme.is_file():
        badge = re.search(r"badge/release-v([0-9][^-)]*)", readme.read_text(encoding="utf-8"))
        if badge and badge.group(1) != version:
            report.error("README.md", "version-drift", "release badge says v%s but marketplace.json says %s" % (badge.group(1), version))
        es_readme = root / "README.es.md"
        if es_readme.is_file():
            es_badge = re.search(r"badge/release-v([0-9][^-)]*)", es_readme.read_text(encoding="utf-8"))
            if es_badge and es_badge.group(1) != version:
                report.error("README.es.md", "version-drift", "release badge says v%s but marketplace.json says %s" % (es_badge.group(1), version))


def check_parity(root: Path, report: Report) -> None:
    en = root / "README.md"
    es = root / "README.es.md"
    if not (en.is_file() and es.is_file()):
        return

    def urls(path: Path) -> set[str]:
        return {
            m.group(1).split("#")[0]
            for m in re.finditer(r"\((https?://[^)\s]+)\)", path.read_text(encoding="utf-8"))
        }

    left, right = urls(en), urls(es)
    only_en = left - right
    only_es = right - left
    en_badges = {u for u in only_en if BADGE_HOST in u}
    es_badges = {u for u in only_es if BADGE_HOST in u}
    if len(en_badges) == len(es_badges):
        report.count("badge-pairs", len(en_badges))
        only_en -= en_badges
        only_es -= es_badges
    report.count("parity-urls", len(left & right))
    for url in sorted(only_en):
        report.error("README.es.md", "parity-missing", "URL present in README.md only: %s" % url)
    for url in sorted(only_es):
        report.error("README.md", "parity-missing", "URL present in README.es.md only: %s" % url)


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--external", action="store_true", help="also check every external URL (network)")
    parser.add_argument("--no-shellcheck", action="store_true", help="skip shellcheck even if installed")
    parser.add_argument("--timeout", type=float, default=20.0, help="per-request timeout in seconds")
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        help="User-Agent for external checks; a bot UA is rejected by several publishers",
    )
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    root = (args.root or find_repo_root(Path(__file__).resolve().parent)).resolve()
    if not (root / "README.md").is_file():
        print("HARNESS ERROR: no README.md under %s" % root, file=sys.stderr)
        return 2

    report = Report(strict=args.strict)
    report.root = root

    md_files = [p for p in iter_text_files(root) if p.suffix.lower() == ".md"]
    check_encoding(root, report)
    external = check_links(root, md_files, report)

    blocks = []
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for start, info, body in extract_fences(text):
            if info in BASH_INFO and "no-check" not in info and body.strip():
                blocks.append(("%s:%d" % (rel, start), body))
    check_shell(blocks, report, use_shellcheck=not args.no_shellcheck)

    check_json_and_versions(root, report)
    check_parity(root, report)

    if args.external:
        check_external(external, report, args.timeout, args.user_agent)

    print("Documentation gate -- %s" % root.as_posix())
    print("Mode: %s | markdown files: %d | bash blocks: %d" % (
        "STRICT" if args.strict else "normal", len(md_files), len(blocks)))
    if args.external:
        print("External links: enabled")
    print()

    if report.findings:
        print("Findings (%d error(s), %d warning(s)):" % (len(report.errors), len(report.warnings)))
        for finding in sorted(report.findings, key=lambda f: (f.level != ERROR, f.code, f.where)):
            print("  " + str(finding))
        print()

    summary = ", ".join("%s=%d" % (k, v) for k, v in sorted(report.checked.items()))
    if summary:
        print("Checked: %s" % summary)
    if report.failed:
        print("RESULT: FAIL%s" % (" (strict: warnings are fatal)" if not report.errors else ""))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
