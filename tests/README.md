# tests/ — what CI enforces, and why

Three gates. All are pure standard library, Python 3.10+, no dependencies, and all
run on every push. `AGENTS.md` documents them for contributors; this file explains
*why each check exists*, so you can tell the difference between a gate protecting a
real invariant and a gate that is merely noise.

```
python tests/validate_skill_inventory.py
python tests/reference_freshness.py
python tests/check_docs.py            # add --external for the network check
```

`--strict` makes warnings / review triggers fatal. CI enforces gates 2 and 3 at their
defaults and runs `--strict` separately, non-blocking (see the workflow for why).

---

## Gate 1 — `validate_skill_inventory.py`

Structure and spec conformance. A skill that breaks one of these is either
unloadable, unportable, or misleading.

| Check | Why it exists |
|---|---|
| Every directory under `skills/` has a `SKILL.md` | A directory without one is invisible to every host. It looks like a skill in review and ships as nothing. |
| Frontmatter parses | An unparseable header means the host cannot read `name` or `description`, so the skill cannot be selected at all. The parser is a hand-written YAML subset (scalars, quoted strings, one level of nested mapping) because PyYAML is not installable here. If PyYAML *happens* to be installed, it is used as a cross-check so the two can never silently disagree. |
| `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and equals the directory name | The name is the identifier a host routes on. A mismatch between directory and `name` produces two identities for one skill and breaks self-selection. |
| `description` present, 1–1024 chars | Required by the spec. Above 300 chars is a **warning**: Codex budgets the entire skill list at 8,000 characters and truncates descriptions first, so a verbose description silently evicts other skills. |
| `license` is `Apache-2.0` | Uniform licence across a library meant for redistribution. |
| `metadata` is exactly `repo`, `version`, `updated`, `keys-required`, in that order, all strings | Order is not cosmetic — it makes frontmatter diffs stable, so a real metadata change is visible as a one-line diff. An extra key is how evidence claims start hiding in frontmatter instead of in a `> **Evidence:**` line a reviewer can check. |
| No unknown top-level keys | **The portability invariant.** Non-OpenCode hosts ignore keys they do not recognise, so an unknown key is a key that does not work everywhere. Anything a host might honour and another might not (`context:`, `hooks:`, host-specific blocks) fails the build. |
| Body under 500 lines / 5,000 est. tokens | A skill body is loaded into context on activation. Past that it crowds out the work it was loaded to do. Detail belongs in `references/`, which loads only when needed. The estimate is chars/4; tune with `--max-body-tokens` if the budget policy changes. |
| No `context: fork`, no `hooks/` directory | Both are Claude Code only. Shipping them means the skill works on one host and silently misbehaves on six others. |
| Zero hard dependencies | The repo's promise is that every skill completes without a paid account. The check looks for input-side artifact terms (`curl`, `fetch`, `web`, `paste`, `CSV`, `HTML`, `URL`) in the "when to use"/"inputs" context, and separately flags credential wording — but ignores it when negated, so "zero API keys" does not trip it. Heuristic, so it is a warning, not an error. |
| Relative links resolve | A broken link in a reference file is a dead end at the exact moment the agent needs the detail, which is when it will guess instead. Links resolve relative to the **containing file**, as GitHub renders them: `references/FOO.md` from `SKILL.md`, plain `FOO.md` from inside `references/`. A link may not escape the skill root, and `references/references/FOO.md` is caught as the double-prefix bug it is. |

Exit code is non-zero on any error, and on any warning under `--strict`.

## Gate 2 — `reference_freshness.py`

Staleness of cited sources. The repo's rule is that a number without a dated source
is not a finding. This gate closes the other half of that: a number whose source has
aged out is no longer a finding either, it is a guess wearing a citation.

It recognises `2026-06-15`, `2026-06`, `Jun 15 2026`, `15 June 2026`, `Jun 2026`,
`(2026)`, and bare years — the last two only when the same line carries citation
context (a URL, `arXiv`, `n=`, `measured`, …), so a stray year in prose is ignored.
Fenced code blocks are skipped because example payloads are not citations.

Under-specified dates are scored as the **last** day of the period they name, so
`2026-03` is read as 2026-03-31 and a bare `2026` as 2026-12-31. This is
deliberately lenient: the gate should never fail a contributor for writing a month
instead of a day. A reported age under 0 just means a period that is still running.

### Why two thresholds, not one

An earlier version of this gate treated any citation older than 90 days as a failure.
On day one that failed **78 of 171 citations** — including Shepard / Zyppy's primary
research and a documented on-the-record statement. That is not a signal, it is noise:
**a primary source does not expire in 90 days.** Shepard's 54 scored experiments from
2026-05-07 do not rot because time passed, and a documented 2025-07 statement is
still exactly what was said. A gate that is always red stops being read, which is
strictly worse than having no gate — it looks like enforcement and is actually a
scratch that everyone learns to dismiss.

So the age at which a citation is *noticed* and the age at which it is a *failure* are
different questions, and the script now answers them separately:

| | Flag | Meaning |
|---|---|---|
| **Review trigger** | `--review-after-days`, default **90** | Reported, not failed. The **finding** may have been superseded even though the **source** has not expired. Re-read the claim; if the source still says it, do nothing. |
| **Stale** | `--stale-after-days`, default **365** | A genuine failure. The source itself has aged out. Re-verify against the primary source, correct the claim or bump `metadata.updated`. |

`--max-age-days N` is kept as a **backwards-compatible alias** for
`--review-after-days`, so every existing invocation keeps working and keeps meaning
what it used to mean. `--strict` promotes review-level findings to failures, and
`--ignore-path GLOB` skips paths as before.

One more attribution rule, because a stale count that is wrong is worse than no stale
count: a **comparative baseline** is not a citation. In *"Ahrefs (reported 2026-03)
… down from 76% in July 2025"*, the `July 2025` figure is a datapoint inside a
2026-03 report, not a second source that expired 15 months ago. The gate attributes
such baselines to the reporting source's date.

The summary always prints **both** counts on one line —
`Citations checked: N / review-triggered: N / stale: N` — because **a gate that finds
nothing must say so loudly**. "171 checked, 0 stale" and "0 checked" mean completely
different things and both exit 0; printing the checked count is what keeps the second
from passing vacuously. Lower the review threshold (`--review-after-days 30`) and the
review count rises sharply, which is how you confirm the check is live rather than
inert.

## Gate 3 — `check_docs.py`

Everything Gate 1 cannot see, which is where every defect that survived to v1.0.2
lived. Gate 1 checks four skill directories; this gate checks the repository: the
README pair, `docs/`, the marketplace JSON, and whether the `curl` commands printed
inside reference files are even valid shell.

| Check | Why it exists |
|---|---|
| Every relative link resolves | Gate 1 only walks `skills/`. The three broken links found in `docs/` after v1.0.2 were invisible to it, and a reader who clicks one lands on a 404 in the file that is supposed to prove the repo's diligence. Resolution is relative to the containing file, because that is what a renderer does — the old skill-root convention passed the gate while 30 links 404'd on GitHub. |
| No absolute paths, nothing escapes the repo | An absolute `/foo` path works on one host's build and nowhere else. `../` out of the repository is a link to a file the reader does not have. |
| Fenced blocks balance | An unclosed fence silently swallows the rest of the document. In a skill body that means the agent reads headings as code and the checklist as prose. |
| `bash` / `sh` blocks parse (`bash -n`) | These are copy-paste commands. A block that does not parse is a command the reader will run and watch fail. 37 blocks across 27 files were checked the first time this gate ran. The WindowsApps `bash.exe` shim is a WSL launcher that exits 1 when WSL is absent, so the shell is probed before use rather than trusted. |
| `shellcheck -S error` on the same blocks | `bash -n` proves syntax, not correctness. Errors only: warnings and style suggestions would drown a document that is deliberately full of illustrative one-liners. Pass `--no-shellcheck` to skip it, and note that a missing shellcheck is a warning, never a silent pass. |
| No BOM, valid UTF-8, no mojibake | `Get-Content` without `-Encoding` on Windows produced a mojibake release note during this project. Double-encoded text looks like an encoding problem to a reader and like a corrupted quote to a reviewer, and both destroy trust in the citation. |
| `marketplace.json` parses and its skill paths exist | The marketplace file is what the installer reads. A path typo means a skill that installs for nobody, and nothing in the skill tree notices. |
| Version is identical in five places | `marketplace.json`, four `SKILL.md` files and the README badge. Drift is how a "fixed in v1.0.3" claim ships in a v1.0.1 artefact — it happened twice here, in both directions. |
| EN/ES URL parity | The Spanish README claims to be a translation, not a summary. A statistic present in one language and missing in the other means one audience is reading a different article. Badge URLs are localised and are matched as pairs, not by string. |
| `--external`: every outbound URL answers | Link rot is the only failure here that a maintainer cannot see without asking. Off by default because it needs the network and because publishers rate-limit; CI runs it weekly and opens an issue. `403`/`429`/`503` are warnings (bot blocking), `404` is an error (dead citation). Probes use `GET`, because several CDNs and affiliate redirectors answer `HEAD` with `404` and `GET` with `200`. |

Exit code is non-zero on any error, and on any warning under `--strict`.

## Fixtures

`fixtures/` holds small, hand-maintained inputs for exercising the skills by hand.
They are inputs only — no gate reads them. Each starts with a one-line header naming
the skill and check it exercises, and each is a deliberate negative or positive case:

| File | Exercises | Expected result |
|---|---|---|
| `blocked-by-wildcard-robots.example.txt` | `aeo-bot-access-audit` step 3 trap (a), scoring rule 4 | BLOCKED, CRITICAL |
| `good-robots.example.txt` | the same skill's recommended posture: block training, allow retrieval | OPEN |
| `answer-late.example.html` | `aeo-citability-audit` answer-near-the-top | FAIL — answer is in section 4 |
| `answer-early-selfcontained.example.html` | the same check, plus quotation/table/date worthiness | PASS |
| `js-schema-unverifiable.example.html` | honest reporting of what a raw-HTML fetch cannot see | "could not verify", never "no schema" |

They stay under ~2 KB on purpose: a fixture that is too big to read in one screen
stops being diffable in review, which is most of its value.
