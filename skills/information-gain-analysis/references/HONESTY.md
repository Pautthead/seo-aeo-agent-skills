# Honesty — caveats, dissent, and the mandatory disclosure block

**This is the most heavily caveated skill in the repo.** The framework it implements is
over-claimed in the market, including by people selling services based on it. Read this
before running the skill, and reproduce §8 in every report you generate.

---

## 1. Google has not confirmed any information gain requirement

Ahrefs is explicit about this, and it is the load-bearing caveat for everything else:
**Google has not confirmed that information gain is a ranking factor or a citation
requirement.** (Ahrefs, 2026-08-20.)

What exists:

- **US11354342B2** — a granted Google patent describing how an assistant assembles an
  answer from multiple sources, deleting overlap. This is a documented *answer
  composition* behaviour.
- **An interpretation** — Ahrefs' "there is no position four" — which is a reasonable
  and sharp reading of that behaviour.
- **A patent describing answer composition is not a confirmed ranking factor.** The gap
  between those two things is where most of the over-claiming lives.

State this every time. Do not soften it, do not footnote it, do not put it after the
verdict. If a report reads "your page lacks information gain, therefore you will lose
AI citations," delete that sentence and replace it.

## 2. There is practitioner dissent, and it is substantive

From r/SEO, 2026-01-26:
> "there is no information gain requirement — how do I know this — I publish 100's of
> 000's of PAAs/FAQs a month"

This is not a weak objection, and it should not be dismissed:

- It is a practitioner reporting **large-scale output that apparently does not get
  devalued.** It is a live counterexample to the strong form of the hypothesis.
- It is consistent with a **weaker** version of the hypothesis, which is the one this
  skill actually implements. Low-gain mass output can survive if it is not displacing
  anything, is not a primary ranking contender, and is not part of a pattern Google has
  reason to act on. That is a small carve-out — and it is the honest one.
- The volume itself may be part of why it survives: a site publishing at that scale is
  doing something else well, and the citation behaviour is confounded.

Present dissent when asked, and whenever the report is going to someone deciding whether
to act on the finding.

## 3. The score is measured by meaning, so it is not automatable

**This is the most important honesty point in the repo. Read it twice.**

The informativeness test — contrast, attribution, boundary, non-derivability,
load-bearing — requires judging whether a number adds information. That is a judgement
about **meaning**. It cannot be reduced to a rule, and no agent can perform it the same
way twice.

| Step | Type |
|---|---|
| Fetching the baseline | Deterministic |
| Enumerating facts into a ledger | Deterministic |
| Matching page facts to ledger rows | Deterministic |
| Counting dimensions A, B, C, G | Deterministic |
| **Deciding whether a number is informative or padding** | **Meaning judgement** |
| **Deciding whether an observation is first-hand** | **Meaning judgement** |
| **Ranking the gain list by acquisition value** | **Judgement** |

**The rules:**

- **Never write "information gain score: 47, measured."**
- Write: "information gain score: 47 — counting steps deterministic, informativeness
  judged from the text."
- Never present the ranked gain list as a finding of fact. It is a proposal, built from
  a reasoned reading of the text, that a human must confirm.
- Two runs can differ. That is a property of the method, not a bug. Surface the
  disagreement rather than averaging it away — the reproducibility failure documented at
  `r/SEO_Xpert`, 2026-07-19 (~150 internal links proposed with total confidence, ~20
  usable; the same page in a fresh session gave different recommendations), is exactly
  this failure mode.

**Language rules.** Use *judged*, *estimated*, *proposed*, *candidate*. Do not use
*measured*, *found*, *confirmed*, or *is*, when referring to §3–§4 output.

## 4. The 2026 enforcement cycle is tightening

Google has run **four spam updates in 2026, versus one in all of 2025**
(§1.5, sourced).

Gary Illyes, Search Central Live Barcelona, 2026-10: Google now considers **scaled AI
content a bigger problem than link spam.**

Lily Ray's summary of how these cycles work:
> "they work, they spread, they get patched"

Read that carefully. It means:

- **Enforcement lags publication** by weeks to months. A page can be indexed, rank
  briefly, and be patched out later.
- **There is no safe steady state.** Practices safe in 2025 were not safe in 2026. The
  2026-10 guidance tightening (§6) was itself a patch.
- **Low gain is not currently the enforcement criterion**, but a pattern of mass
  low-value output is exactly what a scaled-content policy targets. The rubric's
  information gain and Google's enforcement surface overlap on one specific thing:
  **producing more, of less.** Getting that right is defensible under either framework.

Do not promise that a high score confers safety. It does not.

## 5. "AI visibility" rising while traffic falls

Lily Ray documented a GEO vendor case study where **organic traffic fell 66% while
"AI visibility" rose.**

**Correlation is not causation, and the more plausible reading runs the other way.**
Authority gets you into the indexes that feed AI products. A site with established
organic visibility appears in ChatGPT, and the GEO campaign takes credit for something
the SEO was already doing. Lily Ray's point: a brand with authority concludes its GEO
campaign is working when the explanation is that its existing SEO visibility got it into
those indexes.

Practical consequence: **an information gain report is not a GEO campaign**, and a gain
score is not a traffic forecast. Reporting a gain score as expected traffic is the same
category error as reading a vendor "AI visibility" number as a business outcome.

Supporting reality check: **91.07% of cited URLs appeared in exactly one of ChatGPT,
Perplexity and Google AI Overviews** for the same prompt (Kevin Indig, "The Consensus Gap,"
Growth Memo, 2026-05-11; 20,000 prompts, 3.7M URL citations). Single-engine tracking is close
to no tracking. That is a three-engine overlap figure, not a general statement about
"platforms", and the data is Omnia's own tracking set, which Indig states is skewed toward
Omnia's customer base. Citation data is also unstable — run the same prompt ten times, get
different outputs (`r/DigitalMarketing`, 2026-04-17).

## 6. Review at volume does not scale, and review is not the same as originality

Verified, Lily Ray, *The AI Slop Loop*, 2026-04-14
(`https://lilyraynyc.substack.com/p/the-ai-slop-loop`) — her full text, read directly:

> "I would warn marketers or publishers trying to take SEO or GEO advice from large
> language models: the information is contaminated, and should always be verified by
> real experts with experience in the field."

> "There is no real mechanism for distinguishing between information that is true and
> information that is simply repeated across enough sources. Repetition is treated as
> consensus."

> "I recently had a client send me SEO/GEO information that was factually incorrect,
> pulled straight from AI-generated slop on a random, vibe-coded agency blog. The client
> had no idea."

That last one is the operative finding for this skill. A human being was in the loop —
the client — and the artefact still arrived wrong. Review catches errors; it does not
manufacture the original fact that was missing in the first place.

She also ran the mechanism end to end. In January 2026 she published a deliberately
fabricated article about a non-existent Google core update on her own blog, which was
already an established-authority domain in the SEO space. **Within 24 hours Google AI
Overviews was serving the fabricated information to users as fact.** ChatGPT surfaced
the same claim. Only Claude was not fooled. A BBC journalist ran the same test on a
low-authority personal site and got the same result: *"Google parroted the gibberish from
my website, both in the Gemini app and AI Overviews… ChatGPT did the same thing."*

Google's response cited the query as niche with a data void. Lily Ray's answer is the
right one for this repo's purposes: *"Data voids may contribute to the problem, but in my
opinion, they don't excuse it."*

**The practical consequence for an information gain audit.** The failure mode is not
"a page shipped with a typo". It is "a set of plausible, well-formatted, mutually
reinforcing claims that nobody on earth actually measured". Reviewing sentence quality
does not address it, because every sentence can be individually fine.

The unit of judgement is **the pattern a site publishes**, not the sentence. A
brilliantly-researched page on a site producing twelve low-differentiation pages a week
is part of the problem, not the exception.

Consequences for this skill:

- Dimension C (first-hand observation) and dimension A (unique data points) are scored
  **per page**, but the §3.2 slop penalty is a structural judgement about output
  **patterns**. Read a sample of the site's recent output before scoring any single page.
- Adding unique facts to an otherwise low-differentiation publishing pattern is not a
  fix. The pattern is the signal.
- The three dimensions that survive human review are the ones where a human supplied
  something that did not exist before: a measurement, a name, a boundary.

Corroborating: *"SlopShape: Identifying AI-Generated Commercial Web Content"*, Jochen
Madler (Sitefire), `https://arxiv.org/abs/2609.15369`, submitted 2026-09-14, last revised
2026-09-28 (v3), cs.CL. It detects AI-generated commercial posts **from structure alone,
at 97.0 macro-F1 on held-out companies**, using **176 structural features** out of a
203-feature instrument, over a corpus of **2,250 pre-ChatGPT human blog posts from 268
company domains against 11,250 AI mirrors from 5 frontier models**. (Held-out robustness
under rewording: 96.1. Source attribution: 68.6% correct against a 16.7% chance baseline.)
Sentence-level polish does not change the shape. The shape is the tell.

## 7. Google's own guidance, and the word "critical"

Google's 2026-10-01 rewrite of its AI-generated content guidance:
> "It is critical to manually factcheck and review all AI-generated content for accuracy
> and trustworthiness before publishing."

Barry Schwartz's widely-cited observation: **"critical" is a word Google rarely uses.**
It extends to titles, meta descriptions, structured data, and alt text — metadata now
requires review too.

New rater-guidance definitions of "main content" name four quality dimensions —
**effort, originality, talent/skill, accuracy** — and name mass-produced AI content as
an example of "little to no effort." Fake authors are now explicitly called deception.

Two implications: originality is now named in Google's own rater guidance, which
independently supports the direction of this framework even though no "information gain
requirement" exists. And a *stated* human review process is not what Google said — it
said factcheck the output. A process document satisfies the first and not the second.

## 8. Programmatic SEO — the operational form of this framework

**No measurement in this repo's evidence base covers programmatic-page survival.** There is no
sourced deindexing rate to cite here, and this file will not invent one. Anyone quoting a
"X% of programmatic pages get deindexed" figure must produce the study and the date; until then
it is an anecdote.

What *is* defensible is the operational shape that a programmatic-page failure mode implies.
Three properties have been proposed as what distinguishes programmatic pages that hold their
index from programmatic pages that do not:

1. **One datum not present on any other public page.**
2. **≥2 internal links from hand-written pages.**
3. **An intent not already saturated by ten identical pages.**

**These are hypotheses, not findings.** Treat them as the operational form of information gain
arrived at from plausibility rather than from measurement, and check them against your own data.
Map:

| Proposed property | Dimension |
|---|---|
| One unique datum | A (unique data points), D (original data) |
| ≥2 internal links from hand-written pages | **Not measured by this skill.** See below |
| Unsaturated intent | `references/COMPETITOR_SERP.md` §7, the gap list |

**Important:** property 2 is not information gain and this skill does not measure it.
Internal linking is a separate mechanism (passing contextual authority to a page). A
perfect information gain score on an orphaned page means nothing. Flag it rather than
score it.

## 9. What this skill cannot do

- **Confirm any causal link** between gain score and citations. No study exists. This
  skill models a documented mechanism and a measured association.
- **Forecast citations or traffic.** Explicitly out of scope (§5).
- **Detect proprietary data** behind a login, or facts that exist but are unindexed.
  It under-reports by design.
- **See the synthesizer's full corpus.** A 3–5 page proxy is not the real source set.
- **Judge meaning consistently.** §3.
- **Replace a rank check, an accessibility check, or a crawl check.** In that order:
  can it be retrieved, does it rank, does it have gain.
- **Validate a schema.** Not this skill.
- **Transfer across verticals.** A B2B page can hit 80 with a methodology section and
  a sample-size table. A YMYL page cannot reach 60 without original data — and should
  not fake it. Score bands are not portable; the method is.

**No reliable public source gives a citation-lift window.** This file previously carried a
"60–120 days to observe any citation consequence" figure attributed to an n=5 field test. That
source could not be located — no URL, no snippet, no primary text — and the figure is **widely
repeated without a traceable primary**, so it has been removed. What survives is the qualitative
split, and it is enough: on-page changes move in weeks; third-party citation changes move far
more slowly. **Do not quote a number, and do not promise visibility inside 60 days** — anyone
who does is selling a timeline they cannot source. The rule stands on the **absence of
evidence**, not on a figure anyone can produce.

## 10. Mandatory disclosure block

Reproduce this in every report, unedited, after the ranked gain list. It is part of the
output format, not an optional appendix.

```markdown
## Mandatory caveats

**Information gain is not a confirmed Google requirement.** It is modelled from
US11354342B2 (answer composition) and an Ahrefs analysis (2026-08-20). Google has not
confirmed any information gain requirement. There is active practitioner dissent
(r/SEO, 2026-01-26).

**This score is measured by meaning.** Fact enumeration, baseline matching, and
dimension arithmetic are deterministic. Whether a number is informative or is padding
is a judgement about meaning and is not reproducible. Treat the score as a structured
opinion, not a measurement.

**This is not a citation or traffic forecast.** No study links this score to citation
rate. GEO vendor data shows AI visibility can rise while organic traffic falls 66%
(Lily Ray). Authority gets sites into the indexes feeding AI products; correlation is
not causation.

**Human review is not sufficient.** Documented pattern: sites claiming human editors on
AI drafts were devalued anyway, because the problem was the overall pattern of what the
site published (Lily Ray). Google ran four spam updates in 2026 versus one in 2025;
Gary Illyes (Search Central Live Barcelona, 2026-10) says scaled AI content is now a
bigger problem than link spam.

**Coverage is a sample.** The baseline is 3–5 retrieved pages. It is not the source set
an AI answer was synthesized from. No reliable public source gives a citation-lift
window, so do not quote one.
```

## 11. Sources

- Ahrefs, "Information Gain in SEO," Louise Linehan — 2026-08-20 — includes the explicit statement that Google has not confirmed it
- US11354342B2, Google LLC — answer composition, overlap deletion
- Practitioner dissent, r/SEO — 2026-01-26
- Practitioner dissent / reproducibility failure, r/SEO_Xpert — 2026-07-19
- Lily Ray — GEO vendor case study (66% traffic decline), human-in-the-loop failure, cycle summary
- Gary Illyes, Search Central Live Barcelona — 2026-10
- Google Search Central, AI-generated content guidance — updated 2026-10-01
- Barry Schwartz — observation on the word "critical"
- Indig, "The Consensus Gap," Growth Memo — 2026-05-11 — 91.07% of cited URLs appeared in exactly one of ChatGPT, Perplexity and Google AI Overviews; 20k prompts, 3.7M citations; Omnia tracking data, which Indig states is skewed toward Omnia's customer base
- Jochen Madler (Sitefire), "SlopShape: Identifying AI-Generated Commercial Web Content" — `https://arxiv.org/abs/2609.15369` — 2026-09-14, v3 2026-09-28 — **97.0 macro-F1 on held-out companies**, 176 structural features of a 203-feature instrument, 2,250 human posts vs 11,250 AI mirrors
- Nathan Hall, Zenodo — `https://doi.org/10.5281/zenodo.23128812` — v1.2 2026-10-03 — **disclosed competing interest: the author owns Lefty Media Co and builds the plugin that announces the file measured**
- Muck Rack, "What is AI Reading" — 2026-05-07 — **vendor research**; 84% is "earned media" as Muck Rack defines it (Wikipedia and PubMed Central included; journalism alone is 27%), and Muck Rack's own pages contradict each other by 25× on sample size
- `r/DigitalMarketing` — 2026-04-17 — prompt-output instability
- Jochen Madler (Sitefire), "SlopShape: Identifying AI-Generated Commercial Web Content" — `https://arxiv.org/abs/2609.15369` — 2026-09 — **97.0 macro-F1 on held-out companies.** Earlier drafts of this repo rendered this as an accuracy percentage; it is a macro-averaged F1 against a balanced-class definition, not a share of pages classified correctly.
- ProCloser field test — 2026-05-27 — n=5 — **removed: NOT FOUND.** No URL, no snippet, no primary text located. It was cited for a "60–120 days to citation lift" window, and the figure is widely repeated without a traceable primary. Do not reinstate either the number or the attribution.

Method: **[METHODOLOGY.md](references/METHODOLOGY.md)**. Rubric: **[SCORING.md](references/SCORING.md)**.
Baseline: **[COMPETITOR_SERP.md](references/COMPETITOR_SERP.md)**.
