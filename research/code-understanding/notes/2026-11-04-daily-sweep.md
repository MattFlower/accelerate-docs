# Code understanding: daily sweep 2026-11-04

*2026-11-04. Repo path: `agentic-dev-research/research/code-understanding/notes/2026-11-04-daily-sweep.md`
(raw notes for one window, per the repo README). This does not replace
[`first-sweep-2026-11-01.md`](first-sweep-2026-11-01.md). No `report.md` yet.*

**Window.** Since the last successful weekday sweep (~2026-11-03 13:18 UTC, 8:18 AM America/New_York)
through 2026-11-04 ~13:24 UTC.

**Method.** Public X search and the web. X metrics are copied from the X API `public_metrics` on 2026-11-04.

**Scope.** Same as the first sweep. Help a person understand existing code (a repo, an area, or a change).
Review quality and bug finding stay out of scope.

## In scope

### IronBee Code Wiki (`vendor`, weak `engagement`)

Launch post by @serkan_ozal, 2026-11-03T15:03:06Z
([X](https://x.com/serkan_ozal/status/2117633673461674225)).
X API `public_metrics` on 2026-11-04: like_count 5, bookmark_count 0, reply_count 2, retweet_count 1,
impression_count 9185.
The product page is [ironbee.ai/code-wiki](https://ironbee.ai/code-wiki).

What the product page says it does:

- Each connected repo gets a wiki of the default branch.
- Pages name the commit they were written from.
- The wiki rebuilds after merges, with a quiet window, and it runs a daily full rebuild by default.
- Pages include an overview, a where-to-start reading order, and an architecture area map (imports solid,
  HTTP dashed), plus per-area pages.
- Per-area pages describe important flows and cite `file:line` at that commit.
- Every citation is checked against the code at that commit.
- Secrets are redacted.
- Open PRs do not update the wiki.

**Why it matters for human code understanding.** It sits in the same niche as DeepWiki and Google Code Wiki.
The first sweep already cites both. Rebuilds run after merges, and citations are checked, like human-review's
honesty rule. A person can use the wiki to onboard to the default branch. The same pages are a map of the
area a PR touches before review.

**Backlog.** Additional `vendor` evidence for #3 `teach-code`. The area map and the flows also support #7
(structural blast radius). Engagement on the launch post is weak.

**Hand off.** IronBee Code Review is on the same launch post. The post's note_tweet claims 67.4 F2 and 75.3
Recall on the Martian Code Review Benchmark. That claim is review quality. It goes to the Code Review Research
Bot. It is not ranked here.

## Out of scope or rejected

- **stack-diagram** ([caru-ini/stack-diagram](https://github.com/caru-ini/stack-diagram)), created 2026-11-01.
  The GitHub API on 2026-11-04 reported 1707 stargazers and 74 forks. In-window X examples:
  [@0xbobaaa](https://x.com/0xbobaaa/status/2117288829270819013) (like_count 53, bookmark_count 39,
  reply_count 18, retweet_count 2, impression_count 1485) and
  [@arsene_btc](https://x.com/arsene_btc/status/2117723494762844600).
  Rejected. It draws a logo-rich stack diagram from a one-sentence description. It does not read the repo.
  That is README candy, not code understanding of existing structure. Recorded under Rejected in `BACKLOG.md`.
- **Comprehension Standard** ([tacoda/fulcorum-comprehension-standard](https://github.com/tacoda/fulcorum-comprehension-standard)),
  repo created 2026-08-18. The idea is strong. The repo is outside this window, and there was no in-window X
  engagement. Not added in this pass. Leave it for a later deliberate pass.

## Noise skipped

Vibe-coding discourse, harness-engineering news, and generic "human review is the bottleneck" posts. Those
posts are about review quality or verification volume. They belong to the Code Review bot.
