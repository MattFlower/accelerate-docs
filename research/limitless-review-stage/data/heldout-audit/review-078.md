# review-078

{
 "id": "review-078",
 "kind": "clean",
 "repo": "MattFlower/limitless",
 "base": "7cc4e1864e395db91a57cd88c0bfc77c9cd6c067",
 "head": "a7ab09af8e527cff269224c2e2400566e69670b5",
 "snapshot": true,
 "source": "pr #396 review rev396c @ a7ab09a",
 "split": "dev",
 "input": {
  "prompt": "Closes #36. Enforce model-origin exclusions in the router, not only in eval policy.\n\n## Why\n`[routing] exclude_origins` in config.toml is parsed today only by `src/evals/settings.ts` and honoured only by `src/evals/policy.ts` (a model is excluded when its `origin` or `baseOrigin` is listed, or when its `baseOrigin` is \"unknown\" while a list is configured). The runtime `Router` (src/router/router.ts) ignores it, so when subscription quotas ran out, review and verify calls fell back to a CN-origin model even though the policy work assumed such models were excluded. At work, CN-origin models must never be called.\n\n## What\n1. One shared parser for `[routing] exclude_origins` (reuse it in `evalSettings`; the semantics above stay identical, including \"unknown baseOrigin is excluded when a list is configured\"). No exclusion when the key is absent (today's behaviour at home stays unchanged).\n2. The Router treats an excluded model as ineligible on every route: policy cells, out-of-cell fallbacks, the free-first and vendor-avoidance fallbacks, escalation, panel and verifier selection, and models added at runtime (`catalog add`, discovery). The skip reason in the run log and in `routing preview` reads `origin excluded (<origin>; baseOrigin=<baseOrigin>)`. There is NO fallback to an excluded model: when exclusions leave no candidate, the invocation fails with that reason.\n3. Explicit choices are refused up front, never silently skipped: `run --model role=…` and `retry --model`, `routing set`, the Setup tab's routing and fallback saves (HTTP 400 with the reason), `catalog add` of an excluded origin (allowed to add, but `catalog list` marks it excluded and routing never picks it), and `eval run --models` (refuses excluded models with the reason before any trial starts).\n4. Visibility: `routing show`, `catalog list` and the Setup tab show the configured exclusions (read-only; changing them stays a config.toml edit plus restart, on purpose: it is a safety constraint).\n5. Docs: document the key and its semantics where routing config is documented.\n\n## Tests (fake harness only; read test/AGENTS.md)\n- A fallback that would reach an excluded model when every allowed provider is exhausted fails with the reason instead (this is the regression).\n- Each refusal path above (run pin, retry pin, routing set, HTTP setup save, eval run) rejects an excluded model; a model whose baseOrigin is \"unknown\" is excluded only when a list is configured.\n- With no `exclude_origins`, routing is byte-for-byte unchanged (existing routing tests keep passing).\n\nBudget: about 200 changed source lines plus tests. Out of scope: per-repo or per-role exclusion lists, live editing of the list.",
  "spec": null,
  "implementerReport": "",
  "gates": []
 },
 "defects": []
}

# Blocking findings (verifier high/critical), both trials

## trial 0: Verifier failure can omit the exclusion that exhausted the choices
{
 "severity": "minor",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 1347,
 "title": "Verifier failure can omit the exclusion that exhausted the choices",
 "detail": "The exclusion reason is propagated only when every listed verifier is excluded. If an allowed verifier remains but is ineligible because it raised the candidate, `pickVerifier` throws a different error that omits the excluded alternative. The invocation therefore fails without the required origin exclusion reason.",
 "suggestion": "Include collected exclusion reasons when verifier selection fails after filtering, and log excluded verifier choices.",
 "failure_scenario": "A verifier list contains an allowed model that raised the candidate and a CN model excluded by configuration. No verifier can be selected, but the error reports only that the allowed model raised the candidate.",
 "category": "correctness",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1347 only reports exclusions when `!listed.length && exclusions.length`; line 1349 otherwise calls `pickVerifier(listed, avoidVendors, avoidModels, identity)`. src/pipeline/review.ts:325–327 throws `NoCapacityError(`verifier ${targets.map((t) => t.modelId).join(\", \")} raised a candidate it would check`)` when no independent model remains, without the collected exclusions.",
  "trigger": "With CN excluded, configure verifier targets containing one CN model and one allowed model that raised the candidate. The allowed model keeps `listed` nonempty, but independence selection fails; the error omits the origin exclusion reason explicitly required for exhaustion.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 0: Verifier exclusions are omitted from the run log
{
 "severity": "minor",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 1341,
 "title": "Verifier exclusions are omitted from the run log",
 "detail": "The request says the skip reason in the run log reads `origin excluded (<origin>; baseOrigin=<baseOrigin>)`. This verifier-selection path removes excluded alternatives before calling the router, but logs their reasons only when every listed target is excluded. When an allowed verifier remains, the exclusion is invisible in the run log.",
 "suggestion": "Record the excluded verifier alternatives and their reasons when filtering them, including when another verifier is selected.",
 "failure_scenario": "A review system lists one CN verifier and one US verifier with CN excluded; the US verifier runs, but the run log does not explain that the CN verifier was skipped.",
 "category": "correctness",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1341–1343 handles an excluded verifier with `exclusions.push(`${targetId}: ${reason}`); return [];` without logging it. Lines 1349–1350 pass only the selected allowed target through `call(request, { ...constraints, only }, undefined)`. src/router/router.ts:386–388 processes only `c.only` and returns; src/pipeline/context.ts:659–661 logs `skipped: decision.skipped`, which therefore contains no record of the filtered CN verifier.",
  "trigger": "Configure an excluded CN verifier followed by an eligible US verifier. The US verifier runs, but the CN verifier was removed before routing and its exclusion never reaches the run log, contrary to the explicit logging requirement.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 0: Verifier exhaustion can hide the origin exclusion reason
{
 "severity": "minor",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 1347,
 "title": "Verifier exhaustion can hide the origin exclusion reason",
 "detail": "The request says that when exclusions leave no candidate, the invocation fails with the origin exclusion reason. This check reports exclusions only if the filtered list is empty. If the remaining allowed targets are ineligible because they raised the finding, `pickVerifier` throws a different error that omits the excluded alternatives and their reasons.",
 "suggestion": "Include the collected exclusion reasons when verifier selection fails after applying the independence constraints.",
 "failure_scenario": "A verifier list contains an excluded CN model and an allowed US model, and the US model raised the candidate being verified. Selection fails with only the raised-candidate message, despite the CN exclusion preventing the other choice.",
 "category": "correctness",
 "confidence": 0.96,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1342 collects exclusion reasons, but line 1347 throws them only if `!listed.length`. Line 1349 calls `pickVerifier` with the remaining allowed models. src/pipeline/review.ts:321–327 rejects models in `avoidModels` and throws only `verifier ${targets.map((t) => t.modelId).join(\", \")} raised a candidate it would check`.",
  "trigger": "An excluded CN verifier and an allowed US verifier are listed, and the US verifier raised the candidate. Selection fails with the raised-candidate error while dropping the CN exclusion reason. This duplicates C2.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: Skip native smoke checks when all of a provider’s models are excluded
{
 "severity": "major",
 "security": false,
 "file": "scripts/smoke.ts",
 "line": 1019,
 "title": "Skip native smoke checks when all of a provider’s models are excluded",
 "detail": "Native checks still run when a configured exclusion removes every model for Claude or Codex. `cheapestModel` throws the exclusion reason, which `runChecks` records as a failure; `reportChecks` then returns a nonzero exit code. This makes `limitless deploy --smoke` fail for an intentional configuration even if other eligible providers work. Backend checks already treat an entirely excluded provider as skipped.",
 "suggestion": "Apply the same excluded-provider skip handling to native checks before selecting a model.",
 "failure_scenario": "Configure an origin exclusion that excludes every Claude model while leaving another provider eligible, then run the deployment smoke check. Every Claude check fails instead of being skipped, so deployment fails.",
 "category": "correctness",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "scripts/smoke.ts:1019–1020 selects `cheapestModel(id, catalog.models, excludeOrigins)` for native checks without an exclusion skip guard. scripts/smoke.ts:353–354 throws when `models.length && !eligible.length`. scripts/smoke.ts:157–159 converts that exception to `fail(String(error), ...)`, and scripts/smoke.ts:341 returns exit code 1 whenever `rows.some((row) => row.status === \"fail\")`.",
  "trigger": "Keep Claude enabled and configure exclusions covering every Claude model, while another provider remains eligible. All seven Claude smoke checks fail with the exclusion reason instead of skipping, causing deployment with smoke checks to fail.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: Log excluded verifier candidates when another verifier remains
{
 "severity": "minor",
 "security": false,
 "file": "src/pipeline/engine.ts",
 "line": 1341,
 "title": "Log excluded verifier candidates when another verifier remains",
 "detail": "The panel verifier path removes excluded targets before invoking the router. When at least one verifier remains, the collected exclusion reasons are discarded, so the run log does not show the required skip reason for those candidates.",
 "suggestion": "Record the excluded verifier targets and their reasons in the run log before selecting among the remaining targets.",
 "failure_scenario": "A panel verifier list contains one excluded model and one eligible model. Verification uses the eligible model, but the run log never reports `origin excluded (...)` for the excluded candidate.",
 "category": "correctness",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/engine.ts:1341–1347: `if (reason) { exclusions.push(`${targetId}: ${reason}`); return []; }` followed by `if (!listed.length && exclusions.length) throw new NoCapacityError(exclusions.join(\"; \"));`. When an eligible verifier remains, exclusions are discarded without logging. Lines 1349–1350 pass only the selected target: `return call(request, { ...constraints, only }, undefined).catch(skip);`. src/router/router.ts:386–388 considers only that target, so the excluded candidates cannot reach the invocation log's `skipped: decision.skipped` (src/pipeline/context.ts:659–661).",
  "trigger": "Configure origin exclusions and a panel verifier roster containing an excluded model and an eligible model. Verification uses the eligible model, but the excluded candidate's `origin excluded (...)` reason never appears in the run log.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: A declined answer hides the exclusion that exhausted routing
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/context.ts",
 "line": 511,
 "title": "A declined answer hides the exclusion that exhausted routing",
 "detail": "The last-resort return runs before the new exclusion handling. If an allowed model returns an unsure decline and all remaining candidates are excluded, the invocation succeeds with that declined answer without reporting the exclusion. The request requires the invocation to fail with the exclusion reason when exclusions leave no candidate.",
 "suggestion": "Check and report origin exclusions before accepting the declined-answer fallback when they are what prevents further routing.",
 "failure_scenario": "An allowed review model returns a last-resort decline, and the only remaining model has an excluded origin. Routing returns the declined answer instead of failing with `origin excluded (...)`.",
 "category": "correctness",
 "confidence": 0.88,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/context.ts:874 saves the declined result: `if (result.decline?.lastResort) lastResort = { result, target, invocation: updated };`. At src/pipeline/context.ts:511–512, `if (!target && lastResort && !chain) return useLastResort(lastResort, ...)` executes before exclusion reporting and NoCapacityError at lines 513–526.",
  "trigger": "An unpinned invocation receives an allowed model's last-resort decline; all remaining models are excluded or unavailable. The invocation returns the decline without failing with the origin-exclusion reason required by the request.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
