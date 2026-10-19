# Methodology — Information Gain

**Sources for this file**

| Claim | Source | Date | Evidence level |
|---|---|---|---|
| Definition of information gain | Ahrefs, Louise Linehan, `ahrefs.com/blog/information-gain/` | 2026-08-20 | Analysis of a patent, not a confirmed factor |
| Answer-composition behaviour | US11354342B2, Google LLC | patent | Primary — granted patent text |
| "No position four" | Ahrefs, 2026-08-20 | 2026-08-20 | Analyst interpretation of the patent |
| Where gain lives | Bernard Huang (ex-Clearscope) | 2026 | Practitioner assertion, not measured |
| Score distribution | On-Page.ai, Eric Lancheres, 2026-06-12, `https://api.on-page.ai/research/information-gain-study` | 2026-06-12 | ⚠️ **Vendor research** — On-Page.ai sells a scoring product and this is their own metric. 150 pages, 50 keywords, 10 verticals, US/English |
| Google has not confirmed it | Ahrefs, explicit | 2026-08-20 | Direct statement |
| Practitioner dissent | r/SEO | 2026-01-26 | Anecdotal |

---

## 1. Definition

Information gain is **the additional information your page contributes beyond what
already ranks for the query** (Ahrefs, Louise Linehan, 2026-08-20).

Two words in that definition carry the whole method:

- **additional** — measured against something. There is no absolute score. Every
  measurement requires the top results for *that specific query* to have been read.
- **beyond what already ranks** — the baseline is the SERP, not your competitors'
  weakness, and not your own prior output.

The corollary matters: a fact can be true, well-sourced, original to you, and still
carry zero gain, because the top three results already say it. And a fact can be
worthless on its own but high-gain because the SERP has a hole exactly there.

## 2. Where gain lives: the fringe, not the centre

Bernard Huang, formerly of Clearscope, on where genuinely additive content appears:
> "the concepts and entities on the fringe of Google's knowledge graph for the topic."
> — cited in Ahrefs, 2026-08-20

Read this precisely, because it is routinely misapplied as "go long-tail."

The **centre** of a topic is whatever the SERP has already converged on. Every page
that ranks for the core query is, by construction, addressing the centre. Content at
the centre is not automatically bad — but it is, by definition, where gain is lowest,
because the centre is where coverage is densest.

The **fringe** is the set of concepts and entities adjacent to the topic that the
ranking pages touch only glancingly or not at all:

- a segment the SERP generalises about but never segments ("works great for SMBs" — nobody says which of the three use cases it fails for)
- an entity that belongs to the topic but appears on 0–1 ranking pages
- a constraint, failure mode, or boundary condition mentioned once in passing
- the second-order question the pages raise and then never answer

The operational reading: **do not ask "what else is there to say about X?" Ask "what
does the SERP's version of X leave out?"** The first question produces padding. The
second produces gain. This is the difference between dimension C and dimension E in
the rubric, and it is the difference between a page that scores and a page that gets
quoted.

Caveat, stated plainly: Huang's formulation is a practitioner assertion. It is not
measured, and no one has published a study of fringe coverage versus citation rate.
It is adopted here because it is the sharpest available operationalisation of the
definition, not because it is evidence.

## 3. The mechanism: fact-pruning

This is the load-bearing claim of the whole framework, and it comes from Google's own
patent.

**US11354342B2** describes an assistant assembling an answer from multiple sources.
The worked example: the assistant takes **facts A and B** from source 1. It then
consults **source 2**, which contributes **fact C** — and retains only C from that
source, **deleting the overlap**. The overlap adds nothing to the answer, so it is
removed.

Ahrefs' consequence, which is the sharpest available explanation of AI citation
behaviour:
> "In a ranked list, even if you're the fourth site saying the same thing, you're still
> on the SERP… But in a synthesized answer there **is** no position four. Either you
> provide the information that hasn't been said yet, or your content gets cut."
> — Ahrefs, 2026-08-20

Two implications follow directly.

**Implication 1 — Redundancy is not neutral, it is disqualifying.** In a ranked list,
overlap is merely unremarkable: you occupy a slot, you get impressions, the reader
scans past you. In synthesis, overlap is *actively discarded*. The marginal value of
being the fourth correct restatement is not zero — it is **negative**, because it
contributes tokens the synthesizer has already accounted for and must spend context
window resolving.

**Implication 2 — Retrieval and citation are different gates.** Being retrieved and
being cited are two decisions. A page can clear the first and fail the second, and
when it does, the failure is invisible to rank tracking. Your rankings will not
report it.

This is the mechanism the fact-pruning hypothesis rests on. It is a *description of
how an assistant assembles an answer from sources*, documented in a granted patent.
It is **not** a description of a ranking factor, and no one has shown Google applies
it as one. Read §1 of [HONESTY.md](references/HONESTY.md) before relying on it.

## 4. Ranked lists versus synthesized answers

| | Ranked list | Synthesized answer |
|---|---|---|
| Unit | Position (1–10) | Fact |
| Redundant content | Occupies a slot, ~neutral | **Deleted**, ~zero or negative |
| Being 4th | Costs you position, keeps you present | **Removes you** |
| What earns inclusion | Being relevant and authoritative | Being the *only* source for something |
| Failure mode | Ranking below the fold | Absence from the answer entirely |
| Detectable by | Rank tracker | Nothing — no AI citation data in GSC |
| Marginal cost of more pages | Low | Negative; cannibalises your own cluster |

The last row is the one teams get wrong. Publishing more content on a topic where you
already own the ranking does not add inventory — it splits your own coverage across
pages that then compete to be pruned against each other. Lily Ray's summary of the
competitive GEO experiment (arXiv 2605.25517, 252,000 trials, 2026-05-25):
> "The sites that try to create as much content as possible eventually get burned,
> including very big brands."

## 5. Why a page can rank well and still be cut from every AI answer

This is the failure mode this skill exists to name, because rank tracking reports
health while the actual problem is invisible.

A page ranks well when it is relevant, authoritative, well-structured, and matches
intent. It gets cut from every synthesized answer when it is **reliably fourth on
every sub-question**.

The typical sequence:

1. The site publishes a strong, comprehensive, genuinely useful guide. It ranks. It
   is cited in traditional search. The team calls it a winner.
2. Every competitor page covers the same material, drawn from the same sources, in
   the same order. Individually each is good. Collectively they are identical.
3. In a synthesized answer, source 1 supplies the framing, source 2 supplies the
   specific figures, source 3 supplies the caveats. This site's page supplies
   nothing that survives the overlap check.
4. It holds position 4 for eighteen months and appears in zero AI answers. Search
   Console shows stable traffic. Nothing is red.

Nothing in step 1–4 is visible to a rank tracker, a traffic dashboard, or a content
audit that checks for length, headings, and keyword coverage. The page passes every
conventional content check and still contributes nothing.

**The diagnostic:** if your page and its competitors are both excellent and your
citations are zero, the variable to test is not quality. It is *distinctiveness*.

**The secondary diagnostic:** a page can have this problem in one section and not
another. Read section-by-section against the ledger. Frequently a page is
high-gain in two sections and zero-gain in nine, which reads from the outside as
"good page, no citations" and from the inside as a fixable two-section problem.

## 6. What is not information gain

Ruled out explicitly, because each of these is routinely sold as information gain:

- **Length.** Shepard hand-assigns length 6.7/10 — below factually specific (8.3), self-contained
  passages (8.0), and brand/entity trust (6.8) (2026-05-07). Length adds no fact.
- **Formatting.** arXiv 2605.25517 (252,000 trials, 6 LLMs, two-source injected RAG):
  formatting-only edits had little impact. Bullets, tables, and headings change how a
  fact is presented, not whether it is new.
- **Keyword coverage / semantic completeness.** Completeness had smaller gains than
  topical relevance, position, explicit price information, and a recent timestamp.
- **Sampled statistics.** A number that restates what the paragraph already says in
  numeric form carries no information. See the informativeness test in
  [SCORING.md](references/SCORING.md).
- **`llms.txt`.** Not information gain, and not a lever at all. Six independent
  negative measurements — see the repo README. Shipping it costs an hour; budget zero.
- **FAQPage schema.** Shepard hand-assigns structured data 5.6/10 — and he is *more*
  positive on schema than the negative half of his note suggests: *"practically every study
  that looks at schema and AI citations finds a positive relationship. The effect is
  typically small, but it's amazingly consistent across studies."* The other half of his note
  is that *"LLMs don't typically ingest schema as part of their training"* and there is
  *"limited evidence they can at least see schema when searching."* Both are true at once:
  the correlation is real and consistent, and there is no demonstrated mechanism to pull it
  with. Small, consistent, and not a lever. Do not recommend FAQPage as a GEO tactic; do
  recommend schema for rich results and entity clarity, which is a different and honest
  reason.
- **Freshness for its own sake.** Freshness scores 7.0. A date updated to *look* fresh
  is not a fact. A newly measured number is.

## 7. Relationship to rank — do not conflate

> ⚠️ **Every Shepard score quoted in this section is hand-assigned, not measured.** Shepard:
> *"I assigned each score by hand against those criteria… These are not confirmed ranking
> factors. Correlation is not causation."* Read the ordering as a priority sequence. The
> full table is in `aeo-citability-audit` → `references/CITATION_FACTORS.md`.

Shepard ranks URL accessibility **#1 at a hand-assigned 9.5/10**, and search rank (top 10)
**#2 at 9.4/10** (2026-05-07). His summary is "win SEO, win AI citations (most of the
time, with extra steps)." Jeremy Moser (uSERP) via Digiday, 2026-03-10: "80 percent
of GEO is good, fundamental SEO."

Information gain does not contradict this. It explains the residual 20% — the part
where a page ranks and is still absent. The order of operations is fixed:

1. **Can it be retrieved?** Accessibility, indexability, server-rendered content, snippet
   control. Shepard ranks URL accessibility #1 at 9.5.
2. **Does it rank?** 9.4. Without this, gain is irrelevant.
3. **Is the answer near the top of the page?** 8.8.
4. **Does it contain facts nobody else has?** This skill.

Running this skill on a page that does not rank produces a theoretically correct and
practically useless report. Check step 1 and 2 first.

One tension to carry honestly: Ahrefs reports (2026-03, 863K keywords / 4M AIO URLs)
that Google AI Overviews drew only 38% of citations from top-10 organic results, down
from 76% in July 2025. That sits awkwardly against Shepard's 9.4. Treat the
**direction** as the finding and the precise figure as unsettled. Do not print
38%/76% as settled fact.

## 8. Sources

- Ahrefs, "Information Gain in SEO," Louise Linehan — `https://ahrefs.com/blog/information-gain/` — 2026-08-20
- US11354342B2, Google LLC — `https://patents.google.com/patent/US11354342B2/en`
- On-Page.ai Information Gain Score study — Eric Lancheres, On-Page.ai Research, 2026-06-12 — `https://api.on-page.ai/research/information-gain-study` — 150 pages, 50 keywords, 10 verticals, US/English; bins 40.2 / 54.4 / 55.1 / 62.1, median 52/100, Pearson r = 0.17, "within the top 3, position was unrelated to the score" — ⚠️ **vendor research; On-Page.ai sells a scoring product and this is their own metric**
- Cyrus Shepard / Zyppy, "AI citation ranking factors" — `https://signal.zyppy.com/p/ai-citation-ranking-factors` — 2026-05-07, 54 experiments/patents/case studies — ⚠️ **hand-assigned correlation scores, not measurements**
- arXiv 2605.25517, competitive GEO controlled experiment — `https://arxiv.org/abs/2605.25517` — 2026-05-25, 252,000 trials
- Jochen Madler (Sitefire), "SlopShape: Identifying AI-Generated Commercial Web Content" — `https://arxiv.org/abs/2609.15369` — 2026-09-14, v3 2026-09-28 — 97.0 macro-F1 on held-out companies, 176 structural features of a 203-feature instrument
- Jeremy Moser (uSERP) via Digiday — 2026-03-10
- Practitioner dissent, r/SEO — 2026-01-26

Caveats, dissent, and the mandatory disclosure block: **[HONESTY.md](references/HONESTY.md)**.
Rubric and thresholds: **[SCORING.md](references/SCORING.md)**.
