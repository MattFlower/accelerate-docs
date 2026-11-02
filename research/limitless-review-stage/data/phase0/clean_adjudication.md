# Held-out clean-case blocks: blind two-vendor adjudication (2026-10-29)
Adjudicators: codex gpt-6.1-sol@high (adj_<case>.codex.out) and claude opus subagents (adj_<case>.opus.json), same prompt
(LABELS.md rule: medium+, at head, introduced/newly exposed, evidence = repro or quoted code head vs base). Not yet
re-run by the orchestrator (provisional until labels are written to cases.json in Phase 1).

| Case | Claim | Codex | Opus | Outcome |
|---|---|---|---|---|
| review-068 | C4/C8 unrelated skipped test disables gate-evidence substitution (the issue's own scenario) | REAL med | REAL med (repro) | REAL |
| review-068 | C7 test output can forge coverage for a nonexistent file -> criterion "met" | REAL med | REAL med (repro) | REAL (security/trust) |
| review-068 | C10 crash between checkpoint and finishStage rejects cached gates | REAL med | LOW | disputed |
| review-092 | C5 pending identical calls + unrelated call stops agent | PREEXISTING | LOW | not gold |
| review-092 | C9 eviction forgets previous identical result (off by one) | REAL med | LOW | disputed |
| review-092 | C11 changed result doesn't drop earlier occurrences -> misses repeated-failure loop | REAL med | REAL med (repro) | REAL |
| review-092 | C12 never-returning poll defers stop | LOW | LOW | not gold |
| review-108 | C6 gateTestCommand null for new parallel test command -> gate evidence lost | REAL med | REAL med (repro) | REAL |
| review-108 | C13 worker override not in baseline cache identity | REAL med | LOW | disputed |
| review-108 | C14 measurements missing from PR description | UNCLEAR | REAL (process) | not gold (process ask) |
| review-114 | C15/C16 sanitized data missing | NOT_REAL | NOT_REAL | true false block |
| review-133 | C17 --ignore-case misses Unicode case folding (final sigma, ß) | REAL med | LOW | disputed (severity policy) |

=> All three M5.2 held-out clean cases (068, 092, 108) contain real medium defects (both vendors, reproduced) -> relabel real.
=> Held-out true clean = #542's 10 cases. Blocks there: D 4/20 (114 x2 true FB; 133 x2 disputed), production standard
   2/20 (114 x2). D's "+3 clean false blocks" that rejected it (#551) shrink to +2 (or 0 if 133 C17 is real).
   Final judged held-out recall D 33.0% vs production 18.6% (+14.4); D's true clean-block rate is double production's
   (4/20 vs 2/20, see correction below). Retrospective only: re-measure in the tournament.

Later-fix check: review-068 C4/C8 was fixed on main by #647 ("Gate substitution accepts skipped tests inherited from the
base commit"), whose issue reports it caused about 20 of 49 needs_human runs after 2026-10-14. Independent confirmation.


## Correction 2026-10-30
review-133 = sandbox PR #14; LABELS.md (#542 section) already confirmed its Unicode case-folding claim minor. It stays clean; not a dispute. D true clean blocks 4/20 vs production 2/20 (no '2/20 if medium' alternative). Open disputes: 068 C10, 092 C9, 108 C13.

## Orchestrator re-run and rulings, 2026-10-30 (draft rubric severity line, phase1/RUBRIC.md)
Re-ran in phase0/wt/<case> (head checkouts, deps installed):
- review-068 C4/C8 REPRODUCED: applyGateEvidence with a passing target + unrelated skipped file -> "blocked ... skipped tests"; without the skip -> "met". GOLD major (src/pipeline/gate-evidence.ts ~74/104). Later fixed by #647.
- review-068 C7 REPRODUCED: real `bun test` (bun 1.4.3) of a test printing "test/missing.test.ts:" / "(pass) fabricated" -> BunTestCoverage passedFiles ["test/missing.test.ts"]. Untrusted test output becomes factory evidence -> GOLD blocker (trust boundary) (src/gates/test-coverage.ts ~37).
- review-068 C10 -> MINOR (needs a hard crash in a microsecond window between two synchronous writes; consequence = pre-change needs_human). Not gold.
- review-092 C11 REPRODUCED: [poll a changing, poll b changing, failing cmd identical] x12 -> no stop after 12 identical failing calls (36 calls), finish() null. Request explicitly requires dropping earlier same-key entries. GOLD major (requirement_gap) (src/harness/types.ts reconcile ~203-220).
- review-092 C9 -> MINOR (stops a genuine repeat loop at most one call early). Not gold. C5 preexisting, C12 low: not gold.
- review-108 C6 REPRODUCED: gateTestCommand("bun test --parallel=$(bun scripts/test-workers.ts)") -> null (base "bun test" -> "bun test"); head .limitless.toml uses that gate. Gate substitution silently disabled on this repo. GOLD major (newly_exposed) (.limitless.toml:10 / src/pipeline/gate-evidence.ts:13-16).
- review-108 C13 -> MINOR (worker count not in baseline cache key; cost = load-sensitive flake classification only). C14 process ask. Not gold.
=> Relabel review-068, 092, 108 clean -> real with these gold defects (068: C4 major, C7 blocker; 092: C11 major; 108: C6 major).
