# Crawler user-agent catalogue

Exact token strings, vendors, purpose class, and the recommended verdict. Every token here is matched **case-insensitively** on the `User-Agent` request header, and in `robots.txt` `User-agent:` lines.

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

Exact UA strings as published by OpenAI:

```
GPTBot:        Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.2; +https://openai.com/gptbot
OAI-SearchBot: Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot
ChatGPT-User:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot
```

> The version component (`/1.0`, `/1.2`) will drift. **Match on the token substring only** — `-A 'GPTBot'`, not the full frozen string. Verify against the live vendor page before quoting a version in a report.

---

## Anthropic

| Token | Class | Purpose | Verdict |
|---|---|---|---|
| `ClaudeBot` | **T** | Training. | **Block** (recommended default) |
| `Claude-SearchBot` | **R** | Claude's search index — **the token that produces Claude citations**. | **Allow — mandatory** |
| `Claude-User` | **U** | Fetches a URL a user asked Claude to visit. | **Allow — mandatory** |

Exact UA strings:

```
ClaudeBot:        Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)
Claude-SearchBot: Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)
Claude-User:      Mozilla/5.0 (compatible; Claude-User/1.0; +claudebot@anthropic.com)
```

All three share the verification address `claudebot@anthropic.com`. If you have added that address to an allowlist on the theory that it "proves it's Anthropic", note that it proves nothing — an email address in a UA header is not authentication, and anyone can send it.

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

Exact UA strings (product token appears in parentheses):

```
Googlebot:              Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
Google-Agent:           Mozilla/5.0 (compatible; Google-Agent/1.0)
Google-Extended:        Mozilla/5.0 (compatible; Google-Extended)
Google-CloudVertexBot:  Mozilla/5.0 (AppleWebKit/537.36 (KHTML, like Gecko); compatible; Google-CloudVertexBot/1.0; +https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)
GoogleOther:            Mozilla/5.0 (compatible; GoogleOther)
Google-Read-Aloud:      Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Mobile Safari/537.36 (compatible; Google-Read-Aloud)
Google-PageRenderer:    Mozilla/5.0 (compatible; Google-PageRenderer)
```

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
| `AdsBot-Google` | — | Google Ads crawler. Not AI. | Allow if you run ads |

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

```
PerplexityBot:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot
Perplexity-User: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexitybot
```

Both carry the verification address `https://perplexity.ai/perplexitybot`. Perplexity is the clearest case in the catalogue of a **U** token that still deserves citation weight — classify by observed behaviour in your logs, not by the label.

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
YouBot:          Mozilla/5.0 (compatible; YouBot/1.0; https://about.you.com/youbot/)
DuckAssistBot:   DuckAssistBot/1.0; +http://duckduckgo.com/duckduckbot.html
MistralAI-User:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
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
| `Bytespider` / `CCBot` / `img2dataset` | Hugging Face | Training datasets. | **Block** |
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

Explicit allowlines for the retrieval bots are **not required** if no `Disallow` applies to them — a token absent from robots.txt is allowed by default. They are worth writing anyway: they are documentation, they survive a later bad edit, and they make the intent reviewable. If you do write them, they must come **after** any `User-agent: *` block, and remember that group rules are matched by specificity — the longest matching token wins, so an allow for `Googlebot` overrides a `User-agent: *` disallow for `/private/`, but only for the paths the allow covers.

## Sources and confidence

| Entry | Source | Date | Confidence |
|---|---|---|---|
| OpenAI tokens | OpenAI publisher documentation (`openai.com/searchbot`, `/gptbot`, `/bot`) | vendor, current | vendor-documented |
| Anthropic tokens | `anthropic.com` crawler documentation | vendor, current | vendor-documented |
| Google tokens | Google Search Central crawling documentation | vendor, current | vendor-documented |
| Perplexity tokens | `perplexity.ai/perplexitybot` | vendor, current | vendor-documented |
| Bingbot feeds Copilot | Microsoft Bing Webmaster documentation | vendor, current | vendor claim, not independently measured |
| Training-crawl verdict | No consensus. Recommendation in this file is a judgement call, stated as one. | — | **judgement, not evidence** |
| "GPTBot powers ChatGPT Search" | **False.** Contradicts OpenAI's own docs. | — | known-bad source; discard any table repeating it |
