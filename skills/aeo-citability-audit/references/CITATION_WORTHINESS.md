# Citation-worthiness — is this page worth quoting?

Extractability (see [EXTRACTABILITY.md](references/EXTRACTABILITY.md)) asks whether a passage
*can* be lifted. Citation-worthiness asks whether it is *worth* lifting — whether the
page carries the kind of material a synthesizer will keep.

**Where this sits in the weighting:** GeoTest (2026-06) weights Citation Worthiness at
**34 of 100** — the largest single category in its model, ahead of technical
structure, authority and crawlability. Worthiness is not a garnish on an audit; it is
the biggest block of the score.

**And the off-site mirror of it:** Muck Rack, across 25M+ cited links —
**earned media 84% of AI citations vs 0.3% paid.** Whatever makes a page worth
quoting on-page, the same properties are what a journalist or a Reddit commenter
repeats off-site. These are not two problems.

---

## W-01 — Sourced-fact density · Shepard 8.3

**Rule.** Count *externally attributable facts* in the main content, then divide by
1,000 effective words. **PASS** if the ratio ≥ 2.0.

**An externally attributable fact** is a claim a third party could verify without
asking the author. Concretely, any of:

- A specific number with a magnitude or unit — `137 scientific studies`, `25,000 posts
  per day`, `$0.012/task`.
- A specific date — `2026-04-17`, `July 2026`, `Q3 2025`.
- A named person or organisation attached to a claim — `Cyrus Shepard`, `Ahrefs`,
  `Google Search Central`.
- A named study, dataset or patent identifier with a figure — `n=137,210 domains`.

**Explicitly not facts:** adjectives, marketing superlatives, unquantified
improvables ("dramatically faster"), and percentages with no base ("up to 40% faster"
with no denominator). A number without a unit or a base does not count.

**Why density, not presence.** One sourced fact in a 3,000-word page is a footnote.
The signal is that the page is *made of* checkable material throughout, because a
retrieved passage — typically a fraction of the page — needs to contain some. If your
density is 0.2/1,000, a 200-word extracted passage has a 4% chance of carrying one.

**Language calibration — mandatory outside English.** `effective_words =
visible_character_count / chars_per_token[language]`. The `chars_per_token` table is
in SKILL.md Step 3. Do **not** use whitespace token counts for Japanese, Chinese or
Korean, where whitespace tokenisation does not exist and a token count returns roughly
the number of clauses. For CJK, character count divided by 2.2 is the only workable
normalisation.

*Threshold judgement call, labelled:* the 2.0-per-1,000 threshold is our calibration
of GeoTest's signal, not a figure GeoTest published as a pass/fail line. Treat it as a
consistent yardstick for before/after comparison on the same site, not as a proven
universal constant.

---

## W-02 — Coverage of the facts cited pages agree on · Shepard 9.2 (query-answer match)

**Rule.** **PASS** if the page contains at least 70% of the agreed facts in the
operator-supplied fact list, as literal entities (proper nouns, numbers, dates), not
as paraphrase.

**Requires input.** The fact list must be supplied by the operator, derived by the
operator from the pages that currently get cited. Without it, **W-02 is N/A** — and
the report must list it as N/A. Do not invent the fact list; doing so manufactures a
pass out of the auditor's own assumptions.

**This is the information-gain mechanism, in its negative form.** The strongest
thing a synthesizer can do is take facts from one source and add the one fact nobody
else said — everything already covered gets pruned to avoid repetition. A 2026 patent
(US11354342B2) describes exactly this: an assistant answering from source 1 for facts
A+B, then source 2 for fact C *only*, deleting the overlap. The consequence, from
Ahrefs (Louise Linehan, 2026-08-20):

> "In a ranked list, even if you're the fourth site saying the same thing, you're
> still on the SERP… But in a synthesized answer there **is** no position four. Either
> you provide the information that hasn't been said yet, or your content gets cut."

So W-02 measures the *minimum viable* condition: do you at least carry what everyone
else carries? W-02 does **not** measure information gain — there is no dedicated
information-gain check in this skill, because the score is measured by meaning and
cannot be computed deterministically without an LLM, and an LLM-scored check would
violate the deterministic-analysis principle. Report it as an observation with the
patent and Ahrefs cited, not as a score.

**Caveat to carry verbatim:** Ahrefs is explicit that Google has not confirmed any
information-gain requirement. Practitioner dissent is on the record
(`r/SEO`, 2026-01-26): *"there is no information gain requirement — how do I know this
— I publish 100's of 000's of PAAs/FAQs a month."* Present both. The stronger
position is that information gain is a mechanism by which synthesis prunes overlap,
well-evidenced at the mechanism level; the specific claim that Google penalises pages
for low gain is not established.

---

## W-03 — Attributed quotations · Shepard 8.0 (cites sources)

**Rule.** **PASS** if the page contains ≥1 quotation attributed to a **named speaker
and a source**.

Both halves are required. `blockquotes` without attribution are decoration. So is
attribution to an unnamed "experts say".

Acceptable forms:

- `<blockquote>` followed by an attribution in the adjacent `<p>`, `<cite>` or
  `<figcaption>` naming a person and a publication.
- Inline: `"Cyrus Shepard scored it 2.0/10" — Zyppy, 2026-05-07.`
- Footnote or endnote naming the speaker and the venue.

**Language support.** Requires quotation-mark recognition. **Must accept typographic
quotes**: `"…”"` (English), `„…“` (German), `«…»` (French), `“…”` (Spanish/Italian),
`「…」` (CJK). Shipped lexicons: **en, nl, es, pt, it, fr, de**. Elsewhere **N/A**,
never a fail.

**Also log, do not score:** the presence of a `cite` element or `rel="noopener"`
outbound link from a quoted claim. Good practice, weak evidence for citation.

---

## W-04 — External source citations · Shepard 8.0

**Rule.** **PASS** if the page contains ≥3 outbound links whose host is outside the
page's own registrable domain, in the main content region.

**Registrable domain, not hostname.** `docs.example.com` and `blog.example.com` are
the same domain. `example.github.io` is a different registrable domain from
`github.io` for this purpose — public-suffix handling matters or large sites get free
passes.

**Exclude:** navigation, footer, social links, cookie banners, and the site's own
logo link. Only count links inside content blocks.

**Language-agnostic.** Pure link-graph measurement.

**Why it scores:** a page that shows its sources is a page whose claims can be quoted
without the extractor having to extend trust to you first. And in practice it
correlates with earned media — Muck Rack's 84% earned vs 0.3% paid split. Pages that
cite get cited.

**Do not require a minimum link count above 3.** Three high-quality primary-source
links beat thirty aggregator links, and the audit cannot tell the difference. Report
the count and the destinations; let a human judge quality.

---

## W-05 — Comparison tables

**Rule.** **PASS** if the page contains ≥1 `<table>` with ≥2 rows and ≥2 columns of
data.

**Language-agnostic.** Element counting.

**Why worthiness and not just format:** a comparison table is the densest possible
package of extractable, attributable, structured claims on a page. Every cell is a
mini-fact with a named row and column header. When a model answers "how does X compare
to Y", a table is close to a pre-rendered answer. This is the single most
citation-dense structure available to you and it costs nothing but the work of
building it.

**Watch the anti-pattern:** the table that exists only to rank your own product first
against unattributed or invented competitors. It converts a 5.6-scoring structured
signal into a trust liability, and it is the shape most likely to be called out in a
synthesized answer's commentary. If the comparison is not defensible, do not build it.

---

## W-06 — Quotable definitions

**Rule.** **PASS** if the page contains ≥1 sentence that (a) contains a definitional
marker for the detected language, and (b) is ≤40 words / ≤`40 × chars_per_token`
characters.

**Definitional markers by language:**

```
en  is a | are | means | refers to | is defined as | is called | that is,
nl  is een | betekent | verwijst naar | wordt gedefinieerd
es  es un | es una | significa | se refiere a | se define como
pt  é um | é uma | significa | refere-se a | é definido como
it  è un | è una | significa | si riferisce a | è definito come
fr  est un | est une | signifie | désigne | est défini comme
de  ist ein | ist eine | bedeutet | bezeichnet | wird definiert als
```

**≥40 words, not ~40 words.** The point is that a definition has to be liftable as a
single sentence. Long definitions get truncated, and truncation of a definition
produces a wrong definition.

**Why it is worthiness:** a quotable definition is the highest-density citation target
on a page because it is stable. It does not go stale with a price or a ranking, it is
unambiguous when quoted without context, and it is exactly what a model needs to
answer "what is X" without re-reading your whole page.

**Language support:** shipped for the seven languages above. Elsewhere **N/A**.

**Related Shepard factor — explicit phrasing (8.1):** the same principle applied to
claims rather than definitions. "Magnesium glycinate is supported by 137 scientific
studies" is quotable; "this ingredient has better evidence" is not. Full contrast in
[EXTRACTABILITY.md](references/EXTRACTABILITY.md), X-05.

---

## W-07 — Explicit price and a visible timestamp

**Rule.** **PASS** if the page contains (a) a visible price or cost, and (b) a visible
date, both in the main content region.

**Source: arXiv 2605.25517**, 2026-05-25 — 252,000 trials, 6 LLMs, two-source
injected RAG, brand names anonymised, order counterbalanced. This is the most rigorous
single study in the evidence base and it is worth reading the findings carefully.

**What the study found, ranked by effect:**

1. **Topical relevance and list position dominate.** Everything else is second order.
2. **Explicit price information helps, consistently.** Across six LLMs. Not a
   one-model artefact.
3. **A recent timestamp helps, consistently.** Same.
4. **Completeness and trust cues: smaller gains.** Real but clearly second tier.
5. **Formatting-only edits: little impact.**

**How that maps to W-07.** Price and freshness are the two signals the study found to
be reliably helpful across models. Page-format changes are the one it found to be
close to inert. That is a strong, specific, actionable finding — and it is the
empirical reason this audit does not award points for prettier markup.

**Practical caveats:**

- Price only applies to pages where a price exists. A documentation page or a
  methodology write-up has no price to state, and W-07 should be reported as **not
  applicable to this page type**, not as a failure. Judge it against page type.
- "Visible date" means a date a reader can see in the content or byline, not a
  `datePublished` buried in JSON-LD. E-05 covers the machine-readable half; W-07
  covers the human half. A page with only a JSON-LD date has not shown a timestamp to
  a model reading the rendered text.
- Recency means *current*. A date 18 months old is not a fresh timestamp; it is
  evidence of neglect.

**The finding that should govern agent behaviour:**

> "The sites that try to create as much content as possible eventually get burned,
> including very big brands."
> — Lily Ray, commenting on arXiv 2605.25517

Do not let an audit recommendation end in "publish more". Content volume is not a
lever measured by this study. Its two helpful signals are both about *precision*:
state the price, state the date.

---

## Why formatting lost

Formatting-only edits scored little impact across 6 LLMs and 252,000 trials. Three
operational consequences:

1. **Never recommend a reformat as a fix without substance attached.** "Break this
   into sections and add bullets" is not a recommendation this skill should emit on
   its own. If it comes with a moved answer to the top (X-01) or a real table (W-05),
   fine. Alone, it is decoration.
2. **Structure still matters — through structure's effect on extraction.** X-03 and
   X-04 score 8.6 not because pretty HTML wins, but because unstructured DOM prevents
   the extractor from finding the answer at all. The mechanism is extraction, not
   presentation.
3. **Corollary for slop:** AI-generated text is detectable from **structure alone**,
   ~98% accuracy on held-out data (Sitefire / arXiv 2609.15369, 2026-09). You cannot
   paraphrase your way out of a structural tell. Any recommendation this audit emits
   should push toward real structure, never toward shape-matching a competitor's
   post.

---

## Non-English pages: the three thresholds that must move

Everything else in this file is language-agnostic. These three are not.

| Threshold | English value | What to do elsewhere |
|---|---|---|
| W-01 fact density | 2.0 per 1,000 words | Recompute words as `chars / chars_per_token[lang]`. CJK: character count ÷ 2.2. |
| W-06 definition length | ≤40 words | ≤`40 × chars_per_token` characters |
| W-01 "substantive" paragraph floor | ~120 characters | Keep character-based; do **not** port an English word floor |

And the qualitative ones, stated plainly because they do not reduce to a number:

- **Content norms differ.** A German enterprise page or a Japanese B2B page will not
  carry the same explicit price that an English DTC page carries, and W-07 is not a
  defect there.
- **Attribution conventions differ.** Continental European B2B copy cites standards
  and papers inline rather than in footnotes; Japanese technical copy attributes by
  `著者名 (year)` rather than by quotation. W-03 should accept an attribution form,
  not require a `blockquote`.
- **Do not port English paragraph-length habits.** See
  [EXTRACTABILITY.md](references/EXTRACTABILITY.md), multilingual summary.
