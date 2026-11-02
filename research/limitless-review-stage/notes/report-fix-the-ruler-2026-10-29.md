# Fix the ruler, then widen the search

> **Correction (2026-10-29, superseded by phase0/RESULTS.md).** The grader figures below predate Phase 0. Final judged numbers (two-judge consensus plus a code-reading tiebreak): dev production 31.6%, sol@high 41.8% (+10.2), adversarial 49.0% (+17.4), union-of-2 D 47.4% (+15.8); held-out production 18.6%, D 33.0%. The ±5 grader is noisy in both directions rather than biased toward conservative systems. Sol ∪ Opus judged is ~40%, not 50%.


Limitless can plausibly gain 10 or more points of blocking-defect recall, but the first obstacle is the instrument rather than the reviewer. Re-scoring the stored eval trials shows that the ±5-line grader under-credits the bolder variants most: about 3 points for production and about 8 points for the adversarial prompt. The clean-case guardrail runs on 8 trials, so the upper bound on the false-block increase is about 37%. The gold set only measures agreement with one oracle reviewer, and two runs of the same system differ by 8 to 10 points. Under these conditions the current "+8 points, at most +1 clean block" rule misses a real +10 gain about 40% of the time and accepts a variant with no real gain about one time in five. On the reviewer side, the internal data shows two separate failures:

- **Sol stops early.** It averages 0.57 findings per production review and uses about 2 of its 20 minutes.
- **Opus finds defects but rates them minor.** Its location-matched recall doubles from 15% to 30% once minor and nit findings count. Unioned with Sol, the pair reaches 50% recall per trial against Sol's 34%.

The options with the best evidence, all distinct from what has already been tried:

- **(A) Replicate the oracle's procedure.** The gold reviewer works from a PR-specific verification brief, runs at high effort and adds a mutation check.
- **(B) Two-tier discovery.** A wide, recall-tuned, mixed-model discovery stage feeds a blocking channel that admits only witnessed or agreed findings; everything else becomes a comment.
- **(C) Coverage prompt with a checked ledger** for Sol.
- **(D) Attack pass for trust boundaries,** with deterministic triggers and execution that only adds findings.
- **(E) Acceptance tests written from the request** before the reviewer reads the diff.
- **(F) Precomputed impact pack** of out-of-diff context.
- **(G) Deterministic severity,** with parking of defects as follow-ups ended.

External evidence settles none of these. It only decides which options to try first, and a measured tournament on Limitless's own evals decides the rest. The tournament needs a fixed instrument:

- a larger corpus,
- judge-based matching,
- an audited clean set,
- A/A variance runs,
- K≥4 trials,
- paired, PR-clustered statistics.

No external corpus can replace the in-house set, because none is TypeScript-heavy, defect-verified and supplied with clean PRs. The best route to statistical power is labelling the 405 unused orchestrator findings (about 200 more gold defects). Replays of explicitly linked escapes add gold that doesn't come from the oracle. GitHub ReviewBench's roughly 60–80 TypeScript/JavaScript PRs and SecBench.js serve as external checks.

## The reviewer stops early, and Opus finds what it then under-rates

Production review today is one reviewer with a generic prompt: codex/sol-6.1 at medium effort since 2026-10-23, and Opus at high effort for most runs before that. It is read-only but may run targeted tests. The repository's review lenses reach only panel finders, so production never sees them. From the second round on, new non-security majors are turned into follow-ups rather than blocks (internal_findings.md). Since 2026-10-07, **Sol has produced 0.57 findings per review across 299 production reviews**: 72 blocker, 90 major, 7 minor. That is even sparser than the 1.1 per trial it shows in evals, where it uses about 2 of its 20 minutes. This matches what an independent benchmark measured for the same model family. In CRBugBench, **half of gpt-5.6-sol review runs end by turn 17** against turn 35 for opus-5, and only about 8% of agent turns execute code ([CRBugBench](https://arxiv.org/html/2610.13668)). Greptile reports that GPT reviewers "search depth-first and comment less (about 1–2 per review)" and can drop bugs they have already identified, while Claude models comment 7–8 times per review ([Greptile](https://www.greptile.com/blog/model-inversion)). Cursor saw the same over-caution when Bugbot went agentic. It rewrote its prompts to push the agent to investigate and flag more readily: bugs flagged per run rose from 0.4 to 0.7 and resolution rate from 52% to over 70% ([Cursor](https://cursor.com/blog/building-bugbot)).

Opus fails differently. In production it averaged 1.21 findings per review across 398 reviews, but 233 were minor and 145 nit. I re-scored the stored eval trials, and the pattern shows up there as well. In the paired Sol-vs-Opus run (eval-mv7rznhb0nugf7t09om5i6, 49 dev defects, 2 trials), **Opus's blocking recall is 15.3%, but 29.6% of defect-trials have an Opus finding of any severity at the gold location.** In the later opus@high run (eval-mvlhu0571ydkrqq15dbjsa) the figures are 18.9% and 29.5%. Sol at medium effort scores 33.7% either way, because it almost never files minors. The two models also catch different defects. **The per-trial union of Sol's blocking findings and Opus's findings at any severity reaches 50.0%, against 33.7% for Sol alone.** Across both trials Opus catches 12 of the 49 defects that Sol never catches. For comparison, a union of Sol at medium and Sol at high in the same paired run reaches only 46.9%, with 6 extra defects.

Three cautions keep this a hypothesis, not a finding:

- **Matching at any severity is loose.** A nit that happens to sit on the gold line for a different reason gets credit, so the 12 Opus-only defects need a semantic-judge check.
- **Opus files minors on clean PRs.** At high effort it left minor findings on 5 of 7 clean trials, so promoting its minors to blocks would raise false blocks.
- **The corpus PRs are mostly Codex-authored.** That is the cell where Greptile found the non-authoring model strongest (Opus 4.7 at 53.7% against GPT 5.5 at 50.5% on Codex-authored PRs). Opus still lost on blocking recall here. So our data contradicts the "review with the other vendor" claim on severity calibration, not on detection. Opus is a useful finder whose severity labels shouldn't be trusted.

The production record agrees: of 26 escapes that heuristically match an earlier factory non-blocking finding on the same PR, 23 came from Opus (internal_findings.md).

What the reviewer misses, and why, bounds what any lever can do:

- **The 30 production misses** break down as 13 that needed files outside the diff, 9 that needed adversarial execution, 7 visible in the diff and 1 convention.
- **By category,** security recall is 0/12 and spec-mismatch recall 0/6.
- **The ceiling for prompts:** 18 of the 30 misses were found by no system tried. Prompt tweaks that keep a single reading agent will therefore stall well short of the gold.

The literature agrees on the out-of-diff problem: in CRBugBench, bugs visible in the diff are detected at an **odds ratio of 2.6** over those that need other context ([CRBugBench](https://arxiv.org/html/2610.13668)). Swapping the model did not move escapes at all. PRs whose last factory review was Opus averaged 2.0 orchestrator round-1 blocker/major findings; Sol PRs averaged 1.84; both averaged about 3.0 across all rounds. The model is not the binding constraint.

The orchestrator's own review method is the most direct clue to what is. The orchestrator writes a 1.5–2 KB brief specific to the PR, with the full context of issue, spec, prior rounds and recurring-defect memory. The brief restates requirements as concrete checkable claims, names every caller that must adopt a new check, gives specific test inputs and asks targeted questions ("does any caller still have its own inspection?", "do the tests fail without the round?"). `codex exec` then runs that brief on gpt-6.1-sol at high reasoning with write access to add failing regression tests. A mutation check follows: revert the source diff, and the PR's tests must fail. The factory reviewer gets one generic prompt at medium effort, with no brief and no mutation check. **The gold is the product of a procedure, not of a better model.** It is the same Sol model at a different effort, given a plan.

## The ruler under-credits bold reviewers and cannot see false blocks

Five weaknesses in the eval each bias decisions toward conservative variants, and together they make a 10-point gain hard to detect even if it exists.

### The ±5-line grader misses the same defect when it is reported elsewhere

An independent judge reviewed the 192 missed defect-trials that had an uncredited blocking finding in the same file or with a closely matching title. Of these, **27 were the same defect** reported at the root cause in another file, at the caller or catch site, or just past the ±5-line window. Another 158 were judged different and 7 unclear (internal_findings.md). The credit is not spread evenly. My recomputation from the stored trials:

| Run (system) | Grader recall | With judge-matched credit | Gain |
|---|---|---|---|
| E1 dev, sol@medium (production) | 33.7% | 36.7% | +3.1 |
| E1 dev, sol@high (same run) | 43.9% | 46.9% | +3.1 |
| E3 dev, adversarial prompt | 48.0% | 56.1% | +8.2 |
| D dev, union of 2 adversarial samples | 47.4% | 53.6% | +6.2 |
| E3 held-out, standard | 29.1% | 31.4% (34.9% incl. unclear) | +2.3 to +5.8 |
| E3 held-out, adversarial | 34.9% | 37.2% (39.5% incl. unclear) | +2.3 to +4.6 |
| D held-out, union of 2 | 45.5% | 48.9% (51.1% incl. unclear) | +3.4 to +5.6 |

The coordinator's tally puts the adversarial dev run at 45.9% → about 54.1%. My figures differ by about 2 points, probably because of how the denominator is defined; the direction and the gap between systems are the same. The table supports a narrower claim than "the adversarial prompt already clears +10":

- **Different days.** The adversarial dev run and the production dev run happened on different days, so run-level drift is mixed into the gap.
- **The held-out gap is smaller.** On held-out, adversarial vs standard is about +6 points after correction.

The defensible conclusion is that **past rejections were made with a biased ruler and should be retested paired and interleaved under a fixed matcher**. One paired comparison does exist. Within E1, sol@high beat sol@medium by **+10.2 points under corrected credit** (46.9% vs 36.7%), with clean blocks at 3/8 against 2/8. That makes higher effort the cheapest single change that deserves a held-out confirmation. Current benchmarks have abandoned location-only matching for exactly this reason. SWE-PRBench uses an LLM judge with one-to-one assignment, validated at κ=0.75 ([SWE-PRBench](https://arxiv.org/html/2603.26130v1)). SWR-Bench reports 89–95% hit agreement between expert and LLM judges and rejects exact-match metrics ([SWR-Bench](https://arxiv.org/html/2509.01494v1)).

### The gold measures agreement with one reviewer

The 158 "different" verdicts are not adjudicated defects: the judge was asked only "same or different", not "is this real". They do show that variants routinely report other plausible blocking issues that earn nothing. Gold defined by one reviewer structurally penalises a variant that finds *different* real defects. Information retrieval faced this decades ago. TREC treats judgments as pooled and incomplete, and bpref-style measures that use only judged items stay robust when judgments are substantially incomplete ([Buckley & Voorhees, SIGIR 2004](https://www.nist.gov/node/761376)). GitHub's ReviewBench applies pooling to code review. It pools candidate findings from humans, follow-up commits, static analysis and several LLM families, judges them all against one rubric, and makes **grounded recall** against the frozen pool the headline cross-system metric ([GitHub blog](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)).

### Clean labels are contaminated, and the guardrail is too small to inform

Audits found that 6 of 19 M4.5 "clean" PRs had real defects of at least medium severity, and 12 of 17 #235 "false blocks" were real. A better reviewer is therefore *penalised* for finding real defects on mislabelled clean cases. The guardrail is also too small to mean anything. With zero extra blocks in n clean trials, the 95% upper bound on the block-rate increase is about 3/n: **37.5% at the current 8 dev trials** ([Miller 2024](https://arxiv.org/html/2411.00640v1) framework; my calculation). The D variant was rejected on 3 extra false blocks out of 26. The 95% Clopper–Pearson interval for 3/26 runs from about 2.4% to 30%, before any adjudication of whether those blocks were real. SWR-Bench shows a remedy: it **used SZZ to purge "clean" PRs whose defects were fixed later** ([SWR-Bench](https://arxiv.org/html/2509.01494v1)).

### The corpus is too small for a +10-point decision, and same-system noise is high

Miller's paired sample-size formula, under plausible variance assumptions, calls for **about 160–200 gold defects at K=2 trials, or about 110–130 at K=4**, to detect +10 points at 80% power. A cluster design effect for defects nested in PRs adds about 1.2× ([Miller 2024](https://arxiv.org/html/2411.00640v1); my calculation from the eval_methodology notes). The dev split has 49 required defects. Trial noise alone predicts a same-system gap of about 4 points at n=90, K=2; the observed 8–10 points is roughly twice that. That points to **run-level drift** (serving or model changes between days) and **matcher instability**, which pairing does not remove and more cases do not shrink. If the true same-system standard deviation is 8–10 points, the +8 rule accepts a null variant 16–21% of the time and misses a real +10 about 40% of the time. Small-N CLT intervals also under-cover. Bowyer et al. recommend Bayesian paired or clustered models instead ([Bowyer et al., ICML 2025](https://arxiv.org/pdf/2503.01747)).

### The held-out set is used up

The held-out clean set is saturated, and the old held-out defects were seen while labelling and spent on E3 and D. A fresh held-out set has to come from PRs newer than any used in prompt development.

### What "+10 points" should mean

The target should be stated as **+10 absolute points of grounded blocking recall on a frozen, pooled-and-adjudicated gold set, scored with a validated semantic matcher.** The baseline is the stored production trials re-scored under that matcher, which costs nothing and respects the no-rerun-paid-baselines rule. Against a 34% baseline, a relative 10% would be 3.4 points, which is inside the noise. "Without raising false blocks" can't be certified at today's sizes. It becomes testable as a non-inferiority margin on the clean-block rate, measured on all ~48 clean PRs at K≥2 for both arms, paired, after every clean-case block has been adjudicated blind. Even then, a 10-point margin needs about 62–124 paired clean trials and a 5-point margin 250–500, so the precision side has to rest partly on mechanism (witnesses) rather than on counts.

## Seven options, each aimed at a different miss bucket

The options below differ in mechanism, not just in prompt wording. Each names the misses it targets and how it keeps clean false blocks down. Every trigger is deterministic engine code (path or size rules), and LLMs work only inside stages, per AGENTS.md. The expected-gain figures are my judgement from the cited analogues, not predictions. They set the order of the tournament, not its result. Each option, and the combinations below, can be built as an eval variant and run against the same fixed instrument. Several of the cheapest tests need no new paid runs: re-scoring stored trials under the semantic matcher, and replaying the two-tier blocking rule on D's stored findings.

| Option | Targets | Evidence grade | Expected gain (judgement) | False-block control | Wall time / tokens | Trigger |
|---|---|---|---|---|---|---|
| A. Oracle replication: PR brief → Sol@high executor → mutation check | spec mismatch, out-of-diff callers, diff-visible | Internal: it produces the gold; @high alone +10.2 corrected (paired) | Large on in-house gold (inflated by circularity); must win on independent gold | Targeted claims; mutation check is deterministic | +10–20 min; ~3–5× | Every review |
| B. Wide mixed-model discovery + two-tier blocking | early stop, Opus severity mis-rating, run variance | Internal union 50.0% (hypothesis); SecPRBench union; ICML overdispersion; witness/agreement literature | +10–16 on recall; FB depends on the gate | Block only on witness or k-agreement in calibrated categories; rest are comments | Parallel, ~same wall time; k× tokens | Every review (k scaled by size) |
| C. Coverage prompt + checked coverage ledger | diff-visible, early stop | CRBugBench Table 2 (+5–6 for GPT-family); Bugbot; internal checklist +6.3 | +3–6 | Unmeasured; ledger is checked deterministically | ~1.0–1.1× | Every review |
| D. Trust-boundary attack pass | security 0/12, execution 9/30 | SecPRBench (+7.7 with Defending Code harness); AIxCC; CyberGym; agentic PBT | Large on the security slice; +3–8 overall | Only a harness-observed witness blocks; others labelled, not deleted | +5–15 min in parallel; ~2–10× on triggered PRs | Path map to boundary catalog |
| E. Acceptance tests from the request | spec mismatch 0/6 | Otter, e-Otter++, Issue2Test; conformance-overcorrection studies | Small overall, large for its slice | Doubtful tests become non-blocking "spec questions" | +5–10 min | Has an issue/request |
| F. Precomputed impact pack | out-of-diff 13/30 | Observational only (CRBugBench OR 2.6); internal trace finder −3 | Unknown; cheap to test | Context only, no new findings path | Seconds (rg/tsc) | Every review |
| G. Deterministic severity and no follow-up parking | ~6% of escapes already found but not blocked | Internal (26/405 matched); uReview, CodeRabbit per-category rules | +2–3 on escapes | Severity from category and consequence, not from model label | Negligible | Policy |

### A. Replicate the oracle's procedure, then prove it on independent gold

The internal record makes this the most direct lever. The gold was produced by a planner writing a brief specific to the PR, with checkable claims, the callers that must change, test inputs and targeted questions. The brief went to Sol at high effort with permission to write failing tests, and a mutation check followed. The factory has all the inputs: the issue, the spec and its "Out of scope" list, prior rounds and AGENTS.md's recurring-defect list. A planner stage would write the brief (a Claude planner reproduces the oracle's vendor split), a Sol@high executor would carry it out in a scratch copy, and the engine would run the mutation check deterministically: revert the source diff, and the PR's own tests must fail. Higher effort alone already gave +10.2 corrected points in the only paired comparison on record.

The design borrows from evidence elsewhere: Anthropic's security harness found that "goal plus context" works better than long checklists ([Defending Code](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)). Meta's semi-formal reasoning template, which forces premises, then a path, then a conclusion, raised fault localisation top-5 by about 5–12 points on adjacent tasks ([arXiv 2603.01896](https://arxiv.org/abs/2603.01896)). That template targets SecPRBench's finding that **68% of missed security bugs were reported in the right file with the wrong mechanism** ([SecPRBench](https://arxiv.org/html/2610.33509)).

The caveat is circularity. A variant built on the oracle's procedure will score well on gold that the same procedure generated, partly by sharing its blind spots. Option A must therefore be judged on gold that doesn't come from the oracle:

- replays of explicitly linked escapes,
- review-round findings adjudicated blind,
- the ReviewBench TypeScript slice.

### B. Search wide with a mixed portfolio, block narrowly on evidence

Three facts point here: union recall keeps climbing past two samples, model diversity beats repetition, and the internal data shows Opus and Sol catching different defects.

- **SecPRBench:** an oracle union of 8 agents found 91.3% of targets against 78.1% for the best single agent; the top four alone reached about 90% ([SecPRBench](https://arxiv.org/html/2610.33509)).
- **ICML 2026 (25,000 vulnerability-detection trials):** run-to-run detection is overdispersed (κ≈6.8). A portfolio of cheap models hit a high-reliability target for under $1, against about $41 of repeated scans with the strongest single model ([ICML 2026](https://icml.cc/virtual/2026/78010)).
- **CRBugBench ensembles of the same model** gave smaller gains, +4.7 points at 5 samples, but its orchestrator consolidated findings rather than taking a pure union ([CRBugBench](https://arxiv.org/html/2610.13668)).

The concrete design runs k=3–5 finders in parallel: Sol with the adversarial prompt, Sol@high, Opus, and optionally one with a coverage prompt. A pure deduplicated union follows, with no vote. Severity is re-derived from category and consequence rather than taken from the model, and that step alone recovers Opus's under-rated catches.

The precision side must not be another LLM opinion. Validators of this kind show a **true-positive rate above 96% but a true-negative rate typically below 25%**, and majority consensus made the true-negative rate worse, at 19.2% ([Beyond Consensus](https://arxiv.org/html/2510.11822v2)). Context shifts a verifier's threshold without improving its discrimination ([arXiv 2608.16003](https://arxiv.org/abs/2608.16003)). That fits the internal results: a verifier that confirms 94%, and a cross-vendor verifier that changed nothing. The strongest discriminator found is an executable witness: in CMU/SEI's adjudication of static-analysis alerts, **no false positive produced a valid trigger**, while 60% of true positives did ([Klieber et al.](https://arxiv.org/html/2607.09979v1)).

The blocking rule therefore has two tiers. A finding blocks if it has a harness-checked witness, or if at least k independent finders produced a semantically equivalent finding in a category whose measured precision at that agreement level is high. Everything else posts as a non-blocking comment. Uber's uReview likewise sets thresholds per category and suppresses categories of historically low value ([Uber](https://www.uber.com/blog/ureview/)).

This keeps the union's recall in the comment channel and limits blocks to the high-precision part. It can be tested on stored trials before anything is spent: would D's three extra clean blocks have been witnessed or agreed?

### C. Make Sol cover the change before it may stop

This is the cheapest lever and the one aimed squarely at early stopping. In CRBugBench's Table 2, a comprehensiveness or exploration-nudging prompt raised gpt-5.6-sol's top-5 recall from **65.6 to 71.3 before merge and from 49.0 to 54.0 after merge**, at roughly the same cost. It gave claude-opus-4.8 +5.5 and +6.0, and opus-5 about nothing ([CRBugBench](https://arxiv.org/html/2610.13668)). This is not the adversarial "assume it's broken" stance. The prompt asks the reviewer to cover every changed function, entry point and caller, and to report every plausible finding, ranked.

Pairing it with a coverage ledger fits the repository's rule that a model's claims are data. Before finishing, the reviewer lists every changed exported symbol with the callers it inspected, every entry point touched and every requirement mapped to code or a test. The engine checks the ledger against the diff deterministically. Evidence-carrying termination of this kind cut premature unsupported stops from 40/66 to 0/66, but only on synthetic tool-use tasks ([arXiv 2608.23623](https://arxiv.org/abs/2608.23623)), so transfer to review is unproven.

One warning: long prescriptive checklists reduced novel findings in Anthropic's harness ([Defending Code](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)), while the internal AGENTS.md checklist gave +6.3. The ledger should list coverage obligations, not bug patterns.

### D. Attack the trust boundaries the diff touches, and let execution only add findings

Security recall is 0/12, and 9 of the 30 misses needed adversarial execution. The probe prompt's −10 points has a documented explanation: it turned reproduction into a filter. AIxCC systems that **verified with a single execution discarded valid proofs of vulnerability for stateful bugs**, while the strong systems kept a separate, gated lane for candidates without proof ([SoK on AIxCC](https://arxiv.org/pdf/2602.07666)). Rigid procedural scaffolding also made two strong models worse on PBT-Bench ([PBT-Bench](https://arxiv.org/abs/2605.15229)).

The positive evidence:

- **Anthropic's Defending Code harness** works in stages: threat model, then partitioned discovery, then a separate verifier. It raised Opus 5.5's recall by **7.7 points on SecPRBench and alone found all 10 concurrency targets**, at about 10× median cost. OpenAI's Codex Security plugin, tuned to abstain, *lowered* recall by 8.3 points ([SecPRBench](https://arxiv.org/html/2610.33509)).
- **Repeated attempts are the cheapest multiplier:** Claude Sonnet 4.5 went from **28.9% with one trial to 66.7% with 30** on CyberGym ([Berkeley RDI](https://rdi.berkeley.edu/blog/cybergym/)).
- **Diff hints were the largest source of wins beyond fuzzing in AIxCC (15/22).** LLMs solved paths guarded by URL encoding, Unicode normalisation and regexes, which is the shape of this repository's redaction misses ([SoK on AIxCC](https://arxiv.org/pdf/2602.07666)).

The design:

1. **Trigger.** An engine-side path map sends redaction, output, sandbox, git-wrapper and classifier changes to a fixed attack catalog.
2. **Attack generation.** Two or three attacker agents, shown the diff and the AGENTS.md trust boundaries but not the PR's own narrative, write fast-check properties and example tests with targeted generators: encoding chains, chunk splits, truncation order, crafted repositories. They run them with `bun test` under `$TMPDIR`. One attacker should hunt sibling paths, enumerating every other caller of each sink a guard touches. Anthropic's GhostScript case was exactly that pattern ([Anthropic](https://www.anthropic.com/research/zero-days)).
3. **Validation that labels and never deletes.** Findings with a witness block only when the harness, not the model, observes the leak in real output, because generated proofs can fake success ([PoC-Gym](https://arxiv.org/html/2602.04165v1)). Everything else stays as a labelled comment.

Two gaps remain. No study evaluates LLM-written fast-check properties, and fast-check's compatibility with Bun was not verified.

### E. Write acceptance tests from the request before reading the diff

Spec mismatch is 0/6, and the literature says why. LLMs judging conformance from text **flag correct code as non-conforming**, and prompts demanding explanations and fixes make it worse ([arXiv 2603.00539](https://arxiv.org/html/2603.00539v1)). They also over-trust misleading PR descriptions ([CRBugBench](https://arxiv.org/html/2610.13668)). The alternative with evidence makes the spec executable. Otter generates fail-to-pass tests from an issue in 31–37% of cases ([Otter](https://arxiv.org/html/2502.05368v2)), e-Otter++ in 52.5–63% ([arXiv 2508.06365](https://arxiv.org/html/2508.06365v3)), and Issue2Test in 32.9% ([ICSE 2026](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/87/Issue2Test-Generating-Reproducing-Test-Cases-from-Issue-Reports)). Meta's intent-aware just-in-time workflow produced catches on 7.9% of diffs against 4.0% for its generic workflow ([arXiv 2601.22832](https://arxiv.org/abs/2601.22832v1)).

The stage reads only the request and its "Out of scope" list and writes acceptance tests, which then run against the PR head. A failure becomes a finding with a reproducer, and a doubtful test becomes a non-blocking spec question. All the evidence is from Python. The slice is small, but no other option touches it.

### F. Push the out-of-diff context instead of hoping the agent fetches it

Thirteen of 30 misses needed files outside the diff, and only 22.8% of industry bugs are visible locally ([CRBugBench](https://arxiv.org/html/2610.13668)). The trace finder, a second agent told to search for callers, lost 3 points, consistent with CRBugBench's mixed results for sub-agents. A precomputed impact pack removes the agent's decision to look. It lists callers of changed exports, sibling implementations of the same interface, migrations and persisted fields touched, and resume entry points, all from rg and tsc references. It costs seconds and opens no new path to findings. No controlled ablation exists, so this is a cheap probe rather than a bet.

### G. Stop losing defects the factory already found

Of 405 orchestrator blocker/major findings, 26 (6.4%) heuristically match an earlier factory *non-blocking* finding on the same PR. Twenty-two of those were rated minor or nit and 4 were majors parked as later-round follow-ups (internal_findings.md). Deriving severity deterministically from category and consequence (data loss, security boundary, crash, wrong result) and ending the parking of non-security majors recovers these at almost no cost. Such a rubric also enables option B's use of Opus. CodeRabbit and Uber both credit category-level gating for their precision ([Uber](https://www.uber.com/blog/ureview/)).

### What the evidence says not to do

The evidence rules out five approaches:

- **Plain majority voting.** Bugbot abandoned it, and its true-negative rate is the worst measured ([Beyond Consensus](https://arxiv.org/html/2510.11822v2)).
- **Multi-round debate.** In VulTrial, one round beat three, and debate traded false-positive rate for recall without improving precision ([VulTrial](https://arxiv.org/html/2505.10961)).
- **A reproduce-or-drop filter on findings.**
- **Long bug-pattern checklists.**
- **Reasoning effort as the only lever at extreme settings.** gpt-5.6-luna went from 36% to 57% detection at 23× cost ([CRBugBench](https://arxiv.org/html/2610.13668)).

Options combine naturally: A with D and G is "the oracle plus execution", and B with C and G is "wide and calibrated".

## No external corpus replaces ours, but four can complement it

None of the public review benchmarks meets all five harness needs (base and head commits, located gold, clean PRs, mappable severity, verification), and none labels this repository's highest-value classes: trust-boundary omissions, one guard on every path, rollback compatibility and check-then-act races.

| Corpus | TS/JS PRs | Gold source and verification | Clean PRs | Fit |
|---|---|---|---|---|
| GitHub ReviewBench (Oct 2026, MIT) | 68 TS + 15 JS of 219 | Pooled; Claude Sonnet 5 judge; seniors agree 96.6% on TP/FP; about 45% of TPs from Copilot, 1.5% from humans | No | Freshest, most TS; base/head mirrors; ~60–80 usable; top grounded recall 26% ([repo](https://github.com/review-bench/ReviewBench); [review](https://agentpatterns.ai/verification/open-code-review-benchmarks/)) |
| SWE-PRBench (Mar 2026) | 21 TS + 37 JS of 350 | Real human review comments; judge κ=0.75 | No | SHAs, no environments; human gold is incomplete ([arXiv](https://arxiv.org/html/2603.26130)) |
| c-CRAB (Mar 2026) | ~0 (Python) | Each comment has a test that fails at head and passes after the fix | No | Only test-verified set; borrow the method ([arXiv](https://arxiv.org/html/2603.23448)) |
| SWR-Bench (FSE 2026) | 0 (Python) | Change-actions linked to fixing commits; SZZ purge; κ=0.66 | **500** | Only set with clean PRs; borrow the method ([arXiv](https://arxiv.org/html/2509.01494v2)) |
| AACR-Bench (Jan 2026) | ~40 (inferred) | Augmented with LLMs and experts (+285% coverage) | No | Read-only alternative ([arXiv](https://arxiv.org/html/2601.19494v2)) |
| SecBench.js (ICSE 2023) | 600 npm vulnerabilities | Exploit payload plus oracle plus Jest test | No | Execution-verified security set for option D ([repo](https://github.com/cristianstaicu/SecBench.js)) |
| Martian / Greptile (Cal.com slice) | 10 | Backtracked historical bugs | No | Tiny; public since 2025 ([Greptile](https://www.greptile.com/benchmarks)) |

ReviewBench's recall partly measures agreement with other LLM reviewers, given how its gold was produced. It is still the best external generalisation check, scored as grounded recall on its TypeScript/JavaScript slice. Published best recall on human-derived sets clusters at 10–32%, against 60–82% on vendor-run sets, so external numbers won't line up with ours in absolute terms.

The highest-yield corpus work is internal, and there are three kinds:

- **Unused orchestrator findings.** Since 10-07 the orchestrator has filed 405 blocker/major findings across 136 PRs that the factory had approved. The generator (`scripts/review-escape-cases.ts`, #833) exists, but the labelling pass hasn't been run. At the past ~50% adjudication yield that is **about 200 more gold defects**, which alone meets the power target. They must go through blind, pooled adjudication rather than being taken as found.
- **Linked escapes.** These are a second kind of gold that doesn't come from the oracle. Mine fix PRs and commits whose text names the PR that introduced the bug, as AGENTS.md already does ("#323 … until #357"). Developer-named links are the high-precision signal: plain SZZ blame reaches only 0.39 precision, and the best variant 0.66–0.73 ([Rosa et al., ICSE 2021](https://arxiv.org/pdf/2102.03300)). Then replay each introducing PR at its original base, as Greptile and Signal65 did ([Greptile](https://www.greptile.com/benchmarks)).
- **A cleaner clean set.** The same SZZ pass, applied to "clean" cases, removes ones that later needed fixes.

Shadow-running a candidate reviewer on live PRs, with its findings adjudicated rather than delivered, builds paired fresh data at the rate of one extra review per PR. The implementer agent may act on anything flagged, so "addressed" rates are confounded and can't serve as labels.

## Conclusion

Most of the reviewer's lost recall is in how it searches and how findings become blocks, not in which model runs it. The oracle that defines the gold is the same Sol model given a plan, high effort and a mutation check, and Opus already finds much of what Sol misses before filing it as minor. Moving model labels, prompts or vendors around without changing procedure, calibration or the blocking rule has been close to a null across seven experiments. Read that way, the history of "nothing adopted" says more about a ruler that under-credits boldness and can't see false blocks than about how much better the reviewer can get.

That suggests an order of work. First come the measurement fixes that cost nothing because they run on stored trials:

- a validated semantic matcher,
- the stored baselines re-scored under it,
- blind adjudication of every clean-case block,
- A/A runs to size the drift.

Next, grow the gold through pooled adjudication of the 405 escapes and linked-escape replays, and freeze a fresh held-out set. Only then run the options as a tournament, paired and interleaved, with the literature's ranking setting only the order of entry. Screen broadly at K=2 on the enlarged dev set and confirm the leaders at K≥4 on the fresh held-out set. Once implementation starts, trials are cheap relative to a wrong adoption, so measurement, not citations, decides. Adopt a variant when the lower bound of its 95% interval clears zero and its point estimate reaches +10, under a pre-registered clean-block margin. Options A, B and D enter the tournament first, for different reasons:

- **A** must be judged on gold that doesn't come from the oracle, because its home-field advantage on oracle gold is real.
- **B** has the strongest internal signal: the Sol and Opus union on stored trials.
- **D** is the only option that touches the 0/12 security slice, which no prompt-only lever has moved.

Which of them, if any, clears +10 is a question for the tournament to answer.
