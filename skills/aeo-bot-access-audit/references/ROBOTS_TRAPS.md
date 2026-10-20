# robots.txt traps — four documented failure modes

Each entry: the failure, why it is hard to see, a **detection procedure** you can run, and the **fix**.

The organising fact: **a clean robots.txt proves nothing on its own.** Cloudflare, Akamai and AWS WAF enforce their rules *before* the origin ever parses a robots file. Trap (d) is the one that catches experienced teams.

---

## Trap 1 — `User-agent: *` + `Disallow: /` silently killing every unlisted agent

### The failure

```text
User-agent: *
Disallow: /

User-agent: Googlebot
Disallow: /admin/
```

The wildcard group does not "fall through" to the Googlebot group for unlisted paths. Result: **Googlebot, Bingbot and every named bot are blocked from `/`**, while the site looks correctly configured at a glance because the well-known bots have their own groups lower down. Classic late-stage private staging protection that shipped.

The variant that looks correct and is not:

```text
User-agent: OAI-SearchBot
Allow: /

User-agent: *
Disallow:
```

This one is fine. The failure is specifically a wildcard **`Disallow: /`** combined with reliance on named groups to carve out an exception that only covers some paths.

### Why it is hard to see

It is not an error. `robots.txt` has no concept of an error. The file returns 200, every group is syntactically valid, and every SEO tool reports the named bots as "allowed". The site just disappears from every engine that is not explicitly carved out — and since `Googlebot` is usually carved out for `/admin/` only, the search consequence appears first as "we lost rankings last week" with no visible cause.

### Detection procedure

```bash
# Fetch and inspect group structure. Count wildcard disallows at the root.
curl -sSL https://example.com/robots.txt -o robots.txt

# Every User-agent line, in order:
grep -n -i '^user-agent' robots.txt

# Every root-level wildcard block:
grep -n -i -A3 '^user-agent:[[:space:]]*\*' robots.txt
```

Deterministic rule the agent applies:

> If the file contains a `User-agent: *` group whose rule set includes `Disallow: /` (or `Disallow: /` with a trailing wildcard), that group applies to **every** bot not named in another group that has a longer, more specific match. Report **CRITICAL** if any citation-class bot (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot`, `Bingbot`) is not explicitly allowed at the root.

Also check the **other** order, which is just as common and just as fatal:

```bash
# Does a wildcard disallow of "/" appear in ANY group, wildcard or not?
grep -n -iE '^\s*disallow:\s*/\s*$' robots.txt
```

### Fix

Remove the wildcard root disallow. If the intent was to protect a staging environment, host it on a different hostname with HTTP Basic auth — not a robots rule, which is not access control.

```text
User-agent: *
Disallow: /admin/
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

User-agent: Googlebot
Disallow: /admin/

User-agent: OAI-SearchBot
Disallow: /admin/

User-agent: Claude-SearchBot
Disallow: /admin/
```

**Verify:** re-run the edge test from `EDGE_VERIFICATION.md` for each citation-class bot on two or three root-level URLs. Every one must return `200`.

---

## Trap 2 — blocking `/assets/`, `/wp-content/`, `/static/` — HTML renders, content does not

### The failure

```text
User-agent: ClaudeBot
Disallow: /
Disallow: /assets/
```

or more subtly, a CMS-generated rule:

```text
User-agent: *
Disallow: /wp-content/
```

### Why it is the worst of the four

**It does not look like a block.** The bot gets a 200. The HTML arrives. But the CSS, JS and images under the blocked path do not, and the page renders as unstyled source — or, if the framework is client-side rendered, as a near-empty shell with the body text injected by a bundle that never loaded.

This is the classic silent, catastrophic failure. It scores fine on every accessibility checker, produces no error in any log worth reading, and the page is in the index with the answer text simply absent. It directly attacks Shepard's factor 14, content visibility in HTML, at 7.6 — while appearing to address factor 1 at 9.5.

A quieter variant: blocking only `/assets/css/` and `/assets/js/` while allowing images. The page looks nearly fine in a screenshot review and the content layer is still dead.

### Detection procedure

```bash
# 1. Does robots.txt block a render-critical path?
grep -n -iE 'disallow:.*(/assets/|/static/|/wp-content/|/wp-admin/|/media/|/css/|/js/|/_next/|/dist/)' robots.txt

# 2. Does the page's HTML reference assets under a blocked prefix?
curl -sSL -A 'Claude-SearchBot' https://example.com/pricing \
  | grep -oE '(src|href)="[^"]+"' \
  | grep -E '/(assets|static|wp-content|_next|dist)/' \
  | sort -u
```

Cross-reference the two outputs. **Any asset URL emitted by the page under a prefix disallowed in robots.txt is a finding.**

3. Cheap behavioural check — does the served HTML contain the answer text, or only a mount point?

```bash
# Count the real prose versus the JS shell.
curl -sSL -A 'Claude-SearchBot' https://example.com/pricing | wc -c
curl -sSL -A 'Mozilla/5.0'    https://example.com/pricing | wc -c
```

If the bot-fetched body is dramatically smaller than the browser-fetched body, the content is being assembled client-side and the bot receives a shell. Both sizes being small is a separate content problem. This comparison is a heuristic, not a proof — confirm with the asset cross-reference above.

### Fix

Allow all render-critical paths for retrieval bots:

```text
User-agent: Claude-SearchBot
Disallow: /admin/
Allow: /

User-agent: OAI-SearchBot
Disallow: /admin/
Allow: /
```

If you want to block training crawlers while letting them fetch assets, you do not need to — blocking them is not a privacy mechanism, and there is no rendering benefit to letting them through partially. Block them entirely or not at all.

**Verify:** the asset cross-reference above returns zero URLs under a disallowed prefix, and the bot-fetched body byte count is within roughly 10% of the browser-fetched body.

---

## Trap 3 — confusing `ClaudeBot` with `Claude-SearchBot`, or `GPTBot` with `OAI-SearchBot`

### The failure

Three distinct mistakes, all common:

**(a) Blocking the wrong token.** Blocking `GPTBot` to keep content out of OpenAI training, and believing ChatGPT Search is now also excluded. It is not. `OAI-SearchBot` is untouched, still fetches, still cites. The intended privacy outcome fails and the intended visibility outcome is unaffected — the worst of both worlds. Identically for `ClaudeBot` / `Claude-SearchBot`.

**(b) Allowing the wrong token and hoping.** Allowing `GPTBot` and `ClaudeBot` because "we want to be in AI answers", without adding `OAI-SearchBot` and `Claude-SearchBot`. This *accidentally* works — retrieval tokens are allowed by default when unlisted — which is exactly why the mistake persists uncaught. The site gets citations for the wrong reason, and nobody notices the file is wrong until a future edit fixes one group and breaks the other.

**(c) A published table that is simply wrong.** There is no professional consensus on the training-crawl decision, and at least one widely-copied 2026 crawler table claims `GPTBot` powers ChatGPT Search. That claim contradicts OpenAI's own documentation. Any table containing it is wrong and should be discarded, not merged.

### Why it is hard to see

None of these produce an error. The bot that matters keeps fetching, so nothing breaks — the mistake is only visible in what you *intended*, and only once you read the file with the catalogue in hand.

### Detection procedure

```bash
# Which citation-class tokens are named at all in robots.txt?
for t in GPTBot OAI-SearchBot ChatGPT-User ClaudeBot Claude-SearchBot Claude-User \
         PerplexityBot Perplexity-User Googlebot Google-Agent Bingbot; do
  printf '%-20s ' "$t"
  grep -qi "^user-agent:[[:space:]]*$t\$" robots.txt && echo "named" || echo "not named"
done
```

Then apply the classification rule from `CRAWLERS.md`:

| Finding | Class | Rule |
|---|---|---|
| `GPTBot` disallowed, `OAI-SearchBot` absent | T blocked, R allowed | Privacy goal met. Working as intended. Report as a **confirmed correct configuration**. |
| `GPTBot` **allowed**, `OAI-SearchBot` absent | T allowed, R allowed | Coincidentally correct for citations. Flag: the reason is wrong, and the file invites a future edit that fixes the visible group and breaks the invisible one. **MAJOR — write the explicit allow.** |
| `ClaudeBot` disallowed, `Claude-SearchBot` absent | T blocked, R allowed | Correct. Report as confirmed. |
| `ClaudeBot` allowed, `Claude-SearchBot` absent | T allowed, R allowed | Same as the GPTBot case above. **MAJOR.** |
| Any citation-class token disallowed | R blocked | **CRITICAL.** The site has chosen to exit that engine. Spell out the consequence. |

The check that catches the worst version of this bug is not in robots.txt at all:

```bash
# What did the retrieval bot actually request, and with what result?
curl -sS -o /dev/null -w '%{http_code}\n' \
  -A 'Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)' \
  https://example.com/pricing
```

### Fix

Write the retrieval tokens explicitly, even though they are allowed by default. Explicit allowlines are self-documenting and survive the next bad edit:

```text
# Retrieval — needed for citations. Explicit even though the default allows.
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Training — the site's choice, documented as such.
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /
```

### What to say to a client who wants "no training, but still cite me"

That posture is coherent and achievable — it is exactly the block-training / allow-retrieval default in `CRAWLERS.md`. Deliver it, state plainly that it is a **traffic and content-protection decision with no expected citation cost** under any vendor's published documentation, and state the limits honestly: blocking a named token governs that token only, does not bind other crawlers, and is not a legal position. Do not let "block training" drift into "block AI" in the same conversation — those are different outcomes and the second one costs citations.

---

## Trap 4 — WAF/edge blocking wins over robots.txt

### The failure

The robots.txt is perfect. Every retrieval bot is explicitly allowed. And no AI bot can read a single page, because Cloudflare Bot Management, an Akamai bot manager rule, or an AWS WAF rate rule is challenging or denying the request at the edge — **before** the origin ever parses a robots file.

```text
robots.txt says:  User-agent: Claude-SearchBot → Allow: /
edge says:        403 · cf-mitigated: challenge
```

**robots.txt is a request for politeness, not an access control.** It is fetched by the crawler over the same connection, through the same WAF, subject to the same rules as the page. A challenge rule does not "respect" your robots.txt, because at the moment the challenge fires there is no page context in which a robots file has been read.

Common sources of edge blocking that nobody remembers installing:

- A "block AI scrapers" Cloudflare WAF rule added during a scraping incident and never revisited.
- Bot Management set to **Block** for the "AI Scrapers / Crawlers" category — a one-click toggle that applies to the entire zone, including your own crawler's paths.
- An Akamai bot manager rule, or an AWS WAF rate-based rule with a threshold that a well-behaved crawler exceeds.
- A geo-fence or IP allowlist added for another purpose.
- Mobile-only or authenticated-only rules on the CDN configuration.

### Why it is hard to see

**This is the trap that makes the other three survivable, because it invalidates the usual verification method entirely.** The standard practitioner check is "fetch robots.txt, confirm it looks right, done" — and that check passes. It proves only that `/robots.txt` was served. It proves nothing about whether `/pricing` was served to the bot. Report a clean robots.txt as a clean audit and you will have missed the single most expensive finding available, on the factor Shepard scores highest of all 23.

### Detection procedure

Never conclude from robots.txt. Test each URL, with each bot's exact token.

```bash
curl -sS -o /dev/null -D - \
  -A 'Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)' \
  https://example.com/pricing
```

**The verification command, in one line per bot:**

```bash
for u in 'Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)' \
         'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot' \
         'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' \
         'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)' \
         'Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)'; do
  printf '%s → ' "${u:0:40}"
  curl -sS -o /dev/null -w '%{http_code}\n' -A "$u" https://example.com/pricing
done
```

Compare against a baseline — the same URL with a plain browser UA:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' -A 'Mozilla/5.0' https://example.com/pricing
```

**Interpretation, in order:**

1. Browser `200` + bot `403` / `401` / `429` / `503` / challenge body → **edge is blocking the bot. CRITICAL.** robots.txt is irrelevant; it was never consulted.
2. Browser `200` + bot `200` → pass, for this bot from this network. See the caveat below before calling the site open.
3. Bot `200` but with a challenge or interstitial body → see the "Just a moment" detection in `EDGE_VERIFICATION.md`. **This is a fail.**

Status codes, header discriminators and per-vendor detection are in [`EDGE_VERIFICATION.md`](EDGE_VERIFICATION.md) — read it before writing the finding.

### Fix

Find the rule, don't guess at it. In order of likelihood:

- **Cloudflare** — dashboard → Security → WAF → Custom Rules, then Security → Bots. Look for rules matching AI bot user-agents, and for the Bots "AI Scrapers / Crawlers" category override. Fix by adding a `Skip` for the security products on the verification rules that carry the retrieval bots, or by excluding the known AI bot UAs from the blocking rule. Do **not** disable Bot Management globally.
- **Akamai** — bot manager rules on the security policy attached to the hostname.
- **AWS WAF** — Web ACLs and rules associated with the CloudFront distribution or the ALB; check rate-based rules and the `AWSManagedRulesCommonRuleSet` bot-control sub-list.
- **CDN default** — check whether the CDN has a "block non-verified bots" or "verified bot only" setting enabled.

Then re-run the verification command above. The pass condition is unchanged and is not negotiable: **every citation-class bot, every audited URL, HTTP 200 with real content in the body.**

### The caveat this trap cannot fully resolve

A `200` from your laptop is evidence, not proof. Bot Management scoring, IP reputation, ASN and geo all change what a request receives, and a real crawler arrives from a different network than you do. Before reporting an edge block as definitive, repeat the fetch from a **second network** — ideally a datacenter IP, since that is what real crawlers use. If you cannot, say so in the report rather than letting "200 from my IP" stand as "open". Server logs are the only ground truth: search them for `OAI-SearchBot` and `Claude-SearchBot` as distinct tokens over the last 30 days and read the status codes. If the retrieval tokens do not appear in the logs at all while other bots do, the edge is dropping them before the origin ever sees them — which is the strongest possible confirmation, and requires no further argument.
