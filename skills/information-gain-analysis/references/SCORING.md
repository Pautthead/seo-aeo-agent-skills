# Scoring — Information Gain, 0–100

Two things to know before you read the table:

1. **Rank position scores zero points.** By design. See §1.
2. **This rubric is measured by meaning.** The counting steps are deterministic and
   reproducible. The informativeness test in §3 is not — it is a judgement, and you
   must label it as one. Never present §3 output as a measurement.

---

## 1. Why rank is excluded from the score

⚠️ **Vendor research.** On-Page.ai **sells a scoring product, and the Information Gain Score
is their own proprietary metric.** The figures below are means on *their* instrument, their
corpus and their scale. Cite them as vendor research; do not treat them as an independent
measurement of the same thing this rubric measures. Canonical source:
`https://api.on-page.ai/research/information-gain-study` — Eric Lancheres, On-Page.ai
Research, 2026-06-12. 150 pages, 50 keywords, 10 verticals, US/English, single-day scan.

| Bin (unique data points per page) | Mean Information Gain Score | n |
|---|---|---|
| 0–1 | **40.2** | 45 |
| 2–5 | **54.4** | 45 |
| 6–14 | **55.1** | 38 |
| 15+ | **62.1** | 22 |

Overall, the study reports a **median page score of 52/100** (n=150) and a Pearson
**r = 0.17** — a weak linear relationship between data density and the score.

The load-bearing sentence is the study's own: **"Within the top 3, position was unrelated to
the score."** All 150 pages were top-3, so there is nothing in the data to separate position
1 from position 3. Data density did move the score. The variable that moved it was originality,
not rank.

Two consequences, and one trap:

- A rubric that included rank would score position 1 above position 3. The study says that
  separation is not there — within the top 3, position and the score are unrelated.
- **The trap:** including rank would launder a known-good signal (rank matters a lot —
  Shepard hand-assigns it 9.4/10, an opinion rather than a measurement) into a label called
  "information gain." A report saying "gain score 40, low" when the real problem is that the
  page ranks #40 is a wrong finding, confidently stated. Excluding rank keeps this skill
  honest about what it measures.

**Scope honesty:** the correspondence between On-Page's means and this rubric's bands is
**ordinal, not numeric** — do not print "On-Page: 62" next to "ours: 62" as if they were the
same instrument.

## 2. What counts as a unique data point

A **unique data point** is a discrete, checkable assertion about the world that appears
on your page and appears on **none** of the baseline pages you fetched.

Not a data point:

- A statistic you cannot attribute (no source, no date, no n)
- A number that restates a neighbouring number (dimension D non-derivability)
- A number so vague it cannot be checked ("most agencies", "significant improvement")
- An opinion, however well argued
- A definition — unless the definition itself is novel and settles a dispute
- A fact present on any baseline page, however you phrase it

## 3. The informativeness test — five gates, all must pass

**This is the anti-gaming step. Run it on every candidate before counting it anywhere.**

A candidate passes only if it clears **all five**. Failing **2 or more** disqualifies
it entirely: it is excluded from every count and from the ranked gain list.

| # | Gate | Pass condition | Fails when |
|---|---|---|---|
| 1 | **Contrast** | It disagrees with, qualifies, or refines something a baseline page states outright. | It restates the baseline in different words. |
| 2 | **Attribution** | Traceable to a named source, or to an observation the author names themselves. | An orphan number with no source. |
| 3 | **Boundary** | Has a stated scope — sample size, date range, segment, geography, version. | A number with no boundary. It cannot be evaluated or cited, so it is not information. |
| 4 | **Non-derivable** | Cannot be computed from another number already on the page. | "87% of 340" next to "340 users" — the second is arithmetic, not evidence. |
| 5 | **Load-bearing** | A reader would change a decision if it were removed. | Decoration. Passengers. |

### 3.1 Penalty for statistic-stuffing

If **three or more** numbers on the page fail gate 2 **and** gate 3 (i.e. unattributed
*and* unbounded), apply **−10**. Those numbers are removed from the count first; the
penalty is applied after.

Rationale, and why this is not a judgement call: padding with numbers that carry no
information is *structurally detectable*, not merely detectable by reading for meaning.
Jochen Madler (Sitefire), *"SlopShape: Identifying AI-Generated Commercial Web Content"*,
`https://arxiv.org/abs/2609.15369` (2026-09), detects AI-generated commercial posts **from
structure alone, at 97.0 macro-F1 on held-out companies**, using 176 structural features out
of a 203-feature instrument over 2,250 pre-ChatGPT human blog posts against 11,250 AI
mirrors from 5 frontier models. The shape is the tell — you cannot paraphrase your way out of
it. Number-density without number-substance produces exactly that shape. This penalty is the
rubric's attempt to catch the shape, which is the one part of it that does not depend on
meaning.

Note what this means: the penalty threshold (3) is a judgement call, labelled as one.
The *reason* for it has a measured basis. Do not present the −10 as a derived value, and do
not restate 97.0 macro-F1 as an "accuracy percentage" — it is a macro-averaged F1 score
against a balanced-class definition, not a share of pages classified correctly.

### 3.2 Structural slop penalty

Apply **−10** if **three or more** of these are present. Each is a structural marker,
each is binary, each is countable:

1. **Number density without number structure** — figures everywhere, n/date/source
   nowhere.
2. **Uniform section rhythm** — every section the same length, same shape, same number
   of items. Real expertise is lumpy; slop is not.
3. **Hedged superlatives** — "comprehensive", "ultimate", "in-depth", "navigate the
   landscape", "it's important to note".
4. **Symmetric lists** — three-item and five-item lists everywhere, because three and
   five are the defaults an LLM reaches for.
5. **No first-person concrete actor anywhere** — no one is named as having done,
   measured, tested, or observed anything.

These five are markers, not proof. A human page can trip one by accident. Three is
where it becomes a pattern — which is exactly the unit arXiv 2609.15369 classifies
against. Apply the penalty and say so in the report; do not assert "this page is AI
slop," which this cannot establish.

## 4. The seven dimensions

Total = 100. Each dimension is a **count** plus a **band**. Bands are labelled
judgement calls except where marked derived.

### A. Unique data points — 30 points

Count of candidates passing all five gates, absent from the baseline.

| Count | Points |
|---|---|
| ≥15 | 30 |
| 10–14 | 24 |
| 6–9 | 18 |
| 3–5 | 12 |
| 2 | 7 |
| 1 | 3 |
| 0 | 0 |

The 15 threshold is **derived** from On-Page.ai's ≥15 band (mean 62.1, n=22 — vendor
research on their own metric; see §1). The intermediate steps are judgement calls,
interpolated on the assumption of roughly monotonic returns. Note that On-Page's own middle
bins are nearly flat (54.4 at 2–5, 55.1 at 6–14), so the smooth gradient this table assumes
is **not** something the source supports across the middle of the range. Treat the
interpolation as a design choice, not a replication.

### B. Fringe entities — 20 points

Count of named concepts or entities from the topic's periphery that appear on your page
and on 0–1 baseline pages. Fringe per Huang: adjacent to the topic, not at its centre.

| Count | Points |
|---|---|
| ≥8 | 20 |
| 5–7 | 14 |
| 3–4 | 9 |
| 2 | 5 |
| 1 | 2 |
| 0 | 0 |

Counting rule: an entity counts once regardless of repetition. A named product,
standard, person, organisation, dataset, failure mode, or segment qualifies. A generic
noun ("agencies", "platforms") does not.

### C. First-hand or proprietary observation — 20 points

Distinct observations where **someone is named as having observed something specific**.

| Count | Points |
|---|---|
| ≥5 | 20 |
| 3–4 | 15 |
| 2 | 10 |
| 1 | 5 |
| 0 | 0 |

Pass condition for a single observation: a named actor **and** a specific observation.
"Our team tested this" with no name and no result is not an observation. "We ran this
against 340 client sites in Q3 2026; 41 returned a 200 for the same URL with different
canonical tags" is.

Repeat observations by the same actor on the same subject count once. Five variations
of "we tested it" is one observation.

### D. Original data — 12 points

Tiered. Highest tier wins; do not sum across tiers.

| Tier | Pass condition | Points |
|---|---|---|
| 1 | The page contains data from a measurement the author ran — with sample size, date range, and stated method | 12 |
| 2 | Data the author generated, but method or n is not stated | 7 |
| 3 | Third-party **primary** data (filings, specs, changelogs, original research) not used by baseline pages | 4 |
| 0 | None | 0 |

Tier 1 is where most of the real work is. It is also the hardest, and most honest
content briefs skip it and jump to C.

### E. Named methodology — 8 points

| Pass condition | Points |
|---|---|
| The page names its method **and** gives steps someone could repeat | 8 |
| Method named, steps absent | 4 |
| Unnamed | 0 |

"Named" means the page commits to a term — a framework name, a defined procedure, a
stated selection rule. The steps must make it applicable elsewhere; a name alone is
branding.

### F. Unique comparison — 6 points

| Pass condition | Points |
|---|---|
| A comparison axis no baseline page uses, **with** a stated verdict | 6 |
| New axis, no verdict | 3 |
| None | 0 |

A verdict means the page commits: "X is better for teams under 10 people, Y for larger."
A table with no conclusion scores 3. Baseline-comparison tables score **0** — comparing
to the same competitors the SERP already compares to is not gain.

### G. Unique process detail — 4 points

First-hand implementation specifics: config, exact steps, thresholds, code, versions,
screenshots of the actual system.

| Count | Points |
|---|---|
| ≥3 | 4 |
| 1–2 | 2 |
| 0 | 0 |

## 5. Assembling the score

```
raw   = A + B + C + D + E + F + G          (max 100)
final = max(0, raw - stuffing_penalty - slop_penalty)
```

Verify the seven subtotals sum to `raw` before reporting. If they do not, the count is
wrong.

### Interpretation bands

Bands are judgement calls. They are calibrated so that band *floor* ≈ the On-Page
means (40 for zero-gain pages, 62 for ≥15 data points) — **ordinally, not numerically**.

| Final | Label | What it means in practice |
|---|---|---|
| 0–19 | **REDUNDANT** | Every fact is already on the SERP. Expect zero citation contribution. |
| 20–39 | **PARAPHRASE** | The classic failure: ranks well, cut from every synthesized answer. |
| 40–59 | **MARGINAL** | Real but thin additions. Below the density where On-Page.ai's ≥15 bin averaged 62.1. |
| 60–79 | **COMPETITIVE** | Enough genuine gain to be worth citing on the topics covered. |
| 80–100 | **DEFINING** | Holds facts nobody else has. Rare, and usually specific to a narrow vertical. |

Score 0–39 is not "bad SEO" and does not mean the page cannot rank. It means the page
is a competent restatement. Those pages can be perfectly successful in traditional
search and entirely absent from AI answers. Say exactly that.

## 6. Production routes — how to actually obtain the fact

**The deliverable is a worklist, not a number.** A report that says "add more unique
content" has failed. Every ranked gain-list row must name a route, a rough cost, and a
rough time.

Classify each surviving candidate by the route that would actually produce it. If you
cannot name a route, the candidate is not a finding — it is a wish. Drop it or find the
route.

| # | Route | What it means | Typical cost | Typical time |
|---|---|---|---|---|
| R1 | **RUN THE NUMBER** | A figure computable from data you already hold — logs, invoices, support tickets, CRM | Low | 2–8 h |
| R2 | **INSTRUMENT THE PRODUCT** | A metric only you can emit, because only you run the system | Med | 1–2 wks |
| R3 | **ASK THE EXPERT** | A named human with direct experience, quoted and attributed | Low | 1–5 days |
| R4 | **READ THE PRIMARY DOC** | A spec, filing, changelog, RFC, or contract nobody else cited | Low | 1–4 h |
| R5 | **RUN THE EXPERIMENT** | You design and execute something; nobody else has the result | Med–High | 2–6 wks |
| R6 | **PUBLISH THE DATASET** | You already have a corpus; you make it findable and citable | Med | 1–3 wks |
| R7 | **OBSERVE BEHAVIOUR** | Systematic observation of something public — crawl the competitor's own outputs, diff their pricing pages over time | Low–Med | 2–8 h |

### Route selection guidance

**Prefer R1 and R7.** They are the cheapest and the fastest, and they are widely
skipped because they feel like small answers. They are not: an R1 figure nobody else
has *is* dimension A and D, at full value, on day one.

- **R1** is the highest-yield route per hour in the entire framework. Most teams hold
  data that would be genuinely differentiating if anyone ran it. Ask: what is in the
  database that we have never once put on the website?
- **R2** is the highest-ceiling route. An instrumented metric is defensible over years
  and cannot be copied. Slower, and worth starting anyway.
- **R3** is the fastest credible authority play. Pass condition: a **named** person and
  a **specific** statement. "Our engineer explained that…" is not this route. The
  name must be publishable, and the quote must say something a competitor's copy could
  not.
- **R4** is the most-skipped and the most reliable. Changelogs, RFCs, contracts,
  pricing pages, and filings contain hard facts nobody wrote a blog post about. Read
  the primary source rather than the three posts summarising it.
- **R5** is for when nothing cheap is available. Do not recommend it as a default; most
  briefs do not survive contact with an experiment.
- **R6** turns existing assets into citable facts. Note §6.1 below before promising it.
- **R7** is underrated. Competitors publish continuously and inconsistently. Their own
  history is primary data about their own product: price changes, removed features,
  doc edits, status-page incidents, changelog entries. **This produces facts no
  competitor will ever publish, because publishing them is against their interest.**

### Ranking rule

Order the gain list by **acquisition value**, not by the score total:

```
rank = (score dimension contribution) ÷ (cost + time weight)
```

Highest-value-and-cheapest first. An R4 fact worth 6 points reachable in an hour outranks
an R5 fact worth 12 points needing six weeks. **Never present an R5 route as the
first recommendation** — it implies effort the team has not committed to and reads as
excuse-making.

Cap the list at **10 rows**. A 40-item worklist gets none of them done. If more than 10
candidates survive, keep the top 10 by rank and record the remainder as a secondary
appendix.

### 6.1 Route caveats

- **R6 (publish a dataset) does not mean "publish a data product."** It means publish
  the artefact and make it findable. Do **not** propose `llms.txt` as part of this —
  six 2026 studies find no link between the file and more citations or more crawling, and bots fetch
  what they are *pointed at*, nobody goes hunting (Ahrefs, 2026-06-15,
  n=137,210 domains). Budget zero against it.

  **State it narrowly.** The accurate claim is that `llms.txt` does not get you cited
  in AI answers — **not** that nobody fetches it, and **never** "does not work" or
  "does nothing." Both overclaim, and this repo's own evidence contradicts them:
  - Of the **3% of files that received any traffic**, **96% of those requests came from
    bots** — 97% of the 137,210 domains received zero requests at all.
  - What is zero is narrower and more interesting: **"Zero AI bots go looking for
    llms.txt files that don't exist."** Bots fetch what they are pointed at; nobody
    hunts.
  - Fetching is real and agent-driven: **"AI agents, and the infrastructure built to
    serve them, drive 10.5% of llms.txt requests — more than any other type of AI bot"**,
    and *"Aside from statespace-indexer and GPTBot, Claude-Code out-fetched every AI
    retrieval bot, every AI assistant, and every AI training crawler."* Announced in
    robots.txt, crawlers demonstrably fetch the file (Nathan Hall, Zenodo
    `10.5281/zenodo.23128812`: *"That is discovery, not adoption."*).
  - Retrieval is not parsing, indexing, ranking or use.
- **R3 (ask the expert) is not a licence to invent a quote.** An unattributed or
  reconstructed quote is a fabrication and, given Google's 2026-10-01 guidance, a
  trustworthiness problem. If you do not have the quote, the route is "request it."
- **R7 (observe behaviour) must respect robots.txt and terms of service.** And a crawled
  observation needs a stated method — when you looked, how many snapshots — or it fails
  informativeness gate 3 (boundary).
- **No route may require a paid tool.** Where a paid tool would help, say what it costs
  as an option, never as a prerequisite.

## 7. Deterministic steps versus meaning judgements

**The single most important honesty constraint in this repo.**

| Step | Type | Reproducible? |
|---|---|---|
| Fetch baseline URLs | Deterministic | Yes |
| Enumerate atomic facts into a ledger | Deterministic | Yes — same page, same rows |
| Match page facts to ledger rows | Deterministic | Yes |
| Count dimensions A, B, C, G | Deterministic | Yes, given the same candidate set |
| Assign D, E, F tiers | Semi-deterministic | Mostly — tier boundaries are stated |
| **Apply the five-gate informativeness test** | **Meaning judgement** | **No** |
| **Verify gating is not padding** | **Meaning judgement** | **No** |
| **Rank the gain list by acquisition value** | **Judgement** | **No** |

Two agents running this on the same page **can and will produce different candidate
sets**, because the candidate set is produced by a meaning judgement. Treat that
difference as a finding worth surfacing, not as noise to average away. (Compare
`r/SEO_Xpert` 2026-07-19: ~150 internal links proposed with total confidence, ~20
actually usable, and the same page in a fresh session produced different
recommendations.)

**Never write "information gain score: 47, measured."** Write
"information gain score: 47 — counting steps deterministic, informativeness judged
from the text." If you cannot label the distinction, you are laundering a judgement
into a measurement, which is the exact failure this repo exists to prevent.

## 8. What the score must never be used for

- **Forecasting citations.** No study links this rubric to citation rate. It does not.
- **Comparing vendors.** Vendor scores from different instruments are not comparable.
- **Tracking over time as a KPI without the inventory.** Scores drift with the SERP,
  not only with the page. A fall from 58 to 41 may mean the baseline moved. **Always
  diff the ranked gain list, not the total.** The inventory is the stable artefact.
- **Replacing a rank check.** See §1.

## 9. Sources

- On-Page.ai Information Gain Score study — Eric Lancheres, On-Page.ai Research, 2026-06-12 — `https://api.on-page.ai/research/information-gain-study` — 150 pages, 50 keywords, 10 verticals, US/English — ⚠️ **vendor research: On-Page.ai sells a scoring product and the Information Gain Score is their own metric.** Bins 0–1 → 40.2 (n=45), 2–5 → 54.4 (n=45), 6–14 → 55.1 (n=38), 15+ → 62.1 (n=22); median page score 52/100; Pearson r = 0.17; "within the top 3, position was unrelated to the score"
- Ahrefs, "Information Gain in SEO" — 2026-08-20
- US11354342B2, Google LLC — answer-composition / fact-pruning behaviour
- Bernard Huang (ex-Clearscope), fringe-of-knowledge-graph formulation — cited in Ahrefs, 2026-08-20
- Jochen Madler (Sitefire), *"SlopShape: Identifying AI-Generated Commercial Web Content"* — `https://arxiv.org/abs/2609.15369` — 2026-09-14, v3 2026-09-28 — **97.0 macro-F1 on held-out companies**, 176 structural features of a 203-feature instrument; 2,250 pre-ChatGPT human blog posts (268 domains) vs 11,250 AI mirrors from 5 frontier models
- Cyrus Shepard / Zyppy — 2026-05-07 — ⚠️ **hand-assigned correlation scores, not measurements**
- `r/SEO_Xpert` — agent reproducibility failure, 2026-07-19 — practitioner anecdote

Caveats: **[HONESTY.md](HONESTY.md)**. Method: **[METHODOLOGY.md](METHODOLOGY.md)**.
Baseline construction: **[COMPETITOR_SERP.md](COMPETITOR_SERP.md)**.
