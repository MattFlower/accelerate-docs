# Improving Limitless's review stage

*2026-09-28 to 2026-11-01. Written 2026-11-01 from the lab notebook, eval records and decisions.*

Limitless reviews every factory change with an LLM reviewer before it can merge. This topic records
two months of work on making that reviewer catch more real defects without blocking clean changes:
everything we tried, what each attempt measured, why most were not adopted, and what finally shipped.
The raw material (notebook, eval configurations, judged results, adjudications, scripts) is kept
beside this report so the work can be checked or resumed.

## Outcome

On 2026-11-01 Matt adopted **the union of two adversarial review samples** as the production review
(Limitless PR #1122): the same routed reviewer (Sol 6.1 at medium effort) runs twice, in parallel,
with the adversarial prompt, and a blocking finding from either run blocks the round.

Held-out evidence, both judges required to match a gold defect to a blocking finding:

| System | Recall on 22 shared held-out cases | Clean false blocks (of 18) |
|---|---|---|
| Previous production: one standard reviewer | 22 of 94 (23.4%) | 0 |
| **Union of two adversarial samples** | **33 of 94 (+11.7 points; one-sided 95% lower bound +5.3)** | **2** (both on review-133) |
| Specialist panel with a rubric verifier (D2) | 31 of 94 (+9.6; lower bound +2.1) | 6 |

Cost is about twice one review's tokens (~$0.06 per review API-equivalent, median 77 s). The goal Matt
set on 2026-10-29 was at least +10 points of blocking recall, with a clean false-block rise of more
than 50% acceptable only for a considerable gain; +11.7 for 2 of 18 met it in his judgement.

What did not work is as important: every prompt-, effort-, model- and verifier-based variant before
it either failed to transfer from dev to held-out or bought recall with too many false blocks
(table below).

## The question and the constraints

- **Goal (Matt, 2026-10-29):** make review "absolutely as good as possible"; at least +10 points of
  blocking-defect recall; tokens are cheap, guessing is not ("we don't have to guess; run evals").
- **False blocks:** a blocked clean change costs a full implementation round. Before 10-29 the rule
  was "at most one extra clean false block"; after, a >50% relative rise needed a considerable gain.
- **Latency:** most reviews should finish within 20 minutes.
- **Never re-run paid baselines** just to refresh them; compare against stored evals.
- **Held-out discipline:** variants are designed on dev cases and confirmed once on held-out.

## How review quality is measured

- **Corpus:** `evals/review/cases.json` in the Limitless repo. Each case is a factory PR at its
  reviewed commit, with gold defects (file, line, description) or a clean label.
  - M4.5 (2026-09): 34, then 53 cases from escaped defects and clean controls.
  - M5.2 (2026-10-08): 57 cases from the orchestrator's adversarial review rounds (90 gold defects),
    split dev/held-out by PR with a fixed seed; #542 added 22 fresh clean cases.
  - Phase 1 (2026-10-30): 108 escape cases (review-134..241) from defects that escaped to `main` and
    were later fixed: 80 dev and 103 held-out defects, labelled under an approved rubric.
- **Grading:** originally a ±5-line location match (`gradeReview`). Phase 0 showed it mis-credits both
  ways, so from #1059 the eval uses a **two-judge semantic matcher** (Claude Sonnet 5.5 and Codex Terra
  6.1 must both say a blocking finding describes the gold defect); agreement with a code-reading
  audit was 93–97%.
- **Clean false block:** a request-changes verdict on a clean case. Every clean-case block that
  decided anything was audited, and several "clean" labels turned out to be real defects (below).
- **Statistics:** paired comparisons on shared cases, PR-clustered bootstrap, one-sided 95% bound.

## Chronology of what we tried

### M4.5 — review quality (2026-09-28 to 10-03)

Built the review-system machinery (shared `runReview`, `eval --systems`, finder panels with a
grounded cross-vendor verifier, consequence-based severity, a round schedule, repo lenses).

| Experiment | Result | Decision |
|---|---|---|
| Single reviewers, k=3 (Opus 5.5, Sonnet 5.5, Sonnet 5, Sol 6.0, Sol 6.1) | Sol 6.1@medium best: 27.6% recall, 18.2% clean FB, $15.6 | Production review → Sol 6.1 |
| Panel: Sol adversarial + Opus careful + verifier | 44.8% recall but 63.6% clean FB (3.5×) | Not adopted |
| Verifier calibration analysis | Verifier confirms 94% of findings, refutes 1.8%; verdicts don't discriminate clean from gold. Panel value comes from two finders | — |
| Cross-vendor verifier replay (1,005 stored candidates) | Vendor shifts severity level, not discrimination; no change in false blocks | Not adopted |
| Held-out clean validation (19 "clean" cases) | **6 of 19 "clean" merged PRs had real ≥medium defects.** On the 13 truly clean: single 28% FB, panel 59% | Panel stays opt-in |
| Local-model lens finder | Ran 1 of 158 trials (timeouts) | Dropped from default roster |

Design notes: `history/08-code-review.md`.

### #235 — causal attribution in the verifier (2026-10-03)

The verifier was asked whether each finding was introduced by the change. Null result: all 30 paired
clean outcomes identical, recall 45.6% vs 44.4%, +28% tokens. The verifier calls 89% of confirmed
findings "introduced". Regrading with corrected labels showed 12 of the 17 "false" blocks were on
cases later relabelled real.

### M5.2 — review parity with the orchestrator (2026-10-08 to 10-21)

Dataset of orchestrator-found defects; pre-registered variants, each run once on held-out.

| Variant | Dev | Held-out | Decision |
|---|---|---|---|
| E1 higher effort (#508) | — | — | Not adopted |
| E2 Opus (#522) | Opus 12.8% vs Sol 35.1% | — | Not adopted (also found production was routing review to Opus for Codex-implemented runs — fixed 10-23) |
| E3 adversarial prompt (#531) | +12.2 after clean audit | +7.0 (< +8), clean FB +1 | Not confirmed |
| Probe + dependencies (#661) | −10.2 | — | Not adopted (execution as a filter hurts) |
| **D union of 2 adversarial samples (#551)** | 47.4% vs 33.7% | +17.0 recall but clean FB 10/26 vs 7/26 (+3 > 1) | Not adopted under the old rule — **re-opened 11-01** |
| Requirement/entry-point trace finder (#552) | −3.1 | — | Not adopted |
| AGENTS.md defect checklist (#553) | +6.3 (< +8) | — | Not adopted |

Review-strength research (`history/14-review-strength.md`): production missed 30 of 49 dev defects;
13 needed files outside the diff, 9 needed running adversarial input; security 0/12, spec-mismatch 0/6;
the reviewer stops early (~1.1 findings, ~2 of 20 minutes).

### Review-improvement research (2026-10-29 onward)

**Deep research** (`notes/literature/`, report `notes/report-fix-the-ruler-2026-10-29.md`): five
angles — recall techniques, precision/decision layers, execution and security, external corpora,
eval methodology. Main conclusion: *fix the ruler first.* The ±5 grader, 8 clean trials and
run-to-run variance of 8–10 points meant the old rule missed a real +10 gain about 40% of the time.
No external corpus fits (none is TypeScript-heavy, defect-verified and has clean PRs).
Plan with options A–G: `notes/plan-2026-10-29.md`.

**Phase 0 — fix the instrument** (`data/phase0/`, `RESULTS.md`):
- Grader audit: of 192 uncredited near-misses, 27 were the same defect; of 166 credited ±5 matches,
  36 were different defects. Replaced by the judged matcher (#1048 → PR #1059).
- Clean-case audit: review-068, -092 and -108 "clean" cases had real defects (one later fixed on
  `main` by #647); review-114 is a harness artifact (its change edits the eval dataset the snapshot
  strips).
- Judged dev recall: production 31.6%, Sol@high 41.8%, adversarial 49.0%, D 47.4%; held-out
  production 18.6%, D 33.0%.

**Phase 1 — a bigger, independent corpus** (`data/phase1/`, `RUBRIC.md`, `PILOT.md`,
`ESCAPES_RESULTS.md`):
- Labelling rubric approved by Matt 10-30: five policy questions plus severity = consequence ×
  realistic trigger.
- 161 review rounds → 448 escape findings adjudicated by two vendors with reproductions; severity
  raters (v3 validated 18/20 on a fresh blind set); 183 gold escape defects; 108 new cases.
- Pool adjudication of 1,130 unmatched stored findings → 70 new dev gold groups (kept as a separate
  tier; never used for held-out).
- Fresh escapes-dev runs (80 defects, k=2), judged recall: production 16.9%, Sol@high 30.6%,
  adversarial 28.5%, **D union 36.2%**, Terra adversarial 28.7% ($0.03, 30 s), Luna 2.5–4.4%,
  Haiku screened out on latency.

**Lab prompts and Terra variants** (10-31, `notes/lab-prompts.md`): compared our prompts with the
Codex `/review` rubric, Anthropic, Gemini and PR-Agent prompts. Gaps: no anti-early-stop rule, no
out-of-diff procedure, and the single-reviewer adversarial text says "a separate step verifies each
finding" when none does.

| Arm (escapes-dev 160 defect-trials, 32 clean trials) | Judged recall | Clean FB |
|---|---|---|
| Production (Sol standard) | 16.9% | 2 |
| Terra adversarial | 28.7% | 6 |
| Terra "thorough" (keep going) | 33.8% | 7 |
| Terra "callers" (trace callers and deleted invariants) | 30.6% | 7 |
| Union of 2 | 36.9% | 8 |
| Terra specialist panel + Sol verifier | ~41.6% | 13 |
| Calibrated-severity finder prompts (3 variants, p4) | 26–39% | 6–9 (null) |
| Rubric severity in the panel verifier (p5) | 39.4% | 9 |

A blind audit of every clean-case block found the claims real but minor: the failure is
**severity over-rating**, not hallucination. Finder-prompt wording could not fix it (p4).

**Rubric verifier and the fast lab** (11-01): the verifier's severity section was made configurable
(eval-only, PRs #1108 and #1112) and variants were screened. After Matt pointed out that a
PR → land → deploy loop per experiment was far too slow, we built an **in-process lab**
(`tools/lab/`): it runs the eval code from a checkout against a copy of the daemon database, giving
numbers in minutes instead of hours.

| Lab run | What | Result |
|---|---|---|
| p6 clean stage | Variants A (no requirement override), B (reach path required), C (step procedure) | Clean FB 9 → 1–2 of 18 |
| p6 defect stage | Same, 29 positive cases | All lost too many defects (A 57 of control's 63) — the override carried request-named failure paths |
| p7 screen | D = A + failure paths realistic; E = narrow override | D 12/18 defect-trials, 3 clean |
| p8 (= full dev for verifier-only changes) | Control / A / D / D2 | 63/9, 57/1, 65/3, **64/2** (blocked of 106 / clean of 18) |
| p9 held-out | D2 panel | 34.4% recall, 6/18 clean FB — dev win did not transfer |

The held-out clean audit (`data/heldout-audit/heldout-audit.md`) confirmed review-124, -130 and -133
are clean: the verifier over-rates patterns that predate the change and triggers that need an operator
action mid-run. The rubric-verifier line was shelved, and union of two — the strongest held-out
result — went to Matt, who adopted it.

### Shipping it (PR #1122)

- `[review] samples` (default 2; `1` restores one standard review).
- The engine now applies the adversarial prompt itself (before, only the eval runner did, so
  production would have run the standard prompt twice — never measured).
- A sample's cancellation or capacity error reaches the engine with its own type.
- The orchestrator's review found two real defects, both fixed: findings citing different prior
  blockers must never merge (a merge could erase a blocker), and a restart must reuse a finished
  sample rather than re-roll it (saved as `review-N.sample-K.json`).

## What we learned

1. **The ruler was the first problem.** A location-based grader, eight clean trials and unaudited
   clean labels made real gains look like noise and noise look like gains. Judged matching, audited
   clean labels and paired statistics changed several decisions.
2. **"Clean" labels are often wrong.** Across M4.5, #235, #535 and Phase 0, a large share of
   "false" blocks were real defects. Audit every clean-case block before it counts.
3. **Detection is not the main gap; severity is.** Strong reviewers raise the defect but rate it
   minor, or raise real-but-minor issues as major. Verifiers confirm almost everything and only shift
   severity levels.
4. **Diversity beats instructions.** Two independent samples of the same reviewer gained more than any
   prompt, effort, model or verifier change. Prompt wording moved *which* cases false-blocked rather
   than how many.
5. **Dev wins often fail on held-out.** E3, D2 and others passed dev and failed held-out. Pre-register
   the rule, design on dev only, spend held-out once.
6. **Fast iteration needs a lab.** Routing every experiment through a release took hours; the
   in-process lab turned a verifier variant into a 15–70 minute run.
7. **Production can differ from what you evaluated.** Review was routed to Opus for Codex-implemented
   runs for weeks; the adversarial framing was applied only in the eval runner. Check the production
   path, not just the eval path.

## Open questions and follow-ups

- Later review rounds of the union were never measured (the corpus is first-round only).
- Doubling review calls raises Codex slot contention; a sample can fall back to another model. Watch
  the model distribution after deploy.
- The held-out set has now been looked at several times; any new candidate needs a fresh held-out set.
- Remaining levers from the plan: out-of-diff impact packs (13/30 misses), execution that only adds
  findings, a security attack pass (security 0/12), acceptance tests written from the request
  (spec-mismatch 0/6), severity anchored to "pre-existing pattern" and "operator action mid-run =
  contrived".
- Routing-policy generation still treats standard single systems as production-shaped evidence.
- Pool gold (70 dev groups) is not yet in `cases.json`.

## What is in this folder

- `report.md` — this write-up.
- `notes/`
  - `lab-notebook.md` — the working notebook (status log, every run, decision and number).
  - `plan-2026-10-29.md` — the options plan (A–G) for ≥10 points.
  - `report-fix-the-ruler-2026-10-29.md` — the deep-research report; `literature/` holds its five
    per-angle notes (recall techniques, precision layer, execution and security, corpora, eval
    methodology, internal findings).
  - `lab-prompts.md` — comparison of public review prompts with ours.
- `history/` — the earlier design and research docs from the Limitless repo
  (`08-code-review.md`, M4.5; `14-review-strength.md`, M5.2), copied for completeness.
- `data/`
  - `phase0/` — grader and clean-case audits, judged rescoring, `RESULTS.md`.
  - `phase1/` — rubric, pilot, escape and pool adjudication, severity raters, `ESCAPES_RESULTS.md`.
  - `grader-audit/` — ±5 grader audit candidates and verdicts.
  - `evals/` — every eval systems file, case list and stored eval report used from 10-21 on.
  - `lab/` — lab run outputs (p6–p9) and the like-for-like held-out judgements.
  - `mini/` — per-defect caught matrices for the mini-eval and held-out comparison.
  - `heldout-audit/` — the held-out and dev clean-case block audits.
- `tools/`
  - `lab/` — the in-process lab (`lab.ts`, `judge.ts`, `sync.sh`, README).
  - `scripts/` — Phase 0/1 analysis and adjudication scripts.
  - `mini/` — per-defect matrix and case-selection scripts.
  - `eval-supervisors/` — the shell supervisors that resumed and judged long eval runs.

### Not included

- Git worktrees, repository caches and copies of the daemon database (about 96 GB, regenerable or
  private), raw Codex traces, and run logs.
- Home-directory paths are written `~`, the local username `<user>`, and strings on Limitless's
  private-strings list are redacted.
- Eval runs live in the daemon database; the stored report JSON here is their exported form.
