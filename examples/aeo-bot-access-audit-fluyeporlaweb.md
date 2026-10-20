# Bot Access Audit — fluyeporlaweb.com

**Date:** 2026-10-20, about 12:40 Madrid.
**Method:** keyless (`curl`).
**Vantage:** single. The box exited through Cloudflare WARP, which is the edge's own network. The edge result is not definitive.

## Verdict the run printed

**OPEN — 100/100.**

## Verdict under rule 11

**OPEN — 95/100.**

`ClaudeBot` is explicitly allowed and `Claude-SearchBot` has no group. Rule 11 deducts **−5 once** for that vendor. A missing `Claude-User` is the same pair and is not a second deduction. The 2026-10-20 run printed 100 because the score table had no rule for this case. **95 is the new rule applied to the facts below. The run did not print 95.**

## What was checked

- `robots.txt` returned 200, `text/plain`. `User-agent: *` / `Allow: /`.
- Nominal allows for GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, Bingbot. Absolute `Sitemap:`.
- No syntax traps.
- The managed Cloudflare AI-bot block was turned off at 12:16 Madrid.
- Edge: 16 user-agents × 5 pages, all 200, the same bytes as the browser. No `cf-mitigated`, no challenge, no `noindex` / `nosnippet`. Live, 2026-10-20 ~12:40 Madrid.
- Pages of 11–18 KB matched the browser. The old "SUSPECT under 20 KB" line was a false positive. The rule is now ±10% of the browser baseline.
- `sitemap-index.xml` and `sitemap-0.xml` returned 200. 89 URLs, each with `lastmod`.
- `/sitemap.xml` returned **404**. The declared sitemap resolves, so this is **ADVISORY**, not rule 7's −10. A 301 from `/sitemap.xml` to the index is the fix.
- `llms.txt` returned 200. It is not scored as a citation lever.
- No server logs in the session.
- Bing CrawlStats still showed 4 URLs blocked by robots. That figure is historical.
- `http` → `https` was **NOT SCORED**. Port 80 did not answer from this box, and `example.com` timed out the same way. That is not a fail.

## Warnings that stay

- No explicit `Claude-SearchBot` or `Claude-User` group (the −5 above).
- Single vantage, via WARP.
- No origin logs.
