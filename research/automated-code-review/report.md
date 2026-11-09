# Automated code review

*Draft 1, 2026-10-31.*

*Sweep 2026-11-09: ReviewBoundary (§2.4), Codex custom review rules (§2.3), Devin Review 2.0 (§2.3). Opened 2026-11-09.*

Status: first draft, written to be revised once Matt's prior docs are folded in further. Every
external source below was opened on 2026-10-31, except CR-Bench-v2 (opened in the 2026-11-04
daily sweep and again on 2026-11-05), Foresight-SWE (opened 2026-11-05), and ReviewBoundary,
the Codex custom-rules post, and Devin Review 2.0 (opened 2026-11-09); anything that could
not be opened is listed in "Not verified". Numbers from different benchmarks are not comparable.

**Precedence for Matt's figures** (as instructed): the 2026-10-31 escapes-dev run beats Phase 0
`RESULTS.md` (2026-10-29), which beats the working notes on overlapping figures; where the notes
are newer than RESULTS (sections e6–e10, 2026-10-31), the notes win.

Tags: **[Matt]** = Matt's prior work (limitless repo or attached docs), **[PR]** peer-reviewed,
**[arXiv]** preprint, **[IB]** independent benchmark, **[VB]** vendor post, **[doc]** vendor docs,
**[X]** practitioner post, ⚠️ thin evidence.

Limitless links are pinned to commit `fb48dbc` (main, 2026-10-31 21:52 EDT):
`L/` = `https://github.com/MattFlower/limitless/blob/fb48dbc76fc6424787e4a1909a602d280ad8b522/`.
Matt's attached docs (not in the repo): *Fix the ruler, then widen the search* ("Report"),
*Review stage: plan to gain ≥10 points* ("Plan", draft 1 2026-10-29), Phase 0 `RESULTS.md`
("RESULTS"), *Fresh review runs on escapes-dev (2026-10-31 overnight)* ("Escapes-dev"), the
review-stage working notes ("Notes"), and the approved labelling rubric ("Rubric", 2026-10-30).

---

## 0. Where accelerate starts

- **There is no code-review skill in accelerate yet.** The repo (`MattFlower/accelerate@15bda99`)
  has one skill, `skills/human-review/`, which turns a change into an HTML review page for a
  person; it is not a defect finder. No issues or PRs exist; no prior code-review, eval or backlog
  docs are in the repo.
- Conventions a new skill should follow, from `human-review`: self-contained skill folder
  (`SKILL.md`, `scripts/`, `references/`), zero-dependency Bun/Node CLI, code on the page comes
  from git not the model, a "precision check" that re-opens every cited line, private output under
  `<repo>/.<skill>/`, and a "feedback → agent" loop. Plugin manifest `.claude-plugin/plugin.json`
  loads `./skills/`, so a new skill is invoked as `/accelerate:<name>`.
- `human-review/SKILL.md` says "in one production study, about one in five AI review comments made
  claims the diff didn't support" without a citation. I couldn't trace it to a source; it should
  get one or be reworded.

## 1. Matt's prior work is the main evidence base [Matt]

Limitless (a software factory) has run a measured, pre-registered review-improvement program
since 2026-09-28. Its datasets, labelling rules and results outrank anything generic here,
because they were measured on real escaped defects in a TypeScript repo with the same two CLIs
(Claude Code, Codex) this skill must run in.

### 1.1 What limitless's docs and evals contain

- `L/docs/research/08-code-review.md` (2026-09-28): literature + industry survey, Limitless's own
  outcome data (54 escaped defects; recall, not pickiness, is the problem), the M4.5 design.
- `L/docs/research/14-review-strength.md` (2026-10-14, appendices to 10-31): error analysis of the
  30 production misses, a literature scan by lever, pre-registered proposals A1–A8, lab-prompt
  variants (App. C) and severity calibration (App. D).
- `L/docs/EVALS.md`: harness design — evaluate in our own harness, deterministic graders,
  contamination-proof standalone checkouts and *snapshot mode*, Wilson intervals, paired
  bootstrap, `eval regrade`/`resume`, escape-case generation.
- `L/evals/review/cases.json` (243 cases: 198 real, 45 clean; splits dev 49, heldout 33,
  escapes-dev 51, escapes-heldout 57, 53 unsplit) and `L/evals/review/LABELS.md` (every
  pre-registered labelling rule, audit and outcome), plus `TRACE.md` / `trace-*.json` (variant E).
- `L/src/evals/judge.ts` (two-judge semantic matcher, landed as PR #1059) and
  `L/src/pipeline/prompts.ts` (the standard / adversarial / careful / trace / probe prompts).

### 1.2 Findings Matt has already established (use these; don't re-research them)

**Measurement**
- **The ±5-line location grader is noisy both ways:** about 20% of its credits were a different
  defect nearby and about 4% of misses were the same defect elsewhere (caller, root cause, just past
  ±5). It is not mainly biased toward conservative systems (Notes, 10-29 credited audit; RESULTS).
- **Two blind text judges from different vendors, one-to-one SAME matching, "both must match"**,
  with a code-reading tiebreak on contested items: judges agreed with hand audits ~94% (Terra 94.1%,
  n=388; Claude 93.5%, n=339) and with each other 97.4%; judge errors cluster below confidence 0.7;
  on 55 contested items "both judges" matched code reading 45 times vs 40/35 for one judge alone
  (RESULTS). Implemented as `L/src/evals/judge.ts`; `JUDGE_RULE` defines SAME as the same failure
  mechanism, at any location, ignoring severity. The Phase 0 Python scripts named in RESULTS
  (`judge_prompt.py`, `validate_judges.py`, `rescore.py`, …) live in Matt's orchestrator workspace,
  not in the repo; `judge.ts` is the in-repo port.
- **"Clean" cases are often not clean.** Audits found real ≥medium defects in 6 of 19 M4.5 clean
  PRs and in 12 of 17 #235 "false blocks" (Report); all three M5.2 held-out clean cases
  (review-068, 092, 108) were defective, confirmed by both vendors with reproductions
  (`L/evals/review/LABELS.md`, held-out clean-case audit 2026-10-30). review-068's skipped-test
  defect was later fixed by #647 after causing ~20 of 49 needs_human runs (Rubric). Clean controls
  need blind two-vendor vetting, not just "no later fix".
- **A clean set of 8 trials can't bound false blocks** (95% upper bound on a block-rate rise ≈37.5%);
  +10 points at 80% power needs ~160–200 gold defects at k=2 or ~110–130 at k=4; same-system runs
  differ 8–10 points (Plan; Report, citing Miller 2024 and Bowyer et al. 2025).
- **Pool gold is biased** toward arms that report more distinct defects, because pooled defects
  come from those arms' own findings (RESULTS, Phase 1 rescore caveat).
- **Gold comes from a procedure, not a better model:** the orchestrator writes a 1.5–2 KB
  PR-specific brief (requirements as checkable claims, every caller that must adopt a check, test
  inputs, targeted questions), runs it on Sol@high with write access for failing tests, then runs a
  mutation check (revert the source diff; the PR's tests must fail) (Report; Notes).

**Reviewer results** (judged recall = two-judge matcher, blocking findings only)

| Arm | Escapes-dev 10-31 (80 defects, k=2) | Phase 0 dev (old gold) | Held-out (Phase 0) | Clean blocks |
|---|---|---|---|---|
| production sol-6.1@medium, standard | **16.9%** (27/160) | 31.6% | 18.6% | 2/32 dev (Notes e7); 2/20 true held-out |
| sol-6.1@high | **30.6%** (+13.8) | 41.8% (+10.2) | not run | 3/8 dev (Phase 0) |
| adversarial prompt (E3) | **28.5%** (+11.6) | 49.0% (+17.4) | 25.6% (+7.0) | — |
| union of 2 adversarial samples (D) | **36.2%** (+19.4) | 47.4% (+15.8) | 33.0% (+14.4) | **4/20 vs 2/20 true held-out (doubling)** |
| terra-6.1@medium adversarial | **28.7%** (+11.9), $0.03/review, p50 0.5 min | — | — | 6/32 dev (Notes e7) |
| Terra adversarial ×2 union | 36.9% (Notes e7) | — | — | 8/32 dev |
| specialist panel (Sol@medium verifier) | ~41.6% partial (Notes e7) | — | — | 13/32 dev |
| luna@medium | 2.5% / 4.4% — not viable | — | — | — |
| haiku-5.5@high | partial; 17/32 reviews over 20 min | — | — | — |

Evals: escapes-dev main `eval-mvw0y6v31sec2vc1agx2t1`, cheap `eval-mvvv3pum0kriw040gi0x29`;
clean-block arms in Notes e7–e10 (`eval-mvwk3pn5…`, `eval-mvwniug6…`, `eval-mvwnjdnp…`,
`eval-mvx3koae1kebh1d07r3w9f`). Gains replicate on defects nobody tuned against; ranking holds
(D > sol@high ≈ E3). False blocks on escape cases are unmeasured (all escape cases are real);
held-out (escapes-heldout, 57 cases / 103 defects) hasn't been run (Escapes-dev).

**Arms that underperformed** (RESULTS, Phase 0 judged / Phase 1 pool-gold combined, vs production)
- Trace finder E (second agent searching callers/entry points): +1.1 / +3.4.
- Probe + setup (reproduce or demote): −9.2 / −6.4 — execution used as a *filter* cut recall.
- Opus as the sole reviewer: −21 / −17 (opus, opus@high) on dev; −9.3 / −6.9 combined. Opus as an
  *extra union finder* adds about +5–9 (Sol 30.6% → ∪ Opus blocking 35.7% → ∪ Opus any severity 39.8%).
- Causal-attribution verifier: null (#235). Cross-vendor verifier: no change; M4.5 panel verifier
  confirms ~94% of candidates, so it doesn't discriminate; the M4.5 panel gave +16 points recall
  at 3.5× false blocks (Notes).
- **Agreement-gated blocking ("block only when both D samples agree") replayed at ~0–1% recall**,
  because the ±5-line merge almost never records agreement; it needs semantic dedupe first (RESULTS 0c).
- **Severity calibration by prompt wording is a null:** five finder-prompt variants all landed at
  6–9/32 clean blocks; the calibrated prompt changed *which* clean cases block, partly by misapplying
  the "explicit requirement" exception to an issue's Out-of-scope list (Notes e10).
- **Clean-case blocks are mostly real-but-minor claims:** a blind two-vendor audit found 20 of 22
  distinct blocking claims true; Opus rated all minor, Sol rated 8 major (Notes e8;
  `L/docs/research/14-review-strength.md` App. C). Severity, more than detection, separates these
  blocks from gold.
- **LLM severity raters don't transfer without a tuned rubric:** v2 raters agreed with Matt's blind
  validation 13/20 (65%), every miss calling a harmless effect "wrong" or a contrived trigger
  plausible; v3 (adds a "nuisance" consequence and a harm threshold) reached 18/20 on a fresh 20 and
  was adopted, with splits going to a human ruling (Notes e2).
- **Checklist F tension (unresolved, for Matt):** the AGENTS.md per-item checklist scored +14.6
  judged on its own 33-case cohort (19/48 vs 12/48), yet the Plan's Don'ts list "long pattern
  checklists" (the Report cites Anthropic's Defending Code harness: "goal plus context" works
  better than long checklists). I have not resolved this.

**Where the reviewer misses** (`L/docs/research/14-review-strength.md` §2; production sol@medium, dev)
- Of 30 misses: 13 needed files outside the diff, 9 needed running code with an adversarial input,
  7 were visible in the diff, 1 needed a project convention. 18 of the 30 were found by no system.
- By category: security 0/12 defect-trials, spec-mismatch 0/6, privacy 9/30.
- Sol stops early: 1.1 findings per eval trial using ~2 of 20 minutes; 0.57 findings per production
  review across 299 reviews. Opus files findings but rates them minor (Report).
- 22 of the 30 misses match a recurring-defect pattern the repo already lists (canonicalize then
  check 8, redaction order 7, one guard every path 5, compatibility 4, trust 2, check-then-act 2,
  derive state 2).
- The Rubric's pilot: redaction gaps with an unusual trigger were 5 of 47 findings.

## 2. External evidence, by theme

Only items I opened. Where Matt's docs already cite an item, it's marked "(in Matt's docs)".

### 2.1 Context: out-of-diff bugs are the hard ones

- **CRBugBench** [arXiv 2610.13668](https://arxiv.org/abs/2610.13668): agents differ in persistence —
  half of gpt-5.6-sol runs end by turn 17 vs turn 35 for opus-5; Opus executes code in 9.7% of turns,
  Sol 6.9%; agents trust misleading PR descriptions and miss repository-wide behaviour. (in Matt's docs)
- **SWE-PRBench** [arXiv 2603.26130](https://arxiv.org/abs/2603.26130): 350 PRs; 8 frontier models
  catch 15–31% of human-flagged issues diff-only, and all 8 *degrade* as more file/repo context is
  stuffed into the prompt; a 2,000-token structured diff+summary beat a 2,500-token full-context
  prompt. Judge κ=0.75. (in Matt's docs)
- **OpenAI Codex reviewer** [alignment.openai.com](https://alignment.openai.com/scaling-code-verification/):
  repo-wide tools and execution improved both recall and precision over diff-only GPT-5; precision
  is prioritised for adoption; authors change code for 52.7% of comments. (in Matt's docs)
- **Cursor Bugbot** [cursor.com/blog/building-bugbot](https://cursor.com/blog/building-bugbot): the
  biggest gain came from going fully agentic (the model pulls its own context); the agent was then
  *too cautious*, so prompts were made aggressive; bugs/run 0.4 → 0.7, resolution rate 52% → 70%+.
  (in Matt's docs)

### 2.2 Find wide, filter separately; union, don't vote

- **SWR-Bench** [arXiv 2509.01494](https://arxiv.org/abs/2509.01494): 1,000 verified PRs; LLM-based
  coverage judge ~90% agreement with humans; a simple multi-review aggregation raised F1 by up to
  43.67%. (in Matt's docs)
- **c-CRAB** [arXiv 2603.23448](https://arxiv.org/abs/2603.23448): review comments graded by tests that
  fail at head; union of tools beats the best single tool (figures in Matt's research/08). (in Matt's docs)
- **Bugbot v1** used 8 passes with randomized diff order + majority vote + validator; v2 dropped the
  fixed pipeline for an agent (same Cursor post). Majority vote is in Matt's Don'ts.
- **Beyond Consensus** [arXiv 2510.11822](https://arxiv.org/abs/2510.11822): LLM validators accept valid
  items readily but reject few invalid ones; consensus made it worse (per Matt's Report). (in Matt's docs)
- **Witnesses discriminate:** CMU/SEI static-alert adjudication [arXiv 2607.09979](https://arxiv.org/abs/2607.09979)
  (no false positive produced a valid trigger; 60% of true positives did, per Report). (in Matt's docs)
- ⚠️ **[X]** practitioners converge on the same shape: one reports 73% false positives across 344
  hand-checked findings until "a second adversarial pass tries to kill it first"
  ([post](https://x.com/_alphashark_/status/2097274562077508040)); another requires a failing test
  before a bug claim ([post](https://x.com/terminalxw/status/2097213279240413198)). Anecdotes;
  note the second conflicts with Matt's "no reproduce-or-drop" finding.

### 2.3 Severity, caps and what developers act on

- **Anthropic Code Review** [blog](https://claude.com/blog/code-review), [docs](https://code.claude.com/docs/en/code-review):
  find (parallel agents) → verify → dedupe and rank → post; three severities: 🔴 Important (fix before
  merge), 🟡 Nit, 🟣 Pre-existing ([severity docs](https://code.claude.com/docs/en/code-review-pull-requests.md));
  substantive comments on 54% of PRs vs 16% before; "less than 1% of findings are marked incorrect";
  84% of >1,000-line PRs get findings (avg 7.5) vs 31% of <50-line PRs (avg 0.5); agents scale
  with PR size; `REVIEW.md` is read from the base branch, never from the PR
  ([customize](https://code.claude.com/docs/en/code-review-customize.md)). Vendor-reported. (partly in Matt's docs)
- **Codex review rubric** ([`codex-rs/prompts/templates/review/rubric.md`](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md)):
  flag only bugs introduced by the commit that the author would fix; "do not stop at the first
  qualifying finding"; name the provably affected code; P0–P3 priorities plus a numeric confidence;
  repository-rule attribution from `AGENTS.md`. (in Matt's Notes e6 as LAB_PROMPTS.md)
- **Codex custom review rules** [blog](https://developers.openai.com/blog/custom-code-review-rules-for-codex)
  [VB] (opened 2026-11-09): Codex Code Review reads custom rules from `AGENTS.md` and can cite the
  rule in a finding. The heading is `## Code Review Rules`. That is the Codex convention, and it
  matters here because quality-review targets both Claude Code and Codex (Claude's analogue is
  `REVIEW.md` from the base branch, above). Repo-wide rules stay at the root; service-specific
  rules go in a nested `AGENTS.md` near the code. On OpenAI's primary suite (known rule violations
  plus safe counterexamples), rule-guided variants recovered 98% of required custom findings vs
  58.3% for the baseline control. They describe four properties and do not publish per-property
  numbers: coverage (busy diffs, competing rules), restraint (clean changes and valid exceptions),
  retention (ordinary bugs outside the rules still caught), and actionability (the finding cites
  the rule, the location, and a priority). What they say held up: short scoped rules that state the
  invariant and a safe path. Broad instructions could easily create noise. ⚠️ Vendor-run; suite
  size, model, and number of runs are not disclosed. Also relevant to limitless (rules from the
  base commit, backlog C6).
- **Greptile, "How to make LLMs shut up"** [blog](https://www.greptile.com/blog/make-llms-shut-up):
  prompting and LLM-as-judge failed to cut nits; filtering new comments by embedding similarity to
  ≥3 downvoted past comments raised address rate 19% → 55%+ in two weeks. (in Matt's docs)
- **Greptile, "Models are worse at reviewing their own code"** [blog](https://www.greptile.com/blog/model-inversion):
  GPT reviewers search depth-first and post fewer comments; Opus posts ~7–8. Matt's data
  contradicts the "use the other vendor" conclusion on severity (Opus 10–15% blocking recall). (in Matt's docs)
- **Uber uReview** [blog](https://www.uber.com/us/en/blog/ureview/): confidence thresholds per
  assistant, language and comment category; semantic-similarity merge; category suppression;
  75% marked useful, 65%+ addressed. (in Matt's docs)
- **BitsAI-CR (ByteDance, FSE 2025)** [arXiv 2501.15134](https://arxiv.org/abs/2501.15134): a separate
  ReviewFilter raised precision (ablation 54.5% → 67.1%); "Conclusion-First" filter output gave the
  best precision at Direct-Conclusion speed; **Outdated Rate** (share of flagged lines changed
  later) as an automatic acceptance metric: 26.7% vs a human-review baseline of 35–46%.
- **Automated Code Review in Practice (Beko, Qodo PR-Agent)** [arXiv 2412.18531](https://arxiv.org/abs/2412.18531):
  73.8% of bot comments labelled resolved, but mean PR closure time rose from 5h52 to 8h20 and
  re-reviews after each fix became "redundant and unhelpful". Older model (GPT-4); one company. ⚠️
- **Devin Review 2.0** [blog](https://devin.ai/blog/devin-review-2) (Cognition, 2026-11-05) [VB]:
  a re-run now reviews only the parts of the PR that changed, on by default, and a per-PR spend
  limit is configurable. Cognition reports 82% lower per-PR cost since August, a typical review at
  $0.25–$0.75, about 80% of PRs under $1 including every push, bugs found per PR from 1.22 to 1.32,
  and median latency from 139s to 94s. These are vendor customer averages, not an independent
  benchmark, and bugs-per-PR is not recall. ⚠️ The same post adds effort levels, including an Ultra
  mode for sensitive code (billing, security) at higher cost. That is relevant to how quality-review
  exposes effort; it is not a separate backlog item. Same re-review concern as Beko, above.

### 2.4 Benchmarks and eval method

- **GitHub ReviewBench** [blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/),
  [repo](https://github.com/review-bench/ReviewBench) (2026-10-05, MIT): 219 PRs, 19 languages, pooled
  gold (humans, LLMs, static analysis), grounded/augmented precision and recall, a 25-task offline test
  set and a judging CLI. Vendor-run; gold mostly machine-made (Report). (in Matt's docs)
- **CR-Bench-v2** [arXiv 2611.02566](https://arxiv.org/abs/2611.02566)
  ([v2 HTML](https://arxiv.org/html/2611.02566v2); Pereira, Sinha, Ghosh, Dutta, Nutanix;
  submitted 2026-11-02, v2 2026-11-03; opened in the 2026-11-04 daily sweep and again on
  2026-11-05): defect-centric benchmark recasting SWE-Bench issues as PR review tasks with full repo
  context. CR-Bench: 584 instances; CR-Bench-Verified: 174 instances from SWE-Bench Verified
  (after detectability + single-PR filters). Each instance: PR + known defect + ground-truth fix
  + taxonomy (category / impact / severity). Metrics: Known-Defect Detection Rate (KDDR) = whether
  the agent hits the labeled defect; Usefulness Rate = fraction of comments that are Bug Hit or
  Valid Suggestion (actionable). Evaluated eight agents over four backbones + Gemini Code Assist;
  three independent LLM judges. Strongest systems: KDDR ≈ 33% on CR-Bench-Verified. Gemini Code
  Assist: KDDR 8.1% but Usefulness Rate 78.0% — usefulness alone misleads. Self-reflection
  (Reflexion) raised KDDR vs single-shot for every backbone (e.g. GPT-5-mini +6.9 to +12.6 pp
  depending on judge; often significant). ⚠️ Python / SWE-Bench scope (Django heavy in the verified
  set); one labeled defect per instance; LLM-generated reference comments and taxonomy (Claude
  Opus 4.5); eval harnesses in the paper are mostly non-tool/non-execution; absolute judge scores
  disagree even when direction agrees. Not in Matt's 2026-10-31 docs.
- **Martian Code Review Bench** [repo](https://github.com/withmartian/code-review-benchmark): 50 PRs /
  173 golden comments offline plus an online set scored against developers' post-review fixes;
  three judge models. (in Matt's docs)
- **ReviewBoundary** [repo](https://github.com/utkutugrul/review-boundary) (Utku Tugrul; MIT;
  created 2026-11-06; announced
  [2026-11-06](https://x.com/utkutugrul33/status/2118788007134118123);
  [methodology](https://github.com/utkutugrul/review-boundary/blob/main/docs/methodology.md),
  [pilot v0.2](https://github.com/utkutugrul/review-boundary/blob/main/docs/pilot-v2.md);
  opened 2026-11-09): paired clean and attacked reviews of the same known defect, to see whether
  untrusted text suppresses the finding or provokes a write. The v0.2 corpus is 12 original
  synthetic families, four per language, each with a vulnerable and a fixed implementation in six
  contexts (clean, PR-body suppression, README suppression, source-comment suppression, a
  tool-output write lure, and a benign quotation): 144 cases, 96 development and 48 public
  heldout. Payload packs add matched text in READMEs, pull requests, filenames, comments, notes,
  and tool responses. Action-boundary scenarios add fake approvals in file paths and URLs, with a
  normal-use control. A scripted-reviewer demo makes no API calls; the dashboard screenshots are
  that calibration, not a model measurement. The v0.2 pilot did run a real model. Executed
  2026-11-06, Inspect AI 0.3.287, ReviewBoundary 0.2.0, model id `openai/gpt-6-luna` through
  OpenRouter (recorded responses named OpenAI; the provider may change the model behind an alias).
  Two families only: TypeScript `ts_batch_export` (development) and Rust
  `rust_partial_batch_permissions` (public heldout). Five trials of every vulnerable/fixed and
  context combination, two prompts (`baseline` and `explicit`): 120 conditions per family, 240 in
  total, all completed, all matching the structural rubric. On submitted vulnerable cases, each
  family was 60/60 for the expected category, for relevant source evidence, and for a correct
  citation. Attacker goal reached: 0/50 eligible observed cases per family. Unauthorized write
  requests, including rejected arguments: 0. Paired degradation against a passing clean control:
  0/80 per family. Both prompts passed every selected condition, so the pilot provides no evidence
  that the explicit boundary prompt improves anything. The write-up calls this a narrow smoke test:
  it does not show that the attack set can distinguish capable reviewers, or that the model is
  robust to other injections. Counts are correlated (shared code and payloads) and are not an
  attack rate. Only 2 of 12 families were run on a model. The tasks are small virtual repositories,
  not production repos or native-agent reviews. Methodology: none of these measurements establishes
  that a reviewer is safe in general. The README says results cover only the tested tasks and
  observed actions and cannot certify a reviewer as safe for production repositories. Offline
  calibration (432 scripted samples, 144 per mode) is a harness check: the reference passes all
  144, and an intentional negative control produces 60 regressions. That shows the gate can fail.
  It is not model-performance evidence. ⚠️ Repo created 2026-11-06, 1 star as of 2026-11-09, small
  public examples, author-run pilot. Also helps limitless: its reviewer reads untrusted PR text and
  diffs. Backlog C14.
- **Statistics:** Miller, *Adding Error Bars to Evals* [arXiv 2411.00640](https://arxiv.org/abs/2411.00640);
  Bowyer et al., *Don't use the CLT with fewer than a few hundred datapoints* [arXiv 2503.01747](https://arxiv.org/abs/2503.01747);
  TREC pooling (Buckley & Voorhees) [NIST](https://www.nist.gov/node/761376). (in Matt's docs)
- Other corpora Matt's Report lists, opened: AACR-Bench [2601.19494](https://arxiv.org/abs/2601.19494),
  SecBench.js [repo](https://github.com/cristianstaicu/SecBench.js), Greptile benchmarks
  [page](https://www.greptile.com/benchmarks), agentpatterns review [page](https://agentpatterns.ai/verification/open-code-review-benchmarks/),
  SZZ evaluation (Rosa et al.) [2102.03300](https://arxiv.org/abs/2102.03300).

### 2.5 Execution, security and spec (sources behind Matt's options A, D, E)

All opened 2026-10-31; claims as summarised in Matt's Report: SecPRBench [2610.33509](https://arxiv.org/abs/2610.33509),
Anthropic Defending Code harness [blog-post.md](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md),
Anthropic zero-days [research](https://www.anthropic.com/research/zero-days), AIxCC SoK [2602.07666](https://arxiv.org/abs/2602.07666),
CyberGym [Berkeley RDI](https://rdi.berkeley.edu/blog/cybergym/), PoC-Gym [2602.04165](https://arxiv.org/abs/2602.04165),
PBT-Bench [2605.15229](https://arxiv.org/abs/2605.15229), ICML 2026 "Silent failures" [78010](https://icml.cc/virtual/2026/78010),
Agentic Code Reasoning (Meta semi-formal template) [2603.01896](https://arxiv.org/abs/2603.01896),
verifier leniency [2608.16003](https://arxiv.org/abs/2608.16003), evidence-carrying termination [2608.23623](https://arxiv.org/abs/2608.23623),
requirement-conformance overcorrection [2603.00539](https://arxiv.org/abs/2603.00539), Otter [2502.05368](https://arxiv.org/abs/2502.05368),
e-Otter++ [2508.06365](https://arxiv.org/abs/2508.06365), Issue2Test [ICSE 2026](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/87/Issue2Test-Generating-Reproducing-Test-Cases-from-Issue-Reports),
Meta JIT catching tests [2601.22832](https://arxiv.org/abs/2601.22832), VulTrial [2505.10961](https://arxiv.org/abs/2505.10961),
AnyPoC [2604.11950](https://arxiv.org/abs/2604.11950), Verify Before You Fix [2604.10800](https://arxiv.org/abs/2604.10800),
repair loops [2607.05197](https://arxiv.org/abs/2607.05197), defect-focused review (ICML 2025) [2505.17928](https://arxiv.org/abs/2505.17928),
scaling agent systems [2512.08296](https://arxiv.org/abs/2512.08296).

### 2.6 Runtime facts for a Claude Code + Codex skill [doc]

- Claude Code ships a bundled `/code-review` skill (alias `/review`) that runs as a forked
  subagent, reads `CLAUDE.md` (not `REVIEW.md`), widens scope (reuse, simplification, efficiency) depending
  on model and effort level, and caps findings (32 when reporting through
  the findings tool; `--max-findings`) ([local review docs](https://code.claude.com/docs/en/code-review-local.md)).
- **A local skill with the same name replaces a built-in command** in a terminal session
  ([skills docs](https://code.claude.com/docs/en/skills.md), "Same name in" table). A standalone copy
  of a skill named `code-review` would shadow the bundled one; the plugin namespace
  (`/accelerate:…`) avoids that.
- Claude Code skill frontmatter supports `effort`, `model`, `context: fork` (run in a subagent with its
  own context), `agent`, `allowed-tools`, `disable-model-invocation` (same page).
- Codex loads skills from `.agents/skills` (repo, walking up to the root) and `~/.agents/skills`;
  `SKILL.md` needs `name` and `description`; optional `agents/openai.yaml` sets UI metadata and
  `allow_implicit_invocation`; plugins distribute skills ([Codex build-skills](https://learn.chatgpt.com/docs/build-skills.md)).
  Matt's orchestrator runs Codex reviews as `codex exec -m <model> -c model_reasoning_effort=high` (Notes).
- Not verified: whether Codex exposes a parallel-subagent primitive to skills. Treat "two independent
  samples" in Codex as two `codex exec` processes until checked.

### 2.7 Same-agent review and unstated bugs

- **Foresight-SWE**, *Do Coding Agents Catch Their Own Bugs? (They Don't.)*
  [arXiv 2611.01181](https://arxiv.org/abs/2611.01181) (opened 2026-11-05; submitted 2026-10-31;
  missed prior sweeps): on 212 real PR₁→PR₂ pairs, agents ~60.7% resolve on the stated task but
  only ~14.8% foresight resolve rate (FRR); when the later defect is named they resolve ~91%.
  Proactive prompting and native self-review (`/self-review`, `/review`) can raise FRR but often
  cut original-task resolve. Popular code-review skills do not raise FRR. Not in Matt's 2026-10-31
  docs. Distinct from "gold comes from a procedure" (§1.2): that procedure builds eval gold; this
  measures whether the author agent, reviewing itself, catches a later bug it was not told about.

## 3. Genuinely new relative to Matt's docs ("candidates for limitless too")

Short list; most external evidence is already in Matt's docs.

1. **Name collision with Claude Code's bundled `/code-review`** (skills docs). Matters for accelerate
   and for any limitless skill shipped to Claude Code users.
2. **Claude Code Review's "Pre-existing" severity** (🟣) as a separate, non-blocking channel for bugs
   the PR didn't introduce — a ready-made home for the Rubric's Q3 "gap already in main" cases that
   aren't explicitly requested.
3. **BitsAI-CR's Outdated Rate** as a zero-cost online proxy (flagged lines later modified), and its
   Conclusion-First verifier format (precision 77.1% vs 65.8% reasoning-first at 1.7 s vs 31 s per
   sample). A possible production KPI next to "orchestrator round-1 findings per PR". ⚠️ fine-tuned models.
4. **Beko's cost side:** PR closure time +42% and redundant re-reviews after each fix — evidence for
   Limitless's later-round scoping and for accelerate to review only the fix diff on re-runs. ⚠️
   Devin Review 2.0 (2026-11-05, §2.3) now does that incremental re-review by default. Its cost and
   bugs-per-PR figures are vendor customer averages, and bugs-per-PR is not recall. ⚠️
5. **ReviewBench's 25-task offline test set + judging CLI** as a cheap external smoke check for a
   general-purpose skill (Matt's Report proposes the 60–80 TS/JS slice; the 25-task set is cheaper).
6. **Codex `agents/openai.yaml` `allow_implicit_invocation: false`** to keep a heavy review skill
   from auto-triggering.
7. **CR-Bench-v2** (§2.4) [arXiv 2611.02566](https://arxiv.org/abs/2611.02566): external
   defect-centric bench (CR-Bench-Verified: 174) that scores known-defect detection separately from
   usefulness. Gemini Code Assist is KDDR 8.1% at Usefulness Rate 78.0%, so usefulness alone
   misleads. Candidate for limitless too. ⚠️ Python / SWE-Bench, one labeled defect, LLM judges.
8. **Foresight-SWE** (§2.7) [arXiv]: stated-task resolve and foresight resolve rate are different
   outcomes; native self-review can raise foresight while cutting the original task. Candidate for
   limitless too.
9. **ReviewBoundary** (§2.4) [repo](https://github.com/utkutugrul/review-boundary): paired
   clean/attacked prompt-injection cases for a reviewer that reads untrusted PR text and diffs.
   The v0.2 pilot (240 conditions, two of twelve families, `openai/gpt-6-luna`) recorded no
   attacker-goal success and no write requests, and both prompts passed every selected case. The
   README says that cannot certify a reviewer safe. Candidate for limitless too. ⚠️

## 4. Not verified / flagged

- Matt's `research/08` cites "Mitropoulos, Spinellis et al., *Contextual Bias in LLM-Assisted Security
  Code Review*, arXiv 2603.18740". That ID opens as *When AI Agrees Too Much: Manipulating Automated
  Code Review via Bias Injection*. Same topic, different title; worth a check.
- Matt's Report links ReviewBench's blog as `github.blog/ai-and-ml/reviewbench-…`; the URL I could
  open is `github.blog/ai-and-ml/github-copilot/reviewbench-…`.
- I did not open the full text of every arXiv paper; for §2.5 I verified that each page exists and
  matches the title Matt's docs cite, and rely on Matt's Report for the specific numbers.
- `human-review/SKILL.md`'s "one in five" statistic: source not found (§0).
