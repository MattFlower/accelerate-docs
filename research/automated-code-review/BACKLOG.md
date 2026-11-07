# Code review skill — backlog

*Draft 1, 2026-10-31.*

**How this is ranked.** By expected gain per unit of effort, where gain is judged blocking recall on real
escaped defects at an acceptable clean must-fix rate, and effort is build + eval cost (S ≈ ≤1 day,
M ≈ 2–5 days, L ≈ 1–3 weeks). Items with replicated measurements outrank items with only literature
support; literature only decides what to *try* first. The eval harness is first because nothing below can
be ranked honestly without it (Matt: "fix the eval first", Plan answers).

**Statuses.** `proposed` (not built or measured for this skill) · `testing` (being measured; qualifiers
say how far, e.g. "replicated on dev, held-out pending") · `shipped` (in the skill, with the eval run that
justified it) · `rejected` (measured or argued out — the *why* and the evidence stay so it's never retried
blindly). Qualifier `blocked on X` = can't be tested until X exists.

**Sources.** [Matt] = limitless repo (`L/` = `https://github.com/MattFlower/limitless/blob/fb48dbc76fc6424787e4a1909a602d280ad8b522/`)
or Matt's attached docs (Report = *Fix the ruler, then widen the search*; Plan = *Review stage plan* draft 1
10-29; RESULTS = Phase 0 RESULTS 10-29; Escapes-dev = 10-31 run; Notes = working notes; Rubric = approved
labelling rubric 10-30). External links are in [report.md](report.md).

**Name clash warning.** Report "Options A–G" and Plan arms T0–T9/G are *proposals*. Phase 0 eval arms
"D", "E", "F" are different things: D = union of two adversarial samples, E = trace finder, F = AGENTS.md
checklist. This file always writes "Option D" vs "arm D".

Numbers are judged blocking recall (two-judge matcher) vs production unless stated; escapes-dev = 80 untuned
defects, k=2 (eval-mvw0y6v31sec2vc1agx2t1; cheap arms eval-mvvv3pum0kriw040gi0x29).

---

## A. v1 build choices (ranked)

### 1. Eval harness on real diffs with known bugs — `proposed`, cost M
- **Idea:** runner that executes the skill headless in Claude Code and Codex on snapshot repos built from a
  slice of limitless escapes-dev (51 cases / 80 gold) + 16 audited dev clean cases, scores with a port of
  limitless's two-judge matcher, reports recall + clean must-fix rate with Wilson CIs, A/A drift, paired
  PR-clustered bootstrap. Plus a small non-limitless corpus (15–25 Rubric-labelled escapes from Matt's other
  repos, or ReviewBench's 25-task test set) for generalisation.
- **Source:** [Matt] `L/docs/EVALS.md`, `L/evals/review/cases.json`, `L/evals/review/LABELS.md`,
  `L/src/evals/judge.ts` (#1059), RESULTS (judge validation), Plan Phase 0–1; ReviewBench repo.
- **Why it helps:** every other item is a guess without it; ±5-line scoring misattributes ~20% of credits
  (Notes credited audit).
- **Test:** validate the ported judge on ~50 hand-checked pairs (target ≥90% agreement, like limitless's
  93–97%); A/A on production-equivalent arm shows drift < effect sizes we care about.
- **Note:** keep escapes-heldout (57 / 103) untouched for limitless's decision run.
- **Note:** RegBench-Py (ORION, arXiv 2610.35223; 154 verified real-world Python PRs) is a possible
  secondary corpus. ⚠️ Python, while the main slice is TypeScript. ORION is **also relevant to
  limitless** (Option A / T5); see item 11.

### 2. Core reviewer: adversarial prompt × 2 independent samples at high effort, unioned — `testing (held-out passed and live in limitless at medium effort; accelerate eval pending)`, cost S
- **Idea:** v1 default per [design-v1.md](design-v1.md) §3, prompt from [notes/adversarial-prompt.md](notes/adversarial-prompt.md) (`L/src/pipeline/prompts.ts` l.482/561).
- **Source:** [Matt] Escapes-dev: arm D 36.2% vs prod 16.9% (+19.4), p50 3.2 min, $0.39; Phase 0 dev +15.8,
  held-out +14.4 (33.0 vs 18.6); pool-gold combined +15.7. External: Bugbot (aggressive agentic prompt),
  SWR-Bench (aggregation).
- **Why:** largest replicated gain of anything tried.
- **Cost of it:** doubles true held-out clean blocks (4/20 vs 2/20, RESULTS 0b) → must-fix gate (item 4) is
  part of this choice, not optional.
- **Update 2026-11-06:** limitless adopted this on 11-01 with Sol 6.1@medium: paired held-out +11.7 pts
  (one-sided 95% lower bound +5.3), 2/18 clean false blocks. In production (49 reviews) p50 went from 63 s to
  77 s and median cost about doubled; request-changes rate held at about 30%.
- **Test:** accelerate eval in both runtimes.

### 3. Rule-guided severity (consequence × trigger → deterministic mapping) — `proposed`, cost S
- **Idea:** finder emits `consequence` + `trigger` + scenario; script maps to severity using the Rubric line
  (generalised; [design-v1.md](design-v1.md) §5). Model's own severity ignored for tiering. = Plan arm **G**.
- **Source:** [Matt] Rubric; Notes e2 (rater v2 13/20 = 65% vs Matt's blind validation, v3 18/20); Notes e8
  (20/22 clean-block claims real but minor/major split by vendor); Notes e10 (finder-prompt calibration null).
- **Why:** clean-case blocks are mostly real-but-minor issues rated major; detection isn't the problem there.
- **Test:** clean must-fix rate with vs without mapping at equal recall; agreement of mapped severity with
  gold severity on escapes-dev.

### 4. Two-tier channel with semantic dedupe (must-fix only if witnessed or corroborated) — `proposed (blocked on semantic dedupe)`, cost M
- **Idea:** dedupe the two samples with the judge's SAME rule; must-fix only if a failing command/test was
  observed or both samples report it at major+; rest are comments. = Report **Option B** / Plan **T4** (minus
  mixed models).
- **Source:** [Matt] RESULTS 0c: agreement gating replayed at ~0–1% recall because the ±5 merge never records
  agreement — not rejected, blocked on dedupe; Report (Beyond Consensus, CMU witness study).
- **Why:** the only proposal that targets D's false-block cost directly.
- **Test:** dedupe accuracy vs hand pairs; recall of must-fix tier vs arm D's any-blocker rule; clean must-fix
  rate (target ≤ production's).

### 5. Packaging: distinct name, explicit invocation, both runtimes — `proposed`, cost S
- **Idea:** `skills/quality-review/` with `agents/openai.yaml`; not named `code-review`; runtime-neutral effort
  and sampling text. **our own idea**, constrained by docs.
- **Source:** Claude Code skills docs (same-name skill replaces bundled command); Codex build-skills docs.
- **Test:** install via plugin in Claude Code and via `.agents/skills` in Codex; both invoke and produce
  schema-valid JSON on one fixture.

### 6. Hide author self-assessment; gate results authoritative — `proposed`, cost S
- **Source:** [Matt] `L/src/pipeline/prompts.ts` (implementer report omittable; "author framing lowers defect
  detection"; l.640 gate rules), `L/docs/research/08-code-review.md`; CRBugBench (misleading PR descriptions).
- **Test:** A/B on the eval with PR description included vs summarised to requirements only.

### 7. Out-of-diff impact pack (deterministic) — `rejected on stored data, not built`, cost M
- = Report **Option F** / Plan **T8**. 13/30 production misses needed files outside the diff
  (`L/docs/research/14-review-strength.md`); CRBugBench: out-of-diff bugs harder. Cheap and short by design
  (SWE-PRBench: dumped context degrades). One concrete shape is AST impact analysis feeding oracle
  synthesis (ORION, arXiv 2610.35223). Distinct from trace finder (arm E, +1.1/+3.4).
- **Test:** recall on the out-of-diff subset of escapes-dev.
- **Result 2026-11-06 (no paid run):** the 13/30 figure does not describe what the union of two still misses.
  Of the 45 escapes-dev defects union D never caught, 3 sit in files outside the diff, 36 sit within 3 lines of
  a changed line, and only 5 fix commits edited a source file outside the diff. Limits: this shows where the
  defect and fix live, not which files a reviewer had to read to see it, and it covers one repo's dev split.
  Reopen if a corpus shows misses that depend on unread files.

### 8. Acceptance claims from the request — `proposed`, cost S–M
- = Report **Option E** / Plan **T7**. Spec-mismatch 0/6 (research/14); Rubric Q3 makes unmet explicit
  requirements gold. Literature: Otter, e-Otter++, Issue2Test; caution from requirement-conformance
  overcorrection (2603.00539) and Notes e10 (Out-of-scope misread).
- **Test:** recall on spec-mismatch defects; clean must-fix rate (overcorrection risk).

### 9. Trust-boundary attack pass — `rejected as a third added sample (limitless dev screen)`, cost M
- = Report **Option D** / Plan **T6**. Security 0/12 (research/14); redaction gaps 5 of 47 pilot findings
  (Rubric Q5). SecPRBench (68% of missed security bugs = right file, wrong mechanism; union of 8 agents),
  Defending Code harness, AIxCC SoK, CyberGym (repeated attempts) — per Report.
- **Test:** recall on security/redaction subset; must not filter other findings.
- The security lens (item 10) is this pass inside `quality-review`, not a second copy of the evidence above.
- **Result 2026-11-06 (lab screen p10, Sol 6.1@medium, one sample, 51 escapes-dev + 16 dev clean, k=2):** union D
  plus the pass reached 62/160 vs D 58/160, +2.5 pts against a pre-registered +5 bar (one-sided lower +0.6).
  Alone it found 22/160 overall, 16/52 security against D's 17, with 0/32 clean blocks. D plus the pass found
  21/52 security and no new non-security defects. A security focus finds much the same security defects as
  the union, so it adds little on top. Item 10's single lens is untested as a replacement for a sample: the
  same screen scored one adversarial sample plus the pass at 53/160, 3.1 pts below D. Caveat: the prompt was
  written after reading the missed defects, so even this gain is dev-influenced. Held-out not spent. A third plain
  adversarial sample gained +5.1 post hoc, so this focused sample did worse than simply sampling again.

### 10. Security lens inside quality-review — `proposed`, cost M
- **Idea:** security review is a second lens of the one `quality-review` skill, built on the trust-boundary
  attack pass (item 9). Not a separate skill, and not a restatement of item 9.
- **Source:** Matt's decision 2026-10-31 + the existing trust-boundary/security evidence already cited in
  this backlog.
- **Test:** security-slice recall on the eval (SecBench.js-style cases already cited) without raising
  clean-case false blocks.

### 11. PR-specific brief + mutation check (oracle replica) — `proposed`, cost M–L
- = Report **Option A** / Plan **T5**. "Gold comes from a procedure, not a better model" (Report; Notes).
  Mutation check alone is deterministic and cheap where the PR adds tests.
- **Source:** ORION, [arXiv 2610.35223](https://arxiv.org/abs/2610.35223) — execution as a finder
  (PR intent, AST impact, function-level behavioral oracles, differential tests), not a filter.
  ⚠️ Python-only, single paper, baselines' configuration unknown. **also relevant to limitless**
  (Option A / T5).
- **Test:** recall vs core; time budget (<20 min typical, Plan answers).

---

## B. Existing limitless work (status as of 2026-10-31)

| Item | What | Evidence | Status for accelerate |
|---|---|---|---|
| T0 | production sol@medium, standard prompt | escapes-dev 16.9%; Phase 0 dev 31.6, held-out 18.6; clean 2/32 dev | baseline arm |
| T1 | sol-6.1@high, standard prompt | escapes-dev 30.6% (+13.8), $0.35, 3.7 min; Phase 0 +10.2; pool +10.6; clean 3/8 (Phase 0) | `testing (replicated on dev, held-out pending)` — runtime-neutral form = "highest effort" |
| T3 / arm E3 | adversarial prompt, single sample | escapes-dev 28.5% (+11.6), $0.20; Phase 0 +17.4; held-out +7.0; pool +11.4 | `testing (replicated on dev, held-out pending)` — in v1 core |
| arm D | union of 2 adversarial samples | escapes-dev 36.2% (+19.4); held-out +14.4; paired held-out at adoption +11.7, 2/18 clean; true clean 4/20 vs 2/20 | `testing (live in limitless since 2026-11-01; accelerate eval pending)` — v1 core, needs item 4 |
| T9 | cheap Terra-6.1 adversarial | 28.7% (+11.9), $0.03, 0.5 min; ×2 union 36.9%; clean 6/32, union 8/32 (Notes e7) | `testing (replicated on dev, held-out pending)` — Codex-only model; cost lever |
| — | third adversarial sample (union of three) | post hoc on stored runs: +5.1. Live lab screen p12 (2026-11-07): 61/160 vs union of two 58/160, +1.9 vs a +5 bar, one-sided lower −2.5; 0/30 clean blocks outside review-082; p50 324 s vs 190 s, cost +29% at the median. Per-sample quality matched the stored run (21.5% vs 21.9% location recall), so the post-hoc estimate was optimistic | `rejected` at this bar — the extra sample adds about 2–4 points |
| T9 | luna@medium | 2.5% / 4.4% | `rejected` — not viable |
| T9 | haiku-5.5@high | partial 6/26, 4/23; 17/32 over 20 min; 5 errors | `rejected` for now — latency/reliability |
| T2 / Option C | coverage prompt + per-file ledger | Terra arm V2 "thorough": 33.8%, clean 7/32 (Notes e7); CRBugBench +5–6 top-5 recall for GPT family; Sol lab screen p11 (2026-11-06): union of two 33/80 vs adversarial 30/80, +3.8 vs a +5 bar, one-sided lower −2.8, 0/15 clean pairs outside review-082, 1.47 vs 1.63 findings per trial | prompt `rejected` on Sol at this bar; ledger never built — the prompt did not raise finding count |
| V3 | caller + deleted-invariant tracing prompt | 30.6%, clean 7/32 (Notes e7) | `proposed`, low priority |
| T4 / Option B | mixed-model union + two-tier block | two-tier blocked on dedupe (RESULTS 0c); Sol ∪ Opus +5–9 | split: two-tier = item A4; mixed union = item C2 |
| T5 / Option A | oracle replica | Report | item A11 |
| T6 / Option D | attack pass | p10 dev screen +2.5 on top of union, 0/32 clean | item A9, `rejected` as a third sample; security lens = item A10 |
| T7 / Option E | acceptance tests | Report | item A8 |
| T8 / Option F | impact pack | 5 of 45 union misses had fixes outside the diff | item A7, `rejected` on stored data |
| G | deterministic severity, stop parking majors | Rubric; Notes e2/e8/e10 | item A3 |
| arm F | AGENTS.md per-item checklist | +14.6 on its own 33-case cohort (19/48 vs 12/48); #553 +6.3 on ±5, not adopted | `proposed — tension flagged for Matt`: conflicts with the "no long checklists" Don't; unresolved |
| — | specialist panel (Sol@medium verifier) | ~41.6% partial, clean 13/32 (Notes e7) | `proposed`, low — highest recall, worst clean |
| — | finder-prompt severity calibration | null: 30.0% / 6/32 vs 28.7% / 6/32 (eval-mvx3koae1kebh1d07r3w9f) | `rejected` (see below) |
| — | rubric in the verifier's severity scale | untried (Notes e10) | `proposed` |

---

## C. Post-v1 improvements

1. **Rated-severity rater as a separate pass** (v3 rater with "nuisance" class, 18/20) instead of in-finder
   fields — `proposed`, S. [Matt] Notes e2.
2. **Other-vendor sample as an extra union finder** (comment channel only) — `proposed`, S, modest:
   Sol 30.6% → ∪ Opus any-severity 39.8% (~+5–9), clean 2/8 unchanged (RESULTS 0c). Opus alone is rejected.
3. **Re-review only the fix diff on re-runs** — `proposed`, S. Beko: redundant re-reviews, PR closure +42%. ⚠️
4. **Outdated-rate tracking** (did flagged lines change later?) as an online acceptance metric — `proposed`, M.
   BitsAI-CR. ⚠️
5. **Learned suppression of disliked comments** (embedding similarity to ≥3 downvoted) — `proposed`, M.
   Greptile 19% → 55%+. Needs a feedback log; human-review already has a feedback channel.
6. **Repo rules from the base commit** (AGENTS.md/CLAUDE.md/REVIEW.md, never from the change) —
   `proposed`, S. Anthropic Code Review reads REVIEW.md from base; limitless reads lenses from base (GUIDE.md).
7. **Feed findings into the human-review page** as annotations — `proposed`, M. **our own idea**
8. **Pre-existing channel** (🟣) for bugs not introduced by the change — `proposed`, S. Anthropic Code Review.
9. **CR-Bench-Verified smoke + Reflexion second pass** — `proposed`, cost S–M. Also helps limitless.
   - **Idea:** Add CR-Bench-Verified (174), or a small TS/JS-filtered slice if one exists, as an external
     defect-centric smoke check. Score with a KDDR-style known-defect hit plus a usefulness split, and
     measure a Reflexion-style second pass against single-shot and against adversarial×2. Track Usefulness
     Rate separately from blocking recall so helpful comments can't fake defect recall. Prefer the Verified
     subset. This does not replace the limitless escapes eval.
   - **Source:** [CR-Bench-v2](https://arxiv.org/abs/2611.02566) (*CR-Bench-v2: Evaluating the Real-World
     Utility of AI Code Review Agents*; submitted 2026-11-02, v2 2026-11-03; opened in the 2026-11-04
     daily sweep and again on 2026-11-05). [report.md](report.md) §2.4.
   - **Why:** Existing external options (ReviewBench, Martian) are comment-gold or pooled. CR-Bench
     grounds each task in a known SWE-Bench defect plus a fix. Gemini Code Assist is KDDR 8.1% at
     Usefulness Rate 78.0%, so a high usefulness rate is not known-defect recall. Best systems are about
     33% KDDR, which warns against merge-gating. Reflexion raised KDDR versus single-shot for every
     backbone. That is weak evidence for a cheap self-critique pass as a finder variant, not as a
     reproduce-or-drop filter. The split matches quality-review's blocking-recall plus clean must-fix
     framing.
   - **Test:** Port or script a runner. Start with a 25–50 task slice, then the full verified set if the
     slice is informative. Compare KDDR and comment usefulness for production versus adversarial×2, and
     A/B single-shot versus one Reflexion iteration versus adversarial×2. Score with the two-judge SAME
     matcher or the paper's KDDR judge, plus usefulness. Report Wilson CIs. Do not contaminate
     escapes-heldout.
   - **Cost:** S for a 25–50 task slice; M for full verified.
10. **External smoke check on ReviewBench test set (25 tasks, has Codex CLI example)** — `proposed`, S.
11. **Same-agent review as a measured anti-pattern** — `proposed`, M. Also helps limitless.
    - **Idea:** Treat "author agent then same-agent review" as a measured anti-pattern; prefer independent
      review samples (already in adversarial×2); optionally test a foresight-style pack (unstated edge
      cases / silent-wrong-result) as a lens, not same-session self-review.
    - **Source:** [Foresight-SWE](https://arxiv.org/abs/2611.01181) (*Do Coding Agents Catch Their Own Bugs?
      (They Don't.)*; submitted 2026-10-31). [report.md](report.md) §2.7.
    - **Why:** Reinforces independence over self-review; quantifies the self-review tradeoff; relevant if
      quality-review is a post-implement gate in an agent loop.
    - **Test:** On escapes-dev, independent adversarial×2 vs same-session self-review after implement;
      blocking recall + clean must-fix (and resolve-rate if used in a factory loop).

---

## Shipped

_(none yet)_

## Rejected

Each with the evidence so it isn't retried without new reason.

- **Majority vote across samples** — kills recall; validators accept nearly everything and consensus
  worsens it (Report: Bugbot dropped its voting pipeline; Beyond Consensus TNR 19.2%). [Plan Don'ts]
- **Multi-round debate** — raises recall and false positives, not precision (Report: VulTrial). [Plan Don'ts]
- **Reproduce-or-drop filter** — execution must add findings, never filter; arm probe+setup −9.2 judged
  (22.4 vs 31.6), −6.4 pool gold; #661 21.4% vs 31.6% (Report: AIxCC SoK). [RESULTS; `L` issue #661]
- **Long pattern checklists** — "goal plus context" beats long checklists (Report: Defending Code harness).
  ⚠️ Conflicts with arm F's +14.6 on its own cohort; flagged for Matt, not settled.
- **Extreme effort alone** — big cost for the gain (Report: Luna 36→57% at 23×).
- **Out-of-diff impact pack (item 7)** — not built: 3 of 45 union misses sit outside the diff and 5 of 45 fixes
  touched a source file outside it. See item 7 for the limits of that measure.
- **Trust-boundary pass as a third sample (item 9)** — +2.5 pts vs a +5 bar; it re-finds the union's security
  defects. See item 9.
- **Trace finder (arm E)** — +1.1 judged / +3.4 pool gold; #552 −3.1 on ±5. [RESULTS; `L/evals/review/TRACE.md`]
- **Opus as sole reviewer** — −21 / −17 (opus, opus@high) judged dev; −9.3 / −6.9 pool; #522 12.8% vs 35.1%
  ("panel with Opus not worth pursuing"). Kept only as extra union finder (C2). [RESULTS; issue #522]
- **Causal-attribution verifier** — null (#235). **Cross-vendor verifier** — no change; M4.5 verifier confirmed
  ~94% of candidates (doesn't discriminate); M4.5 panel +16 points recall at 3.5× false blocks. [Notes; PLAN M4.5]
- **Severity calibration via finder-prompt wording** — five variants all 6–9/32 clean blocks; calibrated
  prompt misapplied the requirement exception to Out-of-scope lists (Notes e10, eval-mvx3koae1kebh1d07r3w9f).
- **"Fix" setup prompt** (+setup) — 30.6 vs 31.6 judged (−1.0); +2.5 pool gold. Noise-level. [RESULTS]
- **luna@medium** (2.5% / 4.4%) and **haiku-5.5@high** (17/32 over 20 min) as reviewers. [Escapes-dev]
- **±5-line location grading as the primary metric** — ~20% accidental credits, ~4% missed SAME. Kept only
  as a secondary score. [Notes credited audit; #1059]
- **Usefulness Rate as a substitute for known-defect recall** — CR-Bench-v2 Gemini Code Assist is
  KDDR 8.1% at Usefulness Rate 78.0% ([2611.02566](https://arxiv.org/abs/2611.02566), daily sweep
  2026-11-04). Keep a known-defect hit (KDDR or judged recall) as the detection score.
- **Claude Code ultrareview as an eval baseline arm** — source: https://code.claude.com/docs/en/ultrareview.md.
  Rejected by Matt 2026-11-06 on cost: about $5-$25 per review after free runs, so roughly $335-$1,675
  for one 67-case pass at k=1, before repeats; no published recall or precision.
