# Phase 0 results (2026-10-29) — free work on stored trials

Scripts: ../scripts/ (build_judge_inputs.py, judge_prompt.py, judge_codex.py, validate_judges.py, rescore.py, replays.py,
clean_blocks.py, adj_codex.sh). Data: this directory. Labels: evals/review/cases.json at origin/main fa71b024.

## 0a. Semantic matcher (two judges, blind to system)
- Judges: Claude Sonnet 5.5 (subagents; my shell's `claude` CLI login has expired) and Codex gpt-6.1-terra@medium
  (`codex exec`). Per trial: required gold defects vs all findings, one-to-one SAME matching, text only.
- Validation on dev E1/E3/D (vs the two earlier audits): Terra 94.1% agreement (n=388), Claude 93.5% (n=339),
  Terra vs Claude 97.4% (n=342). Most judge-vs-audit disagreements were audit errors (the audits judged only the
  finding the ±5 grader happened to credit). Judge errors cluster at confidence < 0.7.
- Rule used: caught = both judges match the gold to a finding that satisfies the blocking rule ("both");
  "either" = liberal bound. 33 blocking disagreements across 772 trials remain for a tiebreak.

## Final judged recall (METHOD: two-judge text consensus — Claude Sonnet 5.5 + GPT-6.1 Terra — with a code-reading Opus tiebreak on the 55 contested items; final_table.py)
Code-reading tiebreak: 26 SAME / 28 DIFFERENT / 1 UNCLEAR (counted as not caught). On contested items the
"both judges" rule matched code reading 45/55 times; Terra alone 40, Claude alone 35.

| Split | System | ±5 grader | Final judged | vs production |
|---|---|---|---|---|
| dev | production sol-6.1@medium standard (E1) | 33.7 | 31.6 (31/98) | — |
| dev | production + setup (#661, another day) | 31.6 | 30.6 (30/98) | −1.0 |
| dev | sol-6.1@high (same run as E1) | 42.9 | 41.8 (41/98) | +10.2 |
| dev | adversarial prompt (E3) | 45.9 | 49.0 (48/98) | +17.4 |
| dev | union of 2 adversarial samples (D) | 47.4 | 47.4 (46/97) | +15.8 |
| dev | checklist F, own 33-case cohort | 27.1 | 39.6 (19/48) | +14.6 (prod 12/48 on the same cohort) |
| dev | trace finder (E) | 30.6 | 32.7 | +1.1 |
| dev | probe + setup | 21.4 | 22.4 | −9.2 |
| dev | claude/opus / opus@high | 14.3 / 16.8 | 10.2 / 14.7 | −21 / −17 |
| heldout | production standard (#541) | 25.6 | 18.6 (16/86) | — |
| heldout | adversarial (#541) | 32.6 | 25.6 (22/86) | +7.0 |
| heldout | D union of 2 (#551) | 42.0 | 33.0 (29/88) | +14.4 |
- Production on two different days: 31.6 vs 30.6, so run-level drift for production is small; per-trial noise is
  not (15 of 98 defect-trials discordant).
- Opus any-severity (Claude judge): 22.4 / 25.3 — it finds about twice what it blocks.
- Data caveat: E2's sol-6.1@medium arm is cached copies of E1's trials, so E2 was never an A/A.
- Under-measured: held-out recall excludes the new real defects in review-068/092/108 (not yet labelled).

## 0b. Held-out "clean" blocks, blind two-vendor adjudication (clean_adjudication.md)
- All three M5.2 held-out clean cases (review-068, 092, 108) contain real medium defects, agreed by both vendors with
  reproductions (gate-evidence substitution defeated by any skipped test; test output can forge coverage; loop detector
  misses repeated failures; gate test command no longer recognised). They should be relabelled real.
- Remaining held-out clean = #542's 10 cases. True false blocks there: production 2/20 (review-114), D 4/20 (114 ×2,
  133 ×2 disputed: Unicode case folding, Codex medium / Opus low).
- CORRECTION 10-30: review-133 is sandbox PR #14 (sb#14), whose Unicode case-folding claim LABELS.md already confirmed
  MINOR on 10-16 (the request doesn't ask for folding), so review-133 stays clean and is not an open dispute.
- So #551's clean-block comparison ("10/26 vs 7/26") becomes 4/20 vs 2/20 on true clean cases: D doubles the clean-block
  rate (above Matt's 50% threshold), against final judged held-out recall 33.0% vs 18.6% (+14.4). Retrospective;
  the rejection rested partly on mislabelled cases, but D's true false-block rate is still higher.

## 0c. Replays
- Two-tier "block only when both D samples agree": recall ~0–1%. The ±5-line merge almost never records agreement
  (as in M4.5), so agreement-gated blocking needs semantic dedupe first.
- Sol ∪ Opus (E2, paired per trial): Sol 30.6% → ∪ Opus blocking 35.7% → ∪ Opus any severity 39.8%, clean 2/8 unchanged.
  The writer's 50% used loose location matching; judged it is ~+9.

## What this changes in the plan
1. Adopt the two-judge semantic matcher in the eval harness (factory PR) and regrade stored evals.
2. Held-out: 068/092/108 → real; the M5.2 held-out clean set is gone; #542's set is the only clean held-out.
3. Strong priors for the tournament: adversarial-family variants (E3 +17.4, D +15.8, F +14.6) and sol@high (+10.2)
   beat production on dev under final judged matching; the clean-block evidence used to reject them was mislabelled.
4. Agreement-based blocking requires semantic dedupe; Opus as an extra finder adds ~+5–9.

## Phase 1 rescore with pool gold (2026-10-30, dev only; scripts/p1_rescore_pool.py -> phase1/rescore_pool.json)
Pool gold = 70 new dev defect groups from stored-trial findings no judge matched (two-vendor adjudication, v3 raters,
orchestrator rulings, Opus mechanism dedup, Q3 filter). A trial catches a group when one of its own findings in the
group is blocker/major. Old gold = Phase 0 final judged result.

| Arm | old gold | pool gold | combined | vs production |
|---|---|---|---|---|
| production sol@medium (E1) | 31/98 31.6 | 24/138 17.4 | 55/236 23.3 | — |
| production + setup | 30/98 30.6 | 31/138 22.5 | 61/236 25.8 | +2.5 |
| sol@high | 41/98 41.8 | 39/138 28.3 | 80/236 33.9 | +10.6 |
| adversarial E3 | 48/98 49.0 | 34/138 24.6 | 82/236 34.7 | +11.4 |
| union of 2 adversarial D | 46/97 47.4 | 44/134 32.8 | 90/231 39.0 | +15.7 |
| trace finder E | 32/98 32.7 | 31/138 22.5 | 63/236 26.7 | +3.4 |
| probe + setup | 22/98 22.4 | 18/138 13.0 | 40/236 16.9 | −6.4 |
| opus / opus@high | 10/98, 14/95 | 23/138, 24/137 | 14.0, 16.4 | −9.3 / −6.9 |
Caveats: pool gold comes from these arms' own findings (defects no arm found are absent for all), so it favours arms
that report more distinct defects; D spends two samples. Escape gold (80 dev) has no stored trials: fresh runs only.
