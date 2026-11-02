# Code understanding: backlog

*Draft 3, 2026-11-02 (draft 2 plus the 2026-11-02 sweep; see "Changes in draft 3" below). Repo path: `agentic-dev-research/research/code-understanding/BACKLOG.md`.*
*It follows the layout in that repo's README (`research/<topic>/report.md` + `notes/` + optional `BACKLOG.md`)
and the style of `research/automated-code-review/BACKLOG.md`. Findings and sources are in
[`research/code-understanding/notes/first-sweep-2026-11-01.md`](notes/first-sweep-2026-11-01.md)
and [`research/code-understanding/notes/sweep-2026-11-02.md`](notes/sweep-2026-11-02.md)
until a `report.md` is written.*

**Baseline.** `accelerate/skills/human-review` (v0.6.2, 2026-10-30) is ground truth. Everything here is ranked by
what it adds *on top of* that skill. Ideas the skill already does are listed under **Shipped**, with the file path.
Abbreviations: `HR/` = `https://github.com/MattFlower/accelerate/blob/main/skills/human-review/`.

**How this is ranked.** By expected gain per unit of effort. Gain means a person reaches a correct, critique-ready
understanding of a repo, a working-tree change, or a PR in less time, without lowering defect detection (the earlier
report warns that saving time by reading less core logic lets defects through). Effort is build plus eval cost
(S ≈ ≤1 day, M ≈ 2–5 days, L ≈ 1–3 weeks). Measured evidence beats practitioner reports, and practitioner reports beat
engagement alone. Measurement items come first because nothing below can be ranked honestly without them. That is the
same rule as the code-review backlog's "fix the eval first".

**Evidence labels.** `measured-RCT` (randomized or controlled study) · `measured-obs` (observational or field data) ·
`practitioner` (someone describes their own use) · `vendor` (launch post or docs) · `engagement` (X numbers only, as
returned by the X API on the date written next to the number: 2026-11-01 in draft 2, 2026-11-02 in draft 3) · `our own idea`.

**Statuses.** `proposed` · `testing` · `shipped` (in human-review, path cited) · `rejected` (with the reason).

**Targets.** `HR` = extend human-review · `new skill` = a new human-facing skill in accelerate · `limitless` = the
factory's deliver/review stages.

---

## A. Ranked

### 1. Comprehension quiz at the end of the page — `proposed`, cost S, target HR
- **Idea:** a `quiz` block of 3–5 medium-difficulty multiple-choice questions about the change ("which path still
  runs when X is null?"), each with a per-option explanation. It is shown only after the reviewer's own pass, like
  other held-back content. The score and wrong answers go into the **Copy feedback** export. Questions must cite the
  `path:line` that answers them, so the build can check them like annotations.
- **Sources:** Geoffrey Litt's `/explain-diff` skill ends every explainer with a 5-question interactive quiz
  ([gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)). His rule is "I won't send code to
  others until I can pass the quiz" ([X](https://x.com/geoffreylitt/status/2072522307688333378): 83 likes, 28 bookmarks,
  10,370 impressions; the skill post [X](https://x.com/geoffreylitt/status/2072522312856039461): 197 likes, 301 bookmarks).
  Also zarazhangrui's *codebase-to-course* quizzes "test application not memorization"
  ([repo](https://github.com/zarazhangrui/codebase-to-course); [X](https://x.com/zarazhangrui/status/2035962536474837019):
  1,808 likes, 2,088 bookmarks, 209,513 impressions). Evidence: `practitioner` + `engagement`, with support from
  `measured-RCT`: Anthropic's RCT found AI users scored 17% lower on a comprehension quiz (50% vs 67%, d=0.738), and
  people who asked conceptual or explanation questions kept their understanding
  ([Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills),
  [arXiv 2601.20245](https://arxiv.org/html/2601.20245v1)).
  **(Im)Paired Programming** is the same pattern on a build-a-website task: 54 students used either an editing agent
  or a chatbot. Agents helped the initial completion and harmed comprehension, so users were less able to extend
  their code without the agent. Copy+paste prompts and auto-accepted edits were linked with lower comprehension.
  Users still preferred agents
  ([arXiv 2607.26375](https://arxiv.org/abs/2607.26375),
  [code](https://github.com/nbalepur/impaired-programming)). Evidence for that result: `measured-RCT` (student sample).
  Retrieval testing beats re-reading for retention
  ([Roediger & Karpicke 2006](https://pubmed.ncbi.nlm.nih.gov/16507066/)).
- **Why it helps:** today the page shows what changed but never checks that it landed in your head. A quiz turns
  passive reading into retrieval, and it shows you which part you didn't get. It also gives us a **comprehension
  metric**, which the earlier report said human-review lacks.
- **Test:** on 6–10 real PRs (limitless PRs, accelerate's own commits, the `ky` change used for dogfooding), score the
  quiz and log time. Check the questions: are they answerable from the page, are any gotchas, and how many does the
  precision check reject? Then compare against canary defects (item 2): do people who fail a question miss the canary
  in that area?
- **Quiz rules taken from `teach`** ([SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)): every option has the same number of words,
  the correct option's position varies, and nothing in formatting or order gives the answer away. **Don't rely on the
  prompt for position.** `teach`'s docs report the correct answer landed in slot A "33 times out of 33 across nine
  lessons" even after an instruction-level fix, and conclude "the real fix is a quiz component… that shuffles the
  answers" ([docs](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md); the docs cite issue #335, which returned 404 on 2026-11-01;
  related open issue [#985](https://github.com/mattpocock/skills/issues/985), and [#611](https://github.com/mattpocock/skills/issues/611)). So HR's renderer should shuffle answers with a seed, and
  `build --check` should warn on unequal option lengths. Matt Pocock's own claim: "The /teach tests knowledge retrieval as well as just teaching"
  ([X](https://x.com/mattpocockuk/status/2076545046204071987), 3 likes).
- **Risk:** questions can leak held-back findings. Keep them after the pass, and phrase them about behavior, not bugs.

### 2. Measure it: time per file and stop, reveal events, quiz score in the export — `proposed`, cost S, target HR
- **Idea:** add timestamps per `focus` stop and per file, the reveal time, and quiz answers to the **Copy feedback**
  Markdown. Pair this with the canary-defect protocol from the earlier report.
- **Sources:** carried over from `agentic-dev-research/research/making-prs-easier-to-review/report.md`, the sections
  "Claims to validate" and "Self-instrumentation". It has not shipped: `HR/assets/app.js` stores viewed state and
  comments in `localStorage`, but no timing. Evidence: `our own idea` (from the earlier report).
  Supporting evidence for the second measure below: (Im)Paired Programming found that a completion metric missed the
  harm, and an "extend the code without the agent" task showed it
  ([arXiv 2607.26375](https://arxiv.org/abs/2607.26375)). Evidence for that result: `measured-RCT` (student sample).
- **Why it helps:** every other item here is a guess without it. It tells us whether a block saves minutes or only
  moves them. The extend task tells us whether the reader can still work once the page is closed.
- **Test:** 10 reviews with the export on. Check the timings add up to wall-clock time, and that viewed-but-skipped
  files show near-zero time. Beside the quiz, a second comprehension measure: a small follow-up change made by hand
  after reading the page, with the agent closed (extend it without the agent). Log whether the person can do it.

### 3. `teach-code`: stateful, mission-led lessons about a repo or one area of it — `proposed`, cost M (v1) / L (v2), target new skill in accelerate (reuses the HR renderer)
*Merges the old #3 (slice explainer), #10 (repo onboarding course), and #14 (learner profile), 2026-11-01, after
reading Matt Pocock's `teach`.*
- **Idea:** a user-invoked skill, `/teach-code <area | question | "this repo">`. It keeps a small learning workspace
  per repo **outside the repo's tree** (like HR's `.human-review/`, excluded from git), so state carries across sessions.
  - **v1 (M): one lesson.** Interview first, with 2–3 questions: what change are you about to make (the *mission*), and
    what do you already know here? Open from a screen or an endpoint the reader already knows, then the stops go
    behind it (the parts, the requests, the files). Then a short lesson about one slice at head, built from HR
    blocks: background, terms, a 3–6 stop reading order into real `code` blocks pulled from git, one diagram, a
    worked example (#4), and the quiz (#1). Name one "read this yourself next" file or doc, and say who to ask (#11).
    Apply HR's `build --check` and its "look at it" render step. That opening is Floorplan's "start from a screen"
    entry, kept inside this skill: it is how the lesson starts.
  - **v2 (L): a course.** Numbered lessons in execution order (entry point → one traced flow → edges); durable
    reference cards (glossary, module map, flow) kept apart from the lessons; `learning-records/` written only when
    the quiz or your answers *show* understanding, a disclosed prior skill, or a fixed misconception; earlier quiz
    items brought back for spaced review; and a stop rule ("you can make the change; go do it").
- **Sources:**
  - Matt Pocock's `teach` ([SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md), [docs page](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md),
    MIT, in [mattpocock/skills](https://github.com/mattpocock/skills)). Its docs say that within code, "users report the
    most value from getting oriented in an unfamiliar codebase or a new team's stack". Launch posts on X:
    [X](https://x.com/mattpocockuk/status/2064023481398824993) (5,054 likes, 7,777 bookmarks, 909,811 impressions) and
    [X](https://x.com/mattpocockuk/status/2063988995692900439) (2,821 likes). His reply "/teach me about this codebase"
    ([X](https://x.com/mattpocockuk/status/2062973868344524834): 282 likes, 137 bookmarks).
  - A community "teach pr" skill (teach the checked-out PR "like a senior engineer onboarding them", with a chosen
    teaching level 1–4) was proposed for that repo and declined: "Cool idea, but not for this repo IMO"
    ([issue #727](https://github.com/mattpocock/skills/issues/727)). The space for a code-specific teacher is open.
  - The slice explainer evidence from the old #3: the Claude Code team's article
    ([X](https://x.com/addyosmani/status/2114604912520921136): 13,390 likes) and Simon Willison's
    [linear walkthroughs](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/).
  - The course evidence from the old #10: codebase-to-course ([repo](https://github.com/zarazhangrui/codebase-to-course),
    5,750 stars per the GitHub API on 2026-11-01), Understand-Anything (`tour[]`,
    [repo](https://github.com/Egonex-AI/Understand-Anything/), 89,517 stars per the API), DeepWiki, Google Code Wiki,
    CodeTour, and [Busjahn et al.](https://researchonline.gcu.ac.uk/ws/portalfiles/portal/24953094/ICPC2015_authors_version.pdf)
    (execution-order reading).
  - The onboarding-skill pattern "build and test first, then trace **one** real flow end to end with file:line, then
    stop": ECC's `codebase-onboarding`
    ([SKILL.md](https://github.com/affaan-m/ECC/blob/main/skills/codebase-onboarding/SKILL.md); ECC repo 294,392 stars
    per the API) and [claudeskills.page codebase-onboarding](https://claudeskills.page/skills/workflow/codebase-onboarding/).
  - **Floorplan**, the strongest new map-style baseline
    ([repo](https://github.com/haydenschmitty/floorplan); 2,069 stars per the GitHub API on 2026-11-02; created
    2026-10-27; current release v0.6.1, with v0.6.0 the previous tag). A Claude Code / Codex plugin.
    Dependency-free Node scripts scan files, imports, routes, and web requests, and match frontend requests to
    backend endpoints, including across repos. The model names the parts in plain English. The map is a local
    `floorplan/index.html`; the folder ignores itself in git. The map zooms from the app to a part, a file, and an
    endpoint. "Start from a screen" is the entry folded into v1 above. The Ask bar answers with a mini-map and a
    step-by-step walkthrough.
    "Update the floorplan" re-reads changed files and highlights Recent work. Edits in `floorplan/architecture.json`
    survive updates. X mention
    ([X](https://x.com/ai_algoit/status/2116825143930732789): 0 likes). Evidence: `vendor` + `engagement` (stars).
  - (Im)Paired Programming, for the extend-by-hand measure in the test
    ([arXiv 2607.26375](https://arxiv.org/abs/2607.26375)). Evidence: `measured-RCT` (student sample). See #1.
  - Evidence: `practitioner` + `engagement`, plus `measured-RCT` for retrieval and spacing (see #1) and for the
    extend-by-hand task.
- **Why a standalone skill, not part of HR:** different input (no diff), state across sessions, and invoked by the
  user before work starts, not after. It shares HR's renderer, block schema, quiz component, and git-truth rules, so
  it's cheap. HR, in turn, reads the learner records for #8.
- **What `teach` does that we should *not* copy:** a free-form HTML lesson for each run (its issues show lessons that
  missed their own script tags ([#1058](https://github.com/mattpocock/skills/issues/1058)), weren't rendered before
  hand-off ([#1109](https://github.com/mattpocock/skills/issues/1109)), and carried few citations
  ([#960](https://github.com/mattpocock/skills/issues/960))). HR's fixed renderer, build validation, and code pulled
  from git already prevent all three. Also don't copy "knowledge from web resources": for a repo, the primary source is
  the code at head, plus ADRs and docs in the repo.
- **Test:** v1 on three limitless areas Matt hasn't touched recently (for example the routing policy and the review
  stage). Run Pocock's `/teach` as-is on the same areas as the **baseline**. Measure quiz score, time to first correct
  edit, factual errors per lesson, and citation count per lesson. After the lesson, a small follow-up change made by
  hand with the agent closed (extend it without the agent), scored beside the quiz. Also check that the lesson's
  first stops are the code behind a screen or endpoint the reader named. v2 only if v1 beats both the baseline and
  reading cold. For v2: onboard to an unfamiliar public repo (for example `ky`) with the course vs. DeepWiki vs.
  Floorplan vs. cold, then make the same small change. Floorplan is the second baseline arm, beside DeepWiki.

### 4. Worked example with real values ("intuition with toy data") — `proposed`, cost M, target HR + item 3
- **Idea:** an `example` block that traces one concrete input through the changed path: input → each stop (file:line)
  → output, before and after. Values come from **running** a test or script, captured with a command (the Showboat
  pattern), not typed in by the model. If nothing can be run, the block is labeled *inferred*.
- **Sources:** Litt's explain-diff has an "Intuition" section: "Use concrete examples with toy data… include example
  data" ([gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)). Simon Willison's animated
  explanation made an algorithm "click" when a walkthrough didn't
  ([guide](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/)). Showboat pulls
  snippets with `exec` so they can't be hallucinated
  ([guide](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/)). Live runtime values
  next to code help comprehension: Projection Boxes ([CHI 2020](https://cseweb.ucsd.edu/~lerner/papers/projection-boxes-chi2020.pdf));
  low-granularity boxes did better than full-state boxes on comprehension tasks
  ([SIGCSE TS 2027](https://2027.sigcse-ts.acm.org/details/sigcse-ts-2027-Papers-1/166/How-Much-Runtime-State-Should-We-Show-Learners-An-EEG-Study-of-Feedback-Granularity-)).
  Evidence: `practitioner` + `measured-RCT` (education setting).
- **Why it helps:** diffs and prose are abstract. One traced example makes the behavior change visible, and it fits
  HR's "code on the page comes from git" honesty rule if the values are captured too.
- **Test:** on 5 behavior-changing PRs, compare quiz score and time with and without the block (alternate PRs). Check
  that every value shown reproduces with the recorded command.

### 5. Decision log sourced from the agent session — `proposed`, cost S–M, target HR (+ limitless)
- **Idea:** a visible `decisions` block: what was asked, what was assumed, alternatives tried and dropped, and why.
  Each entry is tagged by source (*user prompt*, *agent transcript*, *commit message*, *not stated*). HR could read
  the session transcript when it runs in the same conversation. In limitless, the source is the spec plus the
  implement log.
- **Sources:** Addy Osmani's *Agentic Code Review*: agent reasoning "is usually discarded the moment the diff is
  produced… review shifts from checking reasoning… to reconstructing intent"
  ([X](https://x.com/addyosmani/status/2066595308629594363): 1,714 likes, 3,249 bookmarks). Entire records sessions,
  prompts, and reasoning as git-linked checkpoints ([docs](https://docs.entire.com/guides/checkpoints/capture-checkpoints)).
  Haystack uses the coding-agent transcript to explain "why each hunk changed"
  ([X reply](https://x.com/AkshaySubr42403/status/2067331955494912104), 0 likes). Practitioners asking for the same:
  [@UditKhandelwal8](https://x.com/UditKhandelwal8/status/2082542780237352977),
  [@GandhiRohith](https://x.com/GandhiRohith/status/2067630870996103481) (low engagement).
  **DiffNotes** is the same premise, built: the agent that wrote the PR annotates it with a summary, a deploy card
  (migrations, flags, rollback), a risk list, and one why-not-what note per changed block. A browser extension
  overlays the notes on GitHub's Files changed tab. Nothing is posted to the PR. Notes expire. Per-repo rules live
  in `.diffnotes.yml` (the rules file is #9)
  ([DEV, 2026-11-01](https://dev.to/igorkasyanchuk/i-made-my-coding-agent-explain-its-own-pull-requests-j67),
  [repo](https://github.com/igorkasyanchuk/diffnotes), 3 stars per the GitHub API on 2026-11-02). Evidence:
  `practitioner` (low engagement).
  **Flatbread** is a handoff that keeps the dead ends from a Claude Code, Codex, or Cursor session, so the next
  agent can pull an execution brief
  ([X](https://x.com/bulentongun/status/2116366373920391218): 7 likes). Evidence: `engagement` (low).
  The earlier report recommended "label each why by source; write *why: not stated*" (`report.md`, row "Brief and
  summary drawn from…"). It hasn't shipped: HR tags signals and `risk.why`, not the brief or rationale. Evidence
  for the item: `practitioner` + `vendor`.
- **Why it helps:** "what instigated the change" is reviewers' biggest information need (Bacchelli & Bird, cited in
  the earlier report). The agent already has that information, and HR throws it away.
- **Test:** on 5 agent-built changes, have Matt rate each entry as accurate, useful, or neither, and count the
  `not stated` gaps. Make sure no decision entry leaks a held-back finding.

### 6. "Ask about this" from any line or block, answered in the agent session — `proposed`, cost S, target HR
- **Idea:** next to **Comment**, add **Ask** (a question tagged `?`). The feedback export puts questions first. The
  agent answers in chat and, when the answer belongs on the page, adds it as a `note` and rebuilds. This keeps the
  one-file, no-network design.
- **Sources:** PR chat is a common feature in review tools: Tembo Review "Ask about selected code… why they changed"
  ([Tembo](https://www.tembo.io/review)) and Graphite Chat "get instant context on code changes"
  ([Graphite](https://graphite.com/)). GILT, an in-IDE LLM helper, raised task completion (+0.47 sub-tasks, p<.01)
  but **not** quiz scores ([Nam et al., ICSE 2024](https://arxiv.org/html/2307.08177v3)). Evidence: `vendor` +
  `measured-RCT` (mixed).
- **Why it helps:** a static page can't answer the reader's own question, and that is usually the one that blocks
  understanding. The cost is small because the feedback loop already exists (`HR/SKILL.md` "When feedback comes back").
- **Test:** count the questions per review and how many answers turned into page edits. Also check whether question
  areas match wrong quiz answers.
- **Note from `teach`:** a request to let learners annotate a lesson in place was declined in favor of "just make notes
  in the chat window" ([issue #519](https://github.com/mattpocock/skills/issues/519)). HR's export makes in-place notes
  cheap without a server, so the cost argument against it doesn't apply here. The lesson to take is to keep it one
  button, with no new UI mode.

### 7. Structural blast radius and "what it's wired into" map — `proposed`, cost M, target HR
- **Idea:** replace or extend HR's `git grep -w` blast radius with a tree-sitter import/call graph that is 1 hop from
  the changed symbols. Show it as a small diagram of changed and affected nodes, and say "calls" only when the parser
  resolved the call. Fall back to today's text search.
- **Sources:** Understand-Anything `/understand-diff` and its deterministic `computeDiffOverlay` (changed nodes plus
  1-hop affected nodes, no LLM) ([PR #574](https://github.com/Egonex-AI/Understand-Anything/pull/574),
  [repo](https://github.com/Egonex-AI/Understand-Anything/)). X: [@techNmak](https://x.com/techNmak/status/2056477994328396263)
  (101 likes, 109 bookmarks) and [@prasenx](https://x.com/prasenx/status/2058119202712723632) (227 likes, 484 bookmarks;
  the tool isn't named in the text). Practitioner need: "the diff reads fine and you still have no idea what it wired
  itself into" ([X](https://x.com/aiupdatelog/status/2111502507633701033), 0 likes).
  **Floorplan** is the other pattern to copy: dependency-free Node scripts scan files, imports, routes, and
  request-to-endpoint matches, including across repos, and the model only names the parts
  ([repo](https://github.com/haydenschmitty/floorplan)). That request-to-endpoint match is a cross-boundary edge
  HR's grep does not see. See #3 for the rest of the tool.
  **Dyff** offers full-repo symbol search during review (call chains and every use of a symbol, per its README)
  ([site](https://www.dyff.sh/), [repo](https://github.com/dyffs/dyff), 0 stars per the GitHub API on 2026-11-02).
  The site did not load on 2026-11-02, and the README does not describe grouping a 34-file PR into 4-5
  dependency-order stages, so that claim stays unchecked. The walkthrough half (what to read first) is noted on
  the split advisor. Evidence: `vendor` + `engagement`.
- **Why it helps:** HR's blast radius is honest but text-only, covers 5 languages, and says "mentioned", never
  "called" (`HR/SKILL.md` "Blast radius"). A resolved graph answers "what else does this touch" faster.
- **Test:** on 5 PRs, compare the grep and graph outputs by hand: false mentions removed, real callers missed. Time to
  answer "who calls this?"

### 8. Two-depth background (newcomer vs. owner) — `proposed`, cost S, target HR
- **Idea:** split `background` into a *deep background* (collapsed when the git signals say the reader has history in
  these files) and a *narrow background* that is always open.
- **Sources:** Litt's prompt: "include a deep background for beginners (note that it can be skipped if the reader is
  already familiar), and then a more narrow background directly relevant to the change"
  ([gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)). This is the earlier report's #10
  "familiarity-adaptive density", which hasn't shipped. HR always writes for a newcomer (`HR/SKILL.md` "Write for
  someone new to this code"). Evidence: `practitioner` + `measured-obs` (Bacchelli & Bird, via the earlier report).
- **Add a level check, the gap `teach` users report most:** "There is no assessment step… It never did grilling to
  establish my starting point" (`teach` docs, [common questions](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md); request
  [#725](https://github.com/mattpocock/skills/issues/725)). Collapse or open the deep background from (a) the git
  signals, (b) the learner records from #3, or (c) when neither exists, one optional question at the top ("new to this
  area?"). The community "teach pr" skill asks for a teaching level 1–4 up front
  ([#727](https://github.com/mattpocock/skills/issues/727)).
- **Caution from TARS** ([arXiv 2607.15948](https://arxiv.org/html/2607.15948v1)): an in-IDE agent profiles
  expertise and role and adapts explanation depth. Within-subjects, n=18, on Java snippets: 26% faster (mean 224.0s
  vs 304.08s; Mann-Whitney p=0.085, not significant) and no correctness difference (cosine similarity to a
  ground-truth docstring, 0.888 vs 0.886, p=0.18). Self-reported load was lower; the NASA-TLX tests in the results
  are against the scale midpoint in the TARS condition. Adapting depth may save time. It has not been shown to
  improve understanding. Keep this item at cost S, and keep quiz score as the guard. Evidence: `measured-RCT`
  (small, null on correctness).
- **Test:** time on top-of-page for owned vs. unfamiliar areas, with quiz score held constant. Quiz score is the
  guard: a faster top of the page with a lower quiz score fails.

### 9. Per-repo explanation rules file — `proposed`, cost S, target HR
- **Idea:** a repo-owned rules file the page must satisfy. Example: a migration must get a deploy note and a
  rollback note. `build --check` fails when a required note is missing.
- **Sources:** DiffNotes reads a `.diffnotes.yml` on the base branch before the agent writes notes. The post's
  example is "every migration needs a deploy note"
  ([DEV, 2026-11-01](https://dev.to/igorkasyanchuk/i-made-my-coding-agent-explain-its-own-pull-requests-j67),
  [repo](https://github.com/igorkasyanchuk/diffnotes), 3 stars per the GitHub API on 2026-11-02). The fail-closed
  `build --check` is ours; DiffNotes describes the agent reading the rules. See #5 for the rest of the tool.
  Evidence: `practitioner` (low engagement).
- **Why it helps:** HR already checks that claims match the diff. A rule makes a missing deploy or rollback note a
  build failure on the changes that need one.
- **Why it sits here:** effort is S because `build --check` already exists. The gain shows up on the PRs a rule
  names (migrations, config) and is absent otherwise, and the only evidence is one low-engagement tool. That puts
  it under the always-on items #6–#8 and above the split advisor.
- **Test:** on limitless PRs that touch migrations or config, a missing required note fails `build --check`, and a
  present note passes.

### 10. Split and size advisor — `proposed`, cost S–M, target HR
- **Idea:** when the concerns show more than one independent cluster, or the estimated reading time is more than one
  sitting, say so at the top and propose the split. Flag it when the concerns cover more than the brief claims.
- **Sources:** the earlier report's #8 (Barnett, Baum 2019, Paul). It hasn't shipped: no split or size advice in
  `HR/scripts/human-review.mjs`. Evidence: `measured-RCT` / `measured-obs` via the earlier report.
  Dyff's README says its walkthrough tells the reviewer what to read first and what to skip on a large diff
  ([repo](https://github.com/dyffs/dyff), 0 stars per the GitHub API on 2026-11-02;
  [site](https://www.dyff.sh/), which did not load on 2026-11-02). The README does not describe a 34-file PR grouped
  into 4-5 dependency-order stages, so that claim stays unchecked. Not enough to move this item. The symbol-search
  half is noted on #7. Evidence for Dyff: `vendor`.
- **Test:** on 10 past limitless PRs, does the advisor's split match what Matt would split?

### 11. "Who to ask" for the area — `proposed`, cost S, target HR + #3
- **Idea:** one visible line naming the two or three people with the most recent commits to the slice or changed files,
  computed by `collect` from git (HR already computes ownership for its signals). It sits beside "What I need from
  you" or at the end of a lesson. It's a fact, never a judgment.
- **Sources:** `teach`'s "Acquiring Wisdom" section: answer, then "delegate to a **community**" where the learner can
  test their skills ([SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)). For a repo, the community is the code's owners. Onboarding
  skills check the same thing (`git shortlog -sn --since="1 year ago"` "who knows the code",
  [claudeskills.page](https://claudeskills.page/skills/workflow/codebase-onboarding/)). Evidence: `practitioner`.
- **Note:** HR's privacy rules already say signals name contributors, so check before sharing (`HR/SKILL.md`
  "Security and privacy").
- **Test:** for 10 pages, ask Matt whether the named people are the ones he would ask.

### 12. Explain the core change from two or three angles — `proposed`, cost S, target HR + #3
- **Idea:** for the core of a change, give two or three short explanations, each from one angle: what it does,
  which concept it relies on, and why it exists.
- **Sources:** Bernstein et al. randomized 971 first-year students to three diverse LLM explanations (each
  emphasizing a different aspect; the paper's examples are function, concept, and goal) or three generic
  explanations. Open-ended accuracy was about 7.7% higher with the diverse set. Multiple-choice accuracy was
  already high (>87%) and did not differ. The open-ended difference was not significant after Bonferroni
  (z=2.15, p=0.095). The abstract reports no difference in perceived cognitive load
  ([arXiv 2606.28882](https://arxiv.org/abs/2606.28882)). Evidence: `measured-RCT` (education, weak).
- **Why it helps:** one true paragraph can still miss the angle the reader needed. Two or three angles are a small
  addition to the background block and to a #3 lesson.
- **Why it sits here:** the effect did not clear a multiple-comparison correction, and the setting is an intro
  programming course. Cheap to try, and below "Who to ask" (#11), which has a clearer mechanism.
- **Test:** alternate PRs with and without the extra angles and compare quiz score.

### 13. Interactive or animated explainer for the algorithmic core — `proposed`, cost M, target HR (gated)
- **Idea:** for a change whose core is an algorithm or state machine, allow one `interactive` block (a sandboxed
  inline script, still no network) that steps through it.
- **Sources:** [Simon Willison, interactive explanations](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/).
  Litt: "Why are we still reading raw code diffs as the primary UI?"
  ([X](https://x.com/geoffreylitt/status/2019792700023672859): 446 likes, 122 bookmarks). The Claude Code account's tip
  on HTML artifacts to learn from a codebase ([X](https://x.com/claude_code/status/2035966532438863965): 53 likes,
  69 bookmarks). Caution: the earlier report found diagram payoff unproven outside complex tasks (Arisholm). Evidence:
  `practitioner` + `engagement`.
- **Test:** only on PRs tagged algorithmic. Compare quiz and time with and without the block.

### 14. Attach the page to every limitless PR — `proposed`, cost M, target limitless
- **Idea:** limitless's deliver stage runs human-review's `collect`/`build` and attaches `review.html` (or a link) to
  the PR's evidence report.
- **Sources:** Latitude added "a CI step to every PR… that generates an interactive HTML review artifact"
  ([X](https://x.com/geclos/status/2073028203329810437): 5 likes). lucidiff does PR → one HTML explainer, with
  citations checked ([repo](https://github.com/Rishabjs03/pr-karpathy)). Evidence: `practitioner` (low engagement).
- **Note:** HR's privacy rules say not to publish the page unless asked (`HR/SKILL.md` "Security and privacy"), so
  keep it as a local or private artifact.
- **Test:** 10 limitless runs. Does Matt open the page before the diff, and does review latency change?

### 15. "Since you last looked" interdiff — `proposed`, cost M, target HR
- **Idea:** when a page is rebuilt after feedback, show the delta from the last version the reviewer saw (changed
  hunks, and which notes changed) and keep the old comments attached to unchanged lines. Today the new page "starts
  clean" (`HR/SKILL.md` "When feedback comes back").
- **Sources:** `our own idea`. A related review-quality idea is the code-review backlog's C3 "re-review only the fix
  diff".
- **Test:** count re-read minutes on the second round across 5 feedback loops.

---

## Shipped (in human-review today)

| Idea | Where | Notes |
|---|---|---|
| Diff → one self-contained HTML page; branch, PR, range, **uncommitted** work | `HR/SKILL.md` "Decide the scope"; `HR/scripts/human-review.mjs` | Covers PRs and uncommitted changes. Not whole-repo onboarding (item 3). |
| Code on the page comes from git; annotations checked against real lines | `HR/SKILL.md` "Honesty", build `--check` | Same idea as Showboat's exec-pulled snippets. |
| Reading order (`focus`, 3–6 stops, riskiest first) | `HR/SKILL.md` "fields that carry the most weight" | Matches the "literate diff" and tour-mode ideas (Litt, Tembo Tour Mode, constellagent code tour). Replicas Review's guided tour (2026-10-21) puts a plain-English explanation above each file's diff, starts with the most important file, and collapses tests, lockfiles, and generated files at the end ([post](https://replicas.dev/blog/replicas-review)). That matches this row and the mechanical tier below. |
| Group by concern, tests next to their code, callees first | `HR/SKILL.md` `concerns` | Earlier report #1. |
| Written for a newcomer: `background` ("Before this change"), `terms` with hover underlines, readability warnings | `HR/SKILL.md` "Write for someone new to this code"; `HR/references/format.md` | Like Litt's "Background" and codebase-to-course's glossary tooltips. |
| Annotated diffs (note / decision / risk / question), 2–5 per file | `HR/SKILL.md` "Annotations" | |
| Visuals: wireframes, data model, API, states matrix, Mermaid, diagrams, `code` of any file at head | `HR/references/{format,wireframes,diagrams}.md` | Like CodeRabbit sequence diagrams and lucidiff's flow diagram. |
| Findings held back until the reviewer's own pass | `HR/SKILL.md` "The reviewer reads before they see your conclusions" | Earlier report #3. |
| Proven mechanical / generated tier | `HR/SKILL.md` `files` | Earlier report #2. |
| Git signals with provenance tags (verified / author text / inference) | `HR/SKILL.md` "Signals" | Earlier report #4. |
| Text blast radius (JS/TS/Py/Go/Ruby) | `HR/SKILL.md` "Blast radius" | Item 7 upgrades it. |
| "What I need from you" + tests cover / don't cover | `HR/SKILL.md` `ask`, `tests` | Earlier report #6. |
| Precision check on every claim | `HR/SKILL.md` "Precision check" | Earlier report #7. |
| Comment, verdict, and **Copy feedback for the agent** loop | `HR/README.md`; `HR/assets/app.js` | Like hunk-review-changes / constellagent "submit to agent". |

## Hand off to Code Review Research Bot (review quality and bug finding, out of scope here)

- **Macroscope Check Run Agents**: custom agents on every PR as GitHub check runs
  ([X @svpino](https://x.com/svpino/status/2050262803475472687): 47 likes, 39 bookmarks;
  [X @ai_for_success](https://x.com/ai_for_success/status/2050261619939361210): 22 likes).
- **"Battle review"**: a second agent argues against each hunk's author explanation (nitpick / concern / blocking)
  ([hunk-review-changes](https://github.com/lucianghinda/hunk-review-changes)).
- **OpenAI's Codex plugin for Claude Code**: `/codex:review` and `/codex:adversarial-review` of uncommitted changes
  ([X](https://x.com/rezaul_arif/status/2043509181320413621), 1 like; not checked against OpenAI's docs).
- **OpenQodex**: OSS review CLI for unpushed and uncommitted changes ([X](https://x.com/DanKornas/status/2110154613680902197): 39 likes).
- **Claude Code team review process**: incident-causing PRs used as a daily eval set; PRs merged more than doubled while
  the revert share fell by more than 40% (June–September). Article posted on @addyosmani's account
  ([X](https://x.com/addyosmani/status/2114604912520921136)).
- **Steinberger claim** (second-hand): auto-review in a separate session after the PR loses judgment
  ([X](https://x.com/4to1planner/status/2075105831230800376)). Unverified paraphrase of an interview.
- **lucidiff "Risks"**: severity plus failure mechanism, citations checked against the diff
  ([repo](https://github.com/Rishabjs03/pr-karpathy)).
- **Tembo automated review** that runs tests and builds before posting ([Tembo](https://www.tembo.io/blog/tembo-vs-boat));
  **Graphite AI Reviews** ([Graphite](https://graphite.com/)); **CodeRabbit** review findings
  ([docs](https://docs.coderabbit.ai/pr-reviews/walkthroughs)).
- Practitioner loop: Claude writes the code, then "codex to review uncommitted changes"
  ([X @dejavucoder](https://x.com/dejavucoder/status/2035238484261445807): 573 likes, 88 bookmarks).
- **Explainable AI and trust in AI-assisted code review**: within-subjects, n=34, three explanation levels. Full
  explanations gave the highest perceived trust (M=3.99/5) and moderate explanations gave the highest agreement
  with the AI recommendation (89.22%). No explanations were lowest on both. Explanation level did not
  significantly affect review time
  ([arXiv 2607.24601](https://arxiv.org/abs/2607.24601)).

## Merged

- **Old #3 slice explainer, old #10 repo onboarding course, old #14 learner profile → #3 `teach-code`** (2026-11-01).
  They are the same skill at three sizes: one lesson, a course, and the state that connects them. `teach` shows the
  state layer is what makes a multi-session course work (mission, learning records, zone of proximal development).

## Changes in draft 2 (2026-11-01)

- #3 rewritten as `teach-code` (merges old #3, #10, #14). Ranked #3, unchanged position.
- #1 quiz: added `teach`'s answer rules and the "shuffle in the renderer, not the prompt" fix.
- #6 Ask: added `teach` issue #519 context.
- #8 two-depth background: added the level check (`teach`'s most reported gap).
- New #10 "Who to ask" (from `teach`'s "wisdom → community" idea).
- Old #11–#13 keep their content as #11–#13. Old #10 and #14 removed (merged).

## Changes in draft 3 (2026-11-02)

- #1 and #2: (Im)Paired Programming added as supporting `measured-RCT` evidence. #2's test adds an "extend it
  without the agent" task beside the quiz. The same task is in #3's test.
- #3: Floorplan added as the map-style baseline, and as a second baseline arm in the v2 test (beside DeepWiki).
  "Start from a screen or endpoint the reader already knows" is folded into #3's opening. It is how the lesson
  starts, so it stays in this skill.
- #5: DiffNotes and Flatbread added as sources.
- #7: Floorplan's deterministic scan (model only for names; request-to-endpoint matching). Dyff noted on #7 and on
  the split advisor (#10).
- #8: TARS added as a caution. Cost stays S. Quiz score stays the guard.
- New #9 "Per-repo explanation rules file", from DiffNotes' `.diffnotes.yml`. Cost S, target HR. Placed under
  #6–#8 and above the split advisor: `build --check` makes it cheap, and it only fires when a rule matches, on
  one low-engagement source.
- New #12 "Explain the core change from two or three angles". Cost S, target HR + #3, below "Who to ask". The
  education RCT's open-ended gain was not significant after Bonferroni (p=0.095).
- "Who to ask" is now #11. The old #9–#13 are now #10–#11 and #13–#15.
- Shipped reading-order notes: Replicas Review guided tour.
- Hand-off: the XAI trust study ([arXiv 2607.24601](https://arxiv.org/abs/2607.24601)).

## Rejected

_(none yet)_


