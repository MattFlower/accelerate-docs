# Review-eval labelling rubric (APPROVED by Matt 2026-10-30: Q1-Q5 as recommended, severity line below)

This decides which findings count as **gold defects**, the things a factory review must catch. It builds on the
rules already in `evals/review/LABELS.md` (2026-10-08 candidate rule, 2026-10-23 escape-case rule) and the past
precedents listed below. Questions 1–4 at the end are the policy calls only you can make. You don't need to read
TypeScript for any of it.

## Who does what
- **Two adjudicators from different vendors** (Claude Opus and GPT-6.1 Sol, both at high effort) judge every
  candidate independently in a checkout of the exact reviewed commit. They don't see each other's verdicts, which
  reviewer produced the finding, or its original severity.
- **I confirm** every label. Where the vendors disagree, I settle it by running code (a failing test or command),
  never by picking a side.
- **You** approve this rubric once, spot-check about 20 random labels per batch at the logic level, and decide
  policy disputes. TypeScript-specific questions are settled by execution or a third model, never by you.

## What every label carries (so you can check it without reading TypeScript)
1. **Verdict:** real defect / not a defect / not code (process, merge, docs, question).
2. **Severity** (blocker / major / minor / nit) **and the criterion it meets** (below).
3. **Failure scenario in plain language:** who does what, what goes wrong, and what it costs.
   Example: "A gate test is skipped, so the run counts the skipped test as passing evidence and approves a change
   whose new test never ran."
4. **Reproduction:** the command or test, and the output showing the failure at the reviewed commit. Otherwise the
   label says **unreproduced** and why (for example, it needs real macOS Seatbelt or a real GitHub call).
5. **In the change?** Introduced by this PR, newly exposed by it, or already present before it (see Q3).
6. **Fixed later?** Whether the factory's later fix commit addresses this mechanism: yes / partial / no.

## Gold = all of these
- **Real at the reviewed commit:** a reproduction, or quoted code compared against the base that shows the
  mechanism. A claim with neither is rejected.
- **Code, not process.** Merge-conflict requests, PR-description asks, "add measurements to the PR" and answers to
  implementer questions are not gold (precedent: review-108 C14).
- **In the change:** introduced or newly exposed by this PR (Q3 covers requirements the PR was asked to deliver).
- **Major or blocker** under the severity line below. Confirmed minors and nits are kept as optional defects: a
  review that reports one is neither rewarded nor penalised.
- **One defect, one label.** Two findings describing the same mechanism merge. A defect re-raised in a later round
  of the same PR is tagged as a re-raise and counted once per case.

## Severity line (approved 2026-10-30)
Severity = consequence × trigger. Test: "would this plausibly happen in the next month of normal factory operation?"
(deploys restart the daemon daily, so restart-window bugs count unless the window is milliseconds).
- **Blocker:** realistic trigger + loses or corrupts persisted state, leaks a secret or private data, breaks a trust or
  confinement boundary, or stops the factory or deploys.
- **Major:** realistic trigger + real harm: wrong result, silent failure, lost or repeated work, a bypassable check the
  change claims to add, a rollback / older-daemon compatibility break.
- **Minor:** contrived trigger (unusual input, environment or timing the request doesn't ask to handle — e.g. a literal
  `*` in the Bun path, scripts named `ok`/`output`, Ctrl-C in a millisecond window, same-second timestamps, a
  hand-restored label before restart, 25+ inaccessible linked issues, a posting account changed between retries), or a
  cosmetic / diagnostic / test-only cost.
- **Exception (Q5):** a secret leak is at least major even with an unusual trigger.
- **Nit:** style, naming, wording.

Severity comes from this line applied to the reproduction, not from either adjudicator's word.

## Precedents already on record
- **review-082 claim 2:** a confirmed major kept the case clean because AGENTS.md had explicitly adopted that
  behaviour. A behaviour the repository's own rules adopt is not a defect.
- **review-108 C14:** missing measurements in the PR description are process, not gold.
- **Sandbox PR #14:** Unicode case folding not requested by the change is minor, so that case stays clean.
- **review-068 C4:** a skipped test let the gate-evidence substitution pass. It was later fixed by #647 after
  causing about 20 of 49 needs_human runs. This is the kind of defect gold must contain.

## Policy questions for you (my recommendation first)
1. **Missing or weak tests.** "The PR's new test passes even without the change" or "there's no regression test":
   is that gold?
   *Recommend:* gold only when it hides a real behavioural defect that is itself labelled. Otherwise minor.
   A new test that *fails* on the platform the factory deploys from (macOS, default temp directory) is different:
   it blocks `bun run check` and every deploy, so it is judged by that consequence (major).
2. **Bugs introduced by the factory's own fix in an earlier round.** Does such a bug count as a defect in the later
   round's case?
   *Recommend:* yes. Each round is its own reviewed commit, and the factory review approved it.
3. **Requirement not delivered, gap already in main.** The request asks for X, the PR touches X but doesn't fully
   deliver it, and the gap was already in main. Is that gold?
   *Recommend:* yes, when the request explicitly requires X. Spec-mismatch is a known blind spot (0 of 6 caught).
   If the request doesn't mention X, it isn't gold.
4. **Severity line above.** Is the major/minor boundary where you want it? These real pilot disputes show where it
   bites (my proposed rating in brackets):
   - A worker claims its token after the coordinator restarted. The claim secret is no longer registered for
     redaction, so later output containing that secret isn't masked. [blocker: leaks a secret]
   - The factory's Bun path contains a literal `*`. The confinement rule treats it as a wildcard and lets a sandboxed
     reader see more files than intended. [blocker on the rule's wording, but the trigger is very unusual: minor?]
   - The owner pins the review model chain. A panel finder marked local-only then runs on a remote worker, against
     the request's "local finders stay local". [major]
   - A new test fails on macOS when the temp directory is spelled through `/var`, which is macOS's default. It blocks
     a clean local check but breaks nothing at runtime. [major or minor? It fails every default macOS run.]
   - "Add the regression tests for both findings": only a missing test. [minor under Q1]

   *Recommend:* the line as written, with "a check the change claims to add can be bypassed by a realistic input" as
   major even when nothing bad has happened yet. Tell me where you'd move any of the examples.
5. **Redaction gaps with an unusual trigger.** A credential that the factory knows about ends up stored or shown
   unmasked, but only if it appears somewhere odd: inside a gate's name, a retry command, or a saved error message.
   AGENTS.md requires redaction at every boundary, and orchestrator reviews raise these often. In the pilot, 5 of 47
   findings were this kind.
   *Recommend:* major, not minor, because the repository's own rule makes it a requirement. That keeps them gold.
