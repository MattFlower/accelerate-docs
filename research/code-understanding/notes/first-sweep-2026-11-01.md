# Code understanding: first research sweep

*2026-11-01. Repo path: `agentic-dev-research/research/code-understanding/notes/first-sweep-2026-11-01.md`
(raw per-angle notes, per the repo README). A synthesized `report.md` can follow once the backlog's measurement items
(BACKLOG #1–2) have data.*

**Scope.** Helping a person understand code quickly in three cases: (a) onboarding to an existing repo,
(b) uncommitted or agent-made changes, (c) PRs. Review *quality* and bug finding are out of scope here; those items
are in BACKLOG.md under "Hand off".

**Method.** X public search (built-in read tools, read-only, 13 calls) and web search/fetch, 2026-11-01. X engagement
numbers are copied exactly as the X API returned them on that date. "Likes" = like_count, "bookmarks" = bookmark_count.
Matt's earlier report ([research/making-prs-easier-to-review/report.md](../../making-prs-easier-to-review/report.md), 2026-10-08) already covers reading order,
grouping, size and tangling, anchoring, risk signals, and security cues. Those results aren't repeated here. This
sweep adds what that report didn't cover: quizzes and retrieval, worked examples, onboarding and slice explainers,
intent capture, and graph-based impact.

## Baseline: what human-review does today (accelerate v0.6.2)

`/human-review` turns a branch, PR (`--pr`), range, or uncommitted work into one offline HTML page. The CLI
(`scripts/human-review.mjs`, no npm dependencies, Bun or Node) runs `collect`, which writes a line-numbered
`review.txt`, `diff.json`, a `recap.json` skeleton, git signals, a text blast radius, and security cues. The agent
fills in `recap.json` following `SKILL.md` and `references/format.md`. `build` validates it against the real diff and
renders `review.html`. The page has a title, brief, "Before this change" background, terms with hover definitions,
"What I need from you", tests cover / don't cover, git signals tagged by provenance, a footprint bar, a 3–6 stop
reading path, visuals (wireframes, data model, API, states, Mermaid, diagrams, `code` of any file at head), annotated
key-change diffs, blast radius, concern-grouped files with proven mechanical and generated tiers, and findings held
back until the reader has viewed each file. A comment, verdict, and **Copy feedback for the agent** loop closes it.
The format is a Claude Code skill (`SKILL.md` with `name`/`description`/`argument-hint` frontmatter) shipped as a
Claude Code plugin (`.claude-plugin/plugin.json`, `marketplace.json`) or copied into `~/.claude/skills/`. The accelerate
repo has no Codex-specific file (`agents/openai.yaml`) yet. The code-review backlog plans one for `bug-review`.

**Gaps this sweep found** (each maps to a BACKLOG item):
1. Nothing checks that the reader understood: no quiz, no comprehension metric (#1, #2).
2. Diffs only. There's no way to learn an area or a repo *at head* without a change (#3 `teach-code`, which now covers the old #3, #10 and #14).
3. No concrete worked example or runtime values (#4).
4. The agent's session reasoning and alternatives are thrown away, and the brief's "why" has no source tag (#5).
5. The page can't answer the reader's own question (#6).
6. Blast radius is a text search in 5 languages (#7).
7. One fixed depth for every reader. Not split-aware. No delta between rounds (#8, #9, #13).

## Findings

### 1. Practitioners are converging on "explainer first, diff second"
- **Geoffrey Litt** has a public `/explain-diff` skill. Its structure is Background (deep
  background for beginners, which a familiar reader can skip, plus a narrow one) → Intuition (concrete examples with toy
  data, diagrams) → Code (grouped, ordered walkthrough) → Quiz (5 interactive multiple-choice questions). Output is one
  self-contained HTML file, or a Notion page.
  [gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524) (178 forks per the fetched page).
  - Thread posts: "literate diff… structured as prose… Faster to review than a raw diff"
    ([X](https://x.com/geoffreylitt/status/2072522296947011960): 63 likes, 22 bookmarks). "I won't send code to others
    until I can pass the quiz, and I do the same when reviewing others' code"
    ([X](https://x.com/geoffreylitt/status/2072522307688333378): 83 likes). Skill link post
    ([X](https://x.com/geoffreylitt/status/2072522312856039461): 197 likes, 301 bookmarks, 13,536 impressions).
  - Earlier: "'AI code review' should be about teaching people how the code works, not just verifying that it's
    correct" ([X](https://x.com/geoffreylitt/status/2019792700023672859): 446 likes, 122 bookmarks, 29,229 impressions).
    "Human review as the bottleneck for AI work suggests an *education* problem"
    ([X](https://x.com/geoffreylitt/status/2008187325331669159): 276 likes, 152 bookmarks). "AI code review can be an
    essay, not a diff!… ends with a quiz" ([X](https://x.com/geoffreylitt/status/2014715215980409178): 99 likes, 117 bookmarks).
  - He says "Graphite tour mode is pretty good" ([X](https://x.com/geoffreylitt/status/2080442881089687898), 10 likes).
    **Not verified:** a web search found no Graphite "tour mode" in Graphite's docs or site. Tour Mode is verified for
    **Tembo** (below).
- **Simon Willison**: "linear walkthrough of the code that explains how it all works in detail", built with Showboat
  so snippets are pulled by commands, not typed ("ensured that Claude Code would not manually copy snippets… risk of
  hallucinations") ([guide](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/);
  [X](https://x.com/simonw/status/2026702972617633886): 63 likes, 64 bookmarks). Also "interactive explanations" for
  paying down "cognitive debt": an animation made an algorithm click where the walkthrough didn't
  ([guide](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/)).
- **Claude Code team**, per an X Article posted on @addyosmani's account ("How the Claude Code team does code review"):
  review has two purposes, catching bugs and building a shared understanding. For the second: "when anyone wants to
  learn about a piece of the codebase, they ask Claude to generate an explainer about that exact slice… always up to
  date", sometimes with "a mini artifact that visualizes this area". And: "reading trivial diffs line by line… teaches
  you very little" ([X](https://x.com/addyosmani/status/2114604912520921136): 13,390 likes, 1,556 reposts, 34,649
  bookmarks, 2,531,929 impressions). This is the strongest engagement signal in the sweep. Authorship is as the X
  Article presents it. We didn't verify it elsewhere.
- **Addy Osmani, "Agentic Code Review"**: agent reasoning "is usually discarded the moment the diff is produced… review
  shifts from checking reasoning… to reconstructing intent". Also "We made writing cheap, and understanding stayed
  exactly as expensive" ([X](https://x.com/addyosmani/status/2066595308629594363): 1,714 likes, 3,249 bookmarks).
  Related: "Cognitive Surrender" ([X](https://x.com/addyosmani/status/2052124873208799378): 953 likes).
- **Latitude** added a CI step that generates an interactive HTML review artifact on every PR, inspired by Litt
  ([X](https://x.com/geclos/status/2073028203329810437): 5 likes).
- "Feynman DIFF explainer" prompt ([X](https://x.com/LouisLibre/status/2099365075295334532): 16 likes, 40 bookmarks).

### 2. Quizzes and retrieval: the one idea with RCT-grade support
- **Anthropic RCT (52 developers, new Python library):** the AI-assisted group scored 50% vs 67% on a comprehension
  quiz (17% lower, Cohen's d=0.738, p=0.01), with no significant speed gain. The biggest gap was on debugging
  questions. AI users who asked conceptual questions or asked for explanations kept their understanding (65–86% vs
  24–39% for low-engagement patterns) ([Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills),
  [arXiv 2601.20245](https://arxiv.org/html/2601.20245v1)). This is about *writing* with AI, not *reviewing*, but it
  measures what we care about: understanding code you didn't write yourself.
- **Testing effect:** retrieval testing beats re-studying for retention at 2 days and 1 week
  ([Roediger & Karpicke 2006](https://pubmed.ncbi.nlm.nih.gov/16507066/)).
- **Generated question quality** is the risk: an earlier evaluation found GPT-4 code questions often lacked
  meaningful difficulty or plausible distractors ([KTH](http://urn.kb.se/resolve?urn=urn%3Anbn%3Ase%3Akth%3Adiva-336041)).
  The AutoMCQ pilot (8 students) found that generated questions helped surface misconceptions
  ([arXiv 2505.16430](https://arxiv.org/pdf/2505.16430)). Both are via search summaries. We didn't read the full papers.
- **In-IDE LLM help (GILT, 32 participants):** +0.47 sub-tasks completed (p<.01), but no difference in quiz scores or
  time ([Nam et al., ICSE 2024](https://arxiv.org/html/2307.08177v3)). On-demand Q&A helps people get work done. It
  doesn't by itself build understanding.

### 3. Onboarding to a repo: tools and adoption
- **codebase-to-course** (zarazhangrui): a Claude Code skill that turns a repo into one HTML course with scroll
  modules, code ↔ plain-English side by side, animated data flow, quizzes that "test *application* not memorization",
  and glossary tooltips ([repo](https://github.com/zarazhangrui/codebase-to-course);
  [X](https://x.com/zarazhangrui/status/2035962536474837019): 1,808 likes, 2,088 bookmarks, 209,513 impressions). The
  official @claude_code account quoted it as "Claude as a thinking partner to learn from a codebase"
  ([X](https://x.com/claude_code/status/2035966532438863965): 53 likes, 69 bookmarks).
- **Understand-Anything**: Claude Code plugin. Tree-sitter extracts structure deterministically, an LLM adds
  summaries, layers, and guided `tour[]`. The graph can be committed and updated on commit. `/understand-diff` maps
  changed files to nodes plus 1-hop affected nodes, and PR #574 made that a deterministic `computeDiffOverlay`
  ([repo](https://github.com/Egonex-AI/Understand-Anything/), [PR #574](https://github.com/Egonex-AI/Understand-Anything/pull/574)).
  X: [@techNmak](https://x.com/techNmak/status/2056477994328396263) 101 likes / 109 bookmarks. A post with 227 likes
  and 484 bookmarks ([@prasenx](https://x.com/prasenx/status/2058119202712723632)) describes a tool like it without
  naming it.
- **Graphify** is another code-to-knowledge-graph tool using tree-sitter (X mentions only, low engagement:
  [example](https://x.com/chenzeling4/status/2063985404228014317), 8 likes). We didn't verify its repo.
- **DeepWiki** (Cognition, launched 2025-05-05): generated wiki, diagrams, and Q&A for public repos
  ([Cognition](https://cognition.com/blog/deepwiki)). **Google Code Wiki** (public preview 2025-11-13)
  ([Google](https://developers.googleblog.com/introducing-code-wiki-accelerating-your-code-understanding/)).
- **Microsoft CodeTour**: human-authored, committed `.tours` walkthroughs in VS Code
  ([repo](https://github.com/microsoft/codetour/)). There's also a JetBrains "Walkthrough" plugin where an agent
  narrates tours. A Reddit commenter there notes tours go stale and wants "diff-aware tours where the agent explains
  why each hunk changed" ([Reddit](https://www.reddit.com/r/Jetbrains/comments/1t78ocb/walkthrough_an_intellij_plugin_that_lets_any_ai/)).
- **Matt Pocock `teach`**: a stateful teaching workspace (mission, lessons as HTML, learning records used to find the
  "zone of proximal development") ([skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)).
  Full review in §7 below.
- **Evidence on LLM onboarding:** small. Onboarding Buddy had 8 developers; helpfulness was 3.26/4
  ([arXiv 2503.23421](https://arxiv.org/abs/2503.23421)).
- **Reading order for onboarding:** experts read code less linearly than novices, and in execution order more than
  top-to-bottom order ([Busjahn et al., ICPC 2015](https://researchonline.gcu.ac.uk/ws/portalfiles/portal/24953094/ICPC2015_authors_version.pdf)).
  So a course or tour should follow the execution path.

### 4. Understanding a PR: tools that overlap with human-review
- **Tembo Review Tour Mode**: "groups related files into focused sections, explains what changed, and surfaces risk,
  review depth, and merge confidence", plus PR chat ("ask why they changed") ([Tembo](https://www.tembo.io/review),
  [changelog](https://www.tembo.io/changelog)). T3 Code has beta "review guides" with stops, per
  [Tembo's comparison page](https://www.tembo.io/blog/tembo-vs-t3code) (a vendor writing about a competitor).
- **lucidiff**: PR → one HTML explainer (summary, per-file cards, flow diagram, cited risks, test checklist). The model
  fills a JSON schema, citations are checked against the diff, and a fixed template renders it
  ([repo](https://github.com/Rishabjs03/pr-karpathy); [X](https://x.com/Yrishavjs/status/2106339914195607728): 4 likes).
  Its architecture is close to human-review's.
- **hunk-review-changes**: the agent splits the diff into hunks with what/why, then a local web UI, per-hunk comments,
  and an export back to the agent ([repo](https://github.com/lucianghinda/hunk-review-changes)).
- **constellagent**: a review panel with an agent-written "code tour mode" and "submit selected comments to agent"
  ([repo](https://github.com/tridha643/constellagent)).
- **nicobailon/visual-explainer**: an agent skill for HTML pages and decks, including diff reviews and project recaps
  ([repo](https://github.com/nicobailon/visual-explainer)). Only the repo description was read.
- **CodeRabbit** PR walkthroughs include Mermaid sequence diagrams by default ([docs](https://docs.coderabbit.ai/pr-reviews/walkthroughs)).
  **Graphite Chat** gives "instant context on code changes" ([Graphite](https://graphite.com/)).
- **Takeaway:** human-review already covers most of what these tools do (reading order, grouping, visuals, the
  agent feedback loop, citations validated against the diff), and in some ways more strictly (held-back findings,
  proven mechanical tier). Things it doesn't have: quiz, worked example, PR chat/Q&A, graph-based impact, onboarding
  at head.

### 5. Intent and the "why"
- **Entire** (Thomas Dohmke): agent hooks record prompts, transcripts, tool activity, and reasoning, and link them to
  commits with an `Entire-Checkpoint` trailer ([docs](https://docs.entire.com/guides/checkpoints/capture-checkpoints)).
- **Haystack** uses "your coding agent transcript plus analysis" to explain why each hunk changed
  ([X reply](https://x.com/AkshaySubr42403/status/2067331955494912104), 0 likes; product not checked further).
- Practitioners asking for this, all low engagement:
  [@UditKhandelwal8](https://x.com/UditKhandelwal8/status/2082542780237352977) ("the diff is the output of a decision,
  not the decision"), [@GandhiRohith](https://x.com/GandhiRohith/status/2067630870996103481),
  [@dezign_ash](https://x.com/dezign_ash/status/2100452581629886955) ("separates what the agent changed, what it
  tested, and what it only assumes works").

### 6. Concrete values and runtime state
- Projection Boxes show runtime values next to source lines. Users found them useful when they could switch modes on
  demand ([CHI 2020](https://cseweb.ucsd.edu/~lerner/papers/projection-boxes-chi2020.pdf)). Showing only the variables
  each line uses did better than showing full state ([SIGCSE TS 2027](https://2027.sigcse-ts.acm.org/details/sigcse-ts-2027-Papers-1/166/How-Much-Runtime-State-Should-We-Show-Learners-An-EEG-Study-of-Feedback-Granularity-)).
  These are education settings, and the results come from search summaries, not full-paper reads.

### 7. Matt Pocock's `teach` (added 2026-11-01, second pass)

**Source, verified.** Author Matt Pocock (X [@mattpocockuk](https://x.com/mattpocockuk)). Repo
[mattpocock/skills](https://github.com/mattpocock/skills) ("Skills for Real Engineers. Straight from my .agents
directory."), MIT. The GitHub API on 2026-11-01 showed 308,865 stars and 25,999 forks for the whole repo, not for this
skill. Skill folder [`skills/productivity/teach/`](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach):
`SKILL.md` (9.7 KB), `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`, and
`agents/openai.yaml` (Codex metadata: display name "Teach", `allow_implicit_invocation: false`). The user docs are at
[`docs/productivity/teach.md`](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md). Quickstart:
[aihero.dev](https://www.aihero.dev/learn-anything-with-my-teach-skill). History: added 2026-05-27, moved out of
`in-progress` on 2026-06-08, last changed 2026-10-07 (PR #1183: anchor workspace paths, vary quiz answer position).
It's **general-purpose**, not repo-specific: "Teach the user a new skill or concept, within this workspace."

**How it works** (from `SKILL.md` and the docs):
- It's user-invoked only (`disable-model-invocation: true`). The directory you run it in becomes a **teaching
  workspace** for one topic. The docs advise keeping that directory *out of* the project you're working in.
- State lives in files: `MISSION.md` (why, success criteria, constraints, out of scope), `RESOURCES.md` (vetted
  Knowledge sources and Wisdom communities), `lessons/NNNN-*.html`, `reference/*.html` (cheat sheets, glossary),
  `learning-records/NNNN-*.md` (ADR-style), `assets/` (shared CSS, quiz widgets), and `NOTES.md` (preferences). A new
  session continues from these files.
- The mission comes first: if it's missing, the skill interviews you. "Never trust your parametric knowledge": it finds
  high-trust resources before teaching and cites them in every lesson, with one recommended primary source per lesson.
- Lessons are short, one tangible win each, "beautiful… Think Tufte", and aimed at the zone of proximal development
  worked out from the learning records.
- Learning science it uses: fluency vs. storage strength, desirable difficulty (retrieval, spacing, interleaving),
  knowledge first with low difficulty, then skills drilled through a tight feedback loop. Quiz options must be the same
  length, and the position of the correct answer must vary.
- Learning records are written only on *evidence* of understanding, disclosed prior knowledge, a corrected
  misconception, or a mission change. "Coverage is not learning." Old records are marked superseded, not deleted.
- Glossary rules (`GLOSSARY-FORMAT.md`): add a term only once the user understands it, pick one word and list the
  rest as *Avoid* aliases, and use glossary terms inside definitions. Questions that need judgment get an attempted
  answer, then a pointer to a community.

**Known gaps** (the docs' own "Common questions" section plus issues):
- No assessment of starting level: "It never did grilling to establish my starting point"; the request is
  [#725](https://github.com/mattpocock/skills/issues/725).
- No scheduled spaced review, and no reliable stop rule: it's "good at making the next lesson, but not as good at
  knowing when to stop".
- Quiz answers kept landing in the first option: per the docs, slot A "33 times out of 33 across nine lessons" after a
  prompt fix. The docs conclude a shuffling component is the real fix. The docs cite issue #335, which returned 404
  when checked; see [#985](https://github.com/mattpocock/skills/issues/985) and
  [#611](https://github.com/mattpocock/skills/issues/611).
- Lessons ship with few citations ([#960](https://github.com/mattpocock/skills/issues/960)), aren't rendered and
  checked before hand-off ([#1109](https://github.com/mattpocock/skills/issues/1109)), and forget their quiz script
  ([#1058](https://github.com/mattpocock/skills/issues/1058)).
- `GLOSSARY-FORMAT.md` is orphaned: `SKILL.md` doesn't link to it ([#559](https://github.com/mattpocock/skills/issues/559)).
- A made-up procedure: a 2x2 Rubik's cube user got move sequences that don't solve it (docs).
- Results vary a lot by model and harness. Per the docs, Copilot CLI with Codex produced "a single 30-line HTML card".
- A community "teach pr" skill (teaching level 1–4, walks the checked-out PR like a senior onboarding a newcomer) was
  declined for this repo: "Cool idea, but not for this repo IMO" ([#727](https://github.com/mattpocock/skills/issues/727)).
  In-lesson annotation was also declined in favor of notes in chat ([#519](https://github.com/mattpocock/skills/issues/519)).

**Reception on X** (engagement as returned by the X API on 2026-11-01):
- Launch posts by @mattpocockuk: "I poured my 10 years of teaching experience into a skill… it can teach you anything"
  ([X](https://x.com/mattpocockuk/status/2064023481398824993): 5,054 likes, 368 reposts, 7,777 bookmarks, 909,811
  impressions); "/teach is live… Best skill I've ever built" ([X](https://x.com/mattpocockuk/status/2063988995692900439):
  2,821 likes, 2,910 bookmarks); the first version "on the tube" ([X](https://x.com/mattpocockuk/status/2059616119388795367):
  880 likes); the grilling → `/handoff` → `/teach` workflow ([X](https://x.com/mattpocockuk/status/2076373232295587865):
  2,932 likes, 2,618 bookmarks); a reply, "/teach me about this codebase"
  ([X](https://x.com/mattpocockuk/status/2062973868344524834): 282 likes, 137 bookmarks); "I can do it", Rubik's-cube
  proof ([X](https://x.com/mattpocockuk/status/2066874357612151271): 427 likes).
- Others: [@Jilles](https://x.com/Jilles/status/2064083851148730583) ("cooked", learning Astro from a template project;
  67 likes, 66 bookmarks); [@MAXIMISEART](https://x.com/MAXIMISEART/status/2095519045210505335) (Polish how-to; 61
  likes, 245 bookmarks); [@Voxyz_ai](https://x.com/Voxyz_ai/status/2070082137630384226) (59 likes);
  [@crpier42](https://x.com/crpier42/status/2065849866211693057) (codebase lessons served locally with links that jump
  Neovim to the code; 1 like); [@DrockStowe](https://x.com/DrockStowe/status/2083523350811341204) (`/handoff` → `/teach`
  to understand an agent's solution, "then read the code"; 1 like);
  [@itsmattchan](https://x.com/itsmattchan/status/2066903354362491377) (asks for codebase use; 0 likes). Teams building
  their own: a `/teach-me` skill in a codebase ([@thealexkates](https://x.com/thealexkates/status/2060016615983350194),
  1 like).
- Web: a blog write-up of using it to learn a codebase mechanism
  ([magutti.com](https://www.magutti.com/blog/mattpocock-teach-skill-learn-don-t-delegate); linked from
  [X](https://x.com/marcoaxx/status/2063268562186207550)). Not read in full.

**Other repo-onboarding skills found along the way:**
- **ECC `codebase-onboarding`** ([SKILL.md](https://github.com/affaan-m/ECC/blob/main/skills/codebase-onboarding/SKILL.md);
  `affaan-m/everything-claude-code` redirects to `affaan-m/ECC`, 294,392 stars per the API, for the whole repo). It
  reconnoiters manifests, frameworks, entry points, and tests, then maps the architecture and conventions, and outputs
  an onboarding guide plus a starter `CLAUDE.md`. Its focus is orienting the *agent* as much as the human.
- **claudeskills.page `codebase-onboarding`** ([page](https://claudeskills.page/skills/workflow/codebase-onboarding/)):
  "Breadth first, then one deep trace"; run the build and tests ("documentation is often stale"); every claim cites a
  file path; "Stop exploring when the user's question is answered"; verify by opening two random claims. It bundles a
  `repo_map.py`. Popularity unknown.
- **codebase-to-course** (5,750 stars per the API) and **Understand-Anything** (89,517 stars per the API). See §3.
- HermeticOrmus/code-comprehension-skills (2 stars) has the same four-step "entry points → map → trace one flow →
  abstractions" protocol. It's low signal.

**How it compares with human-review and the backlog:** `teach` and HR solve different halves. HR explains a *change*
with git-true code, a fixed validated renderer, and a review loop, but it's stateless and diff-only. `teach` is
stateful, mission-led, and grounded in retrieval practice, but it's generic, free-form HTML, and sourced from the web
rather than the repo. It has no code-specific grounding and no render check, which are the failures its issue tracker
shows. What to take: mission-first interview, learning records with evidence rules, separating lessons from durable
reference, spaced re-quiz and a stop rule, quiz option rules (with a renderer-side shuffle), glossary *Avoid*
aliases, "one primary source to read yourself", and wisdom → who to ask. These went into BACKLOG #1, #3 (now
`teach-code`, merging the old #3, #10 and #14), #6, #8, and a new #10.

## What we didn't verify
- `teach` issue #335 (cited by the teach docs for the 33/33 result) returned 404 on 2026-11-01.
- Star counts are for whole repos (mattpocock/skills, ECC), not single skills.
- Graphite "tour mode" (only Litt's post says it exists).
- Graphify's repo and star count. Haystack as a product. The tool behind @prasenx's post.
- The OpenAI Codex plugin for Claude Code (an X post only).
- Full texts of AutoMCQ, the KTH question study, and the SIGCSE 2027 EEG study (we have search-summary claims only).
- Who wrote the "How the Claude Code team does code review" article, beyond its being posted on @addyosmani's account.


