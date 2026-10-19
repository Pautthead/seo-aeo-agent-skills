# Freshness

## 1. The three questions

The input check must answer three *separate* questions. Collapsing them is the whole bug.

> *"the input check needs to answer three separate questions: can it authenticate now, when did a
> retrieval last succeed, and what is the newest date represented in the retrieved data?"*
> — `r/AiAutomations`, 2026-09-07

| # | Question | Field | Failure it catches |
|---|---|---|---|
| 1 | **Can it authenticate right now?** | `auth_state` | The pipeline cannot refresh, so its numbers are frozen from here on |
| 2 | **When did a retrieval last succeed?** | `last_successful_retrieval_at` | The agent is replaying a cache and does not know how old it is |
| 3 | **What is the newest date inside the data?** | `newest_data_date` | The data itself has aged out, whatever the pipeline says |

They fail independently and they fail in combination:

- **Q1 fails alone** → the workflow errors. Loud. Someone fixes it.
- **Q1 fails, Q2 looks fine** → the reported disaster: *"a GSC OAuth token expired and the agent
  continued using cached Search Console data for two weeks. Rankings were changing while its
  decisions were still based on the old view."*
- **Q2 fails, Q1 is fine** → the agent wrote a cache it cannot date. Fine for a day, unknowable after.
- **Q3 fails** → **the quiet one.** Auth is perfect, the pipeline is perfect, the file is timestamped
  today, and the data is three weeks old. Every green check passes.

A monitoring dashboard built on "did the workflow run?" and "did auth succeed?" catches the first two
and none of the third. `r/AiAutomations` put it exactly right: *"The workflow can run successfully
against an input that should no longer be trusted."*

## 2. A fast query returning old data is still old data

Against a ClickHouse-backed GSC MCP product advertising *"sub-5-second analysis without hallucination
risks"*, `r/SideProject`, 2026-09-24:

> *"a fast ClickHouse query can still return confidently outdated Search Console data unless every
> report exposes its latest import time."*

Three properties of freshness are independent, and only one of them is about the software:

| Property | Question | Broken by |
|---|---|---|
| **Latency** | How long until fresh data arrives? | Vendor pipeline |
| **Currency** | How old is the newest thing I hold? | Nobody refreshing |
| **Representativeness** | Does this sample stand for the world? | Sample size, filters, caps |

Latency of 300ms tells you nothing about currency. A ClickHouse column store will happily answer in
milliseconds from a table last synced 12 days ago. DataForSEO Labs returns in ~200ms from a database
on a **30–90 day** refresh cycle. The observable signal is not response time — it is a **date inside
the payload**, or failing that, the provider's documented refresh window. If neither exists, the class
is `unknown` and you do not get to assume the best.

The "without hallucination risks" framing in that quote is worth naming explicitly: **speed and
verifiability are different properties.** An agent that reports its input's newest date is doing
verifiability. An agent that returns fast is doing neither.

## 3. Thresholds

### The rule

One subtraction, two comparisons, against the source's **expected latency `L`** — the typical age of
the newest row in a healthy, actively-refreshed pull.

```
age = today − newest_data_date          (in days, subject timezone)

age ≤ L            → fresh
L < age ≤ 2L       → aging
age > 2L           → stale
age > retention    → expired        (the source no longer guarantees the data exists at all)
newest_data_date is null → unknown
```

### The `L` table

`L` is **not** a measured optimum. It is a judgement call, set from each source's documented or
well-established latency, with a 3–5× safety band so that a normally-refreshing pipeline never trips
the gate. The classification, not the constant, is what matters: `L` moves a boundary, it does not
create a failure.

| Source family | `L` | Basis | Confidence |
|---|---|---|---|
| `gsc` | **3 days** | Performance data typically final 1–3 days behind; 2× for holiday weekends and data-state lag | documented behaviour |
| `gsc` (Discovery / AI features) | 3 days | same, **but see `SOURCES.md`** — ~75% incomplete for AI features | documented, limited |
| `ga4` | **3 days** | Last 1–2 days incomplete; standard processing 24–48h | documented behaviour |
| `bing_webmaster` | **3 days** | comparable pipeline, less published detail | judgement call |
| `server_log` | **1 day** | Live or near-live; large gaps are the failure mode | judgement call |
| `dataforseo_serp` | **1 day** | Live fetch; observed at `captured_at` | judgement call |
| `dataforseo_onpage` | **1 day** | Live crawl, `observed` semantics | judgement call |
| `screaming_frog` | **1 day** | Local crawl, `observed` | judgement call |
| `scraped_page` | **1 day** | Live fetch, `observed` | judgement call |
| `dataforseo_labs` | **45 days** | Documented **30–90 day** database refresh cycle, midpoint | documented range, not a date |
| `dataforseo_backlinks` | 45 days | Vendor index refresh cycle | vendor-reported |
| `ahrefs` / `semrush` | 45 days | Vendor index refresh cycle | vendor-reported |
| `dataforseo_content_analysis` | 45 days | Runs over its own crawl/index data | judgement call |
| `dataforseo_ai_optimization` | 45 days | Vendor score over an index snapshot | judgement call |
| `user_pasted` | n/a → `unknown` | No date | — |

At `L=45` for Labs, the boundaries are: fresh ≤45d (impossible in practice), aging ≤90d, stale >90d.
**In practice DataForSEO Labs output is `aging` at best and frequently `unknown`, because the 30–90
cycle is a range and the payload does not tell you where in it you are.** Write it that way. The
honest statement is "position unknown, between 30 and 90 days old", not "current".

### The two overrides

**Override A — credential lost and data aged.**
If `auth_state` ∈ `expired | revoked` **and** `age > L`, the class is `stale`, whatever the
arithmetic says. `L` describes a healthy pipeline; this one is not healthy. A credential we
believed we held has gone, so there is no path back to `fresh` — the data is not just old, it is
**frozen**. This is the `r/AiAutomations` failure: an OAuth token expired and the workflow kept
producing confident analysis from a cache for two weeks.

`auth_state: unavailable` is deliberately **excluded** from this override. It means no credential
was ever expected — a user pasted a GSC export into the chat and we hold no keys. There is no broken
expectation of refreshability and no false confidence to correct, and flooring it at `stale` would
make the skill refuse the single most common keyless input, which would break the keyless-first
contract this repository is built on. Age classification alone applies.

The distinction: `expired` and `revoked` are **transitions** from a state we were in. `unavailable`
is a **starting condition**. Only transitions warrant a hard gate.

**Override B — truncated.**
If `truncated: true` at a known cap, the dataset is **partial**, not merely old. Age classification
still applies, but no aggregate may be computed and the report must say the set is a slice.

### Observed-object override

**This is the only condition that produces `freshness_class: observed`.** There is no judgement in
it: it fires exactly when `date_semantics` is `observed` and not otherwise.

For `date_semantics: observed` — a live page fetch, a live SERP, a local crawl — the data is fresh by
construction, so `freshness_class: observed` is recorded and the class gates do not apply. The open
question is *representativeness*, not recency: one SERP is n=1 at one location on one device; one crawl
is what your crawler saw, not what Googlebot saw. Record that in `class_reason` and move on.

### Why 2L

`2L` is the smallest multiplier that tolerates a single missed refresh cycle or a weekend without
tripping. It is arbitrary and defensible: anything in 1.5×–3× would produce a comparable gate, and the
thresholds should be argued with rather than accepted. The alternative — a single hard cutoff like "GSC
older than 7 days is stale" — produces false alarms on every holiday and trains users to disable the
check, which is worse than having no check.

**Note the deliberate asymmetry:** these thresholds say nothing about whether a *change* is
meaningful. A 3-day-old GSC export can already be too old to explain a ranking shift that took 10 days
to happen. Judging whether a window is long enough to support the claim is analysis, not contract —
but if the claim needs a window longer than the data covers, say so.

## 4. The classifier

Python standard library only. No dependencies, no network.

```python
from datetime import date, datetime, timezone

# Expected latency L, in days, per source family. See FRESHNESS.md §3.
L = {
    "gsc": 3, "ga4": 3, "bing_webmaster": 3,
    "server_log": 1, "dataforseo_serp": 1, "dataforseo_onpage": 1,
    "screaming_frog": 1, "scraped_page": 1,
    "dataforseo_labs": 45, "dataforseo_backlinks": 45,
    "dataforseo_content_analysis": 45, "dataforseo_ai_optimization": 45,
    "ahrefs": 45, "semrush": 45, "se_ranking": 45,
}

# Documented retention windows in days, or None where not documented.
RETENTION = {
    "gsc": 16 * 30,          # ~16 months
    "dataforseo_serp": None,
}

BLOCKING_AUTH = {"expired", "revoked"}  # `unavailable` is NOT blocking - see Override A

def classify(env: dict, today: date | None = None) -> tuple[str, str]:
    """Returns (freshness_class, class_reason). Pure function of the envelope."""
    today = today or datetime.now(timezone.utc).date()
    family = env["source_family"]
    semantics = env.get("date_semantics")

    if semantics == "observed":
        return "observed", "directly observed at capture; recency gate n/a"

    ndd = env.get("newest_data_date")
    if not ndd:
        return "unknown", "no date represented in the payload"

    age = (today - date.fromisoformat(ndd)).days
    l = L.get(family)
    if l is None:
        return "unknown", f"no documented latency for source_family '{family}'"

    ret = RETENTION.get(family)
    if ret is not None and age > ret:
        return "expired", f"age {age}d exceeds {family} retention of ~{ret//30} months"

    if age <= l:
        cls = "fresh"
    elif age <= 2 * l:
        cls = "aging"
    else:
        cls = "stale"

    reason = f"age {age}d vs L={l}d for {family} (newest data {ndd}, via {env.get('date_field')})"

    # Override A: credential lost and data already aged out.
    # No `cls == "fresh"` guard here: that condition is unsatisfiable, because
    # age > l can never coexist with cls == "fresh" (fresh is defined as age <= l).
    # It was dead code, so a dead OAuth token silently produced "aging" - the
    # exact silent-stale failure this skill exists to prevent.
    if env.get("auth_state") in BLOCKING_AUTH and age > l:
        cls = "stale"
        reason += "; auth unusable, cannot refresh — floored at stale"
    return cls, reason
```

The override is a **floor at `stale`, not a warning**. That is a deliberate hard line: the
`r/AiAutomations` failure was not that the data was old, it was that the workflow reported success
while making decisions from an input it could no longer refresh. A warning is not a control.

## 5. Traps

### 5.1 OAuth token expiry ≠ data staleness

Different failure, different clock, different fix. Keep them in separate fields.

| | Auth expiry | Data staleness |
|---|---|---|
| Field | `auth_state` | `newest_data_date` |
| Answers | *can I refresh?* | *how old is what I hold?* |
| Clock | token lifetime | the source's latency `L` |
| Detectable by | a live call returning 401 | reading a date in the payload |
| Fix | re-authenticate | re-fetch — or accept a labelled stale report |

Google's OAuth **refresh tokens expire after 7 days of inactivity**, and tokens issued to an app in
*"testing"* publishing status expire in 7 days regardless of use. In practice this means a GSC
integration that "worked fine" in January can start failing in February with no configuration change
and no error in the dashboard — the agent simply falls back to cache. Verify the current policy in
your own Cloud Console project settings rather than trusting this paragraph; Google has changed refresh
token policy before.

The trap is not that the token expired. It is that **the cache made the expiry invisible.** A pipeline
that stores data and retries against it never surfaces a 401 to anything monitoring it. Hence
Override A: once auth is gone *and* the data has aged past `L`, the class stops being about dates and
starts being about the fact that nothing will ever refresh it again.

### 5.2 GSC's two hard limits

**Retention: ~16 months.** Beyond that the property simply has no data. An agent asked about a
24-month trend will silently get 16 months and may present a 16-month chart as a 24-month one. If the
requested window exceeds retention, either refuse or truncate *explicitly* and say which years are
missing. Silent truncation here is indistinguishable from a real decline.

**The 1,000-row cap.** GSC views and exports return at most 1,000 rows. Your total row count for
anything nontrivial is far above this, so the export is the **top 1,000 by impressions** — a slice
that systematically excludes your long tail, which is precisely where the "underperformers hiding in
the data" narrative is found. Any report that ranks pages by clicks from a capped export has
systematically discarded low-impression pages.

Two consequences worth stating in the report:

- **No totals from a capped export.** Summing a top-1,000 slice understates everything and the
  understatement is not uniform — it is biased toward head terms.
- **Coverage percentages are meaningless.** "We appear in 12% of searches" computed on a capped set
  is an artefact of the cap, not of the site.

Workaround when it matters: paginate by date into sub-1,000 chunks and reassemble, or aggregate to a
single dimension (`["date"]` only) so the row count drops under the cap. If you do, set
`truncated: false` and record the reassembly in `provenance_note`.

Also note **in-progress data**: `dataState: "all"` includes the current, still-changing day. Numbers
will move. Record `dataState` in `filters` and prefer `final`.

### 5.3 DataForSEO's 30–90 day refresh cycle

Documented in METHODOLOGY-BRIEF §4, restated because it is the most common misreading in the category:
**Labs output is not real-time.** A `live` suffix in `dataforseo_labs/google/*/live` means *live API
pricing with no queue* — **not** live data. It is a live query against a periodically-refreshed SERP
database. The `SERP` API is the live-fetch product; `Labs` is the index product. Conflating them is
how a 60-day-old rank gets reported as today's.

And the payload does not tell you where in the cycle you are. So the class cannot be computed from the
response — only bounded: *"position between 30 and 90 days old"*. Write it that way.

Also watch the silent cap: 700 keywords max per `keyword_overview` task and 1,000 items per response.
The API **does not error** on the overflow; it returns the first N. Coverage claims from an oversized
request are false with no signal that anything was dropped.

### 5.4 A fetch today returns old data

The general case behind all of these:

- GSC returns rows through the last *complete* day, not today.
- GA4's newest day is incomplete.
- A vendor index refreshes on a schedule and serves whatever is in the table.
- A cached artifact has a `captured_at` from when it was *written*, not refreshed.
- A log-file query against a 30-day CDN retention window silently returns what survives.

Rule: **`captured_at` never substitutes for `newest_data_date`.** If you cannot produce the second,
the class is `unknown` and you report that, rather than reading the first optimistically.

### 5.5 Other traps worth naming

- **Timezone off-by-one.** GSC and GA4 both report in the property's timezone. A property in UTC+13
  and an agent running UTC can disagree by a day at the boundary. `newest_data_date` is in the
  *subject's* timezone; record the timezone in `provenance_note`.
- **Comparison exports.** GSC and GA4 comparison downloads carry two date blocks. Taking `max()` over
  both dates your data to the *older* period — the single most likely way to get a wrong
  `newest_data_date` on a real export.
- **Empty ≠ stale.** Zero rows means the filter matched nothing, or the property is new, or access is
  wrong. It is not "old data". Report `row_count: 0` and investigate; do not classify it `stale`.
- **Future dates.** A `newest_data_date` after today means a clock skew, a timezone bug, or a
  `dateModified` template. `age` goes negative and every comparison passes, which is the worst possible
  failure mode: the gate approves garbage. Treat `age < 0` as `unknown`.
- **`dateModified` is not a data date.** A CMS template or a plugin that rewrites the timestamp sitewide
  makes every page look fresh. Check for identical values across pages before trusting one.
- **Seasonality.** A 28-day window with no prior-year comparison cannot distinguish a decline from a
  normal cycle. Freshness is not comparability; do not let a `fresh` class imply a valid conclusion.

## 6. Reproducibility, which is the sibling problem

`r/SEO_Xpert`, 2026-07-19: an agent proposed **~150 internal link suggestions with total confidence;
~20 were usable.** The same page in a **fresh session** produced different recommendations.

That is not a freshness bug — no date is wrong. It is the same underlying condition: **input the agent
cannot account for.** When it cannot say where a number came from, it also cannot say which of its own
recommendations came from retrieval and which came from its prior. A user who got 20 usable
recommendations out of 150 has no way to identify the 20 in advance.

Labelled provenance is the mitigation, and it is partial — say so plainly:

1. **Separate retrieval-derived from model-derived.** Mark each recommendation's source. If 120 of 150
   are model-prior with no retrieval behind them, the report says that, and the user prunes the list
   themselves instead of trusting a confidence level that means nothing.
2. **Make re-runs comparable.** Same `newest_data_date` + same `source_ref` → a genuinely different
   answer is non-determinism, and the agent should say so rather than present the new answer as an
   update. Different `newest_data_date` → the world moved; that is not a reproducibility failure.
3. **Stamp every figure** so a claim can be traced to a date and re-checked next month. A number with a
   date can be falsified; a number without one can only be argued with.

What labelling does **not** fix: it makes inconsistency visible, it does not remove it. An agent whose
internal-link suggestions vary between sessions has a modelling problem, and an envelope will not
resolve it. Report the variance; do not paper over it.
