# review-115

{
 "id": "review-115",
 "kind": "clean",
 "repo": "MattFlower/limitless",
 "base": "a9c39600d8e9f7fe2f615d8bab4358b8e19316c2",
 "head": "1a9996d371b1e40ce62ce70ee5a5b7cf4f7dfc40",
 "snapshot": true,
 "source": "pr #439 fresh clean set 2026-10-16 @ 1a9996d",
 "split": "dev",
 "input": {
  "prompt": "## Problem\n\"environment verification retry: passes\" (test/failure-injection.test.ts) failed once in the deploy gate on 2026-10-08, with the suite running under `--parallel=4` (deploy of febaff9, attempt 1). The assertion was `Expected: \"succeeded\"`, `Received: \"failed\"`, after 1.6 s. The retry passed. This is the same pattern as the panel-mode test fixed in #424, whose cause turned out to be a real race between panel cleanup's `git status` (with its optional index refresh) and the worktree admin-directory safety check (\"Unsafe worktree Git administration\").\n\n## Change\n1. Reproduce it under contention, **gently: other runs share this machine.** First try running the test file many times under `bun test --parallel=4` together with a few other pipeline-*.test.ts files. That is the real load that triggered it. Only if that doesn't reproduce it, add synthetic CPU load: **at most 4 load processes, at most 10 minutes in total**, keep their pids and stop exactly those. (A previous attempt ran about 20 busy loops for 30 minutes, which starved every other run's gates and was cancelled.) Run the test many times, and on failure dump the run's stage results and events from the store to find which stage failed and why.\n2. Fix the cause. If it is another git call that takes optional locks while a safety check inspects the admin directory, prefer one shared fix (for example `--no-optional-locks` or `GIT_OPTIONAL_LOCKS=0` for read-only status calls in the hardened worktree git wrapper) over a one-off. Don't relax the safety check, and don't just raise timeouts. Explain the cause in one comment where you fix it.\n3. Then run the whole pipeline-*.test.ts set under the same load and report any other flaky test with its cause.\n\n## Tests\n- The test passes 30 times in a row under the same bounded load, at its original deadlines. Report how it failed before the fix.\n- A regression test for the cause if it is in factory code.\n\n## Out of scope\n- Raising timeouts or retrying tests.\n\n## Budget\nSmall; the fix depends on the cause.",
  "spec": null,
  "implementerReport": "",
  "gates": []
 },
 "defects": []
}

# Blocking findings (verifier high/critical), both trials

## trial 0: The fix relaxes the administration safety check
{
 "severity": "major",
 "security": false,
 "file": "src/git/command.ts",
 "line": 65,
 "title": "The fix relaxes the administration safety check",
 "detail": "The request says, “Don’t relax the safety check.” This change instead permits three entries found during the directory listing to disappear without being inspected. The new regression test explicitly establishes that behavior. Although Git normally treats these names as lock files, the inspection no longer verifies every listed administration entry as required.",
 "suggestion": "Remove the source of the optional lock race or coordinate the competing operations while retaining the fail-closed inspection.",
 "failure_scenario": "An index.lock, HEAD.lock, or ORIG_HEAD.lock entry disappears between readdirSync and lstatSync; the wrapper now proceeds where the original safety check refused.",
 "category": "concurrency",
 "confidence": 1,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/git/command.ts:60–64: `const disposable = /^(?:HEAD|ORIG_HEAD|index)\\.lock$/;`, `const lock = dirname(path) === admin && disposable.test(basename(path));`, `const stat = lstatSync(path, { throwIfNoEntry: !lock });`, `if (!stat) return;`. Previously, inspection used unconditional `lstatSync(path)`, which threw for a vanished entry. The new return skips the safety assertions at lines 65–66.",
  "trigger": "A top-level index.lock, HEAD.lock, or ORIG_HEAD.lock disappears between directory listing and lstat. Inspection now succeeds where it previously refused, relaxing the safety check despite the request’s explicit prohibition.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: The fix relaxes the administration safety check
{
 "severity": "major",
 "security": false,
 "file": "src/git/command.ts",
 "line": 64,
 "title": "The fix relaxes the administration safety check",
 "detail": "The new early return accepts a lock entry that disappeared during inspection, where the existing check failed closed. The request explicitly prohibited relaxing that check and required establishing the actual cause before fixing it. The regression test demonstrates the newly accepted condition, but does not establish that it caused the reported environment-verification failure.",
 "suggestion": "Reproduce and identify the failing stage, then address the source of the concurrent lock without relaxing the administration inspection. Report the observed failure and the requested bounded-load results.",
 "failure_scenario": "An inspection lists HEAD.lock, ORIG_HEAD.lock, or index.lock and the entry disappears before lstat: the command now proceeds with an incomplete inspection instead of failing.",
 "category": "correctness",
 "confidence": 1,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/git/command.ts:60-64 adds “const disposable = /^(?:HEAD|ORIG_HEAD|index)\\.lock$/”, then “lstatSync(path, { throwIfNoEntry: !lock })” and “if (!stat) return;”. This explicitly allows inspection to proceed when one of those entries disappears; previously lstatSync(path) threw. test/worktree-git-locks.test.ts:43-49 deliberately removes HEAD.lock during inspection and expects the command to succeed.",
  "trigger": "A listed top-level HEAD.lock, ORIG_HEAD.lock, or index.lock disappears before lstat; inspection now succeeds despite the request explicitly prohibiting relaxation of the safety check. This establishes a requirement violation, not a demonstrated security exploit.",
  "severity": "high",
  "category": "conventions"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: The fix is not tied to a reproduced failure
{
 "severity": "major",
 "security": false,
 "file": "src/git/command.ts",
 "line": 62,
 "title": "The fix is not tied to a reproduced failure",
 "detail": "The request requires: “on failure dump the run's stage results and events from the store,” “Report how it failed before the fix,” and demonstrate 30 consecutive passes under bounded load. No implementer report or other evidence identifies the failing stage, its error, or those runs. The new test simulates a lock disappearing between directory listing and lstat, which previously raises ENOENT; it does not establish that this was the cause of the reported test failure. The requested full pipeline test run and report of other flakes are also unverified.",
 "suggestion": "Reproduce the failure under the requested bounded load, inspect its stored stage results and events, fix the observed cause, and report the before-fix failure and requested validation results.",
 "failure_scenario": "If the environment verification retry fails for a different reason, the new disappearing-lock handling and its passing regression test leave the original deploy-gate flake unresolved.",
 "category": "test-gap",
 "confidence": 0.99,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "PLAUSIBLE",
  "evidence": "test/worktree-git-locks.test.ts:42-49 models an assumed cause: “The concurrent command finishes after the listing and before lstat,” removes HEAD.lock through a mocked lstatSync, and checks factory(\"rev-parse\", \"HEAD\"). src/git/command.ts:54-59 explains that race, but the supplied change contains no captured failure linking it to the environment-verification test.",
  "trigger": "If the original environment-verification failure has another cause, the simulated lock-race regression can pass while that failure remains. The repository evidence does not establish whether this happened.",
  "severity": "high",
  "category": "reliability"
 },
 "agreement": 1,
 "duplicates": []
}
