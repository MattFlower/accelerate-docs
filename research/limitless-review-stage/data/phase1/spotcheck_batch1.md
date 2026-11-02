# Spot-check batch: escape-corpus pilot (20 random of 47 labels)

For each item: does the label follow from the scenario and the evidence? Reply with the numbers you
disagree with and why (logic only; no TypeScript needed). "Gold" means a review must catch it.

**1. PR #636 round 1: Five "is gone" assertions still race zombie reaping**
- Label: **not gold: minor** (severity set by orchestrator)
- Scenario: During an unconfined macOS run (a developer machine or the manual land-pr check), the signal-confinement timeout/cancel test kills a grandchild process whose parent is killed at the same moment. The system's init process may not have collected the dead grandchild yet when the test checks it, so the test sometimes fails even though cleanup worked. The other four sites the reviewer lists cannot fail this way.
- Evidence: unreproduced: the only racy site (signal-confinement:209) runs only under real unconfined macOS Seatbelt, and the race window is launchd reaping a reparented zombie. I did confirm on this Mac that sig
- Fixed in the next round: yes

**2. PR #485 round 2: Short multiline holdout prose written with `\n` escapes still leaks its later lines**
- Label: **GOLD (major)** (adjudicator's reading: breaks a trust or confinement boundary) (severity set by raters)
- Scenario: An agent requests a change containing a JSON-escaped copy of a private multiline holdout. The patch and report reveal the holdout’s second line despite the required privacy boundary.
- Evidence: reproduced: `F1: available=true; patch contains +"[private detail]\nViolet sea"; report contains Factory report: "[private detail]\nViolet sea"; patchLeaks=true; reportLeaks=true.`
- Fixed in the next round: yes

**3. PR #549 round 1: A restored shadow review error is written to its artifact unredacted**
- Label: **GOLD (major)** (adjudicator's reading: leaks a secret or private data) (severity set by orchestrator)
- Scenario: A resumed run contains an old shadow-review error with a credential. Skipping the shadow review copies that credential into its diagnostic artifact, even though the accompanying log is sanitized.
- Evidence: reproduced: `F3 artifact.reason="legacy shadow \u001b[31mSYNTHETIC_ADJUDICATION_549_SECRET"; log.message="Shadow panel skipped: legacy shadow [redacted]"; baseLoadedError="legacy shadow [redacted]"; invocations=0`
- Fixed in the next round: yes

**4. PR #546 round 3: A 40-bit pairing code built from a relay-chosen nonce can be matched offline**
- Label: **GOLD (major)** (adjudicator's reading: breaks a trust or confinement boundary) (severity set by orchestrator)
- Scenario: An attacker intercepts a worker's first pairing connection and searches for a substitute nonce that makes both displayed codes match. If successful, the owner approves the intercepted pairing and the worker trusts the attacker's certificate.
- Evidence: reproduced: `{"target":"6Z3ZW638","comparisonBits":40,"reducedTargetBits":20,"tries":905736,"code":"6Z3ZL7RH","nonce":"00000000000000000000000000000000000000000000000000000000000dd207","prefixMatch":true,"fullMatch":false,"elapsedMs"`
- Fixed in the next round: yes

**5. PR #1014 round 1: Recover before closing uncertain posts; fixed codes on transport errors; test the recovery selector**
- Label: **GOLD (major)** (adjudicator's reading: leaks a secret or private data) (severity set by orchestrator)
- Scenario: After GitHub accepts a question comment but its response is lost, restarting with unavailable privacy inspection permanently closes the checkpoint without recovering the existing comment. Separately, a publication transport error containing configured private text writes that text into diagnostics.
- Evidence: reproduced: `Three temporary tests reused HEAD's fixture with fake GitHub calls. Recovery: before reopening, pending/page=1 and one remote comment; after reopening with private-strings.txt replaced by a directory, done/commentId=null`
- Fixed in the next round: yes

**6. PR #817 round 1: Recover this process's own abandoned invocations; the live-owner skip is only for other processes**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by raters)
- Scenario: An invocation exits but a failed shutdown scan leaves its descendant running. When the same daemon resumes work in a fresh scope, recovery silently skips the abandoned invocation and allows another command to run alongside the surviving process.
- Evidence: reproduced: `first invocation: Invocation termination could not be confirmed: forced shutdown scan failure after failed shutdown: {"orphanAlive":true,"rows":1,"ownerIsCurrentProcess":true} fresh scope: {"exitCode":0,"stdout":"next co`
- Fixed in the next round: yes

**7. PR #536 round 1: A setup arm counts as production routing evidence and makes policy selection order-dependent**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: An operator evaluates the same reviewer with and without dependency setup, then generates routing policy. Both arms enter one model's evidence, and changing their trial order changes the reported pass rate while preventing complete paired comparisons.
- Evidence: reproduced: `F2 {"order":"control-first","countedSystems":["control","setup"],"passRate":1,"pairedCases":0} F2 {"order":"setup-first","countedSystems":["setup","control"],"passRate":0,"pairedCases":0} F2 distinct valid config hashes `
- Fixed in the next round: yes

**8. PR #811 round 2: A post-merge targeted failure gets the slow-run retry**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: A documentation-only change passes its selected tests before merging the latest base, then encounters a much slower transient failure afterward. The automatic recheck is suppressed, so the run requires human intervention even when that recheck would pass.
- Evidence: reproduced: `F3 {"targeted":false,"initialVerdict":"regressed","isSlow":true,"retries":1,"finalVerdict":"flaky","blocking":false} F3 {"targeted":true,"initialVerdict":"targeted_failure","isSlow":false,"retries":0,"finalVerdict":"targ`
- Fixed in the next round: yes

**9. PR #549 round 1: Verification artifacts now store gate evidence without credential or escape redaction**
- Label: **GOLD (major)** (adjudicator's reading: leaks a secret or private data) (severity set by orchestrator)
- Scenario: After a run resumes, a passing gate whose name contains a credential supplies verification evidence. The credential is copied into the stored verification artifact.
- Evidence: reproduced: `F1 {"status":"met","headContainsSecret":true,"headContainsEsc":true,"baseContainsSecret":false,"baseContainsEsc":false}`
- Fixed in the next round: yes

**10. PR #886 round 2: C: the second re-approval guard still compares timestamps strictly**
- Label: **not gold: minor** (severity set by orchestrator)
- Scenario: A trusted owner reapplies a priority label after the failure label, within the same timestamp second as the failed run finishes. The queue rejects that approval on every subsequent poll until the owner approves again later.
- Evidence: reproduced: `F3 {"withoutLatest":{"eligible":true,"priority":1},"withLatest":{"eligible":false,"reason":"priority re-approval required after the latest issue run"}} FAIL: expected eligible:true.`
- Fixed in the next round: yes

**11. PR #592 round 1: The Bun executable allowance is interpreted as a pattern, so a path with glob characters can reopen denied credential reads**
- Label: **not gold: minor** (severity set by orchestrator)
- Scenario: The factory runs from a Bun installation whose path contains a literal wildcard directory. A confined reader receives a broader read permission than intended, permitting access to a credential file that should remain denied.
- Evidence: reproduced: `The throwaway script created synthetic H/.aws/credentials, copied Bun to H/*/credentials, launched that copy, and passed HEAD's generated filesystem settings to wrapCommandWithSandboxMacOS. F2 buildClaudeArgs: accepted a`
- Fixed in the next round: yes

**12. PR #984 round 1: Recovery: check that the tip is still `before` before accepting an equivalent record**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by raters)
- Scenario: An owner journals a renewal with unchanged fields and restarts before sending it. Recovery reports the renewal as applied even though no new remote commit exists, falsely treating interrupted work as completed.
- Evidence: reproduced: `F1: result="applied", confirmed={generation:1,tip:"0000000000000000000000000000000000000001",state:"held"}, intent=null, updates=0. Assertion failed: expected "dropped", received "applied".`
- Fixed in the next round: yes

**13. PR #886 round 2: D: resume per issue, not per run, so inaccessible issues can't starve later ones**
- Label: **not gold: minor** (severity set by orchestrator)
- Scenario: A run links many issues, and its first 25 issues are inaccessible. Their repeated failed requests consume every poll's allowance, so the accessible final issue never receives its lifecycle labels or comments.
- Evidence: reproduced: `F4 {"callsPerPoll":[50,50,50,50,50,50,50,50,50,50],"issue26Calls":0,"labels":[],"comments":0} FAIL: issue 26 had no in-progress label.`
- Fixed in the next round: yes

**14. PR #811 round 2: Only target or skip a test check whose command is a single bun test invocation**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: A repository combines its Bun tests and another required test command in one gate. A documentation-only change causes the factory to remove the additional command, leaving required checks unexecuted.
- Evidence: reproduced: `{"head":"21483e7e2259a5afa853f81830cde22e188e8e61","selection":{"mode":"skipped","changedPaths":["docs/research/10-underspecified-requests.md"],"files":[],"reason":"docs-only change; no test reads the changed files"},"re`
- Fixed in the next round: yes

**15. PR #549 round 1: redactGateDiagnostics treats any object with ok and output keys as a gate result, including package script maps**
- Label: **not gold: minor** (severity set by orchestrator)
- Scenario: A repository has package scripts named ok and output. Resuming its run rewrites the saved output command and inserts a bogus script entry, so unchanged scripts produce blocking audit findings.
- Evidence: reproduced: `F2 {"persistedScripts":{"ok":"true","output":"true # [redacted]","confinementError":false},"findings":[{"rule":"gate-script-changed","severity":"block","detail":"Changed the \"output\" script that a factory check runs (\`
- Fixed in the next round: yes

**16. PR #536 round 1: Setup edits to tracked files reach the reviewer**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: A repository's dependency setup regenerates or overwrites a tracked source file. The reviewer examines those modified bytes instead of the labelled revision, making the trial's findings and score unreliable.
- Evidence: reproduced: `F1 focused setup-path probe (synthetic base Git reads; injected test confinement) {"setupOk":true,"fileAfterSetup":"setup-overwrite"}`
- Fixed in the next round: yes

**17. PR #811 round 2: Keep protected paths protected for patterns with a trailing slash**
- Label: **GOLD (major)** (adjudicator's reading: breaks a trust or confinement boundary) (severity set by orchestrator)
- Scenario: A repository protects its fixtures with a trailing-slash glob that previously worked. An agent edits an existing fixture, and the audit no longer blocks the protected change.
- Evidence: reproduced: `F1 {"pattern":"test/fixtures/**/","baseMatches":true,"headMatches":false,"headProtectedFindings":[]} F1 {"pattern":"test/fixtures/","baseMatches":false,"headMatches":false,"headProtectedFindings":[]} F1 {"pattern":"**/",`
- Fixed in the next round: yes

**18. PR #489 round 2: A failed startup leaves started work running and drops the token's protection too early**
- Label: **GOLD (major)** (adjudicator's reading: breaks a trust or confinement boundary) (severity set by orchestrator)
- Scenario: Startup resumes queued work and then fails, but does not reliably stop everything it started. Token-file protection can disappear before cleanup finishes, so sandbox policies constructed during that interval omit the credential’s read denial.
- Evidence: reproduced: `F1 mount failure: {"landStarted":1,"landStopped":0,"notifierTimersLive":1,"tokenProtected":false} F1 real bind failure: {"protectedDuringIntegrationStop":false,"profileDeniesToken":false} The probe used real integration `
- Fixed in the next round: yes

**19. PR #630 round 2: The marker test fails on macOS outside the sandbox, so `bun run check` fails there**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: A developer or deployment runs the checks on macOS with its normal temporary directory. The new test rejects equivalent paths and fails the checks, preventing an otherwise valid change from shipping.
- Evidence: reproduced: `Exit 1: Expected "[test:start] /var/folders/.../ci-test-start-obS2pQ/hang.test.ts"; received "[test:start] /private/var/folders/.../ci-test-start-obS2pQ/hang.test.ts". 0 pass, 2 skip, 1 fail. Running TMPDIR="$(realpath "`
- Fixed in the next round: yes

**20. PR #536 round 1: Finder replay ignores setup, so a setup system can reuse findings made without dependencies**
- Label: **GOLD (major)** (adjudicator's reading: a realistic input in normal operation gives a wrong result or a silent failure) (severity set by orchestrator)
- Scenario: An operator replays stored panel findings into a trial configured to install dependencies. The trial reuses findings produced without those dependencies instead of running its finders in the requested environment, misrepresenting what the setup arm measured.
- Evidence: reproduced: `F3 {"sourceSetup":false,"targetSetup":true,"validation":"accepted","vendor":"fixture-vendor","reconstructed":{"verdict":"approve","summary":"Finder findings reconstructed from the stored source panel trial.","findings":[`
- Fixed in the next round: yes
