# SEO Data Contract — fluyeporlaweb.com

**Captured:** 2026-10-20, 12:20–13:30 Madrid.
**Subject:** fluyeporlaweb.com
**Spend that day:** DataForSEO **$0.006** = 3 × SERP API live advanced ($0.002/task).

The run used the classifier as it stood then. The "Corrected class" column is this release's `classify()` on the same fields. It is arithmetic on those fields, not a new fetch.

## Evidence gate

Datasets with `role: evidence` are fresh or observed. Labs volumes and Cloudflare analytics are `role: context` (keyword choice, unused chart). They do not pull the report to `unknown`.

| Dataset | Newest date inside the data | Class the run printed | Corrected class | Role |
|---|---|---|---|---|
| GSC by date, final | 2026-10-17 | fresh (age 3d, L=3) | fresh | evidence |
| GSC page and page×query, 90d | 2026-10-19 | fresh. 50 pages, 70 rows, not truncated | fresh | evidence |
| GSC URL Inspection | capture 2026-10-20 | observed | observed | evidence |
| Bing rank / crawl / feeds | 2026-10-18 | fresh | fresh (age 2d, L=3) | evidence |
| DataForSEO SERP ×3 | 2026-10-20 | observed | observed | evidence |
| Page fetch | 2026-10-20 | observed | observed | evidence |
| Labs volumes / KD | null | unknown | **aging** (`provider_refresh_window`, L=45, not fresh) | context |
| Cloudflare analytics | 2026-10-20 | unknown (no source family) | **fresh** as `cdn_analytics` row date (age 0, L=1), or **observed** if read as a live dashboard | context |

GSC 90-day performance was very low: a handful of impressions per ficha, maximum **10** on power-automate `[GSC · 2026-10-17]`. No other impression counts were recorded.

## What the old classifier got wrong on this input

- Labs with no date in the payload was printed `unknown`. The documented 30–90 day window bounds the class at **aging**. It is not fresh because the query returned that day.
- Cloudflare had no family, so missing `L` forced `unknown`. `cdn_analytics` is L=1.
- A mixed report is gated by the weakest **evidence** source. Context sources stay on their own figures.

## Illustrative envelopes the rules now match

These are the worked examples in `skills/seo-data-contract/references/ENVELOPE.md`, not rows from the fluyeporlaweb export. They are here because the 2026-10-20 run followed the old function and disagreed with them.

- Example 5a: newest `2026-09-08`, today `2026-10-19`, truncated. Age is **41 days**, class **stale**, reason names Override B. The old text said 11 days.
- Example 5b: Labs, no date, `provider_refresh_window`, truncated. Class **aging**, not unknown.
- Example 5c: `dateModified` is `content_claim`, age 2d against L=1, class **aging**. The fetch is a second envelope with `date_semantics: observed`.
- A `newest_data_date` after today is **unknown**, not fresh.
