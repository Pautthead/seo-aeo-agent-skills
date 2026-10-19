# Known limitations — the honest ceiling of this skill

This file exists because the market's AEO tooling does not have one, and because a
tool that cannot detect something must say so rather than report a false negative as
a finding.

Everything below is sourced and dated. Where evidence is contested, both sides are
given and the stronger position is named.

---

## 1. It cannot predict citation. It measures readiness.

**The core limit.** A high score means "nothing on-page is a plausible reason for not
being cited". It does not mean you will be cited, and no output of this skill is a
forecast.

**Non-reproducible outputs.** `r/DigitalMarketing`, 2026-04-17:
*"Citation data is noisy. Run the same prompt 10 times, get different outputs."* The
same practitioner class of failure is documented separately: opening a **fresh
session** with an identical page produced different recommendations
(`r/SEO_Xpert`, 2026-07-19), and an agent proposed ~150 internal links with total
confidence of which **~20 were actually usable**.

**Consequence for this skill's design:** the *analysis* is deterministic by
construction — 20 binary checks against fixed rules — because only that layer is
reproducible. The *narrative* around it is model-generated and will vary run to run.
If two runs of this audit disagree about a number, that is a bug in the rules. If two
runs word the recommendation differently, that is expected.

**Never let the model adjust a number.** If a finding looks wrong, fix the rule and
say so. Do not silently re-score.

---

## 2. It cannot see ranking — and ranking is the #2 factor

A keyless run scores **13 of 23** Shepard factors directly and **5** partially (see the
`Keyless?` column in `references/CITATION_FACTORS.md`). Four are wholly unmeasurable: **search rank
(9.4)**, fan-out rank (9.3), known source (5.4) and domain authority (5.0). A fifth, brand / entity
trust (6.8), is measurable on-page only — its off-site half is out of scope.

**Two of the unmeasurable five are the top two factors in the entire list.** That is the
ceiling, stated plainly.

### The contested evidence, both sides

| Position | Source | Claim |
|---|---|---|
| **For** high rank correlation | Shepard / Zyppy, 2026-05-07, 54 experiments scored | Search rank (top 10) = **9.4/10**, rank #2 of 23 |
| **Corroborating** | SearchPilot, 2026-10-02 | Sites that lost organic visibility lost their AI citations too |
| **Against** | Ahrefs, reported 2026-03, 863K keywords / 4M AIO URLs | AI Overviews drew only **38%** of citations from top-10 organic results, down from **76% in July 2025** |

**Which is stronger, and why.** Shepard's 9.4 is the better-evidenced claim: 54
experiments, scored on repeatability/evidence/official support, published with a
methodology. Ahrefs's figure is a single large observational sample of one surface
(Google AI Overviews) at one point in time, and it does not cover ChatGPT, Gemini or
Perplexity at all — which is most of the citation volume. An observational drop from
76% to 38% is also consistent with AI Overview citation *mix* diversifying as more
pages get indexed, without the underlying rank→citation relationship weakening.

**So: treat the direction as the finding and the precise figure as uncertain.** The
supported conclusion is that ranking matters somewhat less than it did, and still
matters. The unsupported conclusion — that organic position is now irrelevant — is
not evidenced by either source. **Do not print 38%/76% as settled fact in a client
report.**

This matters directly for how a score is read. A 100/100 page-level score on a page
that ranks #40 is still a page that will not be cited.

---

## 3. It cannot see the platforms, and platform data is the weakest link

- **91% of AI citations appear on exactly one platform** (Indig H1 2026, via Search
  Engine Journal, 2026-08-08). Single-engine tracking is, arithmetically, near-zero
  tracking. Anyone reporting AI visibility from ChatGPT alone is reporting 9% of the
  signal and calling it 100%.
- **Google Search Console is ~75% incomplete for AI features**, and there is **no
  separate AI Mode data** in Search Console at all. A GSC-based "AI visibility" number
  is a partial number presented as a total one.
- The remaining platform-level data (Otterly.AI, Ahrefs AIO, CueScout) is
  third-party, sampling-based, and non-reproducible at the prompt level.

**What this skill does about it:** it produces no citation-rate claim at all. It
reports page state. If an operator asks "what is our AI visibility", the correct
answer from this skill is "I cannot measure that; here is what I can measure and here
is what I cannot".

---

## 4. Time horizons — and the promise this skill will not make

| Change type | Time to first effect | Source |
|---|---|---|
| On-page edits | Weeks | ProCloser field test, 2026-05-27 |
| Third-party citation changes | 4–12 weeks | ProCloser field test, 2026-05-27 |
| **First citation lift** | **60–120 days** | ProCloser field test, 2026-05-27, n=5, author flags sample as underpowered |

**Never promise a GEO uplift in under 60 days.** Anyone who does is selling a
timeline they cannot control.

**Provenance note:** the 60–120 day figure comes from n=5 clients and the author
explicitly flags it as underpowered. It is the best available figure and it should be
cited with n and the caveat every time. Treat it as an order of magnitude, not a
service-level agreement.

**And the horizon applies to this audit too.** An audit run today cannot have
produced a citation change yet. Re-auditing the same page in 30 days will show
on-page edits and no citation movement; that is the expected result, not a failure.

---

## 5. Stale-input failure — the mode this skill inherits from the data layer

This skill fetches a page. Pages change. The failure documented in the wider
workflow literature applies here in miniature
(`r/AiAutomations`, 2026-09-07):

> *"A GSC OAuth token expired and the agent continued using cached Search Console
> data for two weeks. Rankings were changing while its decisions were still based on
> the old view… The workflow can run successfully against an input that should no
> longer be trusted."*

Corroborated (`r/SideProject`, 2026-09-24) against a product claiming
"sub-5-second analysis without hallucination risks": *"a fast ClickHouse query can
still return confidently outdated Search Console data unless every report exposes its
latest import time."*

**Mitigation built into this skill:** Step 0 requires a fresh fetch with a recorded
timestamp, and the report template prints `Fetched <timestamp>`. If the operator
supplies pasted HTML, the report must say the fetch time is the *paste* time, not the
page's last-modification time. A citability report whose timestamp is a week old is a
report about a page that may no longer exist in that state.

---

## 6. Per-check limitations

| Check | Cannot detect |
|---|---|
| X-01 | Whether the early block *actually* answers the query when no target query is supplied |
| X-02 | Whether a bot is served *different* HTML than your client — needs server logs |
| X-05 | Entity resolution beyond capitalisation — `Acme Ltd` vs `Acme Limited` counts as a mismatch |
| X-05 | **All three lexical checks are N/A outside en/nl/es/pt/it/fr/de** |
| E-01 | Whether the name matches your canonical entity in a knowledge graph — needs external data |
| E-02 | Whether the cluster actually **ranks**; it only checks structure exists |
| E-03 | Whether the named author is credible to anyone else. Do not use it as a proxy for known-source (5.4) or domain authority (5.0) |
| W-01 | Whether a "fact" is *true*. It counts attributable specifics, not accuracy |
| W-02 | Information gain. Requires a fact list; N/A without one |
| W-04 | Citation *quality*. Three primary sources beat thirty aggregators; the check cannot tell |
| W-07 | Price/timestamp relevance to page type — N/A for docs, methodology and editorial pages |
| All | JS-rendered content it cannot fetch; content behind auth; content behind a bot wall |

**Never report a false negative as a finding.** If a check cannot evaluate the input,
it returns N/A, is excluded from the denominator, and is listed by ID in the report.

---

## 7. Five factors that are not on Shepard's list

From our own 5-client field test (ProCloser, 2026-05-27, n=5, underpowered) — these
surfaced in practice and do not appear in the 23:

1. **Third-party citation density.** How often the brand is cited *by other sites*.
   Consistent with Muck Rack's 25M+ cited-links finding: earned media 84% of AI
   citations vs 0.3% paid. Not measurable from one page.
2. **YouTube listicle inclusion.** Presence in "best X" video or list content, which
   retrieval surfaces reach differently from web pages. Not measurable keylessly.
3. **Date-stamped freshness.** Independent signal from E-05 in the field data —
   pages visibly carrying a current date performed better. Directionally consistent
   with arXiv 2605.25517's "recent timestamp helps consistently", but measured on
   clients, not trials.
4. **Entity-naming consistency.** Covered by E-01. See
   [ENTITIES.md](references/ENTITIES.md) for why the cheap/low-risk synthesis beats both
   "it's the 5.8 factor, ignore it" and "it's the biggest win".
5. **On-page citation infrastructure.** Whether the page is built so that a claim
   *can* be extracted — answer-first structure, tables, self-contained blocks,
   attributed sources. Covered by X-01…X-06 and W-03…W-06.

**How to use this section honestly.** n=5 cannot override a 54-experiment scored
study. Use these as **hypotheses worth checking on your own data**, and say so when
you cite them. Items 3 and 5 are the only two with independent corroboration — 3 via
arXiv 2605.25517, 5 via Shepard's structural factors. Items 1 and 2 are
observationally supported but unquantified here. Item 4 is a field observation that
contradicts a scored factor only in emphasis, not in direction.

**This skill scores items 3, 4 and 5 (E-05, E-01, X/W checks) and explicitly does not
claim to score items 1 and 2.** Off-site presence is not a page property. Saying
otherwise would be exactly the false negative this repo refuses to publish.

---

## 8. What this skill deliberately does not do

- **It does not score `llms.txt` absence as a defect.** 2.0/10, six independent
  negative measurements, Google on the record (Danny Sullivan, Search Central Live
  Toronto, 2026-04: *"There is no benefit to creating a llms.txt file for SEO."*).
- **It does not recommend FAQPage schema.** 5.6/10, and Google stopped showing FAQ
  rich results for most sites. Schema is worth doing for rich results and entity
  clarity, not for GEO.
- **It does not automate posting anywhere.** Reddit reported catching 25,000 spammy
  posts/day (2026-07), explicitly to stop *"brands from planting posts meant to get
  them recommended by ChatGPT and Gemini"*, and banned 4 subreddits used in a GEO
  experiment that automated upvotes and comments. **Measure Reddit. Never post to
  it.**
- **It does not award points for formatting.** arXiv 2605.25517: formatting-only
  edits had little impact across 252,000 trials.
- **It does not generate content, fake authors, or rewrite the page.** Google's
  2026-10-01 guidance calls fake authors deception. Analysis is deterministic; prose
  is the operator's.
- **It does not estimate rank.** If rank data is unavailable, the report says "not
  measured".
