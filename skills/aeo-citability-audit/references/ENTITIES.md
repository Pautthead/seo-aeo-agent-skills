# Entity-based optimisation

Entities are how a retrieval system decides *what your page is about* and *who you
are*. They are also the cheapest high-value fix in this audit.

Shepard scores entity consistency at **5.8/10** — eighteenth of 23. That is a modest
score from a rigorous source, and this reference file explains why the field data
disagrees with it, and what to do about that disagreement.

---

## E-01 — Consistent naming

**Rule.** **PASS** if the brand / product / person name is **byte-identical after
whitespace normalisation and case-insensitive comparison** across all four of:

1. `<title>`
2. `<h1>`
3. The first non-empty block of the main content
4. JSON-LD `Organization.name` / `Product.name` / `Person.name`, where present

Where an item is absent, it does not fail the check but is reported as a gap.

**Language-agnostic**, provided you compare the name as written. Note the one real
cross-language hazard: German compounds and Spanish/French stacked surnames can be
written with or without an internal space or hyphen, and an automatic normaliser that
collapses those will report a mismatch that is not one. Normalise whitespace and case;
do not normalise hyphens or apostrophes.

**Case-insensitivity is a deliberate compromise.** Shepard's underlying concern is
that the *same* entity is not represented by the *same string* everywhere — "Acme",
"ACME Corp", "Acme Corporation" and "Acme Corp." are four entities to a naive
knowledge graph. Case-only differences are a much weaker signal, and enforcing
byte-identical case would generate false findings on pages whose title casing is
merely typographic. So: case-insensitive comparison, whitespace-normalised, with
punctuation differences *reported but not failed*.

**What "materially higher in the field test" means.** In an underpowered 5-client field
test (n=5, the author flagged the sample as underpowered, and the source itself could not
be verified) entity-naming consistency surfaced as one of five factors that mattered in
practice but do not appear on Shepard's list. It was rated as cheap and underrated.

**Stronger position:** the field observation is a single small sample and cannot
override a 54-experiment scored study. The correct synthesis is that E-01 is *low
cost and low risk*, not that it is high impact. Do that work anyway — at an hour of
effort, an 18th-ranked factor is still worth an hour — but do not sell it as the big
win, and never cite the field test as if it were a measurement.

---

## E-02 — Topic cluster ranking · Shepard 8.9

The seventh-highest factor, and one of the few high-scoring factors that is
structurally in reach.

**Rule.** **PASS** if, within the internal link graph reachable from the audited page:

- ≥3 **outbound** links to pages sharing the page's topic stem, **and**
- ≥1 **inbound** link from a sibling page on that same stem.

**Topic stem derivation — language-agnostic.** Two acceptable derivations, both valid,
pick one and state which:

1. **URL-path derived** (recommended, works identically in every language): the
   directory segments of the audited URL. `/blog/magnesium-glycinate/dosage/` and
   `/blog/magnesium-glycinate/interactions/` share the stem `magnesium-glycinate`.
   This works for non-Latin scripts, for URLs with no slugs at all, and for sites
   with no directory structure — in the last case it returns zero and E-02 is N/A,
   reported as such.
2. **Heading-derived**: the `h1`/`h2` tokens excluding stopwords. Requires a
   per-language stopword list; only ship it for the languages you have stopwords for,
   otherwise **N/A**, never a fail.

Do not do English stemming or lemmatisation as part of this. It is unnecessary with
path-derived stems and actively wrong for morphologically rich languages where a
naive stemmer merges unrelated terms.

**Honest limit.** This check measures whether the cluster *structure* exists. It
cannot measure whether the cluster **ranks**, which is what the factor is actually
about. A well-built cluster of pages that rank nowhere fails the real test while
passing this one. Say so in the output: E-02 passing means "structure is not your
blocker", not "cluster ranking is healthy".

**Why clusters matter for AI retrieval specifically.** Retrieval fans out across a
topic rather than hitting one URL. A page surrounded by nine siblings that all
reinforce the same entity and the same terminology is a stronger retrieval candidate
than an orphan page with identical content. Cluster membership is also the cheapest
available signal you can build that tells a model what your site is authoritative
*about*.

---

## E-03 — Trust surface · Shepard 6.8

**Rule.** **PASS** if all three are present:

1. A **named author** with a credential or bio — a person's name and either a role,
   a qualification, or a linked author page.
2. An **About path reachable** from the audited page within one click, returning 200.
3. `Organization` or `Person` markup whose `name` matches the visible byline (E-01's
   consistency rule, applied here).

**Partial:** all three present = pass; two = report as fail with the missing item
named; one or zero = fail.

**Language-agnostic.** This is element and link counting plus a name comparison.

**Where this stops.** 6.8 is a middling score and it should stay middling. Shepard's
factor is about recognisable, attributable authorship — not about fame. Authority
you cannot see from one page: prior citations, mentions elsewhere, whether the named
author is known. Do not inflate this check into a proxy for domain authority (5.0) or
known-source status (5.4), both of which are out of scope.

**Do not fabricate authorship.** Google's 2026-10-01 AI-content guidance names
**effort, originality, talent/skill and accuracy** as the four dimensions of main
content quality, names mass-produced AI content as an example of "little to no
effort", and explicitly calls **fake authors deception**. If a page has no real author,
the correct finding is "add a real named author with a real bio", not "generate a
byline". This audit must never recommend inventing a person.

---

## E-04 — URL accessibility and preview control · Shepard 9.5 and 9.2

**Rule.** **PASS** only if all four hold:

1. Final HTTP status after redirects is **200**.
2. No authentication wall, paywall interstitial, or login redirect in the redirect
   chain.
3. Raw response body contains ≥200 characters of content.
4. Neither the HTML nor the response headers contain `nosnippet`, `nosnippetimg`,
   `max-snippet:0`, or a `<meta name="robots" content="… noarchive …">`.

**9.5 and 9.2 are the first and fourth highest factors in the list.** Both are
mechanical. Both are free to fix. If this audit finds nothing else, finding these is
still worth the run.

**On `nosnippet` specifically.** It is the fourth-highest factor and it is a factor
that *removes* you. High repeatability, high evidence, explicit official support —
which is why it scores 9.2: we know with confidence that `nosnippet` suppresses the
excerpt you would otherwise be quoted from. If an operator has deliberately set it,
report it as a finding with the cause stated and stop. Do not argue. Do not remove it
without permission.

**The bot-wall variant.** A Cloudflare / DataDome / PerimeterX challenge returns 200
with a challenge body — so check 1 passes, check 3 catches it if the body is thin, and
the honest report must call it what it is. A 200 that contains a challenge is not a
page. See X-07 in [EXTRACTABILITY.md](EXTRACTABILITY.md).

---

## E-05 — Freshness · Shepard 7.0

**Rule.** **PASS** if the page carries **both**:

1. A machine-readable date — JSON-LD `datePublished` and/or `dateModified`, or
   `<meta property="article:modified_time">`, or an OpenGraph `article:modified_time`.
2. A **human-visible** date in the content or byline, within the last 12 months.

**Both, deliberately.** A JSON-LD date with nothing visible is metadata; a visible
"Updated March 2026" with no machine-readable date is a claim. Corroborated by arXiv
2605.25517 (252,000 trials, 6 LLMs): **a recent timestamp helps consistently** — it
was one of only two signals besides explicit price information to help across every
model tested. That consistency is why E-05 requires the visible half and W-07 counts
it again: the machine-readable half feeds retrieval, the visible half feeds quotation.

**Language-agnostic.** Date parsing needs to accept the formats actually used in the
page's locale — `2026-04-17`, `17/04/2026`, `17.04.2026`, `2026年4月17日`,
`April 17, 2026`. Parse relative dates ("3 days ago") too, but log them as relative:
they are un-verifiable and disappear.

**The failure worth flagging hardest:** a page with a fresh machine-readable date and
a body that has not been touched in two years. That is a false freshness signal aimed
at crawlers rather than readers, and it is the kind of thing a synthesized answer
notices.

---

## The extractability principle that binds this file together

**Entity-optimised content tends to become entity-bloated content.**

The failure sequence:

1. Someone reads that entity clarity matters (5.8) and topical authority matters (8.9).
2. They add the brand name 40 times, restate the product name in every heading, and
   bolt a "Best X for Y" cluster around the page.
3. Prose stops reading as prose. Sentences become noun stacks. The page now has
   entities but few quotable statements.
4. X-05 self-containment drops, because blocks are now full of repeated names with no
   predicate. W-01 drops, because the added words are names, not facts.
5. The page is worse at being cited than before, and worse at being read.

The trap is that this *looks* like progress on an entity dashboard. Entity density is
easy to measure, so it gets measured, and the measurement rewards exactly the wrong
thing.

**The rule that prevents it:** entity consistency is about the *same name being used
everywhere it appears*. It is not about appearing more often. E-01 checks identity
across four surfaces — a page can pass it by being consistent about a name it uses six
times, which is plenty.

**Two tests before recommending any entity change:**

- Would a reader notice the repetition? If yes, it is bloat.
- Does the added sentence contain a fact? If no, it is bloat.

**Related:** long-tail entity-stuffed phrasing is also the shape that reads as
machine-generated. Jochen Madler (Sitefire), *"SlopShape: Identifying AI-Generated
Commercial Web Content"*, `https://arxiv.org/abs/2609.15369` (2026-09) detects AI-generated
commercial posts from **structure alone, at 97.0 macro-F1 on held-out companies**. That is
a macro-averaged F1 score, not a share of pages classified correctly. Entity stuffing is
one of the most reliable structural tells there is. This is the empirical reason not
to let an entity-optimisation pass run unsupervised.

---

## Summary table

| ID | Check | Shepard | Keyless | Language notes |
|---|---|---|---|---|
| E-01 | Name identical in title / h1 / first block / schema | 5.8* | yes | Case-insensitive, whitespace-normalised; do not normalise hyphens |
| E-02 | Topic cluster: ≥3 out, ≥1 in, on topic stem | 8.9 | partial | Path-derived stems preferred; stemming is unnecessary and harmful |
| E-03 | Trust surface: author, About, matching markup | 6.8 | partial | No lexical dependence |
| E-04 | 200, no auth wall, ≥200 chars, no `nosnippet` | 9.5 / 9.2 | yes | No lexical dependence |
| E-05 | Machine-readable **and** visible recent date | 7.0 | yes | Locale-aware date parsing |

\* Shepard 5.8; rated materially more important in an underpowered 5-client field
test. Cheap and low-risk either way. Full caveat in
[LIMITS.md](LIMITS.md).
