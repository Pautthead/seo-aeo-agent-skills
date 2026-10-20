# Extractability — can this page actually be lifted out and cited?

Extractability is the question that separates this audit from a normal on-page SEO
check. A page can rank perfectly and still be uncitable, because ranking rewards the
whole page and citation rewards *one quotable block*.

**Shepard, content visibility (7.6) and answer-near-the-top (8.8) between them:**
an answer that is present, structurally findable, and early is the thing being
measured. Everything in X-01…X-08 is an attempt to observe that mechanically.

---

## X-01 — Answer in the first 1–2 paragraphs · Shepard 8.8

**Rule.** Compute the first 400 visible characters of the main content region, in
document order, from the block list built in Step 1. **PASS** if either:

- the first 400 visible characters contain a block that answers the target query, **or**
- the target query's answer-bearing block appears within the first 2 non-empty blocks.

The query-answer test is explicit-phrasing test: does that block contain a term from
the target query plus a claim about it, rather than a promise to address it later?

**Failing shapes** (all common, all cheap to fix):

- A 3-paragraph preamble about the author's history before any answer.
- "In this comprehensive guide we'll explore…" as the opening block.
- The answer in the page's last section, under a heading like "Conclusion".
- A hero section with three marketing sentences above the actual first paragraph.

**Why characters, not words.** A fixed character budget buys *fewer* words in languages
that spend more characters per token: at the values in the table below, a 400-character
window holds roughly a sixth fewer Spanish words than English ones. The threshold is
therefore slightly *stricter* in Spanish, German and French, not more lenient — which is
the wrong error direction for a position check, because it can flag a good page as late.
Report a near-boundary result in those languages as **not scored** rather than as a fail.
Do not convert this threshold into words.

**Multilingual:** the check is on document position and character count, so it is
language-agnostic. The only language-dependent part is the query-term match, which
uses the operator-supplied target query in the page's own language. No morphology is
required — the audit does not stem, and should not.

---

## X-02 — Text present in the initial HTML · Shepard 7.6

**Rule.** From the raw HTTP response body (Step 0 snapshot), strip `<script>`,
`<style>`, `<noscript>` and all tags, then count visible characters in the main
content region.

- **PASS** if `visible_chars_raw >= 400` and the raw-HTML block list (built the same
  way as the rendered one) contains at least as many non-empty blocks as the
  rendered one.
- **FAIL** otherwise. `200 <= visible_chars_raw < 400` is **FAIL (thin)** — the
  page returns prose, but too little of it to carry an extractable answer. Do not
  leave this band unassigned; a check with an undefined region is not
  deterministic.
- **UNVERIFIABLE** only if only a rendered DOM was captured. Report it as unverifiable.
  Do not pass it.

**Known correctness bug to not reproduce:** `zubair-trabzada/geo-seo-claude` issue #19
falsely reports server-side-rendered sites as JS-rendered. The cause is comparing
across different snapshots or using a heuristic that fires on legitimate hydration
markup. Compare like with like: same URL, same moment, raw vs rendered.

**Signals worth logging but not scoring:**

- `__NEXT_DATA__` / `__NUXT__` / `window.__INITIAL_STATE__` **present but empty of
  article text** — the classic SSR-looking-but-client-only signature.
- Server hints in headers: `x-powered-by: Next.js` with `Cache-Control: private`
  plus short body length.
- Hydration scripts that *contain* the article text inline — this is good SSR, not a
  failure. Do not penalise JSON-embedded content that a renderer would show; only
  penalise text that exists *only* after script execution.

---

## X-03 — Real heading hierarchy · Shepard 8.6 (AI-ready structure)

**Rule.** **PASS** if all three hold:

1. Exactly one `<h1>` in the document.
2. No skipped levels in document order (h1 → h3 without an h2 fails; h2 → h4 fails).
3. At least 3 heading elements total.

**Language-agnostic.** These are element counts; no text is parsed.

**The failure mode this catches:** pages that style a heading with CSS
(`<div class="h2">`) and give it no `h` element at all. Visually a hierarchy,
structurally nothing. An extractor walking the DOM sees an undifferentiated wall of
`<div>`s. This is one of the most common real defects and one of the cheapest to fix.

**Watch for:** a single `<h1>` that is the site logo or a marketing tagline, with the
actual page title demoted to `h2` or styled-div. Fix the `h1`, not the styling.

---

## X-04 — Semantic HTML · Shepard 8.6

**Rule.** Walk every visible text node in the main content region and record the
nearest ancestor element. **PASS** if ≥40% of visible characters sit inside a
semantic block element from this set:

```
p  li  dd  dt  td  th  blockquote  figcaption  caption  summary  h1..h6
```

**Language-agnostic.** Pure structural measurement.

**Why `<dd>` and `<dt>` are in the set, deliberately.** Definition lists are the most
common markup for FAQ answers and glossaries, and they are routinely excluded from
semantic-HTML checks by tools that only whitelist `p`, `li` and `td`. Worse, some
block splitters only split on `<p>`, which makes every `<dd>` invisible — that is
exactly the bug in `zubair-trabzada/geo-seo-claude` issue #80, where `<dl>/<dd>` FAQ
answers are lost, and the resulting report says "answer not near the top" about a page
whose answer is in the first `<dd>`. This audit splits on all ten elements listed in
Step 1.

**Adjacent failure:** text living inside `aria-label`, `alt`, `title` or
`data-*` attributes is not extractable as prose. If >20% of the page's substantive
text lives in attributes, flag it.

---

## X-05 — Self-contained passages · Shepard 8.0

**Rule.** For each block with ≥120 visible characters, the block is *self-contained*
if both:

1. It does **not** open with a pronoun or bare connective in the detected language.
2. It contains at least one content entity — a capitalised token, a number, or a
   quoted term — that does **not** appear in the preceding 200 visible characters.

**PASS** if ≥3 self-contained blocks exist.

**The contrast that matters:**

| Extractable | Not extractable |
|---|---|
| "Magnesium glycinate is supported by 137 scientific studies." | "This ingredient has better evidence." |
| "SearchPilot measured that sites losing organic visibility lost AI citations in 2026." | "As we saw, the same thing happened." |
| "OtterlyAI reports Reddit removed all 4 subreddit communities it built for its 60-day GEO engagement experiment, for a breach of Rule 2 of Reddit's Content Policy." | "Reddit does not like it." |

The right column is not *wrong*. It is **recoverable only with its surrounding
context** — and context is exactly what a synthesizer drops. When a model lifts a
sentence out of a retrieved passage, "This ingredient" resolves to nothing. The
phrase either survives as a dangling reference that an editor deletes, or it is
rephrased into something vaguer than you wrote.

**Language support.** Rule 1 uses a pronoun/connective lexicon. Shipped for:
**en, nl, es, pt, it, fr, de**. Rule 2 is language-agnostic (capitalisation and
numerals). Outside the seven languages, X-05 returns **N/A** — not a failure. A
false negative is not a finding this repo is allowed to publish.

Lexicon roots (extend, do not assume):

```
en  this|that|these|those|it|they|he|she|there|however|also|additionally|moreover
nl  dit|dat|deze|die|het|een|echter|ook|bovendien
es  esto|eso|este|esta|estos|estas|ellos|además|también|sin embargo
pt  isto|isso|este|esta|estes|estas|eles|além|também|no entanto
it  questo|questa|questi|queste|essi|inoltre|anche|tuttavia
fr  ceci|cela|ces|celles|ils|elles|également|en outre|toutefois
de  dies|dieser|diese|dieses|sie|es|außerdem|allerdings|zudem
```

Bare-connective openers (`however`, `also`, `additionally`, `furthermore`,
`de plus`, `por lo tanto`) are included deliberately: they are the most common way a
block loses its subject without an obvious pronoun.

**Counter-caveat — do not invent a chunking ritual.** Shepard does **not** ask you to
carve content into bite-size pieces. His finding is that *clear structure* is
sufficient; a well-headed, well-formed paragraph with a named subject is extractable
whether or not anyone labelled it a "chunk". If this skill started emitting "split
your 400-word paragraph into four 100-word chunks" advice, it would be inventing a
practice the evidence does not support and adding friction with no measured return.
Do not do that. What X-05 actually rewards is **named subjects**, not short blocks.

---

## X-06 — Tables and lists · Shepard 9.0 (intent-format match)

**Rule.** **PASS** if either:

- ≥1 `<table>` with a `<thead>`/`<th>` header row and ≥2 data rows and ≥2 columns, or
- ≥3 `<li>` items inside a single list.

**Language-agnostic.** Element counting only.

**Why format matters.** Intent-format match is 9.0. If the query implies a comparison
and the page answers in flowing prose, the answer is harder to lift without
reformatting — and reformatting is where meaning quietly changes. A comparison table
is a pre-resolved structure: it can be reproduced, partially extracted, or cited as a
unit. Prose cannot.

**Do not score on table quality.** This is a presence check, not an audit of whether
your table is accessible (needs `scope`, `caption`) or semantically correct. Those
belong in a real accessibility audit; do not conflate them.

**Failure shape:** a table rendered as a grid of `<div>`s with `border` styles. Zero
`<table>` elements, so zero extractable structure, and it looks fine.

---

## X-07 — The CSP / JS-dependency silent failure · Shepard 7.6

**Rule.** **PASS** only if the answer-bearing text (first 2 blocks, per X-01) is
present in the raw HTML response. **FAIL** if it is not, regardless of how the page
looks when rendered.

This is a subset of X-02 stated as a separate check because it catches a distinct
failure: **X-02 can be passed while the answer itself is client-injected.**

**The silent failure, described precisely:**

1. The page loads, renders perfectly, and is fully readable in a browser.
2. The raw HTML contains the shell — `<div id="__next">`, `<main>`, skeleton
   placeholders — and little or no prose.
3. Anything that does not execute JavaScript retrieves nothing to quote.
4. There is no error. No warning. No signal in most audit tools. The page scores
   well on every rendered-DOM check.

The dangerous variant is the **CSP-shaped** silent failure: a Content-Security-Policy
with `script-src` restrictions, or a bot-detection layer (Cloudflare, DataDome,
PerimeterX) serving a challenge to non-browser user agents. In both cases the fetch
that an AI crawler receives is not the page — it is a wall — and the failure is
completely silent in a browser-based workflow.

**What to log when it fails:**

- `Content-Security-Policy` header, if present, with its `script-src` and
  `frame-ancestors` directives.
- Whether the raw body contains a challenge/interstitial marker.
- Whether the answer text appears anywhere in the raw bytes (it sometimes does — in
  a JSON blob the client re-renders — which is a *partial* pass: parseable but not
  guaranteed extractable; report as FAIL with the caveat).
- `Cache-Control`, and any `Vary` that would serve a different body to a crawler.

**Actionable fix order:** SSR or SSG the article body first; disable the bot
challenge for verified AI crawler tokens second; `nosnippet` audit third. Nothing
downstream matters if the crawler gets a wall.

---

## X-08 — Content visibility HTML-not-JS and declared language · Shepard 7.6 / 6.3

**Rule, language half.** **PASS** if:

1. `<html lang="…">` or `<html xml:lang="…">` is present, **and**
2. the language detected from the first 3 non-empty blocks is consistent with that
   declaration — same language family, allowing regional variants
   (`en-GB` vs `en-US` pass; `en` vs `de` fail).

**Detection.** Score each candidate language against its stopword list over the first
3 blocks. Highest hit rate wins; if the top two are within 3 points, declare
**MIXED** and mark X-08 N/A with `mixed-language` recorded, because a mixed page has
no single correct answer and a fail would be a false negative.

**Language attribute is not cosmetic.** Language is a Shepard factor at 6.3 and it is
also the precondition for the whole multilingual calibration in Step 3 of the skill:
without a declared language you cannot pick the right `chars_per_token`, and the
per-1,000-words check W-01 becomes meaningless. An undeclared-language page is not
just weaker for AI retrieval — it is unauditable by this skill.

**The HTML half of this factor** — content present in HTML rather than injected by
script — is X-02 and X-07. It is grouped here because it is the same Shepard row;
it is scored twice because the failures are different.

---

## Multilingual summary for this file

| Check | Language-dependent? | Degrades to |
|---|---|---|
| X-01 | No (character position) | — |
| X-02 | No | — |
| X-03 | No (element counts) | — |
| X-04 | No (element counts) | — |
| X-05 | Partly (pronoun lexicon) | **N/A** outside en/nl/es/pt/it/fr/de |
| X-06 | No (element counts) | — |
| X-07 | No | — |
| X-08 | Yes (stopword detection) | **N/A** when MIXED is detected |

Seven of eight checks are fully language-agnostic. That is the design goal: the
market's leading scorer is English-only by regex construction, and most of what it
measures is not a regex problem at all.

**What genuinely does not transfer from English:**

- **Word-count thresholds.** A per-1,000-words threshold must be recomputed from
  `chars_per_token` for the detected language, or it silently means something
  different. See the calibration table in the *Multilingual calibration* section
  below.
- **Typical paragraph length.** English 150–250-word paragraphs are not a universal
  norm; German legal/technical prose and Japanese business prose run structurally
  differently. X-05 measures self-containment, not length, so this audit does not
  inherit the error — but a human reading the report should not be told their
  paragraphs are "too long" by a rule ported from English.
- **Typographic quotation marks.** `"…”"` in English, `„…“` in German, `«…»` in
  French, `“…”` in Spanish. Any quotation or attribution check must accept all of
  them, not just ASCII.

---

## Multilingual calibration — detection, word counting, position checks

This section carries the calibration the skill body points here for. It is
Step 3's language half, in full.

**Language detection.** From the BCP-47 tag in `<html lang>` if present; otherwise
from a stopword-frequency comparison against per-language stopword lists over the
first 3 blocks. Record `detected_language` in the report.

**Word counting that works everywhere.** Never use whitespace token count. Use:

```
effective_words = visible_character_count / chars_per_token[language]
```

`chars_per_token` is a mean word length including the trailing space:

| Language | chars/token | Note |
|---|---|---|
| English | 5.0 | baseline |
| Dutch | 6.4 | long compounds |
| Spanish | 6.0 | |
| Portuguese | 6.0 | |
| Italian | 6.0 | |
| French | 6.6 | elisions |
| German | 6.3 | long compounds + articles |
| Polish / Czech | 6.8 | long inflections |
| Russian / Ukrainian | 6.9 | |
| Japanese, Chinese, Korean | 2.2 | no reliable whitespace; character-based |
| Any other language | 6.0 | conservative default |
| **Mixed-language page** | sum per-language segment | never average |

*Judgement call, labelled as one: these are rounded means, not corpus measurements.
They are used only to convert a character budget into a word budget so that a
per-1,000-words threshold means roughly the same thing in every language. An error
of ±15% in word count does not move W-01 across a realistic boundary.*

**Position checks are character-based, not word-based.** X-01 uses the first 400
visible characters and the first 2 blocks. This is deliberate: it keeps the check
language-agnostic. But a character budget is not neutral across languages — 400
characters is fewer Spanish words than English ones, so the threshold is mildly
*stricter* there. A near-boundary result in a long-token language is **not scored**,
not a fail. Missing a marginal page is acceptable; failing a good one is not.
