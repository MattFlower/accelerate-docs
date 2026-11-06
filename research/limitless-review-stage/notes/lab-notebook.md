# Review-stage improvement research — working notes (started 2026-10-29)

READ THIS FIRST after a context clear. Task from Matt (2026-10-29):
"Review stage is meant to find bugs; make it absolutely as good as possible; happy to spend tokens.
Review what the repo does + what the repo research shows, then /deep-research what it would take to
improve review by >=10%. Dig for weak points. Maybe a better, heavily-analysed defect corpus exists
than ours. Research independently, form a plan with SEVERAL options (not just the best one).
Long running; I'll clear context — take good notes."

Session worktree: ~/code/limitless/.claude/worktrees/bun-test-performance-7b568d
(branch claude/limitless-review-improvement-9a86a9, = origin/main fa71b024 at start). Hand-run session.
Deliverable plan: write to docs/research/15-review-improvement-plan.md in worktree? (decide) + artifact.

## NEXT ACTION
10-30 MATT APPROVED RUBRIC: Q1-Q5 as recommended + severity line = consequence x realistic trigger (my pilot minor rulings on contrived triggers confirmed). PHASE 1 IN PROGRESS (see phase1/PILOT.md). Pending:
(a) PR #1047 (head 5d2251ae) CI green; HANDED to "Limitless system build" 10-30; queued as land entry 326 pinned 5d2251ae. Future labelHistory "by": say "the review-stage session", not "orchestrator". After it lands + deploys, held-out has 10 clean.
(b) SENT 10-30 to Matt: RUBRIC.md (Q1-Q5), spotcheck_batch1.md (20 pilot labels), PILOT.md, D correction (true clean 4/20 vs
    2/20 = doubling), #1047's 3 disputes ruled minor. AWAIT his answers before --write of escape cases.
(c) DONE: severity rater v2 (scripts/p1_sev.py -> sev2/: consequence+trigger, code mapping, Q5 secret+unusual=major,
    random A/B); validated vs my rulings (phase1/my_sev_rulings.json): consensus 86% right; splits -> me.
(d) DONE: Opus no-fix test: severities unchanged -> keep template.
(e) POOL ADJUDICATION DONE 10-30 09:26 -> phase1/pool_merged.json (scripts/p1_pool_merge.py): 386 claims (incl "<id>b"
    splits): agree_gold 79, sev_dispute 107, agree_minor 68, agree_reject 42, verdict_dispute 66, split_one_side 24.
    Both-REAL not gold-dup: 213; of those with >=1 adjudicator blocking: 147 across 45 of 52 cases (review-054: 11!).
    41 both-REAL claims restate existing gold (= pooling sanity check). Verdict disputes with a blocking REAL side: 27 -> my rulings.
    RUNNING: raters on pool (p1_sev.py prompts pool_merged.json -> sev2/pool-*.prompt; log phase1/pool_sev_run.log).
    p1_sev.py score now takes [merged.json out.json]: run `score phase1/pool_merged.json phase1/pool_sev_scored.json`.
    CAUTION before adding pool gold: (1) pool bias: stored arms get credit for what they found -> report recall on old gold
    and new gold separately; (2) 147 new on 45 cases vs ~1-2 gold/case would dominate the metric -> sanity-sample review-054;
    (3) require origin introduced/newly_exposed + rubric severity line, same as escape labels.
(h) #1048 judged matcher LANDED 10-30 as PR #1059 (69512e88), deploy queued. `limitless eval judge <eval-id> --judges a,b`;
    `eval report` shows judged recall, per-judge recall, contested/unjudged, agreement beside ±5. Spend persisted across
    reruns (--max-usd cumulative); agreement = both matched some finding for a gold or both none; unjudged excluded from
    judged metrics. FUTURE NEED (not yet asked of orchestrator): recall split by gold provenance (orchestrator/escape vs pool)
    once pool gold is tiered.
(e2) POOL CHECKS 10-30 (advisor: validate before trusting the 113-117 consensus gold):
    - v2 raters on pool: 117 consensus-gold; repro by >=1 adjudicator 112/113. 92 dev / 21 held-out (19 of 52 pool cases are
      held-out -> pool gold must stay OUT of held-out decisions; tier it, e.g. provenance "pool").
    - MY BLIND VALIDATION (phase1/pool_val_keys.json, pool_val_mine.json): v2 consensus agrees 13/20 = 65% -> does NOT
      transfer. All 7 misses: raters call harmless effects "wrong" (self-correcting status text, extra JSON field, queue
      reorder, missing convenience w/ workaround) or plausible where trigger is contrived. Opus adj said minor on all 7.
      Single-adjudicator rules: Codex 16/20 (4 FP), Opus 14/20 (6 FN); on pilot both ~50% -> no shortcut.
    - RATER v3 (scripts/p1_sev3.py -> sev3/): adds consequence "nuisance" (-> minor) and a harm threshold on "wrong".
      Running on pool + pilot (sev3_run.log). Tuned on the 20 + pilot, so VALIDATE ON A FRESH 20 (exclude pool_val_keys).
      If v3 < ~85% on fresh 20 -> I rule every pool candidate myself.
    - v3 RESULT 10-30 16:40: tuning set 10/12 agreed right (8 splits), pilot 15/17 (16 splits); FRESH 20 (pool_val2_keys.json,
      pool_val2_mine.json, 12 v3-blocking + 8 v3-minor): 18/20 (misses W11 workaround-exists, W13 preexisting anyway).
      -> ADOPTED: v3 consensus sets severity; v3 splits (pool: 126 of 326) + verdict disputes -> my rulings. Use sev3 for escape too.
    - 10-30 incident: my until-waiter counted log lines (pool_dedup 51 < 52 because review-054 was run by hand) -> hung ~6.5h.
      Wait on PIDs / output files, not log line counts.
    - Escape runners collided on limitless-747-r1 (both wrote the same .tmp) -> opus out moved to .collided, re-run.
    - DEDUP (scripts/p1_pool_dedup.py, Opus text-only, "same natural fix" test, vs existing gold) -> pool_dedup/<case>.json.
      review-054: 23 -> 21 groups, C10 = gold G1 (adjudicators missed). Log pool_dedup.log.
    - Q3 (scripts/p1_pool_q3.py: request explicitly requires it?) -> pool_q3/<case>.json; not_explicit gaps are not gold.
    - Terra omits 5 ids even on rerun (046 C4/C6, 070 C7/C10, 101 C4, 105 C8) -> my rulings.
(f) Escape run: adjudication DONE (all 161 rounds, 747-r1 re-run). 10-30 evening: `p1_merge.py all` -> merged.json
    448 findings: agree_gold 115, agree_minor 97, sev_dispute 187, verdict_dispute 24, agree_reject 25, missing 0.
    My rulings on the 22 unruled verdict disputes are in my_sev_rulings.json (reasons: my_dispute_rulings_escape.json);
    only 687-r1/F2 (waiting approval entry blocks the repo's land slot) is gold. v3 raters RUNNING: sev3_todo.txt
    (304 jobs, xargs -P4, log sev3_run.log, ends with DONE). p1_label.py now reads sev3_scored.json (env SEV overrides).
    DONE 10-30 late: v3 scored (289 agree / 133 split); my 113 split rulings in my_sev_rulings.json (80 minor, 29 major,
    4 blocker; precedent: untrusted-controlled trigger crossing an enforced boundary = realistic; 863-r1/F1 low confidence).
    escape_labels.json: 183 gold (159 major, 24 blocker) / 265 not. escape_confirm.json -> generator --write: 108 cases
    review-134..241 (51 escapes-dev / 57 escapes-heldout), defects 80 dev / 103 held-out; matches labels exactly.
    Branch claude/review-escape-gold commit 4ee8fc2f (cases.json + LABELS.md section "Escape-case labelling — 2026-10-30").
    2 cases had /Users/<user>/ placeholders -> rewritten ~/ (evals-cases path test). cases.json now 2.0 MiB > biome 1 MiB
    (biome skips it, warning only). NOTE: `limitless eval run review` without --cases now runs 243 cases incl.
    escapes-heldout -> always pass --cases (rule added to LABELS.md; PR #1071 head now 358caf6f, sent to orchestrator;
    code enforcement = issue #1072, no priority label yet). NEXT: bun run check result, PR, orchestrator handoff; then pool rulings and
    rescoring Phase 0 arms on escapes-dev (judged matcher).
(e3) POOL DEV DONE 10-30 late: pool_mine.json (122 dev rulings) -> scripts/p1_pool_label.py -> pool_labels.json:
    dev 70 new_gold groups (63 major, 7 blocker), 26 existing_gold, 145 not; held-out 19 groups unresolved (not needed:
    pool gold never decides held-out). RESCORE (scripts/p1_rescore_pool.py, RESULTS.md "Phase 1 rescore"): combined dev
    production 23.3, sol@high +10.6, E3 +11.4, D +15.7, E +3.4, probe -6.4, opus -9.3. Ranking survives bigger gold.
    NEXT: write pool gold into cases.json? (decide: optional tier vs required); fresh dev runs on escapes-dev
    (80 defects, no stored trials) for production / sol@high / E3 / D + cheap models; clean-block cost of D.
(e4) 10-30 Matt: "Yes, run them" (fresh escapes-dev runs). Needs #1071 landed + DEPLOYED (cases load from release
    checkout); orchestrator queued land+deploy and will message. Detached launcher scratchpad/launch-escapes.sh (log
    ~/limitless-orch/evals/launch-escapes.log) waits for review-241 in ~/.limitless/app cases.json, then runs
    `eval run review --systems evals/p1-escapes-main-systems.json` (prod, sol@high, E3 adversarial, D union2) and
    p1-escapes-cheap-systems.json (haiku-5.5@high std/adv, luna@medium std/adv), --cases escapes-dev-cases.txt (51), --k 2.
    10-30 23:2x: two launch attempts CANCELLED (ran on OLD daemon f6c6bbb6, which skips unknown cases; deploy updates the
    checkout before restarting). Launcher v2 (scratchpad/launch-escapes2.sh) waits for /api/health "sha" to contain
    e492b400, then starts both evals with --concurrency 8. CURRENT eval ids: ~/limitless-orch/evals/escapes-state.txt,
    kept by detached scratchpad/supervise-escapes2.sh, pid in evals/supervise.pid (resumes INTERRUPTED evals at most 3x each, never auto-resumes FAILED -> "NEEDS ATTENTION" in log; log supervise-escapes.log,
    writes ALL COMPLETED when both finish). Hourly cron check-in 2deee1c7 judges + publishes.
    Terra 6.1: orchestrator OK'd runtime row; ADDED 10-30 (`codex/terra-6.1`, gpt-6.1-terra); probe
    eval-mvvs9sso1r2o4sp1os41u3 passed; Terra std/adv added to cheap systems. MUST: `catalog remove codex/terra-6.1` after
    the screen and tell orchestrator; NEVER generate/apply routing policy from these evals while Terra trials are in them. After runs: `eval judge <id> --judges ...` then report recall + clean? (escape
    cases have no clean cases; false-block cost still from heldout clean set).
    01:12 check-in: Luna std/adv COMPLETE (102/102 each). Haiku 5.5: 4 errors in first 12 trials = 36-min TIMEOUTS (3) and
    'no progress for 600s' (1), Claude concurrency low -> would hold cheap eval ~a day. PLAN: when Terra std+adv reach
    pending=0, (1) kill the supervisor (pid in evals/supervise.pid — my own process), (2) `eval cancel` the CHEAP eval
    (Haiku left partial; report it as screened out on latency with partial recall + timeout rate), (3) restart the
    supervisor for the MAIN eval only (state file with just the main line), (4) treat cheap as done for the results step.
    02:12 DONE: Terra complete (102/102 each, 0 errors); supervisor 48314 stopped; cheap eval-mvvv3pum0kriw040gi0x29
    cancelled (Haiku 16+16 trials, 2+3 errors); supervise-escapes3.sh (pid evals/supervise.pid) watches main only.
    Judging of the cheap eval started 02:14 (`eval judge ... --judges claude/sonnet-5.5,codex/terra-6.1@medium`).
    02:32 daemon restart (#1062 deploy): main resumed by supervisor as eval-mvw0y6v31sec2vc1agx2t1 (prod/E3/D complete,
    sol@high running); cheap JUDGING was killed -> re-run 03:13 detached (log evals/judge-cheap.log). A judge job dies
    on any daemon restart: if unjudged counts stall, re-run `eval judge` (keeps finished judgements).
    04:13: detached scratchpad/judge-main-when-done.sh judges main when it completes (log evals/judge-main.log, ends
    "JUDGE DONE"; retries up to 3x if a restart kills judging). Cheap judging: Luna 2.5/4.4%, Terra std 25.6%.
    Main at 02:12: prod/E3/D 36 of 51 cases, sol@high not started yet (scheduler runs it last) -> ETA ~05:00.
(e5) RESULTS 10-31 05:3x (phase1/ESCAPES_RESULTS.md; page https://claude.ai/artifact/EbjsXZMxL4umyEZ8kuHknW):
    escapes-dev judged recall: prod 16.9, sol@high 30.6 (+13.8), E3 28.5 (+11.6), D 36.2 (+19.4), Terra-adv 28.7 (+11.9,
    $0.03, 30 s), Terra-std 25.6, Luna 2.5/4.4, Haiku partial + 17/32 over 20 min. No Terra judge self-bias. Terra row
    REMOVED + orchestrator told. Proposed (awaiting Matt): held-out decision run on escapes-heldout + heldout clean set:
    prod, sol@high, E3, Terra-adv, D, Terra-adv x2 union (re-add Terra row via orchestrator). Cron 2deee1c7 deleted.
(g) Fresh sweeps (cheap models first) only after pool yield is known.

## Advisor guidance (10-29) — key points
- Measurement is track 1: clean-FB rule rejects variants on mislabeled clean cases (M4.5 6/19, #235 12/17, #535). Option: blind 2-vendor audit of every clean-case block before it counts; ask Matt FB-vs-recall trade.
- Audit ±5-line grader: sample prod misses for same-defect-elsewhere findings (free, stored trials).
- Unbiased gold = escapes to main (SZZ-style fix commits citing earlier PRs).
- '10%' = >=10pp absolute (relative 3.4pp is noise). Say so.
- Later rounds: new non-security majors become follow-ups -> policy, not detection? verify.
- Shadow-mode candidate D on production for big denominators.
- External corpus criteria: PR-level runnable base/head; defects verified by later fix/test; TS overlap; contamination; licence; harness fit.
- Respect no-rerun-paid-baselines; old held-out spent (E3, D) -> fresh held-out needed.

## Status log (newest first)
- 10-29: deep research launched: 5 researchers -> research_notes/Code review recall improvement/*.md; report -> reports/Code review recall improvement.md. Confirmed later-round rule: single review R2+ new non-security majors -> follow-ups (review.ts blockingReviewFindings). TODO analysis: how many orchestrator-found defects were already in factory follow-ups?
- 2026-10-29 start: read memory (m52-review-eval-dataset, limitless-m45-demo-material, replay-235,
  matt-decisions-10-23) and docs/research/14-review-strength.md. Next: map code, deep research.

## What we know (from memory + research/14) — baseline facts
- Production review = single reviewer. Routing: avoidVendor = implementer vendor; implement is
  Codex-first so prod review was claude/opus@high for most runs until 10-23; Matt then said switch
  review to Sol (codex/sol-6.1). VERIFY current routing in code (src/router, engine.ts ~1852).
- Eval corpus: evals/review/cases.json (+LABELS.md). Gold = defects the orchestrator's adversarial
  (Codex) reviews found on factory PRs that the factory reviewer approved. M5.2 dataset 57 cases
  review-040..108 (90 gold), + #542 fresh clean set (+22 clean, +3 real) => review-109..133.
  Dev/held-out split by PR (seed 427202610). Held-out was SEEN by orchestrator while labelling.
- Grader: gradeReview — file match, line ±5, one-to-one, only blocker/major count ("blocking recall");
  clean false-block = request_changes on a clean case.
- Numbers (dev, 49 defects): prod E1 sol@medium standard 33.7% recall, 2/8 clean FB; sol@high 42.9%;
  opus 14.3% (opus@high 16.8% on E2's 35 cases); adversarial prompt 45.9%. Held-out: 25.6% vs 32.6%.
- Variants tried, NONE adopted: E1 effort, E2 Opus, E3 adversarial prompt (held-out +7 < +8), probe+setup
  (#661, -10), D union of 2 adversarial samples (#551: dev 47.4%, held-out +17 recall but clean FB +3),
  E trace finder (#552, -3), F checklist (#553, +6.3). M4.5: panel (2 finders+verifier) +16pp recall but
  FB 3.5x; verifier confirms 94% — doesn't discriminate; cross-vendor verifier no change; causal attribution null.
- Error analysis of 30 prod misses: 13 need files outside diff, 9 need running adversarial input,
  7 visible in diff, 1 convention. Security 0/12, spec-mismatch 0/6. 18 found by no system.
- Sol "stops early": ~1.1 findings/trial, uses ~2 of 20 min.
- Decision rule used so far: +8pp pooled dev recall, clean FB +<=1, held-out once.
- STRUCTURAL WEAKNESSES OF THE EVAL (my early read):
  * tiny clean denominator (8 dev trials; held-out clean saturated) -> FB rule is noise-dominated;
    D (+17 held-out recall) was rejected on +3 clean FB out of 26 trials.
  * gold = "what orchestrator found" (recall relative to orchestrator); reviewers' real extra finds earn 0.
  * line ±5 matching may miss correct findings at another location (e.g. root cause vs symptom).
  * k=2, ~49 defects -> CI wide (±10pp); +8 rule hard to pass, easy to miss real gains.
  * corpus is all one repo (Limitless), concentrated in redaction/confinement/later-round cases.

## Open questions to answer
1. Current production review config (prompt, model, effort, rounds, verifier?) — read code.
2. Latest eval results after 10-23 (any since?). R epic #824 / R1 #827 (findings -> review-eval cases).
3. External corpora: SWE-PRBench, c-CRAB, Martian benchmark, SWR-Bench, CodeReviewer, Defects4J,
   BugsInPy, GHRB, SWE-bench-derived "bug-introducing PR" sets, ContextCRBench, etc. Which are
   heavily analysed + defect-labelled at PR level + licence + contamination?
4. Techniques beyond what was tried: agentic exploration budget, forced exhaustive enumeration,
   per-file/per-hunk decomposition, multi-model union with calibrated severity, execution/PoC,
   mutation-style "what could break", spec tracing, learned project rules, reviewer that writes tests.

## Internal findings (2026-10-29, session 1)
- Prod config: [review] avoid_implementer_vendor=false (Matt 10-23) => single-mode review on default
  review chain (Sol 6.1 @medium per evals; verify chain in config/policy). Lenses ([[review.lenses]] in
  .limitless.toml: compatibility-and-operations) apply ONLY to panel finders -> unused in prod single mode.
- Single-mode prompt: src/pipeline/prompts.ts reviewPrompt (~line 461). Has FINDER_FRAMING for panel
  prompts standard/adversarial/careful/trace/probe. Single mode lacks "report every issue".
- Shadow review: `limitless review shadow-report` -> "No shadow review comparisons" (shadow off).
- Last review eval = eval-mvlhu0571ydkrqq15dbjsa (10-23, opus@high). No review evals since.
- CLI: `cd ~/.limitless/app && bun src/cli/main.ts eval ...` (no `limitless` on PATH in my shell).
  DB read-only: sqlite3 -readonly ~/.limitless/limitless.db (tables eval_runs, eval_trials, review_rounds).
- **BIG UNUSED CORPUS**: review_rounds (orchestrator's findings sent back as factory rounds) since
  ~10-07: 209 review rounds on 136 PRs, 534 findings (146 blocker, 259 major, 121 minor, 8 nit).
  Current corpus gold ~90+. Each is a production-review miss (factory reviewer approved first).
  #833 "review-round escapes become review-eval cases" exists (tooling) — check if used.
  M5.2 adjudication rate was ~50% gold (183 candidates -> 90 gold).

## Internal analysis results (10-29) — scripts in session scratchpad an/ (followups.py, era.py; may be wiped)
- Production reviews since 10-07 (review-N.json artifacts): claude/opus 398 reviews, 1.21 findings/review
  (233 minor, 145 nit, 20 blocker, 83 major) — UNDER-RATES; codex/sol-6.1 299 reviews, 0.57 findings/review
  (72 blocker, 90 major, 7 minor) — reports very little (stops early, even more than eval's 1.1).
- Of 405 orchestrator blocker/major findings (review_rounds since 10-07), heuristic match (same file, line±10
  & title-word overlap>=0.3, or overlap>=0.5) to an EARLIER factory finding on the same PR:
  13 matched a factory BLOCKING finding (repeat/unaddressed), 26 (6.4%) matched a factory NON-blocking
  finding: 22 rated minor/nit (23 of 26 by Opus) + 4 major parked as later-round follow-ups.
  => severity under-rating / follow-up parking accounts for ~6% of escapes (lower bound; heuristic).
- Escapes per PR roughly equal by reviewer model: PRs whose last factory review was Opus: 2.0 orch round-1
  B/M per PR (79 PRs), Sol: 1.84 (50 PRs); ~3.0 across all rounds for both. Model switch did not visibly
  cut escapes (confounded). 475 runs with PRs since 10-07; 136 PRs got orchestrator review rounds.
- Grader audit (scripts/grader_audit.py over E1 eval-mv7igcxy1tl7bg203warej, E3 eval-mv8gnw6f03ggcas1ml9ate,
  E3-heldout eval-mv92iu6p0y8ns1b0ifjg8t, D eval-mvi7bktt0cz50o81qkik8c, D-heldout eval-mvif9n84010bmzy1tk9std):
  651 required defect-trials, 264 caught, 387 missed; 192 missed have an uncredited blocking finding in the same
  file (173) or title overlap>=0.5. Subagent adjudicating SAME/DIFFERENT -> scratchpad an/grader_verdicts.json
  (copy to ~/limitless-orch/review-research/ when done).
- #833 generator (scripts/review-escape-cases.ts) exists; labelling pass NOT done; cases.json still 135.
  So corpus expansion from review_rounds = run generator + model-proposed labels + orchestrator confirm.
- **How the gold is generated (orchestrator method, tools/review-*.sh + orchestrator-bin/codex-review.sh):**
  (1) Orchestrator (Claude, full context: issue, spec, prior rounds, memory of recurring defects) writes a
  PR-SPECIFIC ~1.5-2 KB brief: requirements restated as concrete checkable claims ("loaded only for exit 0...",
  "used by rollback, recovery, reconcile, install..."), targeted questions ("Does any caller still have its own
  inspection?", "Do the tests fail without the round?"), required test inputs; P1/P2/P3 with file:line + repro.
  (2) `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write` executes it (may add failing
  regression tests). (3) Mutation check: revert src diff, run the PR's tests -> must fail. (4) Tests unconfined +
  gate env; biome + tsc. Factory review = one generic prompt at @medium, read-only, no brief, no mutation check.
  => STRONG OPTION: "review brief" planner stage (PR-specific verification plan) + executor(s) at high.
- 10-29 research done: precision_decision_layer.md (key: verifiers accept >96% valid but reject <25% invalid —
  Beyond Consensus 2510.11822; minority veto better; witness program = strongest discriminator (CMU 2607.09979,
  0 FP valid triggers, 60% of real bugs witnessed); debate raises recall+FPR not precision; uReview per-category
  thresholds; recommended rule: block on witness OR k-of-n agreement in high-precision categories; rest = comments;
  3/26 FB CI 2.4-30% => noise).
- 10-29 research done: eval_methodology.md (key: +10pp @80% power needs ~160-200 gold defects at k=2, ~110-130
  at k=4 (Miller 2411.00640); observed 8-10pp same-system run gap ~2x trial noise -> run-level drift + matcher
  instability -> do A/A runs; +8 rule false-accept 16-21% at SD 8-10; clean guardrail: 0/8 -> UB 37.5%,
  need 62-124 paired clean trials for 10pp margin; use PR-clustered paired bootstrap, adopt if LB>0;
  LLM-judge matching (diff family) with location as prefilter, validate on 50-100 hand pairs; TREC pooling +
  blind adjudication; SZZ R-SZZ precision .66-.73 -> candidates only; shadow eval on production).
- 10-29 research done: corpora.md (key: no external set meets all needs; only SWR-Bench has clean PRs (Python).
  Top: GitHub ReviewBench (2026-10-05, 219 PRs, 68 TS + 15 JS, MIT, containerised, gold mostly machine-made,
  top recall 26%) ~60-80 usable TS/JS; SWE-PRBench (350 PRs, 21 TS + 37 JS, human comments, no env);
  c-CRAB (Python, test-verified; method value). SecBench.js 600 npm exploits = security exec set.
  Recipe for own escapes: fix PRs explicitly naming the inducing PR -> replay inducing PR at its base.
  Recommendation: in-house primary; ReviewBench TS slice as external check; grow in-house via linked escapes.)
- 10-29 research done: execution_security.md (key: execution must ADD findings, never filter (explains probe -10);
  repeated attempts strongest lever (CyberGym 28.9%->66.7% at 30 trials); AIxCC: diff hints = 15/22 wins beyond
  fuzzing, LLMs beat URL/Unicode encodings; keep a gated lane for no-PoC findings; rigid PBT scaffolding hurts
  strong models (PBT-Bench); Anthropic agentic PBT 56% valid (86% top-ranked); sibling-caller-missing-check pattern;
  design: trust-boundary-triggered attack pass w/ per-boundary attack catalog (encodings, chunk splits, crafted
  repos, output spoofing), fast-check + examples via bun test, 2-3 attackers unioned, validator only labels/demotes.)
- 10-29 research done: recall_techniques.md (key: CRBugBench 2610.13668 — reviews stop early (gpt-5.6-sol half by
  turn 17), exploration/comprehensiveness prompt +5-6 top-5 recall for GPT-family, nothing for opus-5; out-of-diff
  bugs OR 2.6 harder; ensemble 5 +4.7 @5.5x. SecPRBench (10-24): 68% of missed security bugs = right file, wrong
  mechanism; union of 8 agents 91.3% vs 78.1% best single; Anthropic Defending Code harness (threat model ->
  attack-surface partitions -> PoC verifier) +7.7 @10x, found all concurrency bugs. Greptile: model inversion
  (own family worse; GPT reviewers depth-first, 1-2 comments) — BUT our eval: Opus 14% vs Sol 34%, so don't assume.
  Separate discovery from verification (Bugbot 0.4->0.7 bugs/run after reversing over-cautious prompt).
  Meta JIT catching tests 4x. Ranked: coverage prompt, inversion, min-candidates finder + evidence filter,
  security pass, acceptance tests from request pre-diff, union 4-6 mixed, mutation-guided catching tests.)
- 10-29 GRADER AUDIT DONE (grader_verdicts.json here): 192 uncredited-candidate misses -> 27 SAME, 158 DIFFERENT,
  7 UNCLEAR (review-049 sibling-function x6, review-066 x1). 10 of 51 distinct defects have a SAME (058, 077x2,
  098x3, 105, 103, 060, 061). Typical: root cause in another file/caller, line just past ±5, catch site.
  Per system SAME: E1 sol@medium 3, sol@high 3, E3 adv dev 8, E3 heldout adv 2 / std 2, D dev 6, D heldout 3.
  => ±5-line grader under-credits ~3pp for production, ~8pp for adversarial (dev E3 45.9% -> ~54.1%; E1 33.7 -> ~36.7);
  bias FAVOURS conservative systems; advisor's suspicion confirmed. Fix: LLM-judge matching (location prefilter).
  Watch double-credit: one finding (catalog.ts:94) matched two review-098 golds.
- 10-29 MATT: "we can run a lot of trials once we choose to implement. We don't have to guess — we can run our
  existing evals or write new ones to test different options." => plan = measurement-first TOURNAMENT:
  (1) fix instrument (escape corpus to ~200+ gold, judge matcher, blind clean audit, A/A variance runs),
  (2) run many options at k>=4 paired, PR-clustered bootstrap; literature only to choose what to try first.
  Purposeful A/A and k=4 runs are OK (no-rerun-paid-baselines was about pointless baseline refreshes).
- 10-29 MATT: "If we have a better corpus, that won't be a problem, I'd guess" (re power). My answer: yes for recall
  power (~405 escape findings -> ~200 gold); still needed: audited clean set (escape corpus is all-real), A/A runs
  for run-level drift, judge-based matcher (±5 bias).
- 10-29 REPORT DONE: reports/Code review recall improvement.md (~5,400 words). Writer's extra analyses (scripts/
  persys.py anysev.py union.py): Opus blocking recall 15.3% but ANY-severity at gold location 29.6% (opus@high 18.9/29.5);
  Sol blocking ∪ Opus any-severity per trial = 50.0% vs Sol 33.7%; Opus catches 12/49 defects Sol never does (needs
  judge check; Opus minors on 5/7 clean trials). Corrected-credit E1 paired: sol@high 46.9% vs @medium 36.7% (+10.2),
  clean 3/8 vs 2/8 — cheapest held-out candidate. Options A oracle-replica, B mixed-model union + two-tier block,
  C coverage prompt + ledger, D trust-boundary attack pass, E acceptance tests from request, F impact pack,
  G deterministic severity + stop parking majors. Don'ts: majority vote, debate, reproduce-or-drop, long checklists.
- 10-29 ADVISOR on plan: (1) grader bias claim one-sided -> audit credited ±5 matches (running: an/credited_candidates.json
  166 entries -> credited_verdicts.json); (2) use own numbers: sol@high corrected 45/98=45.9 vs medium 36/98=36.7 = +9.2
  (NOT report's +10.2; report table base counts differ: flag unreconciled); (3) escape corpus selected on reviewer of the
  day (Opus pre-10-23, Sol after) -> split by PR within era, report per era, fresh baseline runs. Also 2 judges of
  different families for matcher; keep old ±5 score alongside.
- 10-29 MATT: "uncertain about using the existing dataset as a corpus ... hasn't been independently reviewed to find
  additional defects; past improvements weren't in the golden set because they weren't found when it was made."
  -> PLAN.md Phase 1.0 GOLD COMPLETION BY POOLING (all stored findings + fresh diverse deep sweeps, blind 2-vendor
  adjudication, clean cases too, TREC-style incremental judging of new arm findings before each decision).
- 10-29 CREDITED AUDIT DONE (credited_verdicts.json): 166 credited ±5 matches on dev -> 127 SAME, 36 DIFFERENT
  (accidental credit), 3 UNCLEAR. Per system DIFFERENT: medium 7/33, high 9/42, adversarial 11/45 (+3 unclear), D 9/46.
  NET judged dev recall (stored - accidental + missed-SAME): production 33-7+3 = 29/98 = 29.6%; sol@high 42-9+3 = 36/98
  = 36.7% (+7.1); adversarial 45-11+8 = 42/98 = 42.9% (+13.3; 39/98 if unclear removed); D 46-9+6 = 43/97 = 44.3% (+14.7).
  => CORRECTION: the ±5 grader is noisy BOTH ways (~20% of credits accidental, ~4% of misses actually caught); it is NOT
  mainly biased toward conservative systems. Absolute recall is overstated; gaps vs production roughly preserved/slightly
  larger for adversarial & D, smaller for @high (+9.2 one-sided -> +7.1 net). Different-day caveat for E3/D vs E1.
- 10-29 MATT ANSWERS: (1) as much increase as possible; (2) FB: my judgement; >50% relative rise in clean-block rate
  needs considerable gain; extra blocks are disruptive and cause their own errors/drift; (3) most reviews <20 min,
  size-scaled, giant PRs leeway; (4) asked what his confirmation role would be; (5) FIX THE EVAL FIRST.
  NEW IDEA: test cheap models (claude/haiku-5.5 efforts low/med/high $0.10/$0.50; codex/luna = gpt-6-luna; gpt-6.1-terra
  in Codex CLI models_cache, NOT in Limitless catalog -> runtime entry needed) for UNIQUE defects as low-cost union
  add-ons -> PLAN arm T9 + pooling sources. Worktree confirmed: .claude/worktrees/bun-test-performance-7b568d,
  branch claude/limitless-review-improvement-9a86a9, clean (all notes outside repo).
- 10-29 MATT: updated Codex; gpt-6.1-terra available in Codex (Limitless still needs a runtime catalog entry for it).
  Matt is a TypeScript BEGINNER (fluent in many languages): good at logical errors, not TS semantic/syntax questions.
  => his role: approve rubric (language-agnostic policy), spot-check ~20 labels/batch at the LOGIC level — each label
  must carry a plain-language failure scenario + a reproduction (failing test/command output) or be marked unreproduced;
  arbitrate only policy disputes. TS-semantic disputes are settled by execution or a third model, never by Matt.
- 10-29 PHASE 0 STARTED (Matt: "Start Phase 0"). Work dir ~/limitless-orch/review-research/phase0, scripts/.
  claude CLI in my shell: OAuth expired -> Claude-family judge = sonnet SUBAGENTS on blind batches
  (phase0/val_claude_in_{0,1,2}.jsonl -> val_claude_out_*.jsonl); OpenAI judge = codex exec gpt-6.1-terra@medium
  (scripts/judge_codex.py, resumable cache phase0/val_terra.jsonl). Judge prompt scripts/judge_prompt.py (per trial:
  required gold G1.. vs all findings F1.., one-to-one SAME matching, blind to system). Validation set = dev evals
  E1 mv7ig, E3 mv8gn, D mvi7b (247 trials, 207 with findings) vs audit truth (grader_verdicts + credited_verdicts).
- 10-29 Phase0 0b: clean-case blocks in stored evals (since ~10-12): 66 blocking findings on 7 clean cases -> 17 clusters
  (phase0/clean_clusters.json). Dev 078/082 already audited 10-14 (LABELS.md). Adjudicating the 14 held-out clusters
  (068 x4, 092 x4, 108 x3, 114 x2, 133 x1) blind by Codex sol@high (scripts/adj_codex.sh -> phase0/adj_<case>.codex.out)
  and Opus subagents (-> adj_<case>.opus.json); checkouts phase0/wt/<case> (my clones phase0/repo, repo-sandbox).
  Policy question for Matt's rubric: review-082 claim 2 confirmed major but kept clean because AGENTS.md adopted it.
  Judge note: one-to-one rule leaves a finding covering two golds credited once (policy decision).
- 10-29 Phase0 0a validation (partial): Terra 97.2% agree w/ audit truth (n108), Claude 93.5% (n339), Terra vs Claude 100% (n100).
  Most Claude "judge+ / truth-" are AUDIT errors (audit judged only the grader's credited finding; another finding in the
  trial was the true catch: review-044, 052, 105); real judge errors at conf <0.7 (review-087 submodule vs post-check).
  Rule: caught iff both judges match, or one matches at conf>=0.7 & other unavailable (refine at final).
  Full rescoring: phase0/all_items.jsonl (772 trials, 14 completed M5.2-era evals); rest_items.jsonl 525 new (440 w/
  findings) -> Claude sonnet subagents rest_claude_in_{0..5} -> rest_claude_out_*; Terra to run after validation finishes.
- 10-29 Claude-judge rescoring COMPLETE (scripts/rescore.py; Terra still partial). Judged blocking recall (grader->claude):
  dev E1 sol@med 33.7->31.6, sol@high 42.9->42.9, adversarial 45.9->49.0, D 47.4->48.5, probe 21.4->22.4,
  std+setup 31.6->32.7, trace E 30.6->32.7, checklist F (48 defect-trials cohort) 27.1->39.6 (!), opus 14.3->11.2
  (any-sev 22.4), opus@high 16.8->14.7 (any 25.3). HELD-OUT: std 25.6->20.9, adversarial 32.6->29.1, D 42.0->37.5.
  => D vs std held-out +16.6 judged. F needs matched-cohort comparison.
- 10-29 Opus adjudication (108/114/133): 108 C6 REAL medium (gateTestCommand returns null for new parallel test command ->
  gate evidence can't satisfy sandbox-blocked criteria; repro'd); C13 LOW; C14 "REAL" = measurements missing from PR
  description (process ask -> NOT gold under LABELS rule). 114 C15/C16 NOT_REAL. 133 C17 LOW (Unicode case folding).
  Await Codex verdicts for agreement.
- 10-29 MATCHER VALIDATED: Terra vs audit 94.1% (n388), Claude 93.5% (n339), Terra vs Claude 97.4% (n342; 6 C-only+, 3 T-only+).
- 10-29 Codex sol@high clean adjudication: 068 C4/C7/C8/C10 REAL medium; 092 C5 PREEXISTING, C9 REAL, C11 REAL, C12 LOW;
  108 C6 REAL, C13 REAL (Opus: LOW), C14 UNCLEAR (process); 114 C15/C16 NOT_REAL (agrees Opus); 133 C17 REAL (Opus: LOW).
  => held-out "clean" 068/092/108 likely REAL (explains saturation: systems block them because they're defective).
- 10-29 CLEAN ADJUDICATION DONE -> phase0/clean_adjudication.md. 068/092/108 REAL (both vendors + repro); 114 true FB;
  133 disputed (C17 severity). D held-out FB on true clean: 4/20 vs prod 2/20 (+2, or 0) vs recall +16.6 judged.
  Disputed claims for tiebreak/orchestrator check: 068 C10, 092 C9, 108 C13, 133 C17.
- 10-29 0c replays (scripts/replays.py; consensus judge, Terra partial -> rerun when rest_terra done):
  * Two-tier "block only if both D samples agree": recall ~0-1% — the ±5-line merge's `agreement` field is almost
    never 2 (same as M4.5: merge never merges) -> agreement needs SEMANTIC dedupe before it can gate blocks.
  * E2 dev paired: Sol alone 30.6%, Sol∪Opus(blocking) 35.7%, Sol∪Opus(any severity) 39.8% (+9.2), clean 2/8 all.
    (writer's 50% used loose location matching; judged value is ~40%.) Opus alone 10.2% blocking / 20.4% any.
- 10-29 PHASE 0 DONE: phase0/RESULTS.md. Key: judged dev recall prod 29.6 / sol@high 42.9 / adversarial 45.9 / D 47.4 /
  F checklist cohort 39.6 vs prod 20.8; held-out prod 18.6 / adv 23.3 / D 30.7 (both-judge). E2's sol arm = cached E1
  (not A/A). Nearest A/A totals 29 vs 30, 15 discordant trials. 068/092/108 real -> D's clean FB 4/20 vs 2/20.
- 10-29 CONFIRMATION: review-068 C4 (skipped test disables gate substitution) was later FIXED by #647 (6b97d45f), whose
  issue says it caused ~20 of 49 needs_human runs since 10-14. Held-out "clean" 068 was defective; blocks were right.
- 10-29 advisor: before reporting reversals, code-reading tiebreak (55 items: 33 judge disagreements, 10 judges-yes/
  audit-DIFFERENT, 12 F-cohort flips) -> Opus subagents phase0/tiebreak_{a,b}_out.json (private map tiebreak_private.json).
  Then ONE set of numbers in PLAN.md, report note, RESULTS.md (name method). Don't claim F +18.8 / D "would pass" yet.
- 10-29 FINAL (code tiebreak 26 SAME/28 DIFF/1 UNCLEAR on 55 contested; both-judge rule right 45/55, Terra 40, Claude 35):
  dev prod 31.6, prod+setup 30.6, @high 41.8 (+10.2), adversarial 49.0 (+17.4), D 47.4 (+15.8), F cohort 19/48 vs prod 12/48
  (+14.6), trace 32.7, probe 22.4, opus 10.2, opus@high 14.7; held-out prod 18.6, adversarial 25.6 (+7.0), D 33.0 (+14.4).
- 10-30 PHASE 1 START (Matt "Start Phase 1"). Dir phase1/. DB snapshot phase1/limitless.db (journal_mode=delete for bun
  readonly), mirrored caches phase1/repos/*.git. Generator DRY RUN (no --write): 181 included rounds, 27 duplicate
  (head already a case), 37 excluded (33 missing delivered_sha, 3 fix touches no defect file, 1 no eligible defect).
  phase1/proposals.json = 545 findings (504 defect-class heuristic; orig sev 153 blocker/262 major/122 minor/8 nit).
  Pre-registered rule (LABELS.md 2026-10-23): split by PR parity (even escapes-dev, odd escapes-heldout); orchestrator
  confirms per finding key; only confirmed defect major/blocker written. claude CLI WORKS again (10-30).
- 10-30 RUBRIC draft phase1/RUBRIC.md (for Matt: 4 policy Qs: test-only, factory-fix bugs, requirement gaps, severity line).
  ADVISOR 10-30: per-case adjudication (1 call/vendor/round), hide original severity, Matt's fields in schema, keep
  pre-registered PARITY split (not era re-split; record era, report per era), pilot ~20 → Matt's first spot-check batch;
  review-133 = sb#14 already minor -> NOT a dispute (fixed RESULTS.md/clean_adjudication.md: D true clean 4/20 vs 2/20).
- 10-30 HARNESS: scripts/p1_prepare.py (items.json: 181 rounds, 448 findings; era opus<10-23: dev 50/39 sol, heldout 58/34 sol),
  p1_prompt.py (adj/<key>.prompt), p1_checkout.sh (wt/<key> + bun install), p1_adj.sh (codex sol@high workspace-write;
  opus = claude -p --model opus --effort high with allowedTools Read/Grep/Glob/git diff|show|log/bun test|-e — classifier
  BLOCKED bypassPermissions), p1_merge.py (merged.json statuses). PILOT 20 keys phase1/pilot_keys.json (5 per split×era).
  First 12 pilot cases: 30 findings: both REAL 27/30; Opus rates 20/30 MINOR (incl. secret not registered for redaction,
  wildcard confinement widening) vs Codex 25/30 major+. Reality agreement high; SEVERITY is the contested axis ->
  plan: severity set by rubric applied to the scenario by a blind third rater + my spot check, not either vendor.
- 10-30 068/092/108: re-ran gold repros myself (068 C4, C7; 092 C11; 108 C6 all reproduced); minors 068 C10, 092 C9/C12,
  108 C13 kept as optional. PR #1047 (branch claude/review-relabel-068-092-108, head 5d2251ae) — Auto-fix on; hand to
  orchestrator ("Limitless system build" session) when CI green. /code-review xhigh done (6 findings, 4 fixed).
- 10-30 ISSUE #1048 filed (priority:2): two-judge semantic matcher + eval judge command + cached judgments + report.
  Terra: no issue needed — `limitless catalog add` runtime entry when needed (operator action).
- 10-30 PILOT DONE (phase1/PILOT.md): 47 findings, 44 both REAL, 27 severity splits; labels 27 gold/20 not
  (pilot_labels.json); Matt sheet spotcheck_batch1.md. Raters v2 consensus 86% vs my rulings. Opus no-fix: unchanged.
  886-r2 F1 ruled minor (stale label only if hand-applied). New rubric Q5 (redaction gaps w/ unusual trigger -> major).
  Pool: 1,130 unmatched stored findings -> 352 claims (52 cases); adjudication running.

## (e6) Lab review prompts (2026-10-31)
Research notes: prompts/LAB_PROMPTS.md (Codex /review rubric verbatim, Anthropic plugins, Gemini, PR-Agent; bundled /code-review summarised).
Key gaps vs ours: no anti-early-stop rule; no out-of-diff procedure; Terra runs under the full `codex exec` agent system prompt, not Codex's review rubric; single-reviewer adversarial text falsely says "a separate step verifies each finding".
Proposed eval variants (dev + clean): V2 keep-going/floor (high false-block risk), V3 caller + deleted-invariant tracing, V1 native Codex rubric via `-c model_instructions_file`, then V4/V5. Not run yet; needs Matt's go-ahead.

## (e7) Terra batch + V2/V3 results 10-31 14:55 (escapes-dev 80 defects x k2 = 160; 16 dev clean x k2 = 32)
judged recall / clean FB: prod sol-std 16.9 / 2/32 (all review-082, from stored eval-mv7igcxy+mvie4edg);
Terra-adv single 28.7 / 6/32 (eval-mvwk3pn5 clean); V2 thorough 33.8 / 7/32; V3 callers 30.6 / 7/32 (eval-mvwniug6);
union2 36.9 / 8/32 ($0.06/trial, p50 77 s); specialist panel (Sol@medium verifier) 41.6 on 77/160 judged so far,
current-label 40.6 / 13/32 ($0.37/trial, p50 280 s) (eval-mvwnjdnp, judging started 14:49). D earlier 36.2.
review-082 blocked by every arm incl prod -> suspect label. Next: blind audit of clean-case blocks, then held-out.
(e8) CLEAN-BLOCK AUDIT 10-31 15:10 (scratchpad audit/: blocking.json 69 findings -> claims-map.json 22 claims; COUNTING-RULE.md
    pre-registered; Opus subagents + Sol@high codex exec, blind, per case snapshot). Both say 20/22 claims TRUE; Opus rates
    ALL minor, Sol rates 8 major (C01-04 smoke/eval exclusions, C08, C11, C12 unredacted CI excerpt, C20 poll=false).
    Pre-registered both-rule: 0 justified -> FB unchanged (prod 2, adv 6, thorough 7, callers 7, union2 8, panel 13 /32).
    C08 (review-082, every arm incl prod) = deliberate: AGENTS.md codified strict-UTF-8 rule same day (1bc16b38).
    Sol-major minus C08: adv 4, thorough 4, callers 3, union2 6, panel 8 /32; prod 2. Panel: 2 blocks minor-only (review-110).
    Diagnosis: Terra raises real-but-minor issues as major -> severity calibration is the lever, not detection.

(e9) 10-31 20:34 p4 CALIBRATION EVAL launched on daemon 299bf698 (has #1094): eval-mvx3koae1kebh1d07r3w9f,
    systems ~/limitless-orch/evals/p4-terra-calibrated-systems.json (terra-adversarial-calibrated, terra-thorough-calibrated,
    terra-calibrated-union2), 67 dev cases k=2. Supervisor ~/limitless-orch/evals/supervise-p4.sh (pid file, log supervise-p4.log;
    resumes up to 4x, then judges sonnet-5.5 + terra). Compare vs stored: prod 16.9%/2 clean FB, terra-adv 28.7%/6, thorough 33.8%/7,
    union2 36.9%/8. Watch under-rated count + security subset. Then pick 1-2 arms for held-out decision run.

(e10) 10-31 21:50 p4 CALIBRATION RESULT = NULL (eval-mvx3koae1kebh1d07r3w9f, settled 21:4x, judged, $0).
    judged recall / clean FB(32) / clean FB excl review-082 (30):
      prod 16.9% / 2 / 0;  terra-adv 28.7% / 6 / 4 -> calibrated 30.0% / 6 / 4
      thorough 33.8% / 7 / 5 -> calibrated 26.3% / 8 / 6;  union2 36.9% / 8 / 6 -> calibrated 38.8% / 9 / 7
      panel ~41.6% / 13 / 11. under-rated stays 0-2/160 (calibration didn't demote true defects either).
    Paragraph reached the model: it changed WHICH clean cases block. review-125 went 0 -> 5/6 calibrated trials, all
    "out-of-scope change" findings: model applied the "explicit requirement -> at least major" exception to the issue's
    Out-of-scope list (exception meant for undelivered requirements). 111 (TMPPREFIX) gained; 116/128 dropped. 078 (exclude_origins=["US"],
    contrived config) and 082 still major in every arm. Conclusion: finder-prompt wording can't calibrate Terra's severity
    (5 variants all 6-9/32). Rubric not yet tried in the panel VERIFIER's severity scale (prompts.ts ~726, own crit/high/med/low).
    Unchecked: calibration text vs generic "Severity:" line order (prompts.ts:658; calibration says "below").
    Decision to Matt: accept trade (+13..22 pts recall for 4-7/30 clean FB) -> held-out, OR try rubric verifier via --replay-finders, OR stop.
    Keep Terra catalog row until held-out decision settles.

## (e11) p5 rubric verifier replay launched 2026-11-01
- #1108 landed (e4f30c24), deployed in b547ae75.
- Eval eval-mvxy49qr0ui70et1b5qa1l: replays terra-specialist-panel finders from eval-mvwnjdnp0uvkd6x11wmbgr through a Sol 6.1@medium verifier with severityRubric; 67 dev cases, k=2, 134 trials.
- Terra-verifier arm dropped: the daemon refuses a verifier that is also one of the finders (by design). Both-arm file kept as p5-rubric-verifier-systems.both.json.
- Supervisor: ~/limitless-orch/evals/supervise-p5.sh (log supervise-p5.log; resumes, judges sonnet-5.5 + terra-6.1@medium).
- Compare against: production 16.9%/2, panel 41.9%/13, free gate regrades 24.4%/4 and 28.1%/4 (security kept), Terra adversarial 28.7%/6, union2 36.9%/8 (clean false blocks /32).
- RESULT (settled 10:38): judged recall 39.4% (63/160; sonnet 45.0%, terra 39.4%, agreement 93.8%), clean false blocks 9/32 (7/30 excl. review-082), under-rated 5 (panel: 1). $32.81 API-equiv, p50 verifier 107 s.
  - Clean blocks: 078 x2, 082 x2, 111 x2, 115 x2, 097 x1 (security finding, high). 7 of 9 = three cases blocking in BOTH trials on findings the rubric verifier rated high (078 exclusion reasons missing from logs; 111 TMPPREFIX unset for preview; 115 "relaxes the admin safety check").
  - vs panel 41.9%/13 (11): -2.5 pts recall, -4 false blocks. vs free regrade 28.1%/4: rubric keeps recall but promotes clean findings to high too. vs production 16.9%/2 (0): +22.5 pts, +7 false blocks.
  - Next: audit 078/111/115 blocking findings (real defect vs label) before the held-out decision.

## (e12) Clean-block audit + rubric mini-eval (p6) 2026-11-01
- Audit (3 independent agents, read-only, rubric + later history): review-078, 111, 115 CLEAN labels all hold. Shared failure: the verifier read request WORDING as an "explicit requirement not delivered" (rubric override: at least high whatever the trigger) — log/message text (078), "wherever" + an assumed confinement that preview lacked at head (111), "don't relax the check" when no safety assertion was weakened (115).
- Ceiling: both judges match only 69/160 required defects to ANY finding in p5, so verifier-only changes cap at 43.1% recall; they can only cut false blocks. Floors: 082 (justified) x2 and 097 (security, blocks unless refuted) x1 → movable clean blocks = 078/111/115 = 6.
- Mechanism: PR claude/rubric-text-option — eval-only severityRubric may be the severity section's TEXT, so variants run from a systems file without a release.
- p6 mini-eval: 38 cases (29 positives where both judges matched a defect to a finding + 9 clean cases with findings), k=2, replay of terra-specialist-panel finders, Sol 6.1@medium verifier. Files: p6-rubric-variants-systems.json, p6-mini-cases.txt.
  - control terra-panel-rubric-sol (built-in rubric, should hit p5's cache)
  - A rubric-a-no-override: drops the undelivered-requirement override; requirement = behaviour it protects; diagnostics/log text explicitly medium
  - B rubric-b-path: A + high/critical needs the reach path at head quoted in evidence, else medium
  - C rubric-c-steps: B's content as a 4-step procedure (path, trigger, harm, severity last) — tests presentation
- DECISION RULE (pre-stated): among variants with >= 60 of the 63 control-blocked defects still blocked (judged, both judges), pick the fewest clean false-block trials on the 9 clean cases; tie → more defects blocked. At most 2 winners go to a full-dev replay (67 cases), then held-out before any adoption claim. Dev-designed variants: mini results are a screen, not evidence of adoption.
- 2026-11-01 Matt: the PR→land→deploy loop is far too slow for iteration; wants lightweight data in minutes.
  → Built ~/limitless-orch/lab (README there): in-process eval runner on a lab copy of the DB, code from the current checkout. Smoke: 2 cases end to end in ~2 min. p6 now runs in the lab (clean stage first, then positives), not via the daemon.
- p6 clean stage (lab eval-mvy4wjxc1nkif261qlj78v, 9 clean cases x2, 8.6 min): clean false-block trials — control 9/18; A 1/18; B 1/18; C 2/18 (the 1 = 097 security floor in every arm; C adds one 128 trial). NOTE all variants also drop 082 (previously judged justified) → watch recall closely in the positive stage.
- p6 positive stage launched: lab eval-mvy57zyu1w8x60202b6l53 (29 cases x2, judged).

(e13) 2026-11-01 p6 defect stage (lab eval-mvy57zyu1w8x60202b6l53, 29 positive cases, k=2, 106 required defect-trials, 72 min + judging):
  judged blocked: control 63, A 57, B 47, C 51 (under-rated 5/11/19/17). Clean (p6 clean stage): control 9/18, A 1, B 1, C 2.
  Decision rule (>=60 blocked): NO variant qualifies. A closest.
  A vs control diff: A lost 7, gained 1 (166). Lost = 200, 218, 237x2, 241x2 (failure-path races the REQUEST asked to handle: read error during reconcile, lost POST response, ref change between reads, same-second timestamps) rated medium "contrived"; 173 (digest omits unowned blocked lands) rated medium, likely via A's "diagnostics" line.
  The control's requirement override was carrying these. Per-defect matrix script: scratchpad mini/perdefect.ts (usage: bun perdefect.ts <evalId> out.json from a checkout).
  p7 screen (running): D = A + "failure paths are realistic; request-named failure path realistic however rare; digest omission = wrong result"; E = A with a NARROW override (explicit requirement whose behaviour is missing at head >= high). Cases: 9 clean + 6 diff positives (p7-screen-cases.txt). Overfit risk acknowledged: winners still go to full 67 dev, then held-out.
  p7 screen result (lab eval-mvy7vnxd0jn329e1fq11n8, 15 min): on the 6 diff cases (18 defect-trials) control 10, A 4, B 2, C 3, D 12, E 9. Clean (18 trials): D 3 (078 x2 via "catalog edited mid-run" concurrency + 097 floor), E 5 (082 x2, 078, 115, 097).
  KEY FACT: for verifier-only changes the 38 mini cases == full 67 dev (other cases have no finding that can block or be matched). So "full dev" for a variant = these 38.
  p8 (running): D and D2 (D minus the generic concurrency clause; concurrency realistic only when another process/loop writes that state; operator config/catalog edits mid-run are not) on all 38. D reuses its 15-case trials from cache.
  p8 RESULT (lab eval-mvy8fxpu1pbcjbd1o86dfl, 38 cases == full dev for verifier-only): judged blocked of 106 / clean FB of 18:
    control 63 / 9; A 57 / 1; D 65 / 3 (078x2 + 097 floor); D2 64 / 2 (078x1, 097x1). Under-rated 2 each.
    Full-dev equivalents (160 defect-trials, 32 clean trials): control 39.4% / 9; D 40.6% / 3; D2 40.0% / 2. Prod sol-std 16.9% / 2 (both 082).
    Decision rule: D2 wins (fewest clean FB); D second. Both are dev-designed -> held-out required.
  p9 HELD-OUT (running): full D2 panel (Terra specialist finders + Sol D2 verifier, no replay) on the 33 heldout cases (23 real + 10 clean), k=2.
    Comparators (stored, not yet judged in-daemon): eval-mv92iu6p0y8ns1b0ifjg8t (prod sol-std + adversarial, 22 real), eval-mvif9n84010bmzy1tk9std (D union2, 33).
    phase0 final judged held-out: prod 18.6 (16/86), adv 25.6, D 33.0; script judges + Opus tiebreak, so re-judge stored ones with lab/judge.ts for like-for-like.
    Then replay p9 finders with D verifier (cheap) as second winner.
  p9 HELD-OUT RESULT (lab eval-mvy9zity0cdbiz3049vths, 48 min + judging, $21.88 API-equiv, p50 205 s): D2 panel judged recall 34.4% (33/96), clean FB 8/20, under-rated 5.
    Clean blocks per case (trials): prod sol-std (eval-mvih4jfr07m09eu0wfoy22) 114x2 only = 2/20; D-union2 (mvif) 114x2 + 133x2 = 4/20; D2 114, 124, 130, 133 x2 each = 8/20.
    review-114 = HARNESS ARTIFACT: change edits evals/review/cases.json which the snapshot strips, so every system blocks "dataset missing". Exclude: prod 0/18, D-union 2/18, D2 6/18.
    D2's 130 blocks = failure-path findings (PR becomes draft mid-round, comment fails after push) -> the D2 failure-path paragraph over-generalises on held-out. 133 trailing-newline (D-union also blocks). 124 race/legacy recovery.
    Audit of 124/130/133 blocks launched (agent, read-only, writes scratchpad/audit/heldout-audit.md). Baseline re-judging (mv92 prod+adv, mvif D-union) running via lab/judge.ts.
  HELD-OUT LIKE-FOR-LIKE (lab/judge.ts, sonnet-5.5 + terra@medium, in-daemon judge): prod sol-std 23.4% (22/94, 22 cases); sol adversarial 30.9% (29/94);
    D union2 36.5% (35/96), clean FB 4/20 (114x2, 133x2) -> 2/18 excl 114; D2 panel 34.4% (33/96), 6/18 excl 114.
    => D2 rubric panel does NOT beat D union2 on held-out (recall -2.1, clean FB +4). Dev win didn't transfer; the failure-path paragraph over-generalises (130).
    D-verifier replay on held-out skipped: D has the broader concurrency clause, so it can only add clean blocks; recall headroom ~1-2 defects.
    Best held-out candidate remains D union2: +13.1 over prod, clean FB +2 (133, audit pending).
  HELD-OUT CLEAN AUDIT (agent, read-only, scratchpad/audit/heldout-audit.md): 124, 130, 133 CLEAN labels ALL HOLD (0 real-major; minors + 1 not-real).
    Verifier over-rates (a) patterns that predate the change (124-A, 130-E/F/H) and (b) triggers needing an operator action mid-run (124-B, 130-F/G). 133 trailing newline = documented, tested behaviour.
    FINAL held-out (like-for-like, excl harness-artifact 114): prod 23.4% / 0 of 18 clean FB; D union2 36.5% / 2 (133, false) -> +13.1 pts for +2/18 FB on one case; D2 panel 34.4% / 6.
    Cost/latency: union2 ~$0.06/trial p50 77 s; D2 panel $0.33/trial p50 205 s.
    Recommendation to Matt (policy call): adopt D union2 in production. Rubric-verifier line: shelved; possible later lab variant adds "pre-existing pattern" + "operator action mid-run = contrived", but held-out is now looked at, so it would need a fresh held-out set.
  PAIRED held-out (22 shared real cases, 94 defect-trials, same judges): prod 22, D union2 33 (+11.7, one-sided 95% lower +5.3, case bootstrap), D2 31 (+9.6, lower +2.1).
  HISTORY: D union2 was NOT adopted 10-21 (#551) under the old rule "clean FB rise <= 1": +17 recall but clean FB 10/26 vs 7/26. Since then: 068 was found really defective (its blocks were right), 114 is a harness artifact, 133 audited false-minor; Matt's 10-29 goal allows a >50% FB rise for considerable gain. So this is a RE-OPEN under the new rule -> Matt's call.
  Production refuses `samples` ("eval-only until adopted", review-system.ts:138) -> adoption needs a code change. Sol D dev clean: only 8 stored dev-clean trials (2/8, same as prod). Cost ~2x production single review.

## 2026-11-01 DECISION (Matt): adopt D union2 in production ("happy with union of two for now")
- Branch claude/review-union-samples: productionReviewSystem = single, adversarial finder, samples 2 (routed; prod review is
  codex/sol-6.1@medium 260/260 last 7 days, same as the eval pin). reviewRequest applies a lone single finder's prompt (was
  only in evals/runner.ts:840, so the engine would have run standard x2). runUnion rethrows invocation errors when no
  onSample (production), so cancellation/no-capacity keep their type.
- Follow-ups to note: evals/policy.ts:62/140 treat "standard, no samples" as production-shaped (now stale); later-round
  adversarial prompt drops the "new majors become follow-ups" sentence (prompts.ts:626, untested in eval); lastReview/artifact
  model comes from the first sample.

## 2026-11-06: backlog screens (A7, A9, T2)

## (e14) Trust-boundary pass PRE-REGISTRATION 2026-11-06 (Matt: pick a backlog item from accelerate-docs, test locally)
Item: BACKLOG A9 (+A10). Impact pack A7 rejected on stored data BEFORE building: of 45 escapes-dev defects union D never caught, 3 are in files outside the diff, 36 within 3 lines of changed lines, and only 5 fix commits edited a source file outside the diff (the ~13/30 of research/14 doesn't hold on this corpus). Matched~caught (D matched 60, caught 58 of 160), so severity isn't the loss: detection is. Security pool: 16 of 45 misses; 17/52 trials caught.
Arm: sol-adversarial-boundary (eval-only `adversarial-boundary`, Sol 6.1@medium, one sample), lab, 51 escapes-dev + 16 dev clean, k=2. CAVEAT: the prompt was written AFTER printing the 45 missed defect summaries, and its attack list (split across lines, path aliases, truncate-before-check) overlaps them and AGENTS.md's rules, so the dev number is dev-influenced; only escapes-heldout can confirm it.
Scoring: per defect-trial OR with stored D (eval-mvw0y6v31sec2vc1agx2t1, same trial index, same judges sonnet-5.5 + terra-6.1@medium). No union control re-run (Matt: no paid baseline refresh); OR is additive so D's stored trials are the floor. Cost-neutral variant: stored E3 (one adversarial sample) OR boundary, vs D.
Advance to escapes-heldout only if: D OR boundary >= +5 pts (>= +8 of 160), paired case-bootstrap 95% lower bound > 0, and boundary-alone clean blocks <= 3 of 32 trials outside review-082. Otherwise stop and record rejected. +5 is a screen bar, not the adoption bar.
  p10 RESULT 2026-11-06 (lab eval-mw51lukc1ww18f40ywsfyp, 36 min, $19.81 API-equiv, p50 68 s; files in p10/): FAILED the pre-registered screen, not advanced; escapes-heldout untouched.
  Judged recall of 160: D 58 (36.2%), boundary alone 22 (13.8%), D OR boundary 62 (38.8%) = +2.5 pts (bar +5), one-sided lower +0.6. Cost-neutral E3 OR boundary 53 (33.1%) = -3.1 vs D.
  Security 52: D 17, boundary alone 16, OR 21 (+7.7 within security). Non-security 108: D 41, OR 41. Gained: 145 G1, 179 G2, 181 G1, 214 G2. Clean 0/32 for boundary alone. 1 trial errored (2 defect-trials count as not caught; can't change the verdict).
  Reading: focus reaches nearly D's security count alone with no clean blocks, but it overlaps D, so it finds the same defects. Status for BACKLOG A9: rejected as a third additive sample at this bar; kept as a screen-grade fact. Not committed or landed; prompt patch in p10/.

(e15) 11-06 p11 T2 COVERAGE PROMPT ON SOL, PRE-REGISTERED before launch.
Arm: sol-6.1-medium-thorough = stored E3 system verbatim with prompt adversarial-thorough (Sol 6.1@medium, one sample), lab, 51 escapes-dev + 16 dev clean, k=2. No ledger: this tests the existing prompt only.
Question: does the prompt widen each sample, so that replacing `adversarial` with it in production's union of two helps at the same sample count?
Estimators: per (case, gold, trial) judged caught, on keys present in both arms. Union of two = OR over the two trials, compared with OR over E3's two stored trials (37.5% of 80; control: real union D per-trial 36.2%).
Primary A (per sample): thorough minus E3 per-trial, stored E3 28.5%.
Primary B (union of two, the decision): OR(thorough) >= OR(E3) + 5 pts (>= +4 of 80), paired case-bootstrap one-sided 95% lower bound > 0.
Clean bar: excluding review-082 (deliberate-rule case), a pair (two trials of one case) blocks on <= 3 of 15 cases. No full stored Sol clean baseline exists and none will be bought; context is Terra adv 6/32, thorough 7/32, D held-out 2/18.
Secondary, reported, not a pass condition: D OR thorough (additive), category split, per-trial p50/p90 latency and cost vs E3, findings per trial.
Advance to escapes-heldout only if B and clean both pass, and then only after asking Matt. A pass here is a screen, not adoption.
CAVEAT: thorough was picked because it beat adversarial on this same escapes-dev set on Terra, so a Sol dev win is selection-influenced. Terra's calibrated variant was null (e10), so it is not run. Stored E3 has 158 of 160 rows.
Archive: ~/limitless-orch/review-research/p11/.
  p11 RESULT 11-06 (lab eval-mw5719bw1y4wluw1wpuwk9, 67 min, $25.15 API-equiv, 134/134 ok, score.py in p11/): FAILED Primary B. Union of two OR(thorough) 33/80 (41.2%) vs OR(E3) 30/80 (37.5%), +3.8 pts vs bar +5, one-sided lower -2.8. Primary A per sample 32.3% vs 28.5% of 158, +3.8, lower -0.7. Clean PASSED: 0 of 15 excl review-082 (only 082 blocked, both trials). Non-registered: mixed pair 31/80. Not advanced; held-out unspent.
  p11 post-hoc controls (not pre-registered): review-161's two defects lack a second E3 trial; on the 78 complete defects B is still +3.8 (31 vs 28). Third-sample comparison on 158 keys: D 56, D+thorough 65, D+E3 64, so thorough beats a plain third adversarial sample by +0.6 (lower -3.2); D+E3 - D is +5.1 (lower +1.9). The additive gain comes from sample count, not the prompt. Latency p50 122 s vs E3 99 s (not same load), cost equal, findings per trial 1.47 vs 1.63: the prompt did not raise finding count. Lead for Matt: a union of three adversarial samples, dev post-hoc, +50% cost, not run live.
