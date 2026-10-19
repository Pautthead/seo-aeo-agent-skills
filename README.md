# SEO + AEO + GEO Skills for AI Agents — four verifiable agent skills

Evidence-backed AI SEO agent skills for Claude Code, Codex, Cursor, OpenCode, **Grok Build**, Gemini CLI, Cline, Hermes and ~75 other hosts. Every scoring rule traces to a dated source. **No API keys, no MCP servers, no subscription.**

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Install](https://img.shields.io/badge/install-npx%20skills-8a2be2.svg)](https://www.npmjs.com/package/skills)
[![API keys](https://img.shields.io/badge/API%20keys-none%20required-brightgreen.svg)](skills/)
[![Skills](https://img.shields.io/badge/skills-4-orange.svg)](skills/)

---

## What this is

Four Agent Skills that run real, deterministic SEO and AEO checks inside an AI coding agent — and tell you, in writing, what they cannot detect.

| Skill | The question it answers | Needs keys? |
|---|---|---|
| [`seo-data-contract`](skills/seo-data-contract/SKILL.md) | Is this data fresh enough and trustworthy enough to act on? | No |
| [`aeo-bot-access-audit`](skills/aeo-bot-access-audit/SKILL.md) | Can AI bots actually fetch this site? | No (just `curl`) |
| [`aeo-citability-audit`](skills/aeo-citability-audit/SKILL.md) | Would this page survive being extracted and cited? | No |
| [`information-gain-analysis`](skills/information-gain-analysis/SKILL.md) | What does this page know that the SERP does not? | No |

## What this is not

- Not a prompt library. Every check has a runnable test and a falsifiable pass condition.
- Not a GEO product. Roughly **80% of GEO is good, fundamental SEO** — if a GEO service doesn't tell you that openly, they are selling you snake oil ([Jeremy Moser, via Digiday, 2026-03-10](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/)).
- Not a subscription. If you cannot run it with zero credentials, it isn't in this repo.
- Not a place where 2026 folklore gets quietly reimplemented. See [What these skills refuse to do](#what-these-skills-refuse-to-do) — that section is the pitch.

---

## The problem

Three failure modes, all of them structural rather than clever.

**1. Silent stale data.** The most-cited structural complaint in agentic SEO. From `r/AiAutomations`, 2026-09-07:

> *"At analook dot com, a GSC OAuth token expired and the agent continued using cached Search Console data for two weeks. Rankings were changing while its decisions were still based on the old view. That is an awkward failure to catch with a simple 'did the workflow run?' check. The workflow can run successfully against an input that should no longer be trusted."*

The workflow exits 0. The report looks fine. Every number in it is a fact about the past phrased in the present tense. `seo-data-contract` exists to make that failure impossible to ship.

**2. Confident, unreproducible output.** From `r/SEO_Xpert`, 2026-07-19: an agent proposed **~150 internal links with total confidence; ~20 were usable.** The same page, opened in a **fresh session**, produced different recommendations. The agent could not reproduce its own prior analysis. Nothing in the output told you which items came from data and which came from the model's priors.

**3. Techniques that were never working.** This is the big one for 2026. `llms.txt` has been sold, blogged and shipped as an AI-visibility lever all year. Six independent 2026 measurements say it does nothing. [The evidence table is below](#what-these-skills-refuse-to-do). So are several other 2026 favourites.

---

## The four skills

### `seo-data-contract` — freshness and provenance before analysis

Every SEO number an agent uses is a claim about the past. This skill forces a dated, sourced envelope onto that number before a word of analysis is written, and refuses the analysis outright when the input can no longer be trusted.

It asks **three separate questions**, and all three have to pass:

1. **Can it authenticate right now?** A cached response is not an auth check.
2. **When did a retrieval last succeed?** Not the vendor's last update. The agent's own last successful pull.
3. **What is the newest date represented *inside* the data?** Not the fetch time. A query run at 14:03 today can return rows whose last complete day is three weeks ago.

Then one deterministic classification — `fresh · aging · stale · expired · unknown · observed` — computed as a subtraction against the source's expected latency. `stale` or `expired` means the agent does not analyse; it emits a freshness block and offers three paths: refresh now, proceed on explicitly labelled stale input, or do the part that needs no stale input at all.

Runs fully offline. Handles the dominant real-world path explicitly: *the user just typed a number in chat*.

### `aeo-bot-access-audit` — can the bots actually read you?

Shepard scores **URL accessibility 9.5/10 — the highest of 23 measured AI citation factors** ([Zyppy, 2026-05-07](https://signal.zyppy.com/p/ai-citation-ranking-factors)). Everything else in this repo is downstream of whether the retrieval bot got bytes back.

Seven steps, all of them `curl`:

- Read `robots.txt` as a spec, not a vibe.
- Classify every `User-agent:` token by purpose — **training vs retrieval vs user-requested**. Blocking `GPTBot` does not block ChatGPT Search (`OAI-SearchBot` does). Allowing `GPTBot` buys you nothing for citations. Most sites get this backwards.
- Run the four documented `robots.txt` traps, including render-critical paths blocked under `/assets/`, `/wp-content/`, `/css/`, `/js/` — which look like a block and behave like a partial success.
- **Verify at the edge, per bot, with the exact UA string.** This is the step everyone skips. Cloudflare, Akamai, Fastly and AWS WAF enforce *before* your origin ever parses a robots file. A perfectly clean `robots.txt` behind a challenge rule means a site no AI bot can read — and a clean robots.txt proves nothing on its own.
- Confirm sitemap discovery.
- Read preview control (`nosnippet`), which is a different decision with opposite economics: blocking `OAI-SearchBot` removes you from that engine; `nosnippet` only limits quotation.

**Training-vs-retrieval policy scores zero points on purpose.** There is no professional consensus, at least one widely-copied 2026 crawler table is simply wrong about it, and it is your decision, not a finding.

### `aeo-citability-audit` — scored for a second consumption mode

Ranking is not the only job a page has. The other one is being *extracted, quoted and attributed* inside a synthesized answer. 20 deterministic checks, 5 points each, across three groups:

| Group | Checks | Points | What it measures |
|---|---|---|---|
| Extractability | X-01…X-08 | 40 | Answer position, server-rendered vs JS-injected, heading hierarchy, semantic markup, self-contained blocks, list/table presence, `<html lang>` |
| Citation-worthiness | W-01…W-07 | 35 | Sourced-fact density, coverage of facts cited pages agree on, attributed quotations, external citations, comparison tables, quotable definitions, visible price + visible date |
| Entity & page integrity | E-01…E-05 | 25 | Naming consistency, topic cluster, trust surface, preview control, machine-readable freshness |

**Multilingual, and honest about it.** Word counting is character-based per language (`chars/token` table for 11 language families), position checks are character-based rather than word-based, and the lexical stages of X-05, W-03 and W-06 ship lexicons for **en, nl, es, pt, it, fr, de**. In any other language those three return **N/A**, never a failing score. The market's leading citability scorer is English-only by regex — a bug documented in its own issue tracker — and the report always lists N/A checks by ID. A report that says 95/100 with two silent N/As is worse than one that says 90/95.

The headline line the audit prints when it scores above 70 with no N/A: *"nothing is wrong on-page."* Not "you will be cited." Shepard's #2 factor is **search rank at 9.4/10** and this audit cannot measure it keylessly.

### `information-gain-analysis` — why you get cited or cut

Google's patent **US11354342B2** describes an assistant answering from source 1 for facts A+B, then source 2 for fact C *only*, deleting the overlap. Ahrefs' consequence is the sentence this repo is built around:

> *"In a ranked list, even if you're the fourth site saying the same thing, you're still on the SERP… But in a synthesized answer there **is** no position four. Either you provide the information that hasn't been said yet, or your content gets cut."*

The skill builds a fact ledger from the pages currently ranking, subtracts it from your page, and returns a ranked **worklist** of facts nobody else has — each with a concrete route to obtaining it. An unproducible fact is a wish, not a finding.

Two rules govern the scoring, and they are the reason this skill is trustworthy:

1. **Rank position contributes zero points.** On-Page.ai's study of 150 top-3 pages found position and originality barely separated positions 1–3, while pages with ≥15 unique data points averaged 62 against 40 for pages with 0–1. Scoring rank here would launder a known-good signal into a label called "information gain."
2. **The counting is deterministic; the meaning judgement is not.** "Is this number informative or padding?" is a judgement about meaning. The skill reports it as a judgement, never as a measurement, and ships a mandatory disclosure block that must be reproduced unedited.

---

## Install

Works with the `skills` CLI (Vercel Labs) across ~75 agent hosts.

```bash
# Auto-detect installed agents
npx skills add Pautthead/seo-aeo-agent-skills

# Explicit host list (recommended: Claude Code needs to be named explicitly,
# otherwise the installer may write only to .agents/skills/, which Claude Code
# does not read)
npx skills add Pautthead/seo-aeo-agent-skills -a claude-code -a opencode -a codex -a hermes-agent
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

`.agents/skills/` is the de-facto portable project location — Codex, Cursor, Cline, Amp, Warp and OpenCode all read it natively, so no symlinks are needed. OpenCode additionally reads `.opencode/skills/`, `.claude/skills/` and `.agents/skills/`, walking up from CWD to the worktree root. Grok Build reads `.grok/skills/` and *also* scans `.agents/skills/` at each tier between CWD and the repo root, and honours `GROK_HOME`.

That is a subset of the ~80 agents the `skills` CLI supports. Any host that can read `SKILL.md` can use these; the paths above are the ones with first-class registry entries.

After install, ask the agent by name or by description — the `description` frontmatter carries the trigger keywords so it can self-select. `AGENTS.md` is the entry point most hosts load automatically.

---

## What these skills refuse to do

This is the section to check if you are here to evaluate us.

### `llms.txt` is not a traffic or citation lever

Six independent 2026 measurements. Every one is negative or null.

| Study | Date | N | Result |
|---|---|---|---|
| [Ahrefs](https://ahrefs.com/blog/llmstxt-study/) | 2026-06-15 | 137,210 domains | 28% have one; **97% received zero requests**; **zero AI-bot requests for files that don't exist — they never go looking** |
| [SE Ranking](https://seranking.com/blog/llms-txt/) | 2026-10-15 | ~300,000 domains | 10.13% adoption; their model got **more** accurate when the variable was removed — *"LLMs.txt might currently introduce more noise than value"* |
| [Otterly.AI](https://otterly.ai/blog/llms-txt/) | 2026-02-05 | 62,100 AI bot visits / 90d | 0.1% hit `/llms.txt`; no positive correlation with AI crawl activity |
| [Search Engine Land](https://searchengineland.com/llms-txt/) | 2026-01-20 | 10 sites, before/after | 8 no change; sites that shipped **new functional content** gained, sites that merely documented existing content gained nothing |
| CueScout | 2026-10-15 | 537 SaaS sites, 80 AI Mode answers | 24.3% cited *with* vs 21.8% *without* (p=0.53, not significant); **none of the 708 cited links pointed at an llms.txt file** |
| Origin server log | 15 days | 345,808 requests | **Zero** requests to `/llms.txt` from any of 22 crawler tokens; robots.txt got 2,135, sitemap.xml got 282 |

Google, on the record — Danny Sullivan, [Search Central Live Toronto, 2026-04](https://developers.google.com/search/blog): *"There is no benefit to creating a llms.txt file for SEO."* Shepard scores it **2.0/10 — the lowest of 23 factors**.

**The one nuance worth shipping, stated as discovery rather than adoption:** crawlers *do* fetch an llms.txt that is announced in `robots.txt` via `Sitemap:` ([Nathan Hall, Zenodo, 2026-09-17](https://doi.org/10.5281/zenodo.22814843)) — 1,549 fetches across 165 site-days, versus zero requests for ten un-referenced sibling files across 60 file-months. The author's own caveat is the correct reading: *"Tell a crawler where a file is and it fetches the file. That is discovery, not adoption."* A fetch is not a citation.

**What we do instead:** ship markdown mirrors. With an llms.txt index plus `.md` mirrors present, agent ingestion cost fell to ~123K tokens / ~10 tool calls versus ~240K tokens / ~20 without them ([a14y research, 2026](https://a14y.dev/research/llms-txt-linking/)). Answer quality tied. *"The cost is ingestion, not generation."* And note what did **not** work there: five link formats were tested and **all five scored 0/5 adoption**. The only thing that moved was one line in the prompt. Budget zero forecast against `llms.txt`; if you ship one, ship it in an hour and announce it.

### FAQPage schema is not a GEO tactic

Shepard scores structured data 5.6/10 and notes *"LLMs don't typically ingest schema as part of their training"* with *"limited evidence they can at least see schema when searching."* Google stopped showing FAQ rich results for most sites a while back (`r/AskMarketing`, 2026-09-29). Several 2026 skills still auto-recommend adding FAQPage. Schema is worth doing for rich results and entity clarity — not for GEO.

### No automated posting to Reddit or any forum

Reddit began labelling legitimate bot accounts (2026-03), reported catching **25,000 spammy posts/day** (2026-07) explicitly to stop *"brands from planting posts meant to get them recommended by ChatGPT and Gemini"*, and **banned 4 subreddits** used in a GEO experiment that automated upvotes and comments. **Measure Reddit. Never post to it.**

### No AI-visibility promises inside 60 days

On-page changes move in weeks. Citation changes take 4–12 weeks; the field test we found puts the first citation lift at **60–120 days** (ProCloser, 2026-05-27, n=5 — the author flags the sample as underpowered). Every report in this repo carries that horizon in the output. If someone promises 60 days, they are selling a timeline, not a method.

### No claim that GEO is a separate discipline

**80 percent of GEO is good, fundamental SEO.** If a GEO service does not openly tell you that success in AI visibility is 80 percent good fundamental SEO, they are selling you snake oil. — Jeremy Moser (uSERP), via Digiday, 2026-03-10

Lily Ray documents the corollary: a brand with established authority appears in ChatGPT and concludes its GEO campaign is working, when the more plausible explanation is that its existing SEO visibility got it into the indexes feeding those products. She also found a vendor case study where organic traffic **fell 66%** while "AI visibility" rose.

### And the thing that matters more than all of the above

**Do not produce a finding the technique cannot actually detect.** If a check is N/A — unsupported language, missing field, unreachable source — report it as *not scored*. Never as a pass, never as a failure. A false pass is what destroys trust in an audit. If you couldn't fetch a page, say so. Note the asymmetry on structured data: summarising fetchers (`web_fetch` and similar) **strip `<script>` tags**, so a page fetched that way genuinely cannot be checked for JSON-LD — but **`curl` returns raw bytes**, so there you must grep the body for `"@type"` and report what's really there. Don't turn a solvable check into a permanent N/A.

---

## Optional paid data — DataForSEO

**Nothing in this repo requires any of this.** All four skills complete with zero credentials. This section exists because one gap — SERP rank data for the two highest-scoring factors — has no free equivalent, and because pricing here has a trap worth knowing about.

DataForSEO is a paid vendor we use and may earn a referral commission from. It is listed here because it is the cheapest bulk SERP/keyword data we found, not because it is required.

| Endpoint | Price | Notes |
|---|---|---|
| `dataforseo_labs/google/*/live` | **$0.012/task + $0.00012/item** | Default. Live-only, no queue. Max 700 keywords/task, 1,000 items/response, 2,000 calls/min, 30 concurrent |
| `historical_rank_overview/live` | $0.12/task + $0.0012/item | Unlocks search rank (9.4) and fan-out rank (9.3) in the citability audit |
| `historical_serps/live` | $0.00012/SERP | |
| `search_intent/live` | $0.012/task + $0.00012/keyword | |
| SERP API (headline) | **$2.00 / 1k live** · $1.20 / 1k priority · $0.60 / 1k standard | See the trap below |

> **Pricing trap.** The headline **$0.60/1k** rate is the *standard* queue, which takes about **5 minutes**. For an interactive agent that is not an equivalent product, so **$2.00/1k live is the honest comparison**. We quote $2.00 everywhere.

**Database refresh is 30–90 days.** Never present Labs output as real-time. Its `newest_data_date` is not in the payload at all; use the provider's stated refresh window and label it `provider_refresh_window`.

**Official MCP server — the server is free, you pay API rates:**

- Remote: `https://mcp.dataforseo.com/v3/mcp` with `Authorization: Basic base64(login:password)`
- Local: `npx -y dataforseo-mcp-server` with `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`
- Source: `github.com/dataforseo/mcp-server-typescript`

**Auth gotcha:** HTTP Basic only, and credentials come from the **API** login at `app.dataforseo.com/api-access`. Using the dashboard login is the single most common auth failure.

**Getting started:** $1 trial credit, $50 minimum top-up. Try DataForSEO: https://try.dataforseo.com/jijqq4kuyyde

---

## How the scoring works

Four rules, applied to every skill:

1. **Deterministic analysis, LLM rewriting.** Scorers, checklists and parsers are reproducible rules the agent applies, not judgements it improvises. Hallucination risk belongs in the layer that produces prose, not the layer that produces numbers.
2. **Every numeric threshold traces to a dated source.** Either it cites `METHODOLOGY-BRIEF §1`, or it is explicitly labelled a judgement call. The `chars/token` table in the citability skill is labelled a judgement call. Shepard's 9.5 for URL accessibility is a measurement. Both say which they are.
3. **Vendor claims are labelled as vendor claims.** `Source: Ahrefs, 2026-06-15, n=137,210 domains — measured` versus `Source: vendor claim, unverified`. A vendor marketing number is never laundered into a fact.
4. **Document your own limits, and mean it.** Every skill carries a `Known limitations` section that is copied into the report verbatim. `information-gain-analysis` says outright that Google has not confirmed any information gain requirement, and ships the practitioner dissent alongside the mechanism.

The honesty rule is enforced in practice: **during validation, one fabricated citation was found and removed.** A statistic attached to a named community report on a specific date, with nothing behind it. It is recorded in `docs/METHODOLOGY-BRIEF.md` §1.9c so the next contributor does not reintroduce it. Two unverifiable quotes were pulled for the same reason.

---

## Roadmap

These are sourced gaps, not invented backlog. They come from a review of the current market and are documented in `docs/METHODOLOGY-BRIEF.md` §5. **None of them is in v1.**

| Planned | Why it is a real gap |
|---|---|
| **JSON-LD schema validator** against rich results | Many skills generate structured data. Almost none validate it. |
| **Internal link graph mapper** | *"Plenty of skills mention it, none actually map a link graph."* Directly relevant to the ~150-suggestions-20-usable failure. |
| **Keyword gap analysis** | Competitive coverage currently requires a paid export. |
| **SERP intent / page-type match** | Shepard's #6 factor (9.0). The citability audit approximates it; nothing scores it properly. |
| **Content decay triage** | Distinguishes traffic decay from position decay from staleness. Requires GSC. |
| **GEO experiment tracker** | One variable, 7–21 days, three engines. The market has no tool that resists the temptation to change five things. |
| **SEO drift as a GitHub Action pre-merge gate** | The stale-data failure caught before merge rather than after a quarterly review. |
| **Framework-specific SEO** for Next.js, Astro, Nuxt | Render output and metadata differ enough that generic advice is wrong. |
| **Multi-site / agency support** | Compare a portfolio against its own baseline instead of each site in isolation. |

---

## Where this fits

Fair context, not a competitive attack. Several of these are good, and some are better at breadth than this repo.

| Repo | ★ | What it does well | Notes |
|---|---|---|---|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 35k | The `npx skills` installer this repo is distributed through | Infrastructure, not SEO |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 55k | Breadth across marketing; the only repo in the market documenting its own limitations — a practice borrowed here | Its own warning about installing to `.agents/skills/` is worth heeding |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 19k | Comprehensive Claude Code SEO surface area | 16 files reference DataForSEO MCP v3 tools that no longer exist (#319); broken on a fresh install (#180) |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | 11k | The closest thing to a dedicated GEO skill set | `citability_scorer` regexes are English-only (#80); `robots` step asks for tools that cannot return the data (#81) |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | 7.5k | Broad technical SEO coverage | Claude Code only |
| [Ryze-AI-Adgent/open-seo-mcp-skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills) | 6k | Live data through MCP out of the box | MCP-first means the keyless path is not the baseline |
| [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | 4k | Opinionated, decisive audits | Opinionated is a feature until it meets a page where the opinion is wrong |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | — | Clean, well-scoped individual skills | Vendor-locked to a SE Ranking subscription; stale as of this writing |
| [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | — | Structured data emphasis | |

Three patterns across the field: most are **Claude Code only**, most need a **paid subscription** for live data, and none document their own limits the way this one does. Where they are stronger — breadth, live SERP data, framework coverage — the roadmap above is the answer.

---

## Contributing

Read [`AGENTS.md`](AGENTS.md) first; it is loaded by Codex, OpenCode, Cline, Gemini CLI, Cursor, OpenClaw and Hermes. Then read [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md), which is the internal source of truth for skill anatomy, portability invariants, and the list of things this repo must never do.

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
python tests/validate_skill_inventory.py
python tests/reference_freshness.py --review-after-days 90 --stale-after-days 365
```

Both run in CI on every push. The first checks spec conformance and that every internal link resolves. The second uses **two thresholds deliberately**: 90 days flags a *review trigger* — the finding may have been superseded even though the source itself has not expired — and 365 days fails. A single threshold would flag every primary research paper older than three months as broken, which is noise, and noise is how gates get ignored.

**The citation rule.** Every numeric threshold must trace to a dated source with a stated level of evidence. **Verify the source actually says what you claim before citing it** — reading the primary text is the minimum, and if you cannot verify it, do not cite it. A claim that cannot be independently verified gets removed, not softened.

---

## License

Apache-2.0. Use it, fork it, vendor it into your own internal audit tooling.

## Credits and sources

Built by [Pautthead](https://github.com/Pautthead). Every claim in these skills traces to one of the following primary sources; the full evidence table with dates and sample sizes is in [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md).

**Measurement and primary sources**

- [Cyrus Shepard / Zyppy — The 23 AI Citation Ranking Factors](https://signal.zyppy.com/p/ai-citation-ranking-factors) (2026-05-07, 54 experiments) — accessibility 9.5, search rank 9.4, llms.txt 2.0
- [Ahrefs — llms.txt study](https://ahrefs.com/blog/llmstxt-study/) (2026-06-15, n=137,210 domains)
- [Ahrefs — Information gain](https://ahrefs.com/blog/information-gain/), Louise Linehan (2026-08-20)
- [Google — Patent US11354342B2](https://patents.google.com/patent/US11354342B2/en) — answer composition and fact pruning
- [arXiv 2605.25517](https://arxiv.org/html/2605.25517) (2026-05-25) — controlled GEO experiment, 252,000 trials, 6 LLMs
- [Nathan Hall, Zenodo, 2026-09-17](https://doi.org/10.5281/zenodo.22814843) — crawler behaviour with robots.txt `Sitemap:` announcement
- [a14y.dev — llms.txt linking research](https://a14y.dev/research/llms-txt-linking/) (2026) — markdown mirrors and ingestion cost
- [arsentev.ai — Crawlers and llms.txt](https://arsentev.ai/research/crawlers-and-llms-txt.pdf) — 15-day origin log study
- [Sitefire / arXiv 2609.15369](https://github.com/pulse-energy-eu/slopshape) — structural detection of AI-generated content
- [Search Engine Land](https://searchengineland.com/llms-txt/) (2026-01-20) · [Otterly.AI](https://otterly.ai/blog/llms-txt/) (2026-02-05) · SE Ranking (2026-10-15) · CueScout (2026-10-15)
- Muck Rack (25M+ cited links) · GeoTest (2026-06) · On-Page.ai (150 top-3 pages) · Indig H1 2026 via [Search Engine Journal](https://www.searchenginejournal.com/) · ProCloser field test (2026-05-27, n=5, underpowered)

**Quoted practitioners**

Jeremy Moser (uSERP) via Digiday (2026-03-10) · Lily Ray, [*The AI Slop Loop*](https://lilyraynyc.substack.com/p/the-ai-slop-loop) (2026-04-14) · Louise Linehan (Ahrefs) · Bernard Huang (ex-Clearscope) · Barry Schwartz · Danny Sullivan and Gary Illyes (Search Central Live, 2026) · `r/AiAutomations`, `r/SEO_Xpert`, `r/SideProject`, `r/SEO`, `r/SEO_Xpert`, `r/DigitalMarketing`, `r/AskMarketing`, `r/bigseo`

**Distribution:** the `skills` CLI by Vercel Labs, verified against the [Agent Skills specification](https://agentskills.io/specification) rather than blog posts — several 2026 install guides publish paths that do not exist.

---

*If a claim in this repo cannot be traced to a dated source, that is a bug. Please open an issue.*