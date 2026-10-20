# Crawler user-agent catalogue

Exact token strings, vendors, purpose class, and the recommended verdict. Every token here is matched **case-insensitively** on the `User-Agent` request header, and in `robots.txt` `User-agent:` lines.

> ### ⚠️ Which strings here are actually vendor-published
>
> **Two of the four vendors in this file publish exact User-Agent strings. Two do not.**
> OpenAI and Perplexity publish them. **Anthropic publishes none**, and Google and Microsoft
> publish token documentation rather than full headers. Each vendor block below is labelled
> accordingly, and the "Sources and confidence" table at the foot of this file carries the
> same distinction. Where a string is marked **OBSERVED**, it was assembled from crawls and
> third-party directories that **actively disagree with each other** — treat it as a
> placeholder, not a citation-grade fact.
>
> **The version component is not stable anywhere.** OpenAI states plainly that *"the version
> number may change."* **Match the token substring, not the frozen string** — `-A 'GPTBot'`,
> not `-A 'Mozilla/5.0 … GPTBot/1.4 …'`. A curl command carrying a stale version is a
> copy-pasteable defect that will look authoritative to whoever runs it.

---

> ## ⚠️ Read this before you copy any table
>
> **The #1 documented practitioner error in AI-search SEO is conflating a training crawler with a retrieval crawler.** It is not a subtle distinction. `GPTBot` and `OAI-SearchBot` are operated by the same company, run in the same infrastructure, and do completely different things. Blocking one does not block the other. Allowing one does not allow the other. Same for `ClaudeBot` / `Claude-SearchBot` / `Claude-User`.
>
> There is **no professional consensus** on whether to allow training crawls, and at least one widely-copied 2026 "AI crawler table" is simply wrong — it claims `GPTBot` powers ChatGPT Search, which contradicts OpenAI's own published documentation. If a source you are copying claims that, discard the source.
>
> **This catalogue's default recommendation is block-training / allow-retrieval.** It costs no citation surface under any vendor's published documentation, and it is the only position that cannot hurt you. It is a recommendation, not a finding: the decision belongs to the site owner, and this repo does not deduct points for it either way.

---

## Purpose classes — the organising principle

Sort every token into exactly one class before writing any rule.

| Class | What it does | If you block it | If you allow it |
|---|---|---|---|
| **T — Training** | Fetches content for model training. No citation, no ranking, no index entry. | Nothing in your AI visibility changes. You lose nothing. | Nothing in your AI visibility changes. Your content enters a training corpus. |
| **R — Retrieval index** | Fetches and stores your page so an AI answer engine *can retrieve and cite* it. | **You disappear from that engine's answers.** This is the only class that determines citations. | You become eligible to be cited. |
| **U — User-requested** | Fetches a URL because a human typed it into a chat. Often not indexed. | The user who asked gets an error inside the chat window. It is not invisible — it is visible and bad. | The user gets a real answer citing your live page. Highest-quality signal available to you. |
| **S — Search index** | Classical search crawler. Also feeds AI Overviews, AI Mode and Copilot on several engines. | You lose both search rankings and AI answers. Never block these to control AI visibility. | Search and AI visibility both flow. |
| **G — Agentic** | Fetches during a live agent run, as a tool call, mid-task. | Agents cannot complete tasks that need your page. Broken tool use, not a soft penalty. | Agents complete tasks and may attribute the answer to you. |

**The rule that follows from the table:** blocking a **T** token is a content-protection decision with zero visibility cost. Blocking an **R**, **U**, **S** or **G** token is a *deliberate exit from that engine*, and it should be made consciously or not at all.

---

## OpenAI

| Token | Class | Vendor docs say | Verdict |
|---|---|---|---|
| `GPTBot` | **T** | Collects training data to improve generative AI foundation models. Does not power ChatGPT Search. | **Block** (recommended default) |
| `OAI-SearchBot` | **R** | ChatGPT's search crawler. Links from ChatGPT search results to the sites it cites. | **Allow — mandatory** |
| `ChatGPT-User` | **U** | User action. Fetches a link the user asked ChatGPT to visit, not an automatic crawl. | **Allow — mandatory** |
| `OAI-AdsBot` | — | OpenAI's advertising crawler for ad-related surfaces. Not a retrieval or citation crawler. | **Either** — allow if you run OpenAI-platform ads, block otherwise |

UA strings **as published by OpenAI** in its crawler documentation
(`https://platform.openai.com/docs/bots`; the `openai.com/searchbot`, `/gptbot` and `/bot`
pages all resolve to that same document). Copied 2026-10-19:

```
GPTBot:        Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot
OAI-SearchBot: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot
ChatGPT-User:  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot
OAI-AdsBot:    Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-AdsBot/1.0; +https://openai.com/adsbot
```

> OpenAI's documentation states explicitly that **"the version number may change."** The
> `/1.4` on `GPTBot` and `OAI-SearchBot` is the current published value, not a frozen fact.
> **Match the token substring, not the string** — `-A 'GPTBot'`, not the full header. Verify
> against `https://platform.openai.com/docs/bots` before quoting a version in a report.
>
> OpenAI also documents a variant of `OAI-SearchBot` with an added `robots.txt;` marker used
> for `robots.txt` fetches. Expect to see it in logs.

---

## Anthropic

| Token | Class | Purpose | Verdict |
|---|---|---|---|
| `ClaudeBot` | **T** | Training. | **Block** (recommended default) |
| `Claude-SearchBot` | **R** | Claude's search index — **the token that produces Claude citations**. | **Allow — mandatory** |
| `Claude-User` | **U** | Fetches a URL a user asked Claude to visit. | **Allow — mandatory** |
| `claude-code` | **G** | Claude Code, fetching during an agent run. Observed in the wild (e.g. `claude-code/2.1.131 (cli)`). | **Allow** — agents cannot complete a task without your page |

**OBSERVED strings — NOT vendor-published.**

Anthropic documents exactly three bots (`ClaudeBot`, `Claude-User`, `Claude-SearchBot`) in
its crawler support article (updated 2026-04-07, also served from `support.claude.com`), with
purpose, robots.txt examples, `Crawl-delay` support and an IP-range list. **It does not print
a single full User-Agent header.** The strings below are what crawls and third-party
directories report, and those directories **disagree with each other** — on the base string,
and on whether `Claude-SearchBot` ends in an email address or a URL (one commonly cited
verification URL, `anthropic.com/claudesearchbot`, returns 404):

```
ClaudeBot:        Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)
Claude-SearchBot: Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)
Claude-User:      Mozilla/5.0 (compatible; Claude-User/1.0; +claudebot@anthropic.com)
```

> ### ⚠️ A User-Agent header is a claim anyone can make
>
> The older version of this file said that all three tokens "share the verification address
> `claudebot@anthropic.com`", and that adding that address to an allowlist "proves it's
> Anthropic." **Both claims are withdrawn.** An email address in a UA header is not
> authentication, and since the vendor publishes no string at all, there is nothing to verify
> the address against. This applies to the **whole string**, not just the address: matching
> `claudebot@anthropic.com`, or the parenthesised base string, or any particular version
> component proves nothing about who sent the request.
>
> **The correct verification method is the published IP list**, not the UA string:
> `https://claude.com/crawling/bots.json`. Verify the request's source IP against Anthropic's
> ranges before treating it as Anthropic traffic.
>
> **Still match on the token substring for a `robots.txt` rule** — a robots directive is a
> request to well-behaved crawlers, and matching `Claude-SearchBot` is what makes that request
> reach the real crawler. Match the substring; do not treat the string as proof of identity.

`ClaudeBot` is the highest-volume fetcher of any un-announced file type in the measured literature (Hall, 2026-09-17: 1,131 of 1,549 `llms.txt` fetches). That is a statement about training crawlers being thorough. It is **not** evidence that Claude cites those pages.

---

## Google

| Token | Class | Purpose | Verdict |
|---|---|---|---|
| `Googlebot` | **S** | Google Search index. Also the source for AI Overviews and AI Mode. | **Allow — never block** |
| `Google-Agent` | **G** | Fetches during AI Mode agentic runs. | **Allow** |
| `Google-Extended` | **T** | Governs use for Gemini Apps training and Vertex AI grounding/retrieval. **Explicitly does not affect inclusion in Google Search**, and therefore does not affect AI Overviews or AI Mode eligibility. | **Either** — see caveat below |
| `Google-CloudVertexBot` | **R** | Retrieval for Vertex AI RAG grounding. | **Allow** if you want Vertex-grounded answers citing you |
| `GoogleOther` | **S** | Unclassified Google fetcher. | **Allow** |
| `Google-Read-Aloud` | **U** | Read-aloud / voice surfacing. | **Allow** |
| `Google-PageRenderer` | **—** | JS rendering, not a user-facing crawler. | **Allow** |
| `AdsBot-Google` | **—** | Google Ads crawler. Not AI. | Allow if you run ads |

Google publishes full user-agent strings for most of its crawlers. Copy them, or match
the token substring. Two tokens are exceptions and are marked below.

```
Googlebot:              Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
Google-Agent (mobile):  Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Google-Agent; +https://developers.google.com/crawling/docs/crawlers-fetchers/google-agent)
Google-Agent (desktop): Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Google-Agent; +https://developers.google.com/crawling/docs/crawlers-fetchers/google-agent) Chrome/W.X.Y.Z Safari/537.36
Google-Extended:        (no separate UA string - robots.txt control token only)
Google-CloudVertexBot:  match the token substring; verify the full string before quoting it
GoogleOther:            Mozilla/5.0 (compatible; GoogleOther)
Google-Read-Aloud:      match the token substring; the Chrome version in its UA changes over time
```

> **`Google-Agent` has no version number.** Google's published strings carry the bare
> token, `Google-Agent`, plus a verification URL. A string like `Google-Agent/1.0` is
> not Google's and will not appear in their documentation. Do not invent a version.
>
> **`Google-Extended` has no UA of its own.** In Google's words: *"Google-Extended
> doesn't have a separate HTTP request user agent string. Crawling is done with existing
> Google user agent strings; the robots.txt user-agent token is used in a control
> capacity."* Do not test it by sending a dedicated UA — test the robots.txt control.
>
> **`Google-PageRenderer` is not in Google's current crawler documentation.** Treat any
> string circulated for it as legacy and unverified.

> ### ⚠️ `Google-Extended` — a genuine judgement call, flagged as such
>
> Google's own documentation states `Google-Extended` does **not** affect Google Search inclusion. But its documentation has historically grouped Vertex AI / Gemini API *grounding* (which is retrieval, and does surface citations) alongside Gemini Apps *training* under the same token. If your business depends on being grounded in Vertex AI or the Gemini API, `Google-Extended` is a retrieval decision, not a training decision, and blocking it is not free.
>
> **Test it rather than guess it.** Check your own access logs for `Google-Extended` and see what request volume and paths appear. If the volume is zero, the decision is free and you can block. If it is non-zero, treat it as class **R** and allow. This skill does not score this token either way — see Rule 10 in SKILL.md.

---

## Microsoft

| Token | Class | Purpose | Verdict |
|---|---|---|---|
| `Bingbot` | **S** | Bing index. Microsoft states Bingbot also feeds Bing Chat and Copilot answers. | **Allow — never block** |
| `msnbot` | **S** | Legacy MSN/Bing crawler, same vendor. | **Allow** |

```
Bingbot: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
msnbot:  Mozilla/5.0 (compatible; msnbot/2.0b; +http://search.msn.com/msnbot.htm)
```

If you see a token like `Copilot` or `bingbot` used for answer retrieval on a specific surface, confirm against your logs — Microsoft has shipped these under the `bingbot` umbrella, which is the practical behaviour that matters for a `robots.txt` decision.

---

## Perplexity

| Token | Class | Purpose | Verdict |
|---|---|---|---|
| `PerplexityBot` | **R** | Perplexity's search index. Source of its citations. | **Allow — mandatory** |
| `Perplexity-User` | **U** | User-initiated fetch. ⚠️ Perplexity documents this as user-requested, but it can still appear in cited answer sources. Treat blocking it as an **R-class** risk, not a free win. | **Allow** |

UA strings **as published by Perplexity** in `https://docs.perplexity.ai/guides/bots`,
copied 2026-10-19. Note that Perplexity's own `PerplexityBot` string contains an
**unbalanced parenthesis** — `(KHTML, like Gecko;`. Copy it verbatim or it will not match:

```
PerplexityBot:  Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)
Perplexity-User: Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)
```

**The two tokens carry different verification addresses.** `PerplexityBot` is
`https://perplexity.ai/perplexitybot`; `Perplexity-User` is
`https://perplexity.ai/perplexity-user`. An earlier version of this file claimed both carried
`/perplexitybot`; that was wrong.

As with every other vendor, a UA header is a claim anyone can make — the embedded address is
not authentication. Perplexity is the clearest case in the catalogue of a **U** token that
still deserves citation weight — classify by observed behaviour in your logs, not by the label.

---

## Other retrieval / search engines

| Token | Vendor | Class | Purpose | Verdict |
|---|---|---|---|---|
| `YouBot` | You.com | **R** | You.com search index, cited in answers. | **Allow** |
| `DuckAssistBot` | DuckDuckGo | **R** | DuckDuckGo AI Answers specifically. **Not** the general search index (that is `DuckDuckBot`). | **Allow** |
| `MistralAI-User` | Mistral | **U** | User-requested fetch when someone asks Le Chat to visit a URL. | **Allow** |
| `Applebot` | Apple | **S** | Apple Search / Siri Suggestions indexing. | **Allow** |
| `Bravebot` | Brave | **S** | Brave Search index; Brave Leo answers. | **Allow** |
| `Meta-ExternalAgent` | Meta | **T** | AI training / discovery. | **Block** |
| `Amazonbot` | Amazon | **T** | Amazon training and discovery. | **Either** — it also has a shopping index function. |

```
YouBot:          YouBot            (verification page about.you.com/youbot/ returned 404 on 2026-10-20 - full string unverified)
DuckAssistBot:   DuckAssistBot/1.0; +http://duckduckgo.com/duckduckbot.html
MistralAI-User:  MistralAI-User    (no published string located - token only)
Applebot:        Mozilla/5.0 (compatible; Applebot/0.1; +http://www.apple.com/go/applebot)
```

---

## Training-only crawlers — recommended verdict: block

All class **T**. None of these produce citations. Blocking them costs you nothing under any vendor's published documentation and is the recommended default.

| Token | Vendor / owner | What it collects | Verdict |
|---|---|---|---|
| `CCBot` | Common Crawl | Backs nearly every LLM training corpus. Widely considered the highest-impact training pipeline on the web. | **Block** |
| `Bytespider` | ByteDance | Bulk training crawl. Aggressive, high volume, widely reported as ignoring rate signals. | **Block** |
| `Meta-ExternalAgent` | Meta | Meta AI crawler. Also honours `Meta-ExternalAgent` allowlisting for verified use. | **Block** |
| `Applebot-Extended` | Apple | Apple Intelligence training. **Distinct from `Applebot`** — blocking this does not affect Apple Search indexing. | **Block** |
| `DeepSeekBot` | DeepSeek | Training. | **Block** |
| `cohere-ai` | Cohere | Training. Token is lowercase in the wild; matching is case-insensitive. | **Block** |
| `omgili` | Meltwater / Omniglot | Training and dataset licensing. | **Block** |
| `AI2Bot` | Allen Institute for AI | Research crawl. | **Either** |
| `Timpibot` | Timpibot | Third-party training proxy. | **Block** |
| `Webzio-Extended` | Webzio | Third-party extended crawler. | **Block** |
| `Diffbot` | Diffbot | Knowledge-graph extraction, not training per se — but it republishes your structured content commercially. | **Your call** |

```
CCBot:              Mozilla/5.0 (compatible; CCBot/2.0; https://commoncrawl.org/faq/)
Bytespider:         Mozilla/5.0 (compatible; Bytespider; spider-feedback@bytedance.com)
Meta-ExternalAgent: meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)
Applebot-Extended:  Mozilla/5.0 (compatible; Applebot-Extended/1.0)
DeepSeekBot:        Mozilla/5.0 (compatible; DeepSeekBot/1.0; +https://www.deepseek.com)
cohere-ai:          cohere-ai
omgili:             omgilibot
Amazonbot:          Amazonbot/0.1; +https://developer.amazon.com/amazonbot
```

> Blocking a training crawler does **not** reliably block every route your content takes into a training corpus — only the named token is governed. It reduces exposure; it does not establish a legal or contractual position. Do not describe it as the latter to a client.

---

## Verdict matrix — the working default

```yaml
# Retrieval / user / agentic / search — allow all of these.
User-agent: OAI-SearchBot      → Allow
User-agent: ChatGPT-User       → Allow
User-agent: Claude-SearchBot   → Allow
User-agent: Claude-User        → Allow
User-agent: Googlebot          → Allow
User-agent: Google-Agent       → Allow
User-agent: Google-CloudVertexBot → Allow
User-agent: PerplexityBot      → Allow
User-agent: Perplexity-User    → Allow
User-agent: Bingbot            → Allow
User-agent: YouBot             → Allow
User-agent: DuckAssistBot      → Allow
User-agent: MistralAI-User     → Allow
User-agent: Applebot           → Allow
User-agent: Bravebot           → Allow

# Training — the recommended default, and the user's decision to make.
User-agent: GPTBot             → Disallow
User-agent: ClaudeBot          → Disallow
User-agent: CCBot              → Disallow
User-agent: Bytespider         → Disallow
User-agent: Meta-ExternalAgent → Disallow
User-agent: Applebot-Extended  → Disallow
User-agent: DeepSeekBot        → Disallow
User-agent: cohere-ai          → Disallow
User-agent: omgili             → Disallow
```

Explicit allowlines for the retrieval bots are **not required** if no `Disallow` applies to them — a token absent from robots.txt is allowed by default. They are worth writing anyway: they are documentation, they survive a later bad edit, and they make the intent reviewable.

**Group matching follows RFC 9309.** A group matches when its product token matches the crawler's user-agent, case-insensitively. Several matching groups are merged. Order does not matter, and a specific group does not have to follow `User-agent: *`. The `*` group applies only when no product token matched. Inside a matched group, the most specific **path** wins (longest path; equal length, Allow wins). Google's extra "longest matching user-agent token" behaviour is Google-specific. It is not the RFC 9309 rule. Do not require an allow to come after `*`, and do not say the longest token wins.

## Sources and confidence

| Entry | Source | Date | Confidence |
|---|---|---|---|
| OpenAI tokens | OpenAI crawler documentation — `https://platform.openai.com/docs/bots` | vendor, current | vendor-documented |
| OpenAI UA strings | Same page, copied 2026-10-19. Vendor states the version number may change. | 2026-10-19 | vendor-published; version drifts |
| Anthropic tokens | `anthropic.com` / `support.claude.com` crawler documentation | vendor, current | **vendor-documented tokens** |
| Anthropic UA strings | **Not published by the vendor.** Assembled from crawls and third-party directories that disagree. | — | **OBSERVED, unverified; version drift expected** |
| Anthropic identity check | Published IP list — `https://claude.com/crawling/bots.json` | vendor, current | **This is the verification method, not the UA string** |
| Google tokens | Google Search Central crawling documentation | vendor, current | vendor-documented tokens |
| Google UA strings | Google publishes full strings for most crawlers (Google section above). Exceptions: `Google-Extended` has no UA; the Chrome version in `Google-Agent` is the placeholder `W.X.Y.Z` | vendor page | vendor-published, with those exceptions |
| Perplexity tokens | Perplexity crawler documentation — `https://docs.perplexity.ai/guides/bots` | vendor, current | vendor-documented |
| Perplexity UA strings | Same page, copied 2026-10-19 | 2026-10-19 | vendor-published (note the unbalanced parenthesis) |
| Bingbot feeds Copilot | Microsoft Bing Webmaster documentation | vendor, current | vendor claim, not independently measured |
| Training-crawl verdict | No consensus. Recommendation in this file is a judgement call, stated as one. | — | **judgement, not evidence** |
| "GPTBot powers ChatGPT Search" | **False.** Contradicts OpenAI's own docs. | — | known-bad source; discard any table repeating it |
