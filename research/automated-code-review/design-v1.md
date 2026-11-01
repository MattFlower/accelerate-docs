# Code review skill — v1 design

*Draft 1, 2026-10-31.*

Status: proposal for Matt to revise. The skill doesn't exist yet. Each choice cites its evidence
([Matt] = limitless repo or Matt's attached docs; see [report.md](report.md) for links) or says **our own idea**.
Figures follow the precedence: 10-31 escapes-dev > Phase 0 RESULTS > working notes, except where newer
notes (e6–e10, 10-31) update RESULTS.

**Principle:** build the eval (§7) before tuning anything. v1 ships the one reviewer recipe that has
replicated on fresh data; every other idea is a layer that's off by default until the eval measures it.

### Scope: one skill, several lenses

`quality-review` is the single entry point for review. v1 ships the bug-finding lens (the measured
core, §3). Security is a planned second lens that builds on the trust-boundary attack pass already
described as an unmeasured layer (§8). Security recall was 0/12 in Matt's limitless data (Plan D).

## 1. What the reviewer does

Given a change (working tree, branch vs base, or a PR), find **real, introduced-by-the-change defects
with a realistic trigger**, rate each by a fixed rule, and put them in two channels: a short
**must-fix** list (only findings that are witnessed or corroborated) and **comments** (everything else).
It doesn't approve, edit code, or post anywhere by default.
- Not a style or "improvement" reviewer: process asks and polish aren't defects (Rubric "Gold"; prompts.ts rubric).
- Complements `human-review` (that skill helps a person review; this one finds defects). Feeding findings
  into the human-review page is post-v1 ([BACKLOG.md](BACKLOG.md) P-7). **our own idea**

## 2. Name and packaging (Claude Code + Codex)

- **Name:** not `code-review`. A standalone copy of a skill named `code-review` replaces Claude Code's
  bundled `/code-review` in terminal sessions (Claude Code skills docs). Working name `quality-review`
  (`/accelerate:quality-review`). Avoiding `code-review` is **our own idea**; the name `quality-review`
  is Matt's decision (2026-10-31).
- **Layout** (one folder works in both runtimes; mirrors `human-review`):
  ```
  skills/quality-review/
    SKILL.md              # name + description (both runtimes); Claude-only keys are ignored by Codex
    agents/openai.yaml    # Codex: display name, allow_implicit_invocation: false
    references/prompt.md  # finder prompt (from limitless, see notes/adversarial-prompt.md)
    references/severity.md# consequence × trigger rule (§5)
    references/schema.json# finding fields (§6)
    scripts/quality-review.mjs# zero-dep Bun/Node: collect diff + impact pack, dedupe, severity, render
  ```
  Codex reads `name`/`description` and optional `agents/openai.yaml`; skills install to `.agents/skills`
  or ship via a plugin (Codex build-skills docs). Claude Code loads it from the plugin's `./skills/`.
- **Explicit invocation only** (`disable-model-invocation: true` in Claude Code;
  `allow_implicit_invocation: false` in Codex): a high-effort review is too costly to trigger implicitly.
  **our own idea**
- **Runtime-neutral settings.** Model names differ per CLI, so SKILL.md states intent, not models:
  "run each reviewer sample at the highest reasoning effort your runtime offers for this task, in a
  fresh context with no access to the author's chat". In Claude Code that maps to `effort: high` /
  a forked subagent; in Codex to `model_reasoning_effort=high` (Matt's orchestrator uses
  `codex exec … -c model_reasoning_effort=high`, Notes). Whether Codex skills can spawn parallel
  subagents is unverified; fallback is two sequential or background `codex exec` runs. **check before build**

## 3. Core recipe (the only measured part)

**Two independent samples of the limitless adversarial prompt at high effort, unioned.**
- Prompt: copied verbatim in [notes/adversarial-prompt.md](notes/adversarial-prompt.md) from limitless `src/pipeline/prompts.ts`
  (`FINDER_FRAMING.adversarial`, line 482; single-reviewer opener line 561; rubric and output rules lines 645–662).
  One deviation: drop "a separate step verifies each finding" when no verifier runs (Notes e6 flags it as false).
- Evidence [Matt, Escapes-dev 10-31, eval-mvw0y6v31sec2vc1agx2t1]: on 80 untuned defects, k=2, judged blocking
  recall production 16.9% → adversarial (E3) 28.5% → sol@high 30.6% → union of 2 adversarial samples (D) 36.2%.
  Replicates Phase 0's ranking (combined dev: D +15.7, E3 +11.4, sol@high +10.6). Cheap Terra adversarial ×1
  28.7% at $0.03/review; ×2 36.9% (Notes e7).
- External support: Bugbot's gains came from going agentic and then making the prompt aggressive (Cursor);
  multi-review aggregation +43.67% F1 (SWR-Bench); union beats best single in c-CRAB and SecPRBench.
- **Why union for recall but not for blocking:** D doubles true clean blocks on held-out (4/20 vs 2/20) and
  Terra union2 blocks 8/32 dev clean vs production 2/32 (RESULTS 0b; Notes e7). That's above Matt's
  ">50% relative rise needs a considerable gain" threshold (Plan answers), so union output goes to the
  comment channel unless §4 promotes it.
- **Hide the author's self-assessment** (implementer report / PR description claims treated as unverified).
  limitless can omit the implementer report because "author framing lowers defect detection" (prompts.ts;
  research/08); CRBugBench: agents trust misleading PR descriptions. Requirements stay in.
- **Effort budget:** reviews mostly under 20 minutes, scaled by change size (Matt, Plan answers). Escapes-dev
  p50: sol@high 3.7 min, D 3.2 min.

## 4. Two-tier output: must-fix vs comments

- **Must-fix** only when a finding is (a) **witnessed** — a failing command or test the reviewer ran, output
  quoted — or (b) **corroborated** — both independent samples report the same defect after **semantic
  dedupe**, and its rule-guided severity (§5) is major or blocker. Everything else is a **comment** with its
  severity shown. Evidence: witness programs had no false-positive triggers (CMU 2607.09979, per Report);
  minority/witness rules beat validators that accept ~everything (Beyond Consensus; M4.5 verifier confirmed
  94%) [Matt, Report Option B; Notes].
- **Semantic dedupe is required before any agreement rule.** Agreement-gated blocking replayed at ~0–1%
  recall because the ±5-line merge almost never records agreement (RESULTS 0c). v1 dedupes with the same
  SAME rule the eval judge uses (`src/evals/judge.ts` `JUDGE_RULE`: same failure mechanism, any location,
  severity ignored), run by the model on the two samples' findings. **Unmeasured** — §7 must measure dedupe
  accuracy and the two-tier rule's recall and clean blocks before relying on it.
- **Execution adds, never filters.** A finding the reviewer couldn't reproduce stays a comment; it's never
  dropped. Probe-as-filter cost −9.2/−6.4 (RESULTS); reproduce-or-drop is a Don't (Plan, AIxCC SoK).
- Gate/CI results the skill is given are authoritative; sandbox errors aren't findings (prompts.ts line 640).
- **False-block cost is explicit:** the report prints how many must-fix items came from witness vs
  corroboration, and the eval reports clean-case must-fix rate next to recall. **our own idea** for the printout.

## 5. Severity: rule-guided, never the model's own label

- Use the approved Rubric's consequence × trigger line. The finder fills two fields — `consequence`
  (one of the classes below, or `nuisance`/none) and `trigger` (realistic / contrived) — plus a plain-language
  failure scenario; `quality-review.mjs` maps them to a severity deterministically. The model's free-text severity
  is recorded but not used for tiering.
- Why: LLM severity raters agreed 13/20 (65%) with Matt's blind validation until a tuned rubric with a
  "nuisance" class reached 18/20 (Notes e2); Opus and Codex split on severity for most pilot findings
  (Notes, 10-30 pilot); five finder-prompt calibration variants were null (Notes e10); clean-case blocks are
  mostly real-but-minor claims rated major (Notes e8). External: Codex rubric P0–P3; Anthropic's three
  severities; uReview per-category thresholds.
- **Rule (generalised from the Rubric; each change noted):**
  - **Blocker** = realistic trigger + loses or corrupts persisted state, leaks a secret or private data,
    breaks a trust or confinement boundary, or stops the service, CI or deploys.
    *(Changed: "stops the factory or deploys" → "stops the service, CI or deploys".)*
  - **Major** = realistic trigger + wrong result, silent failure, lost or repeated work, a bypassable check
    the change claims to add, or a compatibility break with the previous release or data written by it.
    *(Changed: "rollback/older-daemon compatibility" → "previous release or its data".)*
  - **Minor** = contrived trigger, or a cosmetic, diagnostic or test-only cost.
  - **Nit** = style.
  - Realistic means "would plausibly happen in the next month of normal use of this project".
    *(Changed: "normal factory operation" → "normal use of this project"; the Rubric's example that daily
    daemon restarts make restart windows realistic becomes "count the restart, upgrade and retry windows the
    project actually has".)*
  - Unchanged exceptions: a secret leak is at least major (Q5; redaction gaps were 5 of 47 pilot findings);
    an explicitly requested but undelivered requirement is gold even if main already had the gap (Q3;
    spec-mismatch was 0/6); a weak test is a defect only if it hides another labelled defect, but a new test
    failing on the project's supported CI platform is major (Q1, *"platform the factory deploys from" →
    "supported CI platform"*); behaviour the repo's own rules (AGENTS.md/CLAUDE.md) adopt isn't a defect
    (review-082 precedent); lower to minor rather than drop.
- Not "the explicit requirement exception applies to an issue's Out-of-scope list" — the calibrated prompt
  misapplied it that way (Notes e10); `severity.md` should say so. **our own idea** for the wording.
- **Pre-existing** (bug not introduced by the change and not explicitly requested) → comment only, labelled
  pre-existing (Anthropic Code Review's 🟣 channel).

## 6. Output format

- Findings JSON per `references/schema.json`, field-compatible with limitless's review output so its grader
  and judge can score it: `file`, `line`, `title`, `detail`, `failure_scenario`, `category`
  (correctness | security | reliability | data | concurrency | compatibility | test-gap | cleanup |
  conventions), `confidence` 0–1, `introduced_by_diff`, `security`, plus v1's `consequence`, `trigger`,
  `witness` (command + quoted output, or null), `corroborated` (bool), `tier` (must-fix | comment).
- A short Markdown summary in chat: must-fix first (≤ a handful), then comments grouped by file; each item
  quotes the code from git, not from the model (human-review's precision check). **our own idea** to reuse it.
- No auto-fix, no posting in v1. (`/code-review --fix/--comment` exist in Claude Code if wanted.)

## 7. Measurement (build first)

Base it on limitless's fixed instrument. **Carries over:** gold definition and severity line, the two-judge
matcher, pooled gold with blind adjudication, audited clean set, A/A runs, k, bootstrap, decision rule,
snapshot-mode contamination guard. **Doesn't carry over directly:** limitless's harness (`limitless eval`)
runs its own pipeline prompt, not a Claude Code/Codex skill; the factory-specific gate table, implementer
report and audit flags; and the held-out splits (they belong to limitless's decision runs).

1. **Corpus.**
   - Primary: a slice of **limitless escapes-dev** (51 cases, 80 gold defects, all TypeScript) plus the
     **16 dev clean cases** used in Notes e7, rebuilt as standalone two-commit snapshot repos with `evals/`
     stripped so the reviewer can't read the labels (EVALS.md snapshot mode). Recall power: 80 defects × k=2
     = 160 defect-trials; Matt's estimate for +10 points at 80% power is ~160–200 gold at k=2 (Plan) — so
     escapes-dev is roughly enough for large effects only.
   - **Don't touch escapes-heldout (57 cases / 103 defects) or held-out clean** except in a joint decision run
     with limitless; spending them in accelerate burns limitless's held-out. **our own idea**
   - Generalisation check: a small new corpus outside limitless (e.g. 15–25 escaped defects from Matt's other
     repos, labelled with the Rubric), or ReviewBench's 25-task test set. Limitless gold is one repo and the
     prompt was developed on it — circular for a general-purpose skill.
2. **Gold rubric:** the approved Rubric (2026-10-30) with §5's generalisations. Each label carries verdict,
   severity + criterion, plain-language failure scenario, reproduction or "unreproduced", in-change status,
   fixed-later. Matt spot-checks ~20 labels per batch at the logic level (Plan answers).
3. **Matcher:** port `JUDGE_RULE` from limitless `src/evals/judge.ts`. Two judges from different vendors, blind
   to system, one-to-one SAME assignment by confidence; caught iff both judges match; code-reading tiebreak on
   disagreements. Validation in limitless: 93–97% agreement, errors cluster below confidence 0.7 (RESULTS;
   #1059). Re-validate on ~50 hand-checked pairs from accelerate's corpus before trusting it. Keep the ±5
   score alongside for comparison.
4. **Pooled gold:** before each decision, adjudicate every new finding from the arms under test (blind, two
   vendors) and add confirmed defects (TREC pooling). Report the pool bias (it favours arms with more distinct
   findings, RESULTS).
5. **Clean set and false blocks:** blind two-vendor audited clean cases (clean labels were wrong for 068/092/108).
   Report must-fix rate on clean cases per arm with Wilson CIs; 8 clean trials can't bound a 10-point margin,
   so plan 60+ paired clean trials for a non-inferiority call (Notes, eval_methodology).
6. **Runs:** A/A (same arm twice) to measure run-to-run drift (8–10 point gaps observed, Plan); k=2 to screen,
   k≥4 to confirm.
7. **Statistics and decision rule:** paired, PR-clustered bootstrap on recall difference. Adopt if the 95%
   lower bound > 0 and point gain ≥ +10, with clean must-fix rise within Matt's case-by-case judgement
   (>50% relative rise needs a considerable gain). Pre-register before each run. [Matt, Plan; Report]
8. **Runner** (`evals/` at accelerate repo root, outside `skills/` so it doesn't ship): for each case and runtime,
   run the skill headless (`claude -p "/accelerate:quality-review <base>..<head>"`, `codex exec` with the skill), save
   findings JSON, judge, score. Run both runtimes: the skill must work in Claude Code and Codex, and their
   recall will differ. **our own idea** for the runner shape.

## 8. Layers that lack measurement (off by default; enter the eval in this order)

Each is a Plan option/arm with Matt's evidence; none has been run as a reviewer arm.
1. **Rule-guided severity mapping** (§5) — on by default because it only re-labels; measure clean must-fix
   rate with vs without (Plan G).
2. **Out-of-diff impact pack** — a deterministic list of callers/importers of changed symbols, deleted guards
   and their old invariants, given to the reviewer. 13/30 misses were outside the diff (research/14). Differs
   from trace finder E (+1.1/+3.4), which asked a second agent to search; SWE-PRBench warns that dumped context
   hurts, so keep it short (Plan F).
3. **Acceptance claims from the request** — restate each requirement as a checkable claim before reading the
   diff; unmet explicit requirements are at least major. Spec-mismatch was 0/6 (Plan E; Rubric Q3).
4. **Trust-boundary attack pass** — triggered only when the change touches a boundary (input parsing, paths,
   secrets, auth, subprocess); per-boundary attack catalogue; 2–3 attackers unioned; validator only demotes.
   Security was 0/12 (Plan D; SecPRBench, Defending Code harness, AIxCC per Report).
5. **PR-specific brief + mutation check** — the oracle procedure: brief (checkable claims, every caller,
   test inputs, targeted questions), then revert the source diff and confirm the PR's tests fail (Plan A;
   Notes "how the gold is generated"). Mutation check is deterministic and cheap where tests exist.
6. **Opus/other-vendor sample as an extra union finder** — modest (+5–9, RESULTS 0c), comment channel only.

## 9. Open questions for Matt

- Checklist F (+14.6 on its 33-case cohort) vs the "no long checklists" Don't — not resolved here.
- Is a slice of limitless escapes-dev acceptable as accelerate's dev set, given the prompt was tuned there?
- Should accelerate wait for limitless's held-out decision run (prod, sol@high, E3, Terra-adv, D, Terra-adv×2)
  before freezing the v1 core?
