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

**Non-reproducible outputs.** Opening a **fresh session** with an identical page
produced different recommendations
([r/SEO_Xpert, 2026-07-10](https://www.reddit.com/r/SEO_Xpert/comments/1ush4r6/my_experience_with_using_ai_claude_codecodex_for/)),
and an agent proposed ~150 internal links with total confidence of which **~20 were
actually usable**. Citation overlap is noisy for a measured reason: **91.07%** of
cited URLs appeared in exactly one of ChatGPT, Perplexity and Google AI Overviews
(Kevin Indig, "The Consensus Gap," Growth Memo, 2026-05-11).

**Consequence for this skill's design:** the *analysis* is deterministic by
construction — 20 binary checks against fixed rules — because only that layer is
reproducible. The *narrative* around it is model-generated and will vary run to run.
If two runs of this audit disagree about a number, that is a bug in the rules. If two
runs word the recommendation differently, that is expected.

**Never let the model adjust a number.** If a finding looks wrong, fix the rule and
say so. Do not silently re-score.

---

## 2. It cannot see ranking — and ranking is the #2 factor

A keyless run scores **11 of 23** Shepard factors directly and **5** partially (see the
`Keyless?` column in `references/CITATION_FACTORS.md`). Length and structured data are
reported and not scored. Four are wholly unmeasurable: **search rank
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

- **91.07% of cited URLs appeared in exactly one engine** — ChatGPT, Perplexity or Google
  AI Overviews — for the same prompt (Kevin Indig, *"The Consensus Gap"*, Growth Memo,
  2026-05-11, `https://www.growth-memo.com/p/the-consensus-gap`; 20,000 prompts, 3.7M URL
  citations, only 2.37% appeared in all three). ⚠️ **Vendor research** — the data is
  Omnia, Indig's own product, and he states it is "skewed toward Omnia's customer base."
  This is URL-level overlap across three named engines, not a general claim about
  "platforms". Single-engine tracking is, arithmetically, near-zero tracking. Anyone
  reporting AI visibility from ChatGPT alone is reporting a fraction of the signal and
  calling it 100%.
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
| On-page edits | Weeks | Practitioner consensus; consistent with arXiv 2605.25517's "recent timestamp helps consistently" |
| Third-party citation changes | Months, unquantified | No reliable public source |

**Never promise a GEO uplift in under 60 days.** Anyone who does is selling a
timeline they cannot control.

**Provenance note — there is no number here on purpose.** This file previously carried a
"60–120 days to first citation lift" figure attributed to an n=5 field test. That source
could not be located, no URL or snippet was found, and the figure is **widely repeated
without a traceable primary**. It has been removed. **No reliable public source for a
specific citation-lift window exists.** If a user or vendor hands you one, ask for the URL
and the methodology; a number without both is a guess, and this repo does not print guesses.
The rule above survives the removal — it rests on the absence of evidence, not on a figure
anyone can produce.

**And the horizon applies to this audit too.** An audit run today cannot have
produced a citation change yet. Re-auditing the same page in 30 days will show
on-page edits and no citation movement; that is the expected result, not a failure.

---

## 5. Stale-input failure — the mode this skill inherits from the data layer

This skill fetches a page. Pages change. The failure documented in the wider
workflow literature applies here in miniature
([r/AiAutomations, 2026-09-07](https://www.reddit.com/r/AiAutomations/comments/1w9h1sv/an_seo_agent_kept_working_for_two_weeks_after_its/)):

> *"A GSC OAuth token expired and the agent continued using cached Search Console
> data for two weeks. Rankings were changing while its decisions were still based on
> the old view… The workflow can run successfully against an input that should no
> longer be trusted."*

Corroborated ([r/SideProject, 2026-09-24](https://www.reddit.com/r/SideProject/comments/1wp4s2r/do_unique_stuff_a_real_mcp_data_server/)) against a product claiming
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

From an underpowered 5-client field test — these surfaced in practice and do not appear in
the 23. (The specific source could not be verified; treat the whole section as hypotheses,
which is how it is used below.)

1. **Third-party citation density.** How often the brand is cited *by other sites*.
   Consistent with Muck Rack's 25M+ cited-links finding (⚠️ vendor research): earned
   media 84% of AI citations vs 0.3% paid. Not measurable from one page.
2. **YouTube listicle inclusion.** Presence in "best X" video or list content, which
   retrieval surfaces reach differently from web pages. Not measurable keylessly.
3. **Date-stamped freshness.** Independent signal from E-05 in the field data —
   pages visibly carrying a current date performed better. Directionally consistent
   with arXiv 2605.25517's "recent timestamp helps consistently", but measured on
   clients, not trials.
4. **Entity-naming consistency.** Covered by E-01. See
   [ENTITIES.md](ENTITIES.md) for why the cheap/low-risk synthesis beats both
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

- **It does not score `llms.txt` absence as a defect.** Shepard scores it 2.0/10, the
  lowest of his 23. **State the claim narrowly:** an `llms.txt` file does not get you
  cited in AI search answers. It **is** fetched, mostly by coding agents and by the
  industry studying it. **Never write "does not work" or "does nothing"** — those
  overclaim, and the evidence below contradicts them.

  | Study | Type | Date | N | Result |
  |---|---|---|---|---|
  | Ahrefs (`https://ahrefs.com/blog/llmstxt-study/`) | measured | 2026-06-15 | 137,210 domains | 28% have llms.txt; **97% received zero requests**; of the 3% fetched, 96% from bots, 12% from GEO researchers; **zero AI-bot requests for files that don't exist — they never go looking** |
  | SE Ranking | vendor research | 2026-10-15 | ~300,000 domains | 10.13% adoption; XGBoost more accurate with llms.txt removed: *"LLMs.txt might currently introduce more noise than value."* |
  | Otterly.AI | vendor research | 2026-02-05 | 62,100 AI bot visits / 90d | 0.1% hit /llms.txt (84 requests); no positive correlation with AI crawl activity |
  | Search Engine Land | editorial | 2026-01-20 | 10 sites, 90d before/after | *"llms.txt documented those efforts. It didn't drive them."* Sites that launched **new functional content** gained; sites that merely documented existing content gained nothing. ⚠️ SEL's own counts are internally inconsistent (2 up + 8 flat + 1 down = 11 for a stated n=10). |
  | CueScout | vendor research | 2026-10-15 | 537 SaaS sites, 80 AI Mode answers | 24.3% cited with llms.txt vs 21.8% without (Fisher p=0.53); **none of the 708 cited links pointed at an llms.txt file**; site size dominated |
  | Server-log study, Zenodo `10.5281/zenodo.23018429` | measured | 15-day origin log | 345,808 requests | **Zero** requests to /llms.txt from any of the 22 published crawler tokens; robots.txt got 698 from 11 distinct tokens |

  **The upper bound.** The 28% adoption figure is an **upper bound** — Ahrefs' customer
  base skews technical — and their words are: *"Every figure in this study is therefore a
  ceiling on actual llms.txt consumption."*

  **Google, first-party.** Not a secondhand quote, and not the `ai-features` page — the
  sentence sits on the newer AI optimization guide:
  > *"You don't need to create new machine readable files, AI text files, markup, or Markdown
  > to appear in Google Search (including its generative AI capabilities), as Google Search
  > itself doesn't use them."*
  > — [Google Search Central, "AI features and your website"](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

  **Mueller's framing.** His *"temporary crutch, perhaps to save some tokens"* came from a
  Bluesky reply to Lily Ray about Google's **markdown mirrors of developer documentation**,
  not a standalone verdict on `llms.txt` as a file. Also his: *"For non-developer sites,
  I don't think this makes much sense… Making a markdown version of a shoe's specs is not
  going to get you more sales (competitors appreciate tho)."* Write-ups:
  `https://www.seroundtable.com/google-adds-markdown-files-to-help-docs-41342.html`,
  `https://searchengineland.com/google-llms-txt-chrome-lighthouse-478246`.

  **The counter-evidence that must ship with the claim.** Ahrefs, read in full: *"AI
  agents, and the infrastructure built to serve them, drive 10.5% of llms.txt requests —
  more than any other type of AI bot"*, and *"Aside from statespace-indexer and GPTBot,
  Claude-Code out-fetched every AI retrieval bot, every AI assistant, and every AI training
  crawler."* And announced in robots.txt, crawlers demonstrably fetch the file (Nathan
  Hall, Zenodo `10.5281/zenodo.23128812`, 2026-10-03: 1,549 fetches across 165 site-days,
  ClaudeBot = 1,131; ten un-referenced siblings got zero across 60 file-months; his caveat:
  *"That is discovery, not adoption."*). Retrieval is not parsing, indexing, ranking or use.
- **It does not recommend FAQPage schema.** 5.6/10, and Google stopped showing FAQ
  rich results for most sites. Schema is worth doing for rich results and entity
  clarity, not for GEO.
- **It does not automate posting anywhere.** Reddit removed **all four subreddit
  communities OtterlyAI built for its own 60-day GEO engagement experiment**, for a breach
  of **Rule 2 of Reddit's Content Policy** — not specifically for upvote automation
  (`https://otterly.ai/blog/reddit-geo-2026/`, a vendor's self-report of its own failed
  experiment). **Measure Reddit. Never post to it.**
- **It does not award points for formatting.** arXiv 2605.25517: formatting-only
  edits had little impact across 252,000 trials.
- **It does not generate content, fake authors, or rewrite the page.** Google's
  2026-10-01 guidance calls fake authors deception. Analysis is deterministic; prose
  is the operator's.
- **It does not estimate rank.** If rank data is unavailable, the report says "not
  measured".
