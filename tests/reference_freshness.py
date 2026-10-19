#!/usr/bin/env python3
"""Reference staleness checker for skills/*/SKILL.md and skills/*/references/*.md.

Gate 2 of 2. Run from anywhere:

    python tests/reference_freshness.py
    python tests/reference_freshness.py --strict
    python tests/reference_freshness.py --review-after-days 30
    python tests/reference_freshness.py --ignore-path 'skills/seo-data-contract/*'

TWO THRESHOLDS, not one.

  REVIEW  (--review-after-days, default 90)   reported as a review trigger, not a
                                               failure. The citation may have been
                                               superseded even though the source has
                                               not expired.
  STALE   (--stale-after-days, default 365)   a genuine failure. The source itself
                                               has aged out.

The rule this enforces: a number in a skill is only a finding if it traces to a dated
source, and a dated source stops being a finding once the claim behind it may have been
superseded.

Why two thresholds. A primary source does not expire in 90 days. Shepard / Zyppy's
54 scored experiments from 2026-05-07 do not rot because time passed; a documented
on-the-record statement from Gary Illyes in 2025-07 is still exactly what he said. If a
90-day-old citation were a failure, a repository of dated, primary, deliberately-pinned
evidence would be permanently red, and a gate that is always red is not a gate -- it is
noise, and it trains contributors to ignore it. So crossing the review threshold asks a
question (has this been superseded?) and crossing the stale threshold answers it (no,
this source is too old to stand behind).

`--max-age-days` is kept as a backwards-compatible alias that sets the review
threshold, so every existing invocation keeps working and keeps meaning what it meant.

Standard library only.

Exit codes: 0 = pass, 1 = stale citations (or, with --strict, review-level findings too),
2 = harness error.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

SKILLS_DIRNAME = "skills"
SKILL_FILENAME = "SKILL.md"
REFERENCE_DIRNAME = "references"

#: Older than this: reported as a review trigger. The finding may have been superseded
#: even though the source itself has not expired.
DEFAULT_REVIEW_AFTER_DAYS = 90

#: Older than this: a genuine failure. The source has aged out.
DEFAULT_STALE_AFTER_DAYS = 365

MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

_MONTH_ALT = "|".join(sorted(MONTHS, key=len, reverse=True))

# Order matters only for readability: precise forms are matched first, the bare-year
# form last, and overlapping spans from earlier patterns win.

#: 2026-06-15
RE_ISO = re.compile(r"(?<![\d-])(\d{4})-(\d{1,2})-(\d{1,2})(?![\d-])")

#: 2026-06
RE_ISO_MONTH = re.compile(r"(?<![\d-])(\d{4})-(\d{1,2})(?![\d-])")

#: Jun 15 2026 / June 15, 2026 / 15 June 2026
RE_MONTH_DAY_YEAR = re.compile(
    r"\b(?:%s)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b" % _MONTH_ALT, re.IGNORECASE
)
RE_DAY_MONTH_YEAR = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:%s),?\s+(\d{4})\b" % _MONTH_ALT, re.IGNORECASE
)

#: Jun 2026 / June 2026
RE_MONTH_YEAR = re.compile(r"\b(?:%s)\s+(\d{4})\b" % _MONTH_ALT, re.IGNORECASE)

#: (2026) -- a parenthesised year is always a citation year, e.g. `Ahrefs (2026-03)`
#: and `(Shepard 2026)`.
RE_PAREN_YEAR = re.compile(r"\((\d{4})\)")

#: A bare 4-digit year, admitted only when the same line carries citation context.
RE_BARE_YEAR = re.compile(r"(?<![\d./-])((?:19|20)\d{2})(?![\d./-])")

#: Tokens that make a bare year on the same line a citation rather than a passing remark.
CITATION_CONTEXT = (
    "http", "www.", ".com", ".org", ".ai", ".io", "arxiv", "zenodo", "doi",
    "source", "sources", "study", "studies", "report", "survey", "benchmark",
    "measur", "paper", "paper)", "research", "per ", "according", "n=", "p=",
    "dataset", "tested", "test of", "author", "published", "cited", "claim",
)

#: Prefer the latest possible reading of an under-specified date so the gate does not
#: cry wolf: `2026-03` is scored as 2026-03-31, and a bare year as Dec 31 of that year.
DEFAULT_DAY = 31

#: A comparative baseline -- "down from 76% in July 2025" -- names a datapoint *inside* a
#: later report, not a citation that aged out on its own. The Ahrefs figure reported in
#: 2026-03 is dated 2026-03; the July 2025 figure inside it is the comparison point, not
#: a second source. Attributing that baseline to its own date is how this gate flagged
#: primary research as expired when nothing had expired at all, so it is attributed to
#: the reporting source instead.
RE_COMPARATIVE_MARKER = re.compile(r"\b(?:down|up|away)\s+from\b|\bfrom\b|\bvs\.?\b|\bversus\b", re.IGNORECASE)

#: How many lines back a baseline may sit from the marker and from the reporting
#: source's date. Wide enough for prose that wraps mid-sentence, narrow enough that a
#: genuinely separate citation in the next paragraph is still judged on its own date.
BASELINE_WINDOW_LINES = 2

TODAY = _dt.date.today()


# --------------------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------------------


def _safe_date(year: int, month: int, day: int) -> _dt.date | None:
    try:
        return _dt.date(year, month, day)
    except ValueError:
        return None


def _month_name_to_number(token: str) -> int | None:
    return MONTHS.get(token.lower())


def has_citation_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in CITATION_CONTEXT)


def extract_citations(line: str) -> list[tuple[int, int, _dt.date, str]]:
    """Return (start, end, date, matched_text) for every citation date on `line`.

    Earlier, more specific patterns claim their span first; a bare year overlapping an
    already-matched span is dropped, so `2026-06-15` is not also read as year 2026.
    """
    found: list[tuple[int, int, _dt.date, str]] = []
    claimed: list[tuple[int, int]] = []

    def claim(start: int, end: int, date: _dt.date, text: str) -> None:
        if any(not (end <= s or start >= e) for s, e in claimed):
            return
        claimed.append((start, end))
        found.append((start, end, date, text))

    for match in RE_ISO.finditer(line):
        year, month, day = (int(g) for g in match.groups())
        parsed = _safe_date(year, month, day)
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    for match in RE_ISO_MONTH.finditer(line):
        year, month = int(match.group(1)), int(match.group(2))
        if not 1 <= month <= 12:
            continue
        parsed = _safe_date(year, month, _month_last_day(year, month))
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    for match in RE_MONTH_DAY_YEAR.finditer(line):
        month = _month_name_to_number(match.group(0).split()[0])
        day, year = int(match.group(1)), int(match.group(2))
        parsed = _safe_date(year, month, day) if month else None
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    for match in RE_DAY_MONTH_YEAR.finditer(line):
        day, year = int(match.group(1)), int(match.group(2))
        month = None
        for name, number in MONTHS.items():
            if name in match.group(0).lower():
                month = number
                break
        parsed = _safe_date(year, month, day) if month else None
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    for match in RE_MONTH_YEAR.finditer(line):
        year = int(match.group(1))
        month = _month_name_to_number(match.group(0).split()[0])
        if not month:
            continue
        parsed = _safe_date(year, month, _month_last_day(year, month))
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    for match in RE_PAREN_YEAR.finditer(line):
        parsed = _safe_date(int(match.group(1)), 12, 31)
        if parsed:
            claim(match.start(), match.end(), parsed, match.group(0))

    if has_citation_context(line):
        for match in RE_BARE_YEAR.finditer(line):
            parsed = _safe_date(int(match.group(1)), 12, 31)
            if parsed:
                claim(match.start(), match.end(), parsed, match.group(0))

    return found


def _month_last_day(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (_dt.date(year + (month // 12), (month % 12) + 1, 1) - _dt.timedelta(days=1)).day


def _baseline_date(
    lines: list[str], index: int, parsed: _dt.date, match_start: int
) -> _dt.date | None:
    """Return the reporting source's date if `parsed` is a comparative baseline.

    Returns None when the date is not a baseline, or when no later-dated citation is
    nearby to attribute it to -- in which case it is judged on its own date, as before.
    """
    window_start = max(0, index - BASELINE_WINDOW_LINES)
    window = lines[window_start : index + 1]

    # The comparative marker must appear before the date, on its own line or the two
    # lines above it -- "down from **76% in" / "July 2025**".
    marker_seen = False
    for offset, line in enumerate(window):
        limit = match_start if offset == len(window) - 1 else len(line)
        if RE_COMPARATIVE_MARKER.search(line[:limit]):
            marker_seen = True
    if not marker_seen:
        return None

    newest = None
    for offset, line in enumerate(window):
        # Only the reporting source counts, so skip this line's own date.
        for _s, _e, candidate, _t in extract_citations(line):
            if offset == len(window) - 1 and candidate >= parsed:
                continue
            if candidate > parsed and (newest is None or candidate > newest):
                newest = candidate
    return newest


# --------------------------------------------------------------------------------------
# Scanning
# --------------------------------------------------------------------------------------


class StaleCitation:
    """A citation that crossed one of the two thresholds."""

    __slots__ = ("path", "lineno", "date", "age_days", "text", "line")

    def __init__(self, path: str, lineno: int, date: _dt.date, age_days: int, text: str, line: str):
        self.path = path
        self.lineno = lineno
        self.date = date
        self.age_days = age_days
        self.text = text
        self.line = line


def collect_targets(root: Path, ignore: list[str]) -> list[Path]:
    skills_dir = root / SKILLS_DIRNAME
    targets: list[Path] = []
    for skill_dir in sorted(d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))):
        skill_md = skill_dir / SKILL_FILENAME
        if skill_md.is_file():
            targets.append(skill_md)
        references = skill_dir / REFERENCE_DIRNAME
        if references.is_dir():
            targets.extend(sorted(references.rglob("*.md")))
    return [p for p in targets if not is_ignored(p, root, ignore)]


def is_ignored(path: Path, root: Path, ignore: list[str]) -> bool:
    if not ignore:
        return False
    relative = path.resolve().relative_to(root).as_posix()
    import fnmatch

    for pattern in ignore:
        candidate = pattern.replace("\\", "/").rstrip("/")
        if fnmatch.fnmatch(relative, candidate) or fnmatch.fnmatch(relative, candidate + "/*"):
            return True
        if relative == candidate:
            return True
    return False


def scan(paths: list[Path], root: Path, review_after_days: int, stale_after_days: int, today: _dt.date):
    """Return (review, stale, checked, files, ages) for every citation found.

    A citation older than `stale_after_days` is a failure; one older than
    `review_after_days` but younger than that is a review trigger. Both lists are
    returned separately so the summary can show both counts -- a run that reports
    "171 checked / 0 review / 0 stale" must look different on screen from a run that
    reports "0 checked", even though both exit 0.
    """
    review: list[StaleCitation] = []
    stale: list[StaleCitation] = []
    ages: list[int] = []
    checked = 0
    files = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print("WARN: cannot read %s: %s" % (path, exc), file=sys.stderr)
            continue
        files += 1
        relative = path.resolve().relative_to(root).as_posix()
        text_lines = text.splitlines()
        in_fence = False
        for lineno, line in enumerate(text_lines, start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue  # example payloads, not citations
            for start, _e, parsed, matched in extract_citations(line):
                checked += 1
                # A comparative baseline inherits the reporting source's date.
                source_date = _baseline_date(text_lines, lineno - 1, parsed, start)
                if source_date is not None:
                    parsed = source_date
                age = (today - parsed).days
                ages.append(age)
                if age > stale_after_days:
                    stale.append(
                        StaleCitation(relative, lineno, parsed, age, matched.strip(), line.strip())
                    )
                elif age > review_after_days:
                    review.append(
                        StaleCitation(relative, lineno, parsed, age, matched.strip(), line.strip())
                    )
    return review, stale, checked, files, ages


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / SKILLS_DIRNAME).is_dir():
            return candidate
    return start


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Two thresholds:\n"
            "  --review-after-days (default %d)  older than this is a REVIEW TRIGGER,\n"
            "      not a failure: the finding may have been superseded even though the\n"
            "      source itself has not expired.\n"
            "  --stale-after-days  (default %d)  older than this is a genuine FAILURE:\n"
            "      the source has aged out.\n"
            "A primary source does not expire in %d days, so the review threshold must not\n"
            "fail the build on its own; otherwise a repo of deliberately-pinned dated\n"
            "evidence is permanently red and the gate is pure noise.\n"
            "  --max-age-days is a backwards-compatible alias for --review-after-days.\n"
        )
        % (DEFAULT_REVIEW_AFTER_DAYS, DEFAULT_STALE_AFTER_DAYS, DEFAULT_REVIEW_AFTER_DAYS),
    )
    parser.add_argument(
        "--review-after-days",
        type=int,
        default=None,
        help="age past which a citation is reported as a review trigger, not a failure "
        "(default: %d)" % DEFAULT_REVIEW_AFTER_DAYS,
    )
    parser.add_argument(
        "--stale-after-days",
        type=int,
        default=DEFAULT_STALE_AFTER_DAYS,
        help="age past which a citation is a genuine stale failure (default: %d)"
        % DEFAULT_STALE_AFTER_DAYS,
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=None,
        help="backwards-compatible alias for --review-after-days; if both are given, "
        "--review-after-days wins",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero on stale citations OR on review-triggered citations",
    )
    parser.add_argument(
        "--ignore-path",
        action="append",
        default=[],
        metavar="GLOB",
        help="skip paths matching this glob (repeatable); relative to the repo root",
    )
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    parser.add_argument(
        "--min-citations",
        type=int,
        default=5,
        help="warn when fewer than this many citations are found (default: 5)",
    )
    args = parser.parse_args(argv)

    # --max-age-days is the old name for the review threshold. Accepted so every
    # existing invocation keeps working and keeps meaning what it used to mean.
    if args.review_after_days is None:
        args.review_after_days = (
            args.max_age_days if args.max_age_days is not None else DEFAULT_REVIEW_AFTER_DAYS
        )

    if args.stale_after_days < args.review_after_days:
        print(
            "HARNESS ERROR: --stale-after-days (%d) is below --review-after-days (%d); a "
            "citation could never be review-triggered without also being stale"
            % (args.stale_after_days, args.review_after_days),
            file=sys.stderr,
        )
        return 2

    # Windows consoles default to cp1252 and will raise UnicodeEncodeError on the
    # typography these documents use (em dashes, >= signs). Force UTF-8 with
    # replacement so a report is never lost to an encoding error.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):  # pragma: no cover
            pass

    root = (args.root or find_repo_root(Path(__file__).resolve().parent)).resolve()
    if not (root / SKILLS_DIRNAME).is_dir():
        print("HARNESS ERROR: no %s/ under %s" % (SKILLS_DIRNAME, root), file=sys.stderr)
        return 2

    paths = collect_targets(root, args.ignore_path)
    review, stale, checked, files, ages = scan(
        paths, root, args.review_after_days, args.stale_after_days, TODAY
    )

    print("Reference freshness -- %s" % root.as_posix())
    print(
        "Review after: %d days | Stale after: %d days | today: %s | mode: %s"
        % (args.review_after_days, args.stale_after_days, TODAY.isoformat(), "STRICT" if args.strict else "normal")
    )
    if args.ignore_path:
        print("Ignored: %s" % ", ".join(args.ignore_path))
    print("Scanned %d file(s): %s/*/SKILL.md and %s/*/references/*.md" % (files, SKILLS_DIRNAME, SKILLS_DIRNAME))
    print()

    def group_by_file(items: list[StaleCitation]) -> dict[str, list[StaleCitation]]:
        grouped: dict[str, list[StaleCitation]] = {}
        for citation in items:
            grouped.setdefault(citation.path, []).append(citation)
        return grouped

    def group_by_skill(items: list[StaleCitation]) -> dict[str, int]:
        grouped: dict[str, int] = {}
        for citation in items:
            parts = citation.path.split("/")
            skill = parts[1] if len(parts) > 2 and parts[0] == SKILLS_DIRNAME else citation.path
            grouped[skill] = grouped.get(skill, 0) + 1
        return grouped

    # Stale citations are failures: name every one, with the line, so it can be fixed.
    by_file = group_by_file(stale)
    for path in sorted(by_file):
        entries = sorted(by_file[path], key=lambda c: -c.age_days)
        print("%s  (%d stale)" % (path, len(entries)))
        for citation in entries:
            snippet = citation.line
            if len(snippet) > 110:
                snippet = snippet[:107] + "..."
            print("  line %-5d %-12s %5d days old  %s" % (citation.lineno, citation.text, citation.age_days, snippet))
        print()

    # Review triggers are questions, not failures. At this repo's volume (dozens) a
    # line-by-line dump would bury the stale list, so they are counted per file.
    review_by_file = group_by_file(review)
    if review_by_file:
        print("REVIEW TRIGGERS (older than %d days, newer than %d -- not failures)" % (args.review_after_days, args.stale_after_days))
        print("A primary source does not expire on a schedule. These are flagged because the")
        print("FINDING may have been superseded, not because the source has.")
        for path in sorted(review_by_file, key=lambda p: -len(review_by_file[p])):
            oldest = max(c.age_days for c in review_by_file[path])
            print("  %-56s %3d review-triggered (oldest %d days)" % (path, len(review_by_file[path]), oldest))
        print()

    # Both counts on one line, always. A suspiciously clean run must be obvious: a
    # reader has to be able to tell "78 review triggers, 0 stale" from "0 citations".
    print(
        "Citations checked: %d / review-triggered: %d / stale: %d"
        % (checked, len(review), len(stale))
    )

    if checked == 0:
        print("WARNING: no citations were detected at all. This gate passed vacuously --")
        print("         a scan that finds nothing is not the same as a scan that finds")
        print("         nothing wrong.")
    elif checked < args.min_citations:
        print("WARNING: only %d citation(s) detected. A low count usually means the date")
        print("         patterns no longer match how the sources are written." % checked)

    if ages:
        print("Oldest citation:    %d days" % max(ages))
        print("Newest citation:    %d days" % max(0, min(ages)))
        print("(Under-specified dates -- a bare year, `2026-03`, `July 2025` -- are scored")
        print(" as the LAST day of the period, so the gate never flags a source for being")
        print(" imprecisely written. Ages under 0 mean a period still running.)")

    print()

    if stale:
        print("Stale citations per skill:")
        for skill, count in sorted(group_by_skill(stale).items(), key=lambda kv: -kv[1]):
            print("  %-24s %d" % (skill, count))
        print()
        print(
            "Re-verify each of these against its primary source, then either correct the "
            "claim or bump `metadata.updated`."
        )
        print()

    if review:
        print("Review-triggered citations per skill:")
        for skill, count in sorted(group_by_skill(review).items(), key=lambda kv: -kv[1]):
            print("  %-24s %d" % (skill, count))
        print()

    if args.strict:
        if stale or review:
            print(
                "RESULT: FAIL (strict: %d stale citation(s), %d review-triggered)"
                % (len(stale), len(review))
            )
            return 1
        print("RESULT: PASS")
        return 0

    if stale:
        print("RESULT: FAIL (%d stale citation(s))" % len(stale))
        return 1
    if review:
        print(
            "RESULT: PASS (%d stale, %d review-triggered reported -- not failures)"
            % (len(stale), len(review))
        )
        return 0
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
