"""The freshness classifier in FRESHNESS.md is the reference implementation.

Extract the python fence and run it against the worked examples. A drift between
the function and examples 5a–5c is the bug this file exists to catch.
"""

from datetime import date
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FRESHNESS = ROOT / "skills" / "seo-data-contract" / "references" / "FRESHNESS.md"


def load_classify():
    text = FRESHNESS.read_text(encoding="utf-8")
    match = re.search(r"```python\n(.*?)```", text, re.S)
    if not match:
        raise AssertionError("no python fence in FRESHNESS.md")
    namespace: dict = {}
    exec(compile(match.group(1), str(FRESHNESS), "exec"), namespace)
    return namespace["classify"]


def test_future_date_is_unknown():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "gsc",
            "newest_data_date": "2026-10-25",
            "date_semantics": "row_date",
            "date_field": "date",
        },
        today=date(2026, 10, 20),
    )
    assert cls == "unknown"
    assert "5d in the future" in reason


def test_truncated_fresh_stays_fresh_and_names_the_slice():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "gsc",
            "newest_data_date": "2026-10-19",
            "date_semantics": "row_date",
            "date_field": "date",
            "truncated": True,
        },
        today=date(2026, 10, 20),
    )
    assert cls == "fresh"
    assert "Override B" in reason
    assert "truncated" in reason


def test_example_5a_is_41_days_and_stale():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "gsc",
            "newest_data_date": "2026-09-08",
            "date_semantics": "row_date",
            "date_field": "date (current comparison block)",
            "truncated": True,
        },
        today=date(2026, 10, 19),
    )
    assert cls == "stale", reason
    assert reason == (
        "age 41d vs L=3d for gsc (newest data 2026-09-08, "
        "via date (current comparison block)); truncated at a known cap "
        "— partial slice, do not compute aggregates (Override B)"
    )


def test_example_5b_labs_window_is_aging():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "dataforseo_labs",
            "newest_data_date": None,
            "date_semantics": "provider_refresh_window",
            "truncated": True,
        },
        today=date(2026, 10, 19),
    )
    assert cls == "aging", reason
    assert reason.startswith(
        "no observation date in payload; class bounded at aging by the documented "
        "refresh window for dataforseo_labs (L=45d, stale above 90d). "
        "Actual age unknown — not fresh"
    )
    assert reason.endswith(
        "; truncated at a known cap — partial slice, do not compute aggregates (Override B)"
    )


def test_example_5c_content_claim_is_aging_not_observed():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "scraped_page",
            "newest_data_date": "2026-10-17",
            "date_semantics": "content_claim",
            "date_field": "JSON-LD article.dateModified",
        },
        today=date(2026, 10, 19),
    )
    assert cls == "aging", reason
    assert reason == (
        "age 2d vs L=1d for scraped_page "
        "(newest data 2026-10-17, via JSON-LD article.dateModified)"
    )


def test_observed_fetch_stays_observed():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "scraped_page",
            "date_semantics": "observed",
            "truncated": True,
        },
        today=date(2026, 10, 20),
    )
    assert cls == "observed"
    assert "truncated" in reason


def test_cdn_analytics_same_day_is_fresh():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "cdn_analytics",
            "newest_data_date": "2026-10-20",
            "date_semantics": "row_date",
            "date_field": "date",
        },
        today=date(2026, 10, 20),
    )
    assert cls == "fresh", reason


def test_auth_expired_and_aged_floors_at_stale():
    classify = load_classify()
    cls, reason = classify(
        {
            "source_family": "gsc",
            "newest_data_date": "2026-10-10",
            "date_semantics": "row_date",
            "date_field": "date",
            "auth_state": "expired",
        },
        today=date(2026, 10, 20),
    )
    assert cls == "stale"
    assert "floored at stale" in reason


class FreshnessExamples(unittest.TestCase):
    """unittest discovers methods, not bare functions."""


for _name, _fn in list(globals().items()):
    if _name.startswith("test_") and callable(_fn):
        setattr(FreshnessExamples, _name, staticmethod(_fn))
