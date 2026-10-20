# Consistency Report — cross-skill pass

**Scope:** the 20 files across `seo-data-contract`, `aeo-bot-access-audit`,
`aeo-citability-audit` and `information-gain-analysis`.
**Standard locked against:** `docs/METHODOLOGY-BRIEF.md` §2 (skill anatomy) and §3 (portability
invariants).
**Date of pass:** 2026-10-19.

This report exists so the conventions below can be reviewed rather than reverse-engineered from
the diff. Section 8 lists the conventions the incoming 5th skill should follow.

---

## 1. Requested fixes — what changed

### 1.1 YAML `metadata` normalised to four keys

All four `SKILL.md` files now carry **exactly** these keys, in this order, all string values:

```yaml
license: Apache-2.0
compatibility: <normalised sentence>
metadata:
  repo: "seo-aeo-agent-skills"
  version: "1.0.0"
  updated: "2026-10-19"
  keys-required: "none"
```

| Skill | Removed keys | Relocated to `> **Evidence:**` line |
|---|---|---|
| `seo-data-contract` | `evidence` | Yes — brief §1.7, §1.9, §4, §1.4 |
| `aeo-bot-access-audit` | `factor` | Yes — brief §1.1, §1.4, §1.9 |
| `aeo-citability-audit` | `author`, `skill-type`, `research-window`, `primary-source`, `multilingual` | Yes — all six facts preserved (brief §1.1, §1.2, §1.8, §1.9, §1.10, §1.12; research window; audit type; multilingual calibration) |
| `information-gain-analysis` | `author`, `primary-source` | Yes — brief §1.3, §1.9, §1.2, §1.6 |

Also renamed `keys_required` → `keys-required` (underscore form appeared in two skills and
hyphen form is now the standard).

**No information was lost.** Every removed key's content is restated in the Evidence line
immediately below the H1, with the brief section number so it stays traceable.

### 1.2 License

**The brief's premise here was wrong, and I am reporting that rather than "fixing" it.**
All four `SKILL.md` files already declared `license: Apache-2.0`, correctly positioned after
`description`. Two of the four were quoted (`compatibility: "…"`); two were unquoted; the
`license` line itself was identical in all four.

Action taken: **none on `license`** — nothing was missing. I did normalise the surrounding
`compatibility` values to the same unquoted style (see 1.4), so the frontmatter block is now
byte-identical in shape across all four skills.

### 1.3 Internal link style

Locked form: **every markdown link to a sibling reference uses the `references/` prefix,
from `SKILL.md` and from inside `references/` alike.** This follows METHODOLOGY-BRIEF §2
("Reference links are relative from the skill root, one level deep only").

Rewritten: **26 links across 10 files.**

| File | Links converted |
|---|---|
| `aeo-bot-access-audit/references/EDGE_VERIFICATION.md` | 1 |
| `aeo-bot-access-audit/references/ROBOTS_TRAPS.md` | 1 |
| `aeo-citability-audit/references/CITATION_FACTORS.md` | 5 |
| `aeo-citability-audit/references/CITATION_WORTHINESS.md` | 3 |
| `aeo-citability-audit/references/ENTITIES.md` | 2 |
| `aeo-citability-audit/references/LIMITS.md` | 1 |
| `information-gain-analysis/references/COMPETITOR_SERP.md` | 3 |
| `information-gain-analysis/references/HONESTY.md` | 3 |
| `information-gain-analysis/references/METHODOLOGY.md` | 4 |
| `information-gain-analysis/references/SCORING.md` | 3 |

Note that `information-gain-analysis` was described as already correct. It was **not** — its
reference files used a *mixed* style (body links bare, footer links prefixed). Both styles are
now `references/`.

Verified mechanically:
- 61 markdown links to `.md` files across the 20 files.
- **Every one resolves to a file that exists.** Zero broken targets.
- Zero `references/references/` double-prefixes.
- Zero bare `](SIBLING.md)` links remaining inside `references/`.

**⚠️ One consequence you should decide on.** The locked form resolves *from the skill root*,
not from the file's own directory. So `references/EXTRACTABILITY.md` written inside
`references/CITATION_FACTORS.md` is correct per the brief and per this convention, but a
renderer (or a reader clicking it on a GitHub-hosted page) resolving from
`references/CRAWLERS.md`'s own directory gets a dead path. I followed the explicit instruction
and the brief rather than second-guessing it, but this is a real trade-off and the 5th skill's
author needs to know it exists. See §7.

### 1.4 `compatibility` normalised

Standard: a single sentence opening with one of `No dependencies` / `Requires network access` /
`Network access optional`, then specifics. All four are now unquoted YAML strings.

| Skill | Before | After |
|---|---|---|
| `seo-data-contract` | `"No dependencies, no API keys…"` | **already conformant**; quotes removed |
| `aeo-bot-access-audit` | `Network access to the audited origin only…` | `Requires network access to the audited origin only. No API keys, no MCP servers, no paid accounts. Requires curl (or an equivalent HTTP client).` |
| `aeo-citability-audit` | `"Network access optional - accepts pasted HTML…"` | `Network access optional — accepts pasted HTML when offline. No API keys, no MCP, no dependencies.` |
| `information-gain-analysis` | `Works with web fetch alone…` | `Requires network access to the SERP results being baselined. No API keys, no MCP servers, no paid accounts. Refuses to run rather than guessing when the host has no web access at all.` |

Each stays specific and honest about what it actually needs.

---

## 2. The four author questions

### 2.1 `seo-data-contract` 5th value `observed` — KEPT, but it was genuinely broken

**Verdict: keep it. It was already well-designed; it was just not actually implemented
consistently, and there was a real bug.**

Three defects found and fixed:

1. **REAL BUG — a value that exists nowhere else.** `SKILL.md` §"When not to use this" instructed
   the agent to set `freshness_class: observed-now`. That string appears in **no** enum, in no
   example, in no reference file. An agent following that instruction would emit an invalid
   envelope. Fixed to `freshness_class: observed`.

2. **REAL BUG — the enum and the override disagreed.** `ENVELOPE.md` §3 declared the enum as
   five values (`fresh · aging · stale · expired · unknown`), while `FRESHNESS.md` §3 produced a
   sixth (`observed`) and `ENVELOPE.md` §5c used it. `ENVELOPE.md` §5c acknowledged the
   problem in prose ("breaking the enum") but the field reference never listed it, so an agent
   reading §3 would treat `observed` as invalid. Fixed by declaring `observed` explicitly in
   the `ENVELOPE.md` §3 field reference as a *documented override value*, naming its single
   derivation and its two boundaries (a source with no date is `unknown`, not `observed`; a
   stale source is `stale`, not `observed`).

3. **REAL BUG — the gate had no row for it.** The Step 5 gate table covered `fresh`, `aging`,
   `stale`/`expired` and `unknown`, and **omitted `observed` entirely** — so an observed object
   had no defined action at the gate. Added a row: analyse, label `[SRC · observed at
   …]`, and state the *representativeness* limit instead of an age limit.

Also aligned: `FRESHNESS.md` §3 now states this is the only condition that produces `observed`;
`ENVELOPE.md` §6 validation rule 6 now names all three overrides (A, B, observed) instead of
"the two overrides"; the Step 4 check and `ENVELOPE.md` §5c `class_reason` now say what the
override was and what the real limit is.

**Is it easy for an agent to apply?** Yes — after these fixes it is a mechanical rule keyed off
`date_semantics`, not a judgement. That is what made it worth keeping.

### 2.2 `aeo-citability-audit` — "nothing is wrong on-page" line: KEPT, with one scoping fix

**Verdict: keep. It is the best line in the repo and it is consistent with the scoring model.**

Checked it against everything that could contradict it and found **no** contradiction on rank,
band or determinism: Step 4 says print it above 70; the output template says the same;
`LIMITS.md` §1 says the same; the 60–79 "workable" band and the 70 cut-line agree with each
other.

**One genuine contradiction found and fixed.** The line was unconditional on score alone, but
the same skill's N/A accounting removes checks from the denominator ("points_possible = 5 ×
(20 − count(N/A))"), and `LIMITS.md` §6 mandates "Never report a false negative as a finding."
So a page could score 75 with X-05, W-03 and W-06 all N/A and be told it had "nothing wrong
on-page" when three checks **never ran**. That is precisely the false negative the repo refuses
to publish, contradicting its own §0.3 principle.

Fixed minimally — the verbatim sentence is untouched; only its trigger is scoped. Both Step 4
and the output template now require **score > 70 *and* no N/A checks**, with an explicit
instruction on what to print instead when checks are N/A.

### 2.3 `information-gain-analysis` rank scores zero — KEPT, verified consistent

**Verdict: keep. The reasoning is stated and the skill is internally consistent.**

The reasoning is stated explicitly and is strong — `SCORING.md` §1 calls it out as *the trap*
("including rank would launder a known-good signal … into a label called 'information gain'"),
with the concrete failure case (reporting "gain score 40, low" when the real problem is the page
ranks #40). It propagates correctly through `SKILL.md` §Scoring rule 1, `SCORING.md` §8
("Replacing a rank check. See §1"), and `HONESTY.md` §9 ("Replace a rank check, an
accessibility check, or a crawl check"). §1 also correctly flags that the On-Page figures are
ordinal, not numeric, and must not be printed side by side with this rubric's own numbers. No
contradiction found. No change made.

### 2.4 Fabricated attribution sweep — **one found and removed**

I grepped all 20 files for every person name, company name, vendor name and study citation, and
checked each against METHODOLOGY-BRIEF §1.

**Verified traceable to the brief** (no action): Cyrus Shepard / Zyppy, Nathan Hall (Zenodo),
Danny Sullivan, Gary Illyes, Barry Schwartz, Lily Ray, Jeremy Moser (uSERP), Louise Linehan,
Bernard Huang, Ahrefs, SearchPilot, Muck Rack, GeoTest, ProCloser, On-Page.ai, Sitefire /
arXiv 2609.15369, Otterly.AI, CueScout, SE Ranking, Indig, US11354342B2, arXiv 2605.25517,
all `r/*` sources, and all competitor-repo names in §5. The bot-access catalogue's vendor names
(OpenAI, Anthropic, Google, Microsoft, Perplexity, You.com, DuckDuckGo, Mistral, Apple, Brave,
Meta, Amazon, Common Crawl, ByteDance, Cohere, Meltwater, Hugging Face, DeepSeek, Timpibot,
Webzio, Diffbot) are vendor documentation claims in their own right and are labelled
"vendor-documented" in that file's own confidence table.

**🔴 REMOVED — one fabricated citation.**

`information-gain-analysis/references/HONESTY.md` §8 opened with:

> A community report (`r/bigseo`, 2026-05-01) found **60% of programmatic pages deindexed
> within five months.** Anecdotal, unreplicated, self-reported — but unusually specific.

`r/bigseo` appears **nowhere** in METHODOLOGY-BRIEF. Neither does the 60% figure. This was a
specific statistic attached to a specific named community report on a specific date, with
nothing behind it — the exact failure mode the repo exists to prevent. It was also the entire
evidentiary basis of a section that then presented three "survivor properties" as established
findings.

Removed, and replaced with an explicit statement that **no measurement in the evidence base
covers programmatic-page survival**, plus a re-labelling of the three properties as
**hypotheses, not findings**, to be checked against the operator's own data. The dimension
mapping table and the "internal linking is not measured by this skill" caveat were kept — they
are independent of the fabricated statistic. The `r/bigseo` line was also removed from
`HONESTY.md` §11 Sources.

---

## 3. Additional contradictions found and resolved

These were not in the brief. Each is provable from METHODOLOGY-BRIEF or from the files
themselves.

| # | Skill | Contradiction | Resolution |
|---|---|---|---|
| 3.1 | `seo-data-contract` | **Envelope field-count mismatch.** `ENVELOPE.md` declared "8 fields for a pasted file", and its Tier-1 JSON example contains **11 keys**. `SKILL.md` Step 0 said "eight required fields" / "ten optional" and its check enumerated only **7** names, omitting `envelope_version`, `source_ref`, `last_successful_retrieval_at` and `class_reason`. `ENVELOPE.md` §6 rule 1 said "All 8". | Reconciled on **11 required / 7 optional** (18 total — matches the Tier-2 count exactly, and matches the 7 fields ENVELOPE.md §3 marks optional). Updated in `ENVELOPE.md` §1/§2/§6 and `SKILL.md` Step 0 + Scoring. Chose 11 over 8 because it matches the worked example and the Tier-2 total, and because trimming the example would have discarded `class_reason`. |
| 3.2 | `aeo-citability-audit` | **Factor-coverage arithmetic.** `CITATION_FACTORS.md` and `LIMITS.md` §2 both claimed "**14** of 23 factors directly, **4** partially". The table's own `Keyless?` column gives 13 `yes`, 5 `partial`, 4 `no`, 1 unscored. | Corrected to **13 direct / 5 partial**, derived explicitly from the column, with the sum shown. Also reconciled the "not measurable keylessly" list: **4** wholly unmeasurable, plus brand/entity trust (6.8) measurable on-page only. `SKILL.md` output template updated to match. |
| 3.3 | `aeo-citability-audit` | **X-06 Shepard score wrong.** `EXTRACTABILITY.md` headed X-06 "Shepard 8.0 (intent-format match)" and `SKILL.md` Step 2 listed 8.0 — but the brief scores intent-format match at **9.0**, and `CITATION_FACTORS.md` maps factor 6 to X-06 at 9.0. `EXTRACTABILITY.md` contradicted *itself* two paragraphs later ("Intent-format match is 9.0"). | Corrected to **9.0** in both places. |
| 3.4 | `information-gain-analysis` | **`METHODOLOGY.md` §7 contradicted itself and the brief.** It said "Shepard's top factor is search rank (top 10), 9.4/10". Search rank is Shepard's **#2**; #1 is URL accessibility at 9.5. Five lines later the same section says "Shepard ranks URL accessibility #1 at 9.5". | Rewritten to name both correctly: #1 accessibility 9.5, #2 search rank 9.4. |
| 3.5 | `information-gain-analysis` | **`METHODOLOGY.md` §6 — denominator error.** "Shepard scores length **6.7/23**". The factor scale is 0–10. | Corrected to **6.7/10**. |
| 3.6 | `aeo-citability-audit` | **`LIMITS.md` §3 cited the wrong outlet.** "Indig H1 2026, via Search **Engine Land**". The brief §1.9 and the other three occurrences across the repo say Search **Engine Journal**. | Corrected to **Search Engine Journal**. |
| 3.7 | `information-gain-analysis` | **Broken cross-reference.** `METHODOLOGY.md` §3 said "Read §7 of `HONESTY.md` before relying on it." `HONESTY.md` has no §7 on the patent-is-not-a-ranking-factor point — that is §1. | Corrected to **§1**. |
| 3.8 | `aeo-citability-audit` | **X-02 had an undefined band.** PASS at `visible_chars_raw >= 400`, FAIL at `< 200`, and **nothing assigned to 200–399**. A check with an unassigned region is not deterministic, in a repo whose §0.2 requires it. | Added the missing band explicitly: `200 <= visible_chars_raw < 400` → **FAIL (thin)**, with a note not to leave the band unassigned. `UNVERIFIABLE` narrowed to the one condition that warrants it (rendered-DOM-only capture). |
| 3.9 | all | **13 of 20 files did not end with a newline.** Pre-existing, not caused by this pass. | Normalised all 20 to a single trailing newline, UTF-8 without BOM, LF throughout. |

---

## 4. Deliberately left alone

Each of these I could not prove wrong, so I did not touch it.

1. **Two `Lily Ray` quotes in `HONESTY.md` are not verbatim in the brief.** §4 (*"they work, they
   spread, they get patched"*) and §6 (the human-in-the-loop quote about sites claiming human
   editors). The brief documents Lily Ray as a real source (§1.2, §1.8) and contains two of her
   quotes, but not these two. **I could not prove them fabricated, and §6 is described by its own
   author as "the single most operationally important line in this file".** Deleting a
   load-bearing honesty constraint on the strength of an absence would be worse than leaving it.
   **These need author confirmation with a URL before the 5th skill cites anything from this
   file.** Flagging, not clearing.

2. **The 70-point cut-line in `aeo-citability-audit` is an unlabelled judgement call.** The skill
   carefully labels its band names as "a communication convenience, not a measured threshold",
   but 70 specifically is not labelled. I kept the number because it is consistent everywhere it
   appears and there is nothing to derive it from.

3. **`W-02`'s 70% fact-coverage threshold** in `CITATION_WORTHINESS.md` is likewise unlabelled as
   a judgement call, unlike `W-01`'s 2.0 threshold which *is* explicitly labelled. Inconsistent
   labelling, but the value is not demonstrably wrong.

4. **`geo-test`'s Citation Worthiness 34/100 weighting** — the brief §1.10 confirms it. Left.

5. **Non-ASCII in shell examples.** `ROBOTS_TRAPS.md` and `EDGE_VERIFICATION.md` use `grep -A3`,
   `for … in`, `$(…)` and associative arrays that need Bash; the files do note a PowerShell
   equivalent in places but not uniformly. Pre-existing, not a consistency issue in scope.

6. **Description lengths.** `seo-data-contract` and `aeo-bot-access-audit` descriptions run
   slightly over the brief's "~300 chars" guidance. Front-loaded trigger words are present as
   required, which is what §3 actually prioritises. Not worth shortening unprompted.

---

## 5. Files changed (15 of 20)

```
skills/seo-data-contract/SKILL.md                     frontmatter, Evidence, observed fix, 11/7 fields, gate row
skills/seo-data-contract/references/ENVELOPE.md        11/7 tier counts, observed enum, §5c, §6 rule 1+6
skills/seo-data-contract/references/FRESHNESS.md      observed-override uniqueness statement, newline
skills/seo-data-contract/references/SOURCES.md        newline

skills/aeo-bot-access-audit/SKILL.md                  frontmatter, Evidence, compatibility, newline
skills/aeo-bot-access-audit/references/EDGE_VERIFICATION.md   1 link, newline
skills/aeo-bot-access-audit/references/ROBOTS_TRAPS.md        1 link, newline

skills/aeo-citability-audit/SKILL.md                  frontmatter, Evidence, compatibility, X-06, coverage, N/A scoping
skills/aeo-citability-audit/references/CITATION_FACTORS.md    5 links, coverage arithmetic
skills/aeo-citability-audit/references/CITATION_WORTHINESS.md 3 links
skills/aeo-citability-audit/references/ENTITIES.md            2 links
skills/aeo-citability-audit/references/EXTRACTABILITY.md      X-06 score, X-02 band
skills/aeo-citability-audit/references/LIMITS.md              1 link, coverage arithmetic, Indig outlet

skills/information-gain-analysis/SKILL.md             frontmatter, Evidence, compatibility, newline
skills/information-gain-analysis/references/METHODOLOGY.md    4 links, Shepard #1, 6.7/10, §1 cross-ref
skills/information-gain-analysis/references/SCORING.md        3 links, newline
skills/information-gain-analysis/references/COMPETITOR_SERP.md 3 links, newline
skills/information-gain-analysis/references/HONESTY.md        3 links, r/bigseo removal + §11, newline
```

Unchanged: `seo-data-contract/references/{FRESHNESS,SOURCES}.md` content-wise beyond the items
above; `aeo-bot-access-audit/references/CRAWLERS.md`; `aeo-citability-audit/references/CITATION_WORTHINESS.md`
and `ENTITIES.md` (links only).

---

## 6. Verification performed

- All 4 `SKILL.md` frontmatter blocks inspected: identical key set, key order, string values,
  `license` position.
- All 61 intra-repo `.md` links resolved against the filesystem — zero broken.
- Zero `references/references/` double-prefixes.
- Zero bare sibling links remaining in any `references/*.md`.
- Zero non-standard frontmatter keys remaining (grepped for `author`, `factor`, `evidence`,
  `skill-type`, `research-window`, `primary-source`, `multilingual`, `keys_required`).
- Zero `observed-now` / "8 required fields" / "ten optional" strings remaining.
- Encoding verified: 0 replacement characters, UTF-8 without BOM, `§` (U+00A7) and `—` (U+2014)
  intact across all 20 files, LF line endings throughout.

---

## 7. Open question for you

**The link convention has a resolution asymmetry.** Section 1.3 documents this, but it is worth
stating plainly because it will bite the 5th skill:

- `references/` prefixed links are correct **from the skill root** (the brief's rule) and are
  what a skill loader or an agent reading the skill directory expects.
- They are **not** correct when resolved relative to the file's own directory, which is what a
- markdown renderer does when displaying `references/SOMEFILE.md` in a GitHub-style browser view.

The alternatives are (a) keep as-is — status quo per the brief, 26 links now follow it;
(b) switch `references/*.md` files to bare sibling links (`[Extractability](../skills/aeo-citability-audit/references/EXTRACTABILITY.md)`),
which renders correctly but contradicts the brief and re-creates the original inconsistency;
(c) keep the `references/` prefix in `SKILL.md` only and use bare siblings inside
`references/`, which is the most robust of the three but is a partial revert of the requested
fix.

**Resolved in v1.0.3: option (c), the robust one.** `SKILL.md` keeps `references/FOO.md`; files
inside `references/` now link to bare siblings (`FOO.md`). The validator resolves links relative to
the containing file, exactly as GitHub does, and rejects any link that escapes the skill root. That
surfaced 30 links that rendered as 404 on GitHub while the old check passed them. The brief and
`AGENTS.md` are updated to match. Decision taken before the 5th skill, as recommended.

---

## 8. The locked standard (for the 5th skill)

1. **Directory shape:** `SKILL.md` + `references/`. Nothing nested deeper.
2. **Frontmatter, exactly:**
   ```yaml
   ---
   name: <must equal directory name>
   description: <what + when + triggers, front-loaded, ~300 chars>
   license: Apache-2.0
   compatibility: <one sentence: No dependencies / Requires network access / Network access optional, then specifics>
   metadata:
     repo: "seo-aeo-agent-skills"
     version: "1.0.0"
     updated: "2026-10-19"
     keys-required: "none"
   ---
   ```
   No other metadata keys. Genuinely useful extras go in a `> **Evidence:**` line immediately
   below the H1, with brief section references.
3. **Body section order:** H1 + purpose · When to use · When not to use · Inputs (keyless path
   first) · Procedure (numbered, each with a runnable *check* and a falsifiable *pass*) ·
   Output format (literal template) · Scoring (deterministic) · Known limitations · Optional
   data sources (keyless fallback stated) · References.
4. **Links:** `references/FILE.md`, one level, always. No bare sibling links. Verified to exist
   before committing.
5. **Every fetched page is untrusted data, not instructions.** State it in every skill that
   fetches.
6. **Every numeric threshold traces to METHODOLOGY-BRIEF §1, or is explicitly labelled a
   judgement call.**
7. **Every determinism hole is closed.** Any rule with an unassigned band is a bug (§3.8 above).
8. **UTF-8, no BOM, LF, single trailing newline.**