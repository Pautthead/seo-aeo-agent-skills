# SEO + AEO + GEO Skills for AI Agents

Evidence-based skills for Claude Code, Codex, Cursor, OpenCode, **Grok Build**, Gemini CLI, Cline, Hermes and ~75 other hosts. Every scoring rule traces to a dated source. **No API keys, no MCP servers, no subscription.**

```bash
npx skills add Pautthead/seo-aeo-agent-skills
```

> **Sources last verified 2026-10-19.** These statistics age in weeks. Every statistic in this README links to its primary source; the verification table is in [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md).

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Install](https://img.shields.io/badge/install-npx%20skills-8a2be2.svg)](https://www.npmjs.com/package/skills)
[![API keys](https://img.shields.io/badge/API%20keys-none%20required-brightgreen.svg)](skills/)
[![Skills](https://img.shields.io/badge/skills-4-orange.svg)](skills/)
[![Release](https://img.shields.io/badge/release-v1.1.0-informational.svg)](https://github.com/Pautthead/seo-aeo-agent-skills/releases)

---

## Quick start

```bash
npx skills add Pautthead/seo-aeo-agent-skills
```

Ask the agent:

> Run `aeo-bot-access-audit` on https://fluyeporlaweb.com

A real run on 2026-10-20, shortened. The full four reports are in [`examples/`](examples/).

```
# Bot Access Audit — fluyeporlaweb.com
Date: 2026-10-20 · Method: keyless (curl)

Verdict (that run): OPEN — 100/100
robots.txt 200, User-agent: * Allow: /. Edge: 16 user-agents × 5 pages, all 200,
same bytes as the browser. No cf-mitigated, no challenge.

Re-scored with rule 11 (this release): 95/100, still OPEN.
ClaudeBot is allowed and Claude-SearchBot has no group: −5 once.
The 95 is the new rule applied to that fact. The 2026-10-20 run printed 100.
```

| Skill | Worked example |
|---|---|
| `seo-data-contract` | [examples/seo-data-contract-fluyeporlaweb.md](examples/seo-data-contract-fluyeporlaweb.md) |
| `aeo-bot-access-audit` | [examples/aeo-bot-access-audit-fluyeporlaweb.md](examples/aeo-bot-access-audit-fluyeporlaweb.md) |
| `aeo-citability-audit` | [examples/aeo-citability-audit-fluyeporlaweb.md](examples/aeo-citability-audit-fluyeporlaweb.md) |
| `information-gain-analysis` | [examples/information-gain-analysis-fluyeporlaweb.md](examples/information-gain-analysis-fluyeporlaweb.md) |

## The four skills

| Skill | The question it answers | Needs keys? |
|---|---|---|
| [`seo-data-contract`](skills/seo-data-contract/SKILL.md) | Is this data fresh and trustworthy enough to act on? | No |
| [`aeo-bot-access-audit`](skills/aeo-bot-access-audit/SKILL.md) | Can AI bots actually fetch this site? | No (just `curl`) |
| [`aeo-citability-audit`](skills/aeo-citability-audit/SKILL.md) | Would this page survive being extracted and cited? | No |
| [`information-gain-analysis`](skills/information-gain-analysis/SKILL.md) | What does this page know that the SERP does not? | No |

These skills score the same pages for a second job: being **extracted, quoted and attributed** inside a synthesized answer.

---

## A real run

`aeo-bot-access-audit` against `ahrefs.com/blog/llmstxt-study/`, run on 2026-10-19. Reproducible with the commands in the skill:

```
$ curl -sI -A "Mozilla/5.0 ...; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot" <url>
OAI-SearchBot/1.4    HTTP 200
Claude-SearchBot     HTTP 200
PerplexityBot        HTTP 200
GPTBot/1.4           HTTP 200

$ curl -s <origin>/robots.txt
User-agent: *
Disallow: /article
Disallow: /site-explorer/ajax/
...
```

**Finding:** all four AI bots reach the edge and get `200`. The `robots.txt` names no AI bot at all — the wildcard covers them — so nothing is blocked. But there is **no `Sitemap:` directive**, and no named-token policy at all. The site is reachable by AI retrieval bots and has made no deliberate decision about it.

That distinction is the point of the skill. A clean `robots.txt` proves nothing on its own: Cloudflare, Akamai and AWS WAF all enforce *before* your origin parses a robots file. The edge check is the only one that means anything.

---

## Why this exists

Three failure modes, all structural rather than clever.

**1. Silent stale data.** The most-cited structural complaint in agentic SEO. From [r/AiAutomations, 2026-09-07](https://www.reddit.com/r/AiAutomations/comments/1w9h1sv/an_seo_agent_kept_working_for_two_weeks_after_its/):

> *"At analook dot com, a GSC OAuth token expired and the agent continued using cached Search Console data for two weeks. Rankings were changing while its decisions were still based on the old view... The workflow can run successfully against an input that should no longer be trusted."*

The workflow exits 0. The report looks fine. Every number in it is a fact about the past phrased in the present tense.

**2. Confident, unreproducible output.** From [r/SEO_Xpert, 2026-07-10](https://www.reddit.com/r/SEO_Xpert/comments/1ush4r6/my_experience_with_using_ai_claude_codecodex_for/): an agent proposed ~150 internal links with total confidence; ~20 were usable. The same page, in a fresh session, produced different recommendations. Nothing in the output told you which items came from data and which came from the model's priors.

**3. Techniques that were never earning their keep.** `llms.txt` has been sold, blogged and shipped as an AI-visibility lever all year. Six 2026 studies find no link between publishing the file and more citations or more crawling. [The evidence table is below](#what-these-skills-refuse-to-do).

---

## The four skills in detail

### `seo-data-contract` — freshness and provenance before analysis

Every SEO number an agent uses is a claim about the past. This forces a dated, sourced envelope onto that number before a word of analysis is written, and refuses the analysis outright when the input can no longer be trusted.

Three questions, all of which must pass:

1. **Can it authenticate right now?** A cached response is not an auth check.
2. **When did a retrieval last succeed?** Not the vendor's last update — the agent's own last successful pull.
3. **What is the newest date represented *inside* the data?** Not the fetch time. A query run at 14:03 today can return rows whose last complete day is three weeks ago.

Then one deterministic classification — `fresh · aging · stale · expired · unknown · observed` — computed as a subtraction against the source's expected latency. A credential that is `expired` or `revoked` on aged data floors the class at `stale`: the data isn't just old, it's frozen, and there is no path back to `fresh`. `unavailable` deliberately does not floor, because a user pasting a GSC export never had a credential to lose, and refusing that would break the keyless path this repo is built on.

Handles the dominant real-world case explicitly: *the user just typed a number in chat*.

### `aeo-bot-access-audit` — can the bots actually read you?

Practitioners most often miss this, and everything else in the repo is downstream of whether the retrieval bot got bytes back. Seven steps, all of them `curl`:

- Read `robots.txt` as a spec, not a vibe.
- Classify every `User-agent:` token by purpose — **training vs retrieval vs user-requested**. Blocking `GPTBot` does not block ChatGPT Search (`OAI-SearchBot` does). Most sites get this backwards.
- Run the four documented `robots.txt` traps, including render-critical paths blocked under `/assets/` or `/wp-content/`, which look like a block and behave like a partial success.
- **Verify at the edge, per bot, with the exact published UA string.** A 200 from your IP with a spoofed UA tells you the edge does not block that string. It does not prove what the real bot receives — the real bot arrives from a different network, may carry a different version, and may be filtered by IP reputation. For Anthropic there is no published UA string at all; verify identity against the published IP list.
- Confirm sitemap discovery via the `Sitemap:` directive.
- Read preview control (`nosnippet`), which is a different decision with opposite economics.

**Training-vs-retrieval policy scores zero points on purpose.** There is no professional consensus, at least one widely-copied 2026 crawler table is simply wrong about it, and it is your decision, not a finding.

### `aeo-citability-audit` — scored for a second consumption mode

20 deterministic checks, 5 points each, across three groups:

| Group | Checks | Points | What it measures |
|---|---|---|---|
| Extractability | X-01…X-08 | 40 | Answer position, server-rendered vs JS-injected, heading hierarchy, semantic markup, self-contained blocks, list/table presence, `<html lang>` |
| Citation-worthiness | W-01…W-07 | 35 | Sourced-fact density, coverage of facts cited pages agree on, attributed quotations, external citations, comparison tables, quotable definitions, visible price + visible date |
| Entity & page integrity | E-01…E-05 | 25 | Naming consistency, topic cluster, trust surface, preview control, machine-readable freshness |

**Multilingual, and honest about it.** Word counting is character-based per language (`chars/token` table for 11 language families), position checks are character-based rather than word-based, and the lexical stages of X-05, W-03 and W-06 ship lexicons for **en, nl, es, pt, it, fr, de**. In any other language those three return **N/A**, never a failing score. The market's leading citability scorer is English-only by regex — a bug documented in its own issue tracker — and the report always lists N/A checks by ID. A report that says 95/100 with two silent N/As is worse than one that says 90/95.

The audit prints this line whenever it scores above 70 with no N/A: *"nothing is wrong on-page."* Not "you will be cited." Shepard's top-ranked factor is URL accessibility at 9.5; search rank is second at 9.4, and this audit cannot measure it without paid data.

### `information-gain-analysis` — why you get cited or cut

Google's patent **US11354342B2** describes an assistant answering from source 1 for facts A+B, then source 2 for fact C *only*, deleting the overlap. Ahrefs' reading of that is the sentence this repo is built around:

> *"In a ranked list, even if you're the fourth site saying the same thing, you're still on the SERP… But in a synthesized answer there **is** no position four. Either you provide the information that hasn't been said yet, or your content gets cut."*

The skill builds a fact ledger from the pages currently ranking, subtracts it from yours, and returns a ranked **worklist** of facts nobody else has — each with a concrete route to obtaining it. An unproducible fact is a wish, not a finding.

Two rules govern the scoring:

1. **Rank position contributes zero points.** On-Page.ai's study of 150 top-3 pages found position *unrelated* to the score within the top 3, while pages with 15+ unique data points averaged 62.1 against 40.2 for pages with 0–1. Scoring rank here would launder a known-good signal into a label called information gain. (Vendor research: On-Page.ai sells a scoring product and this Information Gain Score is its own metric.)
2. **The counting is deterministic; the meaning judgement is not.** "Is this number informative or padding?" is a judgement about meaning. The skill reports it as a judgement, never as a measurement, and ships a mandatory disclosure block.

---

## Install

```bash
# Auto-detect installed agents
npx skills add Pautthead/seo-aeo-agent-skills

# Explicit host list. Name Claude Code explicitly: running the installer from
# inside an agent session may write only to .agents/skills/, which Claude Code
# does not read.
npx skills add Pautthead/seo-aeo-agent-skills -a claude-code -a opencode -a codex -a grok
```

Claude Code plugin marketplace:

```
/plugin marketplace add Pautthead/seo-aeo-agent-skills
/plugin install seo-aeo@seo-aeo-agent-skills
```

Or copy `skills/<name>/` into your host's directory by hand:

| Host | `--agent` | Project path | Global path |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| **Grok Build (xAI)** | `grok` | `.grok/skills/` | `~/.grok/skills/` |
| Hermes Agent | `hermes-agent` | `.hermes/skills/` | `~/.hermes/skills/` |
| OpenClaw | `openclaw` | `skills/` | `~/.openclaw/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` |
| OpenHands | `openhands` | `.openhands/skills/` | `~/.openhands/skills/` |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` |
| Crush | `crush` | `.crush/skills/` | `~/.config/crush/skills/` |
| Amp | `amp` | `.agents/skills/` | `~/.config/agents/skills/` |
| Warp | `warp` | `.agents/skills/` | `~/.agents/skills/` |
| Kiro CLI | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` |

`.agents/skills/` is the de-facto portable project location — Codex, Cursor, Cline, Amp, Warp and OpenCode all read it natively, so no symlinks are needed. OpenCode additionally reads `.opencode/skills/`, `.claude/skills/` and `.agents/skills/`, walking up from CWD to the worktree root. Grok Build reads `.grok/skills/` and *also* scans `.agents/skills/` at each tier, and honours `GROK_HOME`.

That is a subset of the ~80 agents the `skills` CLI supports. Any host that can read `SKILL.md` can use these.

---

## What these skills refuse to do

Check this section if you are here to evaluate us. Roughly 80% of GEO is ordinary SEO. A service that will not say so is selling a separate discipline the evidence does not support ([Jeremy Moser, via Digiday, 2026-03-10](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/)).

### `llms.txt` does not get you cited in AI answers

Six 2026 studies. None finds a relationship between publishing `llms.txt` and more citations or more crawling. Two are independent measurements (Ahrefs, Arsentev), three are vendor research (SE Ranking, Otterly.AI, CueScout) and one is editorial (Search Engine Land). Three of the six measure fetches of the file rather than citations.

| Study | Date | N | Result | Type |
|---|---|---|---|---|
| [Ahrefs](https://ahrefs.com/blog/llmstxt-study/) | 2026-06-15 | 137,210 domains | 28% publish one; **97% received zero requests**; *"Zero AI bots go looking for llms.txt files that don't exist"* | measured |
| [SE Ranking](https://seranking.com/blog/llms-txt/) | 2026-10-15 | ~300,000 domains | 10.13% adoption; their model got **more** accurate when the variable was removed — *"LLMs.txt might currently introduce more noise than value"* | vendor research |
| [Otterly.AI](https://otterly.ai/blog/the-llms-txt-experiment/) | 2026-02-05 | 62,100 AI bot visits / 90d | 84 requests hit `/llms.txt` (~0.1%); no positive correlation with AI crawl activity | vendor research |
| [Search Engine Land](https://searchengineland.com/does-llms-txt-matter-467740) | 2026-01-20 | 10 sites, before/after | 8 no change; sites that shipped **new functional content** grew, sites that merely documented existing content grew nothing. **One site fell 19.7%**, and their own 2+8+1 does not reconcile with the stated n=10 | editorial |
| [CueScout](https://cuescout.com/blog/does-llms-txt-work) | 2026-10-15 | 537 SaaS sites, 80 AI Mode answers | 24.3% cited *with* vs 21.8% *without* (p=0.53); **none of the 708 cited links pointed at an llms.txt file** | vendor research |
| [Arsentev, origin log](https://doi.org/10.5281/zenodo.23018429) | 2026-09-28 | 345,808 requests / 15 days | **Zero** crawler-token requests to `/llms.txt`; robots.txt got 698, sitemap.xml got 282 | measured |

**The nuance.** "Doesn't work" overclaims. Of the files that are fetched, most of the traffic is not an AI tool: Ahrefs puts AI agents at 10.5% of requests and fifth overall. Named AI bots reach 19.5% only when the four AI categories are added together. Mueller's "temporary crutch" line, which Ahrefs extends to this file, was about Google's markdown developer docs. CueScout's null result is the short version: nothing that gets cited points at the file. For ChatGPT, Perplexity or AI Overviews, Ahrefs calls the file "largely decoration." Budget zero against traffic.

Google's own documentation, in a section headed *"Mythbusting generative AI search: what you don't need to do"*, under the bullet **"LLMS.txt files and other 'special' markup"**:

> *"You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities), as Google Search itself doesn't use them."*
>
> *"It's completely fine if you decide to create and maintain LLMS.txt files (or other similar files) for other services or systems that use these files. Doing so will neither harm nor help your site's visibility or rankings in Google Search, as Google Search ignores them."*
> — [Google Search Central, "Optimizing your website for generative AI features on Google Search"](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

Ahrefs' own caveats travel with the number: 28% adoption is an **upper bound** (their customers skew technical), and *"every figure in this study is therefore a ceiling on actual llms.txt consumption."*

**What we recommend instead.** Markdown mirrors. With an index plus `.md` mirrors present, agent ingestion cost fell to ~123K tokens / ~10 tool calls versus ~240K / ~20 without them ([a14y](https://a14y.dev/research/llms-txt-linking/) - a vendor study of its own tooling; n=5 per arm, one site, so directional). Answer quality tied. *"The cost is ingestion, not generation."* And note what did **not** work there: three link formats were tested — `<link rel="llms-txt">`, `<link rel="alternate" type="text/markdown">`, a visible "For agents" footer link — and **all three scored 0/5 adoption**. The only arm that moved was one line in the prompt.

### FAQPage schema is not a GEO lever

Shepard scores structured data at 5.6 and is careful in both directions: LLMs *"don't typically ingest schema as part of their training"* and there's *"limited evidence they can at least see schema when searching"* — but *"practically every study that looks at schema and AI citations finds a positive relationship. The effect is typically small, but it's amazingly consistent across studies."*

We quote both halves because quoting only the negative one misrepresents the source. The conclusion is unchanged: schema is worth doing for rich results and entity clarity, not as a GEO tactic. Google also stopped showing FAQ rich results for most sites a while back, while several 2026 skills still auto-recommend adding FAQPage.

### No automated forum or Reddit posting

Reddit removed all four subreddit communities **OtterlyAI** had built for its own 60-day GEO engagement experiment, for a breach of Rule 2 of Reddit's Content Policy ([OtterlyAI, 2026-10-01](https://otterly.ai/blog/reddit-geo-2026/)) — a vendor's self-report of its own failed experiment, and the reason the industry automated Reddit in the first place. **Measure Reddit. Never post to it.**

### No AI-visibility promises inside 60 days

No reliable public source gives a citation-lift window. A "60–120 days" figure circulates widely; it could not be traced to a primary source and has been removed from this repo rather than softened. What does hold: on-page changes move in weeks, third-party citation changes move far more slowly. If someone quotes you a precise window, ask them for the study.

### No claim that GEO is a separate discipline

> *"80 percent of GEO is good, fundamental SEO. If a GEO service does not openly tell you that success in AI visibility is 80 percent good fundamental SEO, they are selling you snake oil."*
> — Jeremy Moser (uSERP), via Digiday, 2026-03-10

### And the rule that outranks all of the above

**Do not produce a finding the technique cannot actually detect.** If a check is N/A — unsupported language, missing field, unreachable source — report it as *not scored*. Never as a pass, never as a failure.

One asymmetry worth knowing: summarising fetchers (`web_fetch` and similar) **strip `<script>` tags**, so a page fetched that way genuinely cannot be checked for JSON-LD. But **`curl` returns raw bytes**, so there you must grep the body for `"@type"` and report what's really there. Don't turn a solvable check into a permanent N/A.

---

## Optional paid data — DataForSEO

Nothing in this repo requires any of this. All four skills complete with zero credentials. This section exists because one gap — SERP rank data, for the two highest-ranked factors — has no free equivalent, and because the pricing here has a trap worth knowing about.

This link is a referral link: we may earn a commission if you sign up. DataForSEO is listed because it is the cheapest bulk SERP/keyword data we found, not because it is required. It is not an endorsement of their data quality — the freshness caveat below is real and it is theirs.

Prices checked 2026-10-19 against [dataforseo.com/pricing](https://dataforseo.com/pricing). Vendor pricing changes without notice; verify before you budget.

| Endpoint | Price | Notes |
|---|---|---|
| `dataforseo_labs/google/*/live` | **$0.012/task + $0.00012/item** | Default. Live-only, no queue. Max 700 keywords/task, 1,000 items/response, 2,000 calls/min, 30 concurrent |
| `historical_rank_overview/live` | $0.12/task + $0.0012/item | Unlocks search rank and fan-out rank in the citability audit |
| `historical_serps/live` | $0.00012/SERP | |
| `search_intent/live` | $0.012/task + $0.00012/keyword | |
| SERP API (headline) | **$2.00 / 1k live** · $1.20 / 1k priority · $0.60 / 1k standard | See the trap |

> **Pricing trap.** The headline **$0.60/1k** rate is the *standard* queue, which takes about **5 minutes**. For an interactive agent that is not an equivalent product, so **$2.00/1k live is the honest comparison**. We quote $2.00 everywhere.

**Database refresh is 30–90 days.** Never present Labs output as real-time.

**Official MCP server — the server is free, you pay API rates:**

- Remote: `https://mcp.dataforseo.com/v3/mcp` with `Authorization: Basic base64(login:password)`
- Local: `npx -y dataforseo-mcp-server` with `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`
- Source: [github.com/dataforseo/mcp-server-typescript](https://github.com/dataforseo/mcp-server-typescript)

**Auth gotcha:** HTTP Basic only, and credentials come from the **API** login at `app.dataforseo.com/api-access`. Using the dashboard login is the single most common auth failure.

**Getting started:** $1 trial credit, $50 minimum top-up. → [fluyeporlaweb.com/go/dataforseo](https://fluyeporlaweb.com/go/dataforseo/) (affiliate link).

---

## How the scoring works

Four rules, applied to every skill:

1. **Deterministic analysis, LLM rewriting.** Scorers, checklists and parsers are reproducible rules the agent applies, not judgements it improvises. Hallucination risk belongs in the layer that produces prose, not the layer that produces numbers.
2. **Every numeric threshold is labelled by kind.** It is either a measurement with a traceable source, or explicitly a judgement call. Cyrus Shepard's 9.5 for URL accessibility is a **hand-assigned correlation score, not a measurement** — his own words: *"I assigned each score by hand against those criteria, using AI to help adjust the final numbers... These are not confirmed ranking factors. Correlation is not causation."* We use them for ordering, never as effect sizes. The `chars/token` table in the citability skill is labelled a judgement call.
3. **Source types are labelled.** `measured` (Ahrefs, arXiv, Zenodo) · `vendor research` (SE Ranking, CueScout, OtterlyAI, Muck Rack, On-Page.ai, Indig/Omnia) · `editorial` (Search Engine Land) · `vendor docs` (OpenAI, Perplexity, Google). A vendor marketing number is never laundered into a fact.
4. **Document your own limits, and mean it.** Every skill carries a `Known limitations` section that is copied into the report verbatim.

### What this rule has already cost us

Review found a **fabricated quote** attributed to Danny Sullivan — *"There is no benefit to creating a llms.txt file for SEO."* It is not in any source. It reached us through a research pass and sat in the README until someone went looking for it. It is gone, replaced with Google's own first-party documentation, which is a stronger citation than the secondhand quote we were trying to use.

Also removed: a statistic attached to a named community report on a specific date with nothing behind it; a wrong number (2,135 robots.txt requests) attached to a real study; a metric mislabelled (98% accuracy for what is 97.0 macro-F1); two URLs that silently resolved to blog index pages; a source that could not be found at all; and User-Agent version numbers that were wrong in copy-pasteable commands.

Every one is recorded in [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md) and [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md) §1.9c so the next contributor does not reintroduce them.

---

## Roadmap

Sourced gaps, from [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md) §5. **None are in v1.**

| Planned | Why it is a real gap |
|---|---|
| **JSON-LD schema validator** against rich results | Many skills generate structured data. Almost none validate it. |
| **Internal link graph mapper** | *"Plenty of skills mention it, none actually map a link graph."* Directly relevant to the ~150-suggestions-20-usable failure. |
| **Keyword gap analysis** | Competitive coverage currently requires a paid export. |
| **SERP intent / page-type match** | Top-6 factor in Shepard's ordering. The citability audit approximates it; nothing scores it properly. |
| **Content decay triage** | Distinguishes traffic decay from position decay from staleness. Requires GSC. |
| **GEO experiment tracker** | One variable, 7–21 days, three engines. Nothing in the market resists changing five things at once. |
| **SEO drift as a GitHub Action pre-merge gate** | The stale-data failure caught before merge rather than after a quarterly review. |
| **Framework-specific SEO** for Next.js, Astro, Nuxt | Render output and metadata differ enough that generic advice is wrong. |
| **Multi-site / agency support** | Compare a portfolio against its own baseline instead of each site in isolation. |

---

## Where this fits

Fair context, not a competitive attack. Several of these are good, and some are broader than this repo. Star counts as of 2026-10-19.

| Repo | ★ | What it does well |
|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 55k | Breadth across marketing; its own self-documented limitations are the practice borrowed here |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 35k | The `npx skills` installer this repo ships through. Infrastructure, not SEO |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 19k | Comprehensive Claude Code SEO surface area |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | 11k | The closest thing to a dedicated GEO skill set |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | 7.5k | Broad technical SEO coverage |
| [Ryze-AI-Adgent/open-seo-mcp-skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills) | 6k | Live data through MCP out of the box |
| [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | 4k | Opinionated, decisive audits |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | 175 | Clean, well-scoped individual skills with real example runs |
| [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | 360 | Strictly keyless, named methodology, anti-slop ruleset |

Three patterns across the field: most are **Claude Code only**, most need a **paid subscription** for live data, and few document their own limits. Where they are stronger — breadth, live SERP data, framework coverage — the roadmap above is the answer.

---

## Contributing

Read [`AGENTS.md`](AGENTS.md) first; it is loaded by Codex, OpenCode, Cline, Gemini CLI, Cursor, OpenClaw and Hermes. Then read [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md), the internal source of truth for skill anatomy, portability invariants and the list of things this repo must never do.

**Adding a skill:**

1. `skills/<name>/SKILL.md` plus `references/`. Nothing nested deeper.
2. Frontmatter carries **only** `name`, `description`, `license`, `compatibility` and `metadata` (exactly four string keys: `repo`, `version`, `updated`, `keys-required`). `name` must equal the directory name, lowercase kebab-case.
3. `description` front-loads what it does, when to use it, and its trigger keywords — Codex budgets the whole skill list at 8,000 characters and truncates descriptions first.
4. Body order: purpose · when to use / when not to use · inputs (keyless path first) · procedure with a runnable check and a falsifiable pass per step · output format · scoring · known limitations · optional data sources · references.
5. Links to siblings are `references/FILE.md`, one level, always — and must resolve.
6. No `context: fork`, no hooks in the core. Both are Claude Code only and would break portability.
7. **Zero required API keys.** If it cannot complete without a paid account, it is not ready.

**Validation gates — run before you open a PR:**

```bash
python tests/validate_skill_inventory.py --strict
python tests/reference_freshness.py --review-after-days 90 --stale-after-days 365
```

Both run in CI on every push. The first checks spec conformance and that every internal link resolves; it refuses to report PASS when it checks nothing. The second uses **two thresholds deliberately**: 90 days flags a *review trigger* — the finding may have been superseded even though the source has not expired — and 365 days fails. A single threshold would flag every primary research paper older than three months as broken, which is noise, and noise is how gates get ignored.

**The citation rule.** Every numeric threshold must trace to a dated source with a stated level of evidence. **Open the source and confirm it says what you claim.** Reading the primary text is the minimum. If you cannot verify it, do not cite it — a claim that cannot be verified gets removed, not softened.

---

## License

Apache-2.0. Use it, fork it, vendor it into your own audit tooling.

## Credits and sources

Built by [Pautthead](https://github.com/Pautthead). Full verification table with dates, sample sizes and verdicts in [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md).

**Measured**

- [Ahrefs — We Analyzed 137K Sites](https://ahrefs.com/blog/llmstxt-study/) — Louise Linehan, 2026-06-15, n=137,210 domains
- [Ahrefs — What Is Information Gain in SEO](https://ahrefs.com/blog/information-gain/) — Louise Linehan, 2026-08-20
- [arXiv 2605.25517](https://arxiv.org/abs/2605.25517) — *What Gets Cited: Competitive GEO in AI Answer Engines*, 2026-05-25, 252,000 trials across 6 LLMs
- [arXiv 2609.15369](https://arxiv.org/abs/2609.15369) — *SlopShape*, Jochen Madler (Sitefire), 2026-09. 97.0 macro-F1 on held-out companies from 176 structural features; macro-F1 is not an accuracy percentage
- [Zenodo 10.5281/zenodo.23018429](https://doi.org/10.5281/zenodo.23018429) — Arsentev, 2026-09-28, origin-log study. Author's stated limits: one origin, three pooled hostnames, origin-only logging behind a CDN, self-asserted identity
- [Google — Patent US11354342B2](https://patents.google.com/patent/US11354342B2/en) — "Contextual estimation of link information gain", Google LLC. The "no position four" phrasing is Ahrefs' interpretation, not the patent's text
- [Zenodo 10.5281/zenodo.23128812](https://doi.org/10.5281/zenodo.23128812) — Hall, crawler behaviour with robots.txt `Sitemap:` announcement. Author discloses a competing interest: he owns the plugin he measured

**Vendor research**

- [Cyrus Shepard / Zyppy](https://signal.zyppy.com/p/ai-citation-ranking-factors) — 2026-05-07, 54 experiments. Hand-assigned correlation scores, not measurements
- [SE Ranking](https://seranking.com/blog/llms-txt/) · [CueScout](https://cuescout.com/blog/does-llms-txt-work) (both 2026-10-15) · [Otterly.AI](https://otterly.ai/blog/the-llms-txt-experiment/) (2026-02-05)
- [On-Page.ai — Information Gain study](https://api.on-page.ai/research/information-gain-study) — Eric Lancheres, 2026-06-12, 150 pages. Their own metric, and they sell it
- Kevin Indig, [The Consensus Gap](https://www.growth-memo.com/p/the-consensus-gap), 2026-05-11 — 91% of citations appeared in a single engine (URL-level, across ChatGPT / Perplexity / AI Overviews). Data is Omnia, Indig's own product, and he states the sample skews to its customer base
- Muck Rack (25M+ cited links) — the 84% earned-media figure includes Wikipedia and PubMed Central; journalism alone is ~27%, and sample size is stated inconsistently across their own pages. Directional only

**Editorial**

- [Search Engine Land](https://searchengineland.com/does-llms-txt-matter-467740) — 2026-01-20. Note their own arithmetic does not reconcile (2 up + 8 flat + 1 down = 11 for a stated sample of 10)
- [a14y.dev](https://a14y.dev/research/llms-txt-linking/) — Claude 2.1.141, isolated Docker, n=5 per arm, single site
- Jeremy Moser via [Digiday](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/), 2026-03-10 · Lily Ray, [*The AI Slop Loop*](https://lilyraynyc.substack.com/p/the-ai-slop-loop), 2026-04-14 · John Mueller via [SERoundtable](https://www.seroundtable.com/google-adds-markdown-files-to-help-docs-41342.html), 2026-05-19

**Vendor docs**

- [Google Search Central — AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [OpenAI — crawler documentation](https://platform.openai.com/docs/bots) · [Perplexity — bots](https://docs.perplexity.ai/guides/bots)

**Community reports** (anecdotal, a failure mode, not evidence): [r/AiAutomations, 2026-09-07](https://www.reddit.com/r/AiAutomations/comments/1w9h1sv/an_seo_agent_kept_working_for_two_weeks_after_its/) · [r/SEO_Xpert, 2026-07-10](https://www.reddit.com/r/SEO_Xpert/comments/1ush4r6/my_experience_with_using_ai_claude_codecodex_for/) · [r/SideProject, 2026-09-24](https://www.reddit.com/r/SideProject/comments/1wp4s2r/do_unique_stuff_a_real_mcp_data_server/) · [r/SEO, 2026-01-26](https://www.reddit.com/r/SEO/comments/1qngfmm/is_programmatic_seo_still_a_good_move_in_2026/) · [r/AskMarketing, 2026-09-29](https://www.reddit.com/r/AskMarketing/comments/1wt41hp/guys_have_you_used_any_ai_seo_tools_for_aeogeo/).

**Distribution:** the `skills` CLI by Vercel Labs, verified against the [Agent Skills specification](https://agentskills.io/specification) rather than blog posts — several 2026 install guides publish paths that do not exist.

---

*If a claim in this repo cannot be traced to a dated source, that is a bug. Please open an issue.*