# The 23 AI Citation Ranking Factors

**Source:** Cyrus Shepard / Zyppy, `signal.zyppy.com/p/ai-citation-ranking-factors`,
2026-05-07. 54 experiments, patents and case studies, each scored 0–10 on
repeatability, evidence strength and official support. Corroborated by SearchPilot,
2026-10-02: sites that lost organic visibility lost their AI citations too.

**Author's summary, verbatim:**
> *"win SEO, win AI citations (most of the time, with extra steps)."*

That sentence is the positioning of this entire repo. Read it before proposing a GEO
tactic that is not also an SEO tactic.

---

## The ranked table

| # | Factor | Score | Keyless? | Check |
|---|---|---|---|---|
| 1 | URL accessibility | **9.5** | yes | E-04 |
| 2 | **Search rank (top 10)** | **9.4** | **no** | Rank data required |
| 3 | Fan-out rank | 9.3 | no | Rank data required |
| 4 | Preview control (`nosnippet`) | 9.2 | yes | E-04 |
| 5 | Query-answer match | 9.2 | partial | X-01, W-02 |
| 6 | Intent-format match | 9.0 | partial | X-06, operator-supplied intent |
| 7 | Topic cluster ranking | 8.9 | partial | E-02 |
| 8 | Answer near the top | 8.8 | yes | X-01 |
| 9 | AI-ready structure | 8.6 | yes | X-03, X-04 |
| 10 | Factually specific | 8.3 | yes | W-01 |
| 11 | Explicit phrasing | 8.1 | partial | X-01, W-06 |
| 12 | Cites sources | 8.0 | yes | W-03, W-04 |
| 13 | Self-contained passages | 8.0 | yes | X-05 |
| 14 | Content visibility (in HTML, not JS) | 7.6 | yes | X-02, X-07 |
| 15 | Freshness | 7.0 | yes | E-05 |
| 16 | Brand / entity trust | 6.8 | partial | E-03 |
| 17 | Length | 6.7 | yes | context, unscored |
| 18 | Language | 6.3 | yes | X-08 |
| 19 | Entity consistency | 5.8 | yes | E-01 |
| 20 | Structured data | 5.6 | yes | informational only — **not a GEO lever** |
| 21 | Known source | 5.4 | no | off-site, out of scope |
| 22 | Domain authority | 5.0 | no | off-site, out of scope |
| 23 | **llms.txt** | **2.0** | — | **do not recommend; see below** |

### Three numbers that should be printed together

Any tool that scores "AI readiness" without surfacing these three is selling
something. They are the honest headline of this whole reference file:

- **Search rank — 9.4/10.** The second-highest factor. Ordinary SEO.
- **Structured data — 5.6/10.** Mid-table. Not the lever the 2026 skill market says
  it is.
- **llms.txt — 2.0/10.** The lowest score of all 23.

---

## Factor-by-factor annotation

Each entry: what it means operationally, how this skill checks it, and whether it
needs data beyond the page.

### 1 — URL accessibility · 9.5

**Means:** the crawler can get the page at all. Auth walls, `401`, interstitial
pages, geo-blocks and bot-detection interstitials remove you from the candidate pool
before any ranking or relevance question is asked.
**Check:** E-04 — final HTTP status after redirects is 200; no login redirect;
response body length > 200 characters; no known bot-wall markers in the first block.
**Keyless:** yes.

### 2 — Search rank (top 10) · 9.4

**Means:** pages in the organic top 10 are disproportionately the pages that get
cited. This is the factor that makes GEO 80% ordinary SEO.
**Check:** not checkable from a page. Requires rank data for the target query.
**Keyless:** **no.** This is the single largest gap in a keyless audit.
**Contested:** Ahrefs (2026-03, 863K keywords / 4M AI Overview URLs) measured AI
Overviews drawing 38% of citations from top-10 organic results, down from 76% in
July 2025. Against a 9.4 that is awkward. **Stronger position:** the direction is
the finding, the figure is uncertain. Ranking is still load-bearing; the claim that
organic position no longer matters is unsupported.

### 3 — Fan-out rank · 9.3

**Means:** the same rank effect measured across the wider set of queries a fan-out
retrieval touches — one answer may be assembled from many retrievals, so breadth of
ranking matters more than a single position.
**Check:** not checkable keylessly.
**Keyless:** no.

### 4 — Preview control (`nosnippet`) · 9.2

**Means:** `nosnippet` and `max-snippet:0` deliberately suppress the text excerpt
Google is willing to quote. High score means this factor is *real*, and if you have
switched it on, you have removed yourself from AI answers on purpose.
**Check:** E-04 — grep raw HTML and response headers for `nosnippet`, `nosnippetimg`,
`max-snippet:0`, `data-nosnippet`, and the `noarchive` directive.
**Keyless:** yes.
**Note:** audit for this even when it is the operator's deliberate choice. Report it
as a finding with the cause stated; do not lecture.

### 5 — Query-answer match · 9.2

**Means:** the passage that answers the query must actually contain the answer to
that query, not discuss the topic. Relevance beats coverage.
**Check:** X-01 (answer position) plus W-02 (does the page contain the agreed facts),
using the operator-supplied target query.
**Keyless:** partial — becomes strong when a target query is supplied, N/A when not.

### 6 — Intent-format match · 9.0

**Means:** if the query wants a list, a paragraph about lists does not get quoted as
a list. Format the answer in the shape the query implies.
**Check:** X-06 — presence of tables/lists appropriate to the declared intent; and
comparing the page's format against the SERP's dominant format if rank data exists.
**Keyless:** partial.

### 7 — Topic cluster ranking · 8.9

**Means:** you are cited when you own a cluster, not a page. Retrieval fans out
across the topic; a lone strong page on a site with no surrounding coverage ranks and
recites like a lone page.
**Check:** E-02 — ≥3 outbound links to pages sharing the topic stem, ≥1 inbound link
from a sibling page. Cluster membership is computed from the URL path and `href`
graph, which is language-agnostic.
**Keyless:** yes, with a stated limit (see [ENTITIES.md](references/ENTITIES.md)).

### 8 — Answer near the top · 8.8

**Means:** the extractable answer sits in the first paragraph or two, not at the end
after 900 words of preamble.
**Check:** X-01 — answer-bearing text within the first 400 visible characters or the
first 2 blocks. Character-based on purpose.
**Keyless:** yes. See [EXTRACTABILITY.md](references/EXTRACTABILITY.md).

### 9 — AI-ready structure · 8.6

**Means:** real headings, semantic elements, a document an extractor can walk —
not a `<div>`/`<span>` grid with visually-styled headings.
**Check:** X-03 (one `h1`, no skipped levels, ≥3 headings) and X-04 (≥40% of visible
text inside `p`/`li`/`td`/`th`/`dd`/`dt`/`blockquote`/`figcaption`).
**Keyless:** yes. Fully language-agnostic — these are element counts.

### 10 — Factually specific · 8.3

**Means:** specifics — numbers, dates, named studies, named people — are what survive
being quoted. Vague claims are paraphrased away or dropped.
**Check:** W-01 — ≥2 externally attributable facts per 1,000 effective words. See
[CITATION_WORTHINESS.md](references/CITATION_WORTHINESS.md) for the per-language word
normalisation, which is mandatory outside English.
**Keyless:** yes.

### 11 — Explicit phrasing · 8.1

**Means:** say the thing plainly in a quotable sentence rather than implying it
across a paragraph. "Magnesium glycinate is supported by 137 scientific studies"
beats "this ingredient has better evidence" — see [EXTRACTABILITY.md](references/EXTRACTABILITY.md)
for the full contrast.
**Check:** X-01 plus W-06 (definitional sentences ≤40 words).
**Keyless:** partial — fully yes in the 7 languages with shipped lexicons.

### 12 — Cites sources · 8.0

**Means:** a page that shows its sources is a page whose claims can be quoted without
the extractor having to trust them.
**Check:** W-03 (≥1 attributed quotation with named speaker **and** source) and
W-04 (≥3 outbound citations outside the registrable domain).
**Keyless:** yes.

### 13 — Self-contained passages · 8.0

**Means:** each quotable block stands alone. When a passage is lifted out of your
page it must still make sense to a reader who has not seen the paragraph above it.
**Check:** X-05 — ≥3 blocks that (a) do not open with a pronoun or bare connective
and (b) contain at least one entity not already present in the preceding 200
characters.
**Keyless:** yes in en/nl/es/pt/it/fr/de; **N/A elsewhere** — never a false negative.
**Important caveat:** Shepard explicitly does *not* ask you to chunk content into
bite-size pieces. Clear structure is sufficient. Do not build a chunking ritual.

### 14 — Content visibility (in HTML, not JS) · 7.6

**Means:** the text must be in the initial HTML response. Client-rendered content is
invisible to anything that does not execute JavaScript, and the silent-failure mode
is that your page looks perfect in a browser and scores zero.
**Check:** X-02 (strip tags from raw HTML, compare visible-character count against
rendered) and X-07 (CSP `script-src` restriction, render-blocking bundles,
`client-only` / `__NEXT_DATA__`-without-content signatures).
**Keyless:** yes — but only from raw HTML. If you captured only a rendered DOM, mark
it unverifiable rather than passing it.

### 15 — Freshness · 7.0

**Means:** a visible, verifiable recent date. Corroborated by arXiv 2605.25517: a
recent timestamp helps *consistently* across six LLMs.
**Check:** E-05 — machine-readable `datePublished`/`dateModified` in JSON-LD or
meta, plus a human-visible date in the content.
**Keyless:** yes.

### 16 — Brand / entity trust · 6.8

**Means:** recognisable, attributable authorship. Who wrote this and why should you
believe them.
**Check:** E-03 — named author with credentials or bio, reachable About path,
`Organization`/`Person` markup consistent with the visible byline.
**Keyless:** partial — off-site reputation is out of scope.

### 17 — Length · 6.7

**Means:** long enough to contain an answer. Not "longer is better" — there is no
threshold and padding scores nothing.
**Check:** unscored by design. Report the effective word count for context.
**Do not** turn this into a length target. Lily Ray, commenting on arXiv 2605.25517:
*"The sites that try to create as much content as possible eventually get burned,
including very big brands."*

### 18 — Language · 6.3

**Means:** the content's declared and actual language has to match the retrieval.
Mis-declared or mixed-language pages get mis-routed.
**Check:** X-08 — `<html lang>` present and consistent with the detected language of
the first 3 blocks.
**Keyless:** yes.

### 19 — Entity consistency · 5.8

**Means:** the brand, product and person are named the same way everywhere —
title, `h1`, body, schema, and across the wider web. Inconsistent naming splits
your entity and weakens the association.
**Check:** E-01. Shepard's score is low; our 5-client field test (ProCloser,
2026-05-27, underpowered) surfaced it as materially more important in practice. It
is cheap. See [ENTITIES.md](references/ENTITIES.md).
**Keyless:** yes.

### 20 — Structured data · 5.6

**Means:** moderate, not high. Shepard's notes are the operative text: *"LLMs don't
typically ingest schema as part of their training"* and *"limited evidence they can
at least see schema when searching."*
**Check:** informational only. This audit does **not** award or withhold points for
schema, because the evidence does not support a GEO claim either way.
**Explicit non-recommendation:** do not tell anyone to add **FAQPage** as a GEO
tactic. Google stopped showing FAQ rich results for most sites (`r/AskMarketing`,
2026-09-29). Schema earns its place for rich results and entity clarity.

### 21 — Known source · 5.4

**Means:** whether the model already associates your domain with the topic.
**Check:** out of scope. Requires third-party data.
**Keyless:** no.

### 22 — Domain authority · 5.0

**Means:** general domain strength — the lowest-scoring of the 22 non-llms.txt
factors.
**Check:** out of scope keylessly. Where external data exists, report it with its
source and date; never launder a vendor metric into a fact.
**Keyless:** no.

### 23 — llms.txt · 2.0

**Means:** nothing. Lowest score of all 23 factors, against six independent negative
measurements and Google's own on-the-record statement.
**Check:** none. **Do not recommend.**
**Nuance worth shipping (not worth forecasting):** announced in robots.txt,
crawlers do fetch it (Nathan Hall, Zenodo, 2026-09-17, v1.2 2026-10-03:
1,549 fetches across 165 site-days, ClaudeBot = 1,131; ten un-referenced sibling
files got zero requests across 60 file-months). The author's own caveat is the
correct reading — *"Tell a crawler where a file is and it fetches the file. That is
discovery, not adoption."* Retrieval is not parsing, indexing, ranking or use.

---

## Coverage statement

A keyless run of this audit scores **13 of 23** factors directly and **5** partially, on the
`Keyless?` column above (13 yes + 5 partial + 4 no + llms.txt unscored = 23).

**Not measurable keylessly (4):** search rank (9.4), fan-out rank (9.3), known source (5.4) and
domain authority (5.0). A **5th**, brand / entity trust (6.8), is measurable on-page only — the
visible authorship half scores as E-03, the off-site half is out of scope.

**Of the unmeasurable five, two are the two highest-scoring factors in the entire
list.** This is the honest ceiling of a keyless audit and it must be stated in every
report. A perfect page-level score removes one class of reasons for not being cited.
It is not a prediction, and it is not a promise.
