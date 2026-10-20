# AEO Citability Audit — fluyeporlaweb.com

**Fetched:** 2026-10-20.
**Sample:** 10 fichas. Top 5 by GSC impressions, plus 5 random, seed `20261020`.
**Score:** PASS / (20 − N/A). W-02 was N/A on all 10 (no operator fact list).
**Mean:** about **82/100**. The pages were not re-scored for this file.

The target query was the GSC top query when one existed (power-automate). Otherwise it was the first JSON-LD `keywords` value. That is rung 3 of the ladder this release requires (GSC, then H1, then keywords). **Seven of the ten X-01 fails used that generic keyword.** Those are query-selection results, not a second measurement of the page.

The first pass falsely failed E-03 and W-04 because the article footer was excluded. The scores below are the published ones, after that was noticed. E-01 fails where the title ends `| Fluye` and Organization says `Fluye por la web` (5 of 10).

All 10 passed raw = DOM (X-02, X-07), H1/H2, self-contained blocks, tables and lists, language, schema, byline, and internal links.

| Page | Query used | Score | Fails |
|---|---|---|---|
| automatizar-procesos-con-power-automate | implantacion power automate | 18/19 = 95 | W-03 |
| auditoria-de-seguridad-de-codigo-con-agentes | ia para programar | 13/19 = 68 | X-01, W-01, W-03, W-04, W-07, E-01 |
| revisar-codigo-con-agentes-de-ia | ia para programar | 13/19 = 68 | X-01, W-01, W-03, W-04, W-07, E-01 |
| videos-de-producto-con-ia | ia para videos | 15/19 = 79 | X-01, W-01, W-03, W-04 |
| chatbot-whatsapp-ia-atencion-clientes | chatbot whatsapp | 17/19 = 89 | W-03, E-01 |
| programar-con-ia-agente-de-codigo | ia para programar | 16/19 = 84 | X-01, W-03, E-01 |
| detectar-trabajo-sin-facturar | ia para finanzas | 16/19 = 84 | X-01, W-03, W-06 |
| perfiles-de-leads-con-ia | ia para ventas | 15/19 = 79 | X-01, W-03, W-04, E-01 |
| leads-locales-en-el-pipeline | automatizar ventas | 17/19 = 89 | X-01, W-03 |
| textos-de-marketing-con-ia | ia para marketing | 16/19 = 84 | X-01, W-03, E-01 |

## What this release changes about reading the table

- X-01: record the rung. A rung-3 fail is not a page fail until the H1 was tried.
- X-02: curl without a rendered snapshot is N/A, not a pass.
- Article footers and a social post cited as a source stay in the main content. Profile links do not.
- Coverage of Shepard's list, stated as this release counts it: **11 direct, 5 partial, 2 reported and not scored** (length, structured data). The older "13 direct" line counted those two.
