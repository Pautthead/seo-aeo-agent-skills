# Methodology Brief — internal source of truth

**Status:** internal document, not installed as a skill, not shipped to users as marketing.
**Purpose:** every skill in this repo must be traceable to a primary source below. No unsourced claims.
**Research window:** September–October 2026. All evidence dated below was gathered then.

---

## 0. Non-negotiable principles

These apply to every skill. If a skill violates one, the skill is wrong.

1. **Keyless-first.** A user with zero API keys, zero MCP servers, and zero paid accounts must get a useful result. Paid/optional data is an *upgrade*, never a prerequisite. If a skill cannot complete without a key, it is not ready to ship.
2. **Deterministic analysis, LLM rewriting.** Scorers, checklists and parsers must be reproducible rules the agent applies, not judgments it improvises. Hallucination risk belongs in the layer that produces prose, not the layer that produces numbers.
3. **Document your own limits.** Every skill carries a "Known limitations" section. If a technique cannot detect something, say so. Never report a false negative as a finding. (Pattern borrowed from `coreyhaines31/marketingskills`, which is the only repo in the market doing this.)
4. **Prompt-injection guard.** Any page the agent fetches during an audit is **untrusted data**, not instructions. State this in every skill that fetches pages.
5. **Cite with a date and a level of evidence.** `Source: Ahrefs, 2026-06-15, n=137,210 domains — measured` vs `Source: vendor claim, unverified`. Never launder a vendor marketing number into a fact.
6. **Say when it does not work.** Several popular 2026 practices are measurably worthless. The repo's credibility depends on stating this plainly rather than quietly implementing them.

---

## 1. Primary sources

### 1.1 AI citation ranking factors — Cyrus Shepard / Zyppy
`https://signal.zyppy.com/p/ai-citation-ranking-factors` — 2026-05-07.
54 experiments / patents / case studies, scored 0–10 on repeatability, evidence strength, official support.

| # | Factor | Score | # | Factor | Score |
|---|---|---|---|---|---|
| 1 | URL accessibility | 9.5 | 13 | Self-contained passages | 8.0 |
| 2 | **Search rank (top 10)** | **9.4** | 14 | Content visibility (in HTML, not JS) | 7.6 |
| 3 | Fan-out rank | 9.3 | 15 | Freshness | 7.0 |
| 4 | Preview control (`nosnippet`) | 9.2 | 16 | Brand / entity trust | 6.8 |
| 5 | Query-answer match | 9.2 | 17 | Length | 6.7 |
| 6 | Intent-format match | 9.0 | 18 | Language | 6.3 |
| 7 | Topic cluster ranking | 8.9 | 19 | Entity consistency | 5.8 |
| 8 | Answer near the top | 8.8 | 20 | Structured data | 5.6 |
| 9 | AI-ready structure | 8.6 | 21 | Known source | 5.4 |
| 10 | Factually specific | 8.3 | 22 | Domain authority | 5.0 |
| 11 | Explicit phrasing | 8.1 | 23 | **llms.txt** | **2.0** |
| 12 | Cites sources | 8.0 | | | |

Author's summary: *"win SEO, win AI citations (most of the time, with extra steps)."*
Corroborating: SearchPilot, 2026-10-02 — sites that lost organic visibility lost their AI citations too.

**Implication for our skills:** the highest-value audit finding is almost never a GEO trick. It is "this page doesn't rank" or "this page's answer isn't near the top." Do not let the framework imply GEO is a separate discipline.

### 1.2 Competitive GEO controlled experiment — arXiv 2605.25517
`https://arxiv.org/abs/2605.25517` — 2026-05-25. Rahul Vishwakarma, Shushant Kumar,
Ratnesh Jamidar; cs.AI. **Measured.** ⚠️ The abstract discloses the checklist was
"exercised in an early internal pilot at Sprinklr" — industry-affiliated.
252,000 trials, 6 LLMs, two-source injected RAG, brand names anonymised, order counterbalanced.

- Topical relevance and list position dominate.
- **Explicit price information** and **a recent timestamp** help consistently.
- Completeness and trust cues: smaller gains.
- **Formatting-only edits: little impact.**
- Follow-up commentary (Lily Ray): *"The sites that try to create as much content as possible eventually get burned, including very big brands."*

### 1.3 Information Gain — patent US11354342B2 + Ahrefs
`https://patents.google.com/patent/US11354342B2/en` · `https://ahrefs.com/blog/information-gain/` — 2026-08-20.

Definition (Ahrefs, Louise Linehan): *"the additional information your page contributes beyond what already ranks for the query."*

**The load-bearing mechanism is fact-pruning.** The patent describes an assistant answering using source 1 for facts A+B, then source 2 for fact C *only*, deleting the overlap. Ahrefs' consequence:
> *"In a ranked list, even if you're the fourth site saying the same thing, you're still on the SERP… But in a synthesized answer there **is** no position four. Either you provide the information that hasn't been said yet, or your content gets cut."*

Bernard Huang (ex-Clearscope) on where gain lives: *"the concepts and entities on the fringe of Google's knowledge graph for the topic."* — i.e. at the edges, not the centre.

**Measured magnitude.** ⚠️ **Vendor research** — On-Page.ai **sells a scoring product, and
the Information Gain Score is their own metric.** Eric Lancheres, On-Page.ai Research,
2026-06-12, `https://api.on-page.ai/research/information-gain-study`: 150 top-3 pages,
50 keywords, 10 verticals, US/English, single-day scan. Pages with ≥15 unique data
points averaged **62.1** (n=22); pages with 0–1 averaged **40.2** (n=45). Overall the
study reports a **median page score of 52/100** and Pearson **r = 0.17**. Its own
load-bearing sentence: **"Within the top 3, position was unrelated to the score."** All
150 pages were top-3, so nothing in the data separates position 1 from position 3.
Originality is the variable, not rank.

**Caveat to carry:** Ahrefs is explicit that Google has not confirmed this. The score is measured by *meaning*, so statistic-stuffing fails. There is practitioner dissent (`r/SEO`, 2026-01-26: *"there is no information gain requirement — how do I know this — I publish 100's of 000's of PAAs/FAQs a month"*). Keep that dissent in the reference file.

### 1.4 `llms.txt` — it does not get you cited in AI answers

**This is the best-evidenced finding in the repo. Do not implement it as a growth lever.**

**State the claim narrowly, because the absolute version is false — and this repo's own
research contradicts it.** The defensible claim is: **an `llms.txt` file does not get
you cited in AI search answers.** It *is* fetched, mostly by coding agents and by the
industry studying it. Ahrefs, read in full:

> *"If your goal is showing up in ChatGPT, Perplexity, or AI Overviews, an llms.txt file
> is largely decoration."*

> BUT: *"AI agents, and the infrastructure built to serve them, drive 10.5% of llms.txt
> requests — more than any other type of AI bot"* … and *"Aside from statespace-indexer
> and GPTBot, Claude-Code out-fetched every AI retrieval bot, every AI assistant, and every
> AI training crawler."*

**Never print "does not work" or "does nothing" anywhere.** Those overclaim. Retrieval is
not parsing, indexing, ranking, or use.

| Study | Type | Date | N | Result |
|---|---|---|---|---|
| Ahrefs (`https://ahrefs.com/blog/llmstxt-study/`) | measured | 2026-06-15 | 137,210 domains | 28% have llms.txt; **97% received zero requests**; of the 3% fetched, 96% from bots, 12% from GEO researchers; **zero AI-bot requests for files that don't exist — they never go looking** |
| SE Ranking (`https://seranking.com/blog/llms-txt/`) | vendor research | 2026-10-15 | ~300,000 domains | 10.13% adoption; their XGBoost model became *more* accurate when llms.txt was removed as a variable: *"LLMs.txt might currently introduce more noise than value."* |
| Otterly.AI (`https://otterly.ai/blog/the-llms-txt-experiment/`) | vendor research | 2026-02-05 | 62,100 AI bot visits / 90d | 0.1% hit /llms.txt (84 requests); no positive correlation with AI crawl activity |
| Search Engine Land (`https://searchengineland.com/does-llms-txt-matter-467740`) | editorial | 2026-01-20 | 10 sites, 90d before/after | 8 no change, 1 −19.7%, 2 grew 12.5%/25% — *"llms.txt documented those efforts. It didn't drive them."* Sites that launched **new functional content** gained; sites that merely documented existing content gained nothing. ⚠️ SEL's own arithmetic is internally inconsistent (2 up + 8 flat + 1 down = 11 for a stated n=10); treat the counts as approximate. |
| CueScout (`https://cuescout.com/blog/does-llms-txt-work`) | vendor research | 2026-10-15 | 537 SaaS sites, 80 AI Mode answers | 24.3% cited with llms.txt vs 21.8% without (Fisher p=0.53, permutation p=0.56); **none of the 708 cited links pointed at an llms.txt file**; site size dominated (59% citation in Tranco top-10k vs 6% outside top 1M) |
| Server-log study — Zenodo **`10.5281/zenodo.23018429`** (Evgenii Arsentev, 2026-09-28, CC-BY-4.0) | measured | 15-day origin log | 345,808 requests | **Zero** requests to /llms.txt from any of the 22 published crawler tokens; **robots.txt got 698 requests from 11 distinct crawler tokens**, sitemap.xml 282 |

**Caveats these six must carry.** The Ahrefs 28% adoption figure is an **upper bound** —
Ahrefs' own customer base skews technical — and their words are: *"Every figure in this
study is therefore a ceiling on actual llms.txt consumption."* The server-log study is one
origin behind a CDN with origin-only logging, three pooled hostnames, self-asserted
crawler identity and ~2 days of exposure; it also corrects its own earlier Internet-Draft
figures. Search Engine Land is SEL's own research promoting SEL.

**Google, in its own documentation.** Not a secondhand quote — a first-party statement,
and strictly stronger than anything attributed to a spokesperson:

> *"You don't need to create new machine readable files, AI text files, or markup to appear
> in these features."*
> — [Google Search Central, "AI features and your website"](https://developers.google.com/search/docs/appearance/ai-features),
> in a section headed *"Mythbusting generative AI search: what you don't need to do"*.

Cite the page, not a date: its own footer reads "Last updated 2025-12-10 UTC", while
secondary sources variously claim May, June and July 2026 for different Google pages.

**John Mueller — framing matters.** His "temporary crutch" line came from a **Bluesky reply
to Lily Ray** about Google's **markdown mirrors of developer documentation**, not a
standalone verdict on `llms.txt` as a file. Citable write-ups:
`https://www.seroundtable.com/google-adds-markdown-files-to-help-docs-41342.html` and
`https://searchengineland.com/google-llms-txt-chrome-lighthouse-478246`. His verbatim:
*"it's not done for search"* and *"OF COURSE they can read HTML just fine, so this is imo
more of a temporary crutch, perhaps to save some tokens."* And the line that supports this
repo's position most directly:

> *"For non-developer sites, I don't think this makes much sense… Making a markdown
> version of a shoe's specs is not going to get you more sales (competitors appreciate tho)."*

Cyrus Shepard scores `llms.txt` 2.0/10, the lowest of 23 factors.

**The nuance worth shipping — retrieval is not adoption.** Nathan Hall, Zenodo
**`10.5281/zenodo.23128812`** (v1.2, 2026-10-03; concept DOI `10.5281/zenodo.22814843`),
found crawlers *do* fetch `llms.txt` **when it is announced in robots.txt**:
- `/ai/llms.txt` announced in robots.txt + linked in HTML: 1,549 fetches across 165
  site-days; ClaudeBot = 1,131 of them.
- Ten un-referenced files in the same directory: zero requests across 60 file-months.

The author's own caveat: *"Tell a crawler where a file is and it fetches the file. That is
discovery, not adoption."* It is URL retrieval after robots.txt discovery — **not** evidence
of parsing, indexing, ranking, or use in answers. Two caveats the repo must carry: the
measured file is **`/ai/llms.txt`, not the root file**, and the author **owns Lefty Media Co
and builds the plugin that announces the file being measured**.

**The adjacent finding that IS actionable — markdown mirrors.** a14y research
(`https://a14y.dev/research/llms-txt-linking/`, benchmark `llms-txt-linking-2026-06-27`,
Claude 2.1.141, isolated Docker, n=5 per arm, single site): same task, same model, same
prompt, llms.txt index + markdown mirrors present → ~123K tokens / ~10 tool calls; absent
→ ~240K tokens / ~20 tool calls. Answer quality tied. *"The cost is ingestion, not generation."*

The second study ran **five arms, of which only three were link formats** — `<link
rel="llms-txt">` (0/5), `<link rel="alternate" type="text/markdown">` (0/5), and a visible
"For agents" footer link (0/5). The other two arms were a **no-link control** (0/5) and the
**prompt nudge** (5/5, with 4/5 also pulling sitemap.md). The nudge arm ran 177,735 ± 32,131
tokens against a 266,591 ± 32,066 control = **−33%**, with the highest judge score
(88.8 ± 1.6).
> *"It's not that we picked the wrong link format. Every link format failed. The lever is the instruction, not the markup."*

The same survey puts CrUX-top-100k `llms.txt` adoption at **27% (50,074 sites reached)**.

Practical read: ship `.md` mirrors (they cut ingestion cost when *anything* fetches them).
If you ship llms.txt at all, ship it in an hour and announce it in robots.txt. Budget zero
forecast against it.

### 1.5 Google content guidance — the 2026 tightening
Google's 2026-10-01 rewrite of its AI-generated content guidance:
> *"It is critical to manually factcheck and review all AI-generated content for accuracy and trustworthiness before publishing."*

Barry Schwartz's widely-cited point: **"critical" is a word Google rarely uses.** It applies to titles, meta descriptions, structured data and alt text — i.e. even metadata now requires review.

New rater-guidance definitions of "main content" name four quality dimensions — **effort, originality, talent/skill, accuracy** — and name mass-produced AI content as an example of "little to no effort." **Fake authors are now explicitly called deception.**

Gary Illyes (Search Central Live Barcelona, 2026-10): Google considers scaled AI content a **bigger problem than link spam**. Four spam updates ran in 2026, versus one in all of 2025.

### 1.6 AI slop is detectable from structure
Jochen Madler (Sitefire), *"SlopShape: Identifying AI-Generated Commercial Web Content"*,
`https://arxiv.org/abs/2609.15369` — submitted 2026-09-14, v3 2026-09-28, cs.CL.
**Measured.** The metric is **97.0 macro-F1 on held-out companies** — *not* an accuracy
percentage — from **176 structural features** out of a 203-feature instrument. Corpus:
2,250 pre-ChatGPT human blog posts across 268 company domains vs 11,250 AI mirrors from 5
frontier models. Held-out reworded robustness 96.1; source attribution 68.6% correct
against a 16.7% chance baseline.

You cannot paraphrase your way out — the shape is the tell. This is the empirical basis for
any anti-slop guidance in this repo.

### 1.7 Stale-input failure mode — the gap this repo leads with
`r/AiAutomations`, 2026-09-07:
> *"At analook dot com, a GSC OAuth token expired and the agent continued using cached Search Console data for two weeks. Rankings were changing while its decisions were still based on the old view. That is an awkward failure to catch with a simple 'did the workflow run?' check. The workflow can run successfully against an input that should no longer be trusted."*

The proposed fix, and the basis for `seo-data-contract`:
> *"the input check needs to answer three separate questions: can it authenticate now, when did a retrieval last succeed, and what is the newest date represented in the retrieved data?"*

Corroborating, `r/SideProject` 2026-09-24, against a ClickHouse-backed GSC MCP product claiming "sub-5-second analysis without hallucination risks": *"a fast ClickHouse query can still return confidently outdated Search Console data unless every report exposes its latest import time."*

Practitioner consensus, `r/SEO_Xpert` 2026-07-19 — an agent proposed ~150 internal links with total confidence; **~20 were actually usable**. And: opening a **fresh session** with the identical page produced different recommendations, i.e. the agent cannot reproduce its own prior analysis.

### 1.8 GEO ≈ 80% ordinary SEO
Jeremy Moser (uSERP) via Digiday, 2026-03-10:
> *"80 percent of GEO is good, fundamental SEO. If a GEO service does not openly tell you that success in AI visibility is 80 percent good fundamental SEO, they are selling you snake oil."*

Lily Ray on correlation: a brand with established authority appears in ChatGPT and concludes its GEO campaign is working, when the more plausible explanation is that its existing SEO visibility got it into the indexes feeding those products. She also documented a GEO vendor case study where organic traffic **fell 66%** while "AI visibility" rose.

Positioning consequence: this repo must never imply AEO/GEO is a separate discipline to be bought. It is an audit of the same pages, scored for a second consumption mode.

### 1.9 Measurement reality
- **91.07% of cited URLs appeared in exactly one engine.** Kevin Indig, *"The Consensus
  Gap"*, Growth Memo, **2026-05-11** — primary: `https://www.growth-memo.com/p/the-consensus-gap`
  (secondary coverage: Search Engine Journal, Greg Jarboe, 2026-08-08,
  `https://www.searchenginejournal.com/ais-impact-is-outrunning-measurement-the-trust-and-attribution-gap-facing-brands/584141/`).
  Scope matters and is usually lost in paraphrase: this is **URL-level overlap across three
  named engines** — ChatGPT, Perplexity and Google AI Overviews — not a general statement
  about "platforms". 20,000 prompts, 3.7M URL citations; only **2.37%** of cited URLs
  appeared in all three for the same prompt. ⚠️ **Vendor research** — the data is Omnia,
  Indig's own product, and he states the dataset "is skewed toward Omnia's customer base."
  Single-engine tracking is near-zero tracking.
- **AI Overviews are right most of the time and still misleading you.** New York Times +
  Oumi, April 2026 (*How Accurate Are Google's A.I. Overviews?*, 4,326 SimpleQA searches):
  **85% accurate with Gemini 2** (Oct 2025), **91% with Gemini 3** (Feb 2026) — the 91% is
  the Gemini 3 figure specifically, not an overall number. More than half of the correct
  February responses were **"ungrounded"**: ungrounded **37%** of the time in October,
  rising to **56%** with Gemini 3. Oumi's own headline is harsher than ours — only **39%
  of Gemini 3 overviews were both correct and fully supported**, and only **67% of
  individual claims** were supported by cited sources. **Google publicly disputed the
  study** (Ned Adriance: *"This study has serious holes… It doesn't reflect what people are
  actually searching on Google"*), on the grounds that SimpleQA is OpenAI-built and
  unrepresentative. Any honest citation carries the dispute.
- Google's own Search Console data is reported ~75% incomplete for AI features; there is **no separate AI Mode data** in Search Console.
- "Citation data is noisy. Run the same prompt 10 times, get different outputs" (`r/DigitalMarketing`, 2026-04-17).
- **No reliable public source gives a specific citation-lift window.** The "60–120 days to
  first citation lift" figure this brief previously carried came from a field test that
  could not be verified, and it has been removed (see §1.9c). What survives is the
  qualitative position and it is enough: on-page changes move in weeks; third-party
  citation changes take longer. **Do not quote a number, and do not sell a timeline you
  cannot source.** The rule "never promise a GEO uplift in under 60 days" stands on the
  absence of evidence, not on a figure anyone can produce.

### 1.9b Lily Ray's verified experiments — read directly, not paraphrased

Primary source, full text read 2026-10-19: `https://lilyraynyc.substack.com/p/the-ai-slop-loop`, *The AI Slop Loop*, 2026-04-14.

> "I would warn marketers or publishers trying to take SEO or GEO advice from large
> language models: the information is contaminated, and should always be verified by
> real experts with experience in the field."

> "There is no real mechanism for distinguishing between information that is true and
> information that is simply repeated across enough sources. Repetition is treated as
> consensus."

The loop mechanism, as she describes it: one AI-generated article hallucinates a detail → sites running AI content pipelines scrape and regurgitate it → more AI-generated sites scrape the same misinformation → a fabricated claim now has citations. *"For a RAG-based system like Perplexity or AI Overviews, enough citations are basically all it needs to treat something as fact."*

**Her own experiment, January 2026.** She published a deliberately fabricated article about a non-existent Google core update on her own blog — an established-authority SEO domain. Within 24 hours Google AI Overviews served the fabricated information to users as fact, and contextualised a detail from the fake article against a real 2024 incident. ChatGPT surfaced the same claim. Claude was not fooled. BBC journalist Thomas Germaine ran the same test on a low-authority personal site and got the same result.

Her September 2025 origin case: Perplexity invented a "September 2025 Perspectives Core Algorithm Update", citing two AI-generated articles on agency blogs. As of this writing it is still in the retrieval layer and LLMs still answer it with complete confidence.

Relevance to this repo: a human being was in the loop — her client, who forwarded the wrong information without knowing — and the artefact still arrived wrong. **Review catches errors; it does not manufacture the missing original fact.**

### 1.9c Claims we removed during validation, and why

Recorded so the next contributor does not reintroduce them.

| Claim | Origin | Action | Reason |
|---|---|---|---|
| "Several sites claimed to have human editors reviewing the AI drafts. Google devalued them anyway…" | Attributed to Lily Ray | **Removed** | The full text of *The AI Slop Loop* does not contain this quote. It is likely real but from another post; unsourced, it fails the repo's own standard. Replaced with §1.9b, which is verified. |
| "60% of programmatic pages deindexed within 5 months" plus three survivor properties | `r/bigseo`, 2026-05-01, surfaced in a research pass | **Removed** | Could not be independently verified. The three properties remain valuable as *hypotheses*, re-labelled as such. |
| "There is no benefit to creating a llms.txt file for SEO." attributed to **Danny Sullivan**, Search Central Live Toronto, 2026-04 | Unsourced quote | **Removed** | No source located anywhere, and the linked URL was a blog *index*, not a post. Per the repo's own rule an unsourced quote fails. Replaced with Google's first-party documentation (§1.4), which is strictly stronger. |
| "25,000 spammy posts/day" attributed to Reddit, 2026-07 | Reddit Inc blog | **Removed** | NOT CONFIRMED. The post *"How We're Keeping Reddit Real and Safe in the AI Era"* (2026-07-06) is listed in the Reddit Inc blog index, but the permalink 404'd and the body was never read. Do not print the figure. |
| "Reddit began labelling legitimate bot accounts (2026-03)" | Reddit Inc blog | **Removed** | Unverified in the verification pass. Do not print. |
| "60–120 days to first citation lift" (n=5 field test, 2026-05-27) | Unidentifiable field test | **Removed** | No URL, no snippet, no primary text — **NOT FOUND**. This number was load-bearing for the "no 60-day promises" position, which is exactly why it could not be left resting on a source nobody can open. The position survives without the figure; see §1.9. |
| "robots.txt got 2,135 requests" | Origin-log study, Zenodo `10.5281/zenodo.23018429` | **Corrected** | NOT FOUND in the deposited data. The aggregate gives **`post_robots: 698`** (11 distinct crawler tokens) for the 9–11 Sept post-deployment window. `345,808 requests` and `crawler_ctx_retrievals: 0` are correct. |
| "~98% accuracy" for arXiv 2609.15369 | SlopShape | **Corrected** | The metric is **97.0 macro-F1 on held-out companies**, not an accuracy percentage. See §1.6. |
| "five link formats all scored 0/5" | a14y.dev | **Corrected** | Five arms, of which only **three** were link formats; the other two were a no-link control (0/5) and the prompt nudge (5/5). See §1.4. |
| "AI agents account for **10.5% of llms.txt requests — more than any other bot type**" | Ahrefs, `llmstxt-study` | **Corrected** | Misattribution of the *unit*. The 10.5% is **AI agents alone**, and that category sits **fifth overall** (SEO audit tools 21.7%, unidentified 14.9%, general crawlers 13.1%, tech profiling 11.6%). "More than any other bot type" belongs to the **19.5%** figure obtained by combining the four AI categories. Also added: **77% of bots fetching the file are not AI tools**, and the Claude-Code quote's omitted prefix *"Aside from statespace-indexer and GPTBot"*. |
| "Six **independent** 2026 studies" | README headline | **Corrected** | Three of the six (Ahrefs, OtterlyAI, Arsentev) measure **fetches of the file**, not citations; three are vendor research and one is editorial. "Independent" was wrong and is gone. Current wording: *"Six 2026 studies find no link between publishing the file and more citations or more crawling."* |
| Mueller's *"temporary crutch … to save some tokens"* framed as being about `llms.txt` | via Ahrefs | **Corrected** | The thread's subject was Google's **markdown developer docs**. Ahrefs extends the point to the file. The README now attributes the extension to Ahrefs rather than to Mueller. |
| "the most common state in the market" (for a site with no `Sitemap:` directive) | Our own example finding | **Removed** | Unsourced generalisation about the market. The factual observation (no named-token policy, no `Sitemap:` directive) stands on its own. |
| "Every **claim** links to its primary source" | README header note | **Corrected** | Too broad: it swept in quotes, competitor star counts and vendor prices, which are labelled differently. Now reads *"every statistic"*, with the secondary sources listed in `SOURCE-VERIFICATION.md`'s appendix. |

### 1.10 Off-site authority, and the Reddit trap
⚠️ **Vendor research.** Muck Rack, "What is AI Reading", 2026-05-07, 25M+ cited links:
**earned media 84% of AI citations vs 0.3% paid.** Three caveats: "earned media" is
Muck Rack's own definition (*"journalism, academic research, government sources,
encyclopedic sites, and third-party corporate content"*), so Wikipedia and PubMed Central
sit **inside** the 84% — it is not 84% journalism; Muck Rack's own 2026-05-27 webinar recap
says "1 million or more links", a 25× discrepancy against its 7 May post; and the full
report is gated.

GeoTest (GEO Score v6.0, in force since 2026-10-04) weights Citation Worthiness at 34/100 —
the largest single category — measuring sourced facts per 1,000 words, coverage of facts
cited pages agree on, attributed quotations, external citations, comparison tables, quotable
definitions. ⚠️ **Vendor research** — GeoTest sells the scoring product and the weights are
asserted, not derived. Note its own position is consistent with this repo's:
**"llms.txt (reported, not scored), 0 pts: Reported as a recommendation. It carries no
points until citation data shows it matters."**

**Do not automate Reddit posting.** Reddit **removed all four subreddit communities
OtterlyAI built for its own 60-day GEO engagement experiment**, for a breach of **Rule 2 of
Reddit's Content Policy** — not, as previously written, specifically for upvote
automation. Cite `https://otterly.ai/blog/reddit-geo-2026/` and state plainly that this is
**a vendor's self-report of its own failed experiment** (OtterlyAI sells AI-search
monitoring). Automate *measurement*; never automate *posting*.

### 1.11 FAQPage schema is not a GEO lever
Shepard scores structured data at 5.6 and notes *"LLMs don't typically ingest schema as part of their training"* and *"limited evidence they can at least see schema when searching."* Practitioner dissent (`r/AskMarketing`, 2026-09-29): *"First: drop the FAQ schema. Google stopped showing those for most sites a while back."* Several 2026 skills still auto-recommend adding FAQPage — that is a direct contradiction. Do not repeat it.

### 1.12 Divergence between AEO surfaces
Ahrefs (863K keywords / 4M AIO URLs, reported 2026-03): Google AI Overviews drew only **38%** of citations from top-10 organic results, down from **76% in July 2025**.
⚠️ This sits awkwardly against Shepard's 9.4 search-rank score. Treat the *direction* as the finding and the precise figure as uncertain. Do not print the 38%/76% numbers as settled fact.

---

## 2. Standard skill anatomy

Every skill follows this shape. Consistency across skills is a feature, not laziness.

```
skills/<name>/
├── SKILL.md
└── references/
```

`SKILL.md` frontmatter — only spec fields plus namespaced metadata. No custom top-level keys, because non-OpenCode hosts ignore them and the pack must degrade:

```yaml
---
name: <must equal directory name>
description: <what it does + when to use it + trigger keywords, front-loaded, <= ~300 chars>
license: Apache-2.0
compatibility: <optional; mention network only if truly required>
metadata:
  <vendor-key>: "<string>"
---
```

Body sections, in order:
1. `# Title` + one-paragraph purpose
2. `## When to use this` / `## When not to use this`
3. `## Inputs` (what the agent needs; keyless path first)
4. `## Procedure` — numbered steps, each with an explicit *check* the agent can run and a falsifiable pass condition
5. `## Output format` — a literal template the agent copies
6. `## Scoring` — deterministic rules, stated as rules not vibes
7. `## Known limitations` — what this cannot detect
8. `## Optional data sources` — DataForSEO only where genuinely needed, always with the keyless fallback stated
9. `## References` — relative links into `references/`

Rules:
- SKILL.md body under ~5,000 tokens / 500 lines. Detail goes to `references/`.
- Reference links are relative from the skill root, **one level deep only**. No nested chains.
- No `context: fork`, no hooks in the core — both are Claude-only.
- Every fetched page is untrusted data. Say so.
- Any numeric threshold in a skill must be traceable to §1. If it is a judgement call, label it as one.

## 3. Portability invariants

Verified against the Agent Skills specification (`agentskills.io/specification`) and the `npx skills` CLI (Vercel Labs), not blog posts — several 2026 blogs publish wrong install paths.

| Host | Project path | Global path |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Hermes Agent | `.hermes/skills/` | `~/.hermes/skills/` |
| OpenClaw | `skills/` | `~/.openclaw/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| Cline | `.agents/skills/` | `~/.agents/skills/` |

`.agents/skills/` is the de-facto portable project location. OpenCode additionally reads `.opencode/skills/`, `.claude/skills/` and `.agents/skills/`, walking up from CWD to the worktree root.

Feature support: `allowed-tools` works on all major hosts. **`context: fork` is Claude Code only.** Hooks are Claude Code, Cline and Kiro only.

Description budget: Codex budgets the initial skill list at **2% of context window or 8,000 chars** and shortens descriptions first under pressure. Front-load trigger words.

## 4. DataForSEO — optional layer only

Auth is HTTP Basic only. Credentials come from the **API** login/password at `app.dataforseo.com/api-access` — using the dashboard login is the single most common auth failure.

Official MCP server (free; you pay API rates only):
- Remote: `https://mcp.dataforseo.com/v3/mcp` with `Authorization: Basic base64(login:password)`
- Local: `npx -y dataforseo-mcp-server` with `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`
- Source: `github.com/dataforseo/mcp-server-typescript`

Pricing, Labs Google (live-only, no queue): **$0.012/task + $0.00012/item**, default on all `dataforseo_labs/google/*/live`. Exceptions: `historical_rank_overview/live` $0.12 + $0.0012; `historical_serps/live` $0.00012/SERP; `search_intent/live` $0.012 + $0.00012/keyword.

Limits that bite agents: max **700 keywords** per `keyword_overview` task, max **1000 items** per response, 2000 calls/min, 30 concurrent, 1 task per live call. Database refresh cycle is **30–90 days** — do not present Labs output as real-time.

**Pricing trap to document.** SERP API headline rates are $2.00/1k live, $1.20/1k priority, $0.60/1k standard. The $0.60 figure is the standard queue, which takes ~5 minutes. For an interactive agent that is not an equivalent product, so **$2.00 is the honest comparison**. State this whenever a rate is quoted.

Referral link (README only, optional-data table): `https://try.dataforseo.com/jijqq4kuyyde`

## 5. Market gaps this repo occupies

Derived from `RankSpotAI/awesome-seo-agent-skills` (CC0, "Nobody has built these well yet") plus independent review of the top-30 repos.

| Gap | Status in market | Our answer |
|---|---|---|
| Input freshness / silent-stale failure | **Nobody.** Most-cited structural complaint. | `seo-data-contract` (v1) |
| Deterministic analysis layer, LLM only for rewriting | Only `tigerless-labs/seo-ops` (no licence declared, structural checks only, no content/temporal layer) | Throughout |
| Keyless *site-scale* AEO audit | Two camps only: keyless-but-prompt-only, or data-rich-but-subscription-locked | This repo's baseline |
| Internal link graph mapping | *"Plenty of skills mention it, none actually map a link graph"* | Roadmap |
| Schema **validation** against rich results | *"Many skills generate JSON-LD, none validate it"* | Roadmap |
| Multilingual citability scoring | `zubair-trabzada/geo-seo-claude` issue #80: `citability_scorer` regexes are English-only | `aeo-citability-audit` (v1) |
| Skills documenting their own limits | Only `coreyhaines31/marketingskills` | Throughout |

Known correctness bugs in the current leaders, for context — do not reproduce:
- `zubair-trabzada/geo-seo-claude` #81: wrong Content-Signal keys, tools that cannot return the data the steps ask for, a wrong RFC number. #80: English-only regexes; `<dl>/<dd>` FAQ answers invisible to the block splitter. #19: falsely reports server-side-rendered sites as JS-rendered.
- `AgriciDaniel/claude-seo` #319: 16 files reference DataForSEO MCP v3 tool names that no longer exist, and the cost table is wrong. #180: broken on a fresh install (`lxml` 6 pin).
- `seranking/seo-skills`: stale ~4 months; vendor-locked to a SE Ranking subscription; `pagespeed_check.py: KeyError 'audit_details'`.
- `coreyhaines31/marketingskills` warning worth heeding: running the installer from inside an agent session may install only to `.agents/skills/`, which Claude Code does not read. Pass `-a claude-code` explicitly.

## 6. What this repo must never do

- Recommend `llms.txt` as a traffic or citation lever.
- Recommend FAQPage schema as a GEO tactic.
- Automate posting to Reddit or any forum.
- Promise a GEO uplift in under 60 days.
- Report a finding the technique cannot actually detect.
- Present a vendor claim as a measured result.
- Require a paid tool to complete the core workflow.