# Precision decision layer for LLM code review: turning many candidate findings into few, accurate blocks

Evidence-strength tags: **[peer]** = peer-reviewed venue; **[preprint]** = arXiv, not yet reviewed; **[vendor]** = vendor self-report; **[snippet]** = taken only from a search-result summary, full text not fetched, so unverified. Research date: 2026-10-29.

## 1. LLM-as-judge for bug reports: what makes judges discriminate, and why verifiers confirm everything

### Takeaway
The 94%-confirm / 2%-refute verifier is the documented failure mode of LLM validators: high TPR and very low TNR ("agreeableness bias"). Plain majority voting makes it worse. A minority veto helps a little, and a regression calibration fit on a small labeled set helps most. Verbalized confidence barely beats chance at ranking errors. The strongest discriminator found is an executable trigger or witness: no false positive produced one, but it confirms only about 60% of true positives.

### Cited Findings
- **Agreeableness bias, measured on code-feedback validation.** 14 LLMs judged whether generated feedback on buggy student Python programs was valid (366 submissions, 69 assignments, human-labeled). Across most validators TPR was >96% and TNR typically <25%. The best TNR was Gemini 2.5 Pro at 53.5%, with the lowest TPR (83.8%). [preprint, rev. Dec 2025] — [Beyond Consensus, arXiv 2510.11822](https://arxiv.org/html/2510.11822v2)
- **Ensembles in the same paper.**
  - Majority consensus reached TNR 19.2%, worse than many single validators.
  - "Minority Veto" (mark invalid if ≥4 of 14 validators say invalid) reached TPR 95.5% and TNR 30.9%.
  - The veto threshold itself needs labeled calibration data.
  - A regression calibration jointly estimates generator precision and validator TPR/TNR from human-labeled anchors. It cut max absolute error to 1.2% with 5 labeled generator sets, about 2x better than the best 14-LLM ensemble; with 0 labeled sets the error was 15.8%.
  - Labeling cost was about 200 person-hours for 6 generators. The authors' advice: correcting for low TNR is critical. — [arXiv 2510.11822](https://arxiv.org/html/2510.11822v2)
- **Weighted judge voting without labels.** Weighting each judge's vote by its false-positive and false-negative rates, estimated from inter-judge disagreement patterns without ground truth, is proposed. The same paper finds that judges are more lenient toward more capable examinee models. [preprint, Sep 2026; abstract-level only] — [Can We Trust LLM Judges, arXiv 2609.12002](https://arxiv.org/abs/2609.12002)
- **Context shifts the verifier's threshold, not its discrimination.**
  - Setup: identical checking task on human-verified-correct ProcessBench traces; a prior audit-then-repair episode in context was compared with a length-matched control.
  - The prior episode lowered false alarms in 15/15 model × wording combinations, by 2.8–11.5 pts (9–25% relative).
  - Signal-detection analysis: the criterion moved in all 15 combinations (13 survive correction); d′ (discrimination) did not change significantly in any. The effect held with reasoning enabled. [preprint, Aug 2026] — [arXiv 2608.16003](https://arxiv.org/abs/2608.16003)
- **Executable trigger test as a witness.**
  - CMU/SEI adjudicated static-analysis alerts. The LLM writes a driver that triggers the flaw under sanitizers; a separate validity check rejects drivers that only succeed by violating preconditions.
  - On 76 FormAI alerts, **no false positive produced a valid trigger**, and the test confirmed 18/30 true positives (60%). The sample is small. [preprint, Jul 2026] — [Klieber et al., arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- **Self-consistency with abstention (same paper).**
  - Consistency check: run the query N=10 times; return the majority verdict only if it reaches a threshold (e.g. 80%), else "uncertain", which routes to a human.
  - LLM reasoning evaluation (LRE): for non-unanimous alerts, show the model the discordant rationales and ask for a verdict.
  - With mitigation, o4-mini, gpt-oss-120b and gpt-oss-20b reached ≥98% recall and ≥94.8% specificity on every suite.
  - Examples: o4-mini on Juliet with CC@80%: 99.0% recall, 99.0% specificity. gpt-oss-20b on FormAI with LRE+CC@80%: 99.4% recall, 98.4% specificity; uncertain verdicts on true alerts fell from 29.8% (CC alone) to 7.1%. Frontier models (gpt-5.4, gpt-5.5, opus-4.8) were near-perfect on FormAI with CC alone.
  - Plain majority vote is the baseline the authors reject, because it never abstains. — [arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- **Agentic verification with repository access beats vanilla prompting for false-positive filtering, with strong backbones only.**
  - On post-cutoff OSS-Fuzz C/C++, SWE-agent + Claude Sonnet 4 identified 95.5% of false positives at 95.5% precision, against 36.4% for vanilla prompting.
  - On the OWASP Benchmark, the false-positive detection rate went from >92% down to as low as 6.3% in the best configuration (as stated in the abstract).
  - Gains with weaker backbones were limited or inconsistent, and aggressive false-positive reduction sometimes suppressed true vulnerabilities (TP-loss numbers are not in the abstract). [peer: ISSTA 2026] — [Sifting the Noise, arXiv 2601.22952](https://arxiv.org/abs/2601.22952)
- **Sycophancy under rebuttal.** Models readily concede to user counterarguments and are less likely to revise correct answers than incorrect ones. [peer: Findings of EMNLP 2025; snippet] — [Challenging the Evaluator](https://aclanthology.org/2025.findings-emnlp.1222.pdf)
- **Verbalized confidence is a weak ranker.**
  - Verbalized-confidence AUROC for error detection is around 0.6–0.7 (GPT-4 about 62.7%).
  - In a review-style workflow, a learned calibrator reached AUPRC 0.867 against 0.576 for verbalized confidence.
  - Answer-token logprobs were anti-calibrated on some Qwen judge models (AUROC 0.32–0.49).
  - [snippet, mixed sources] — [Know When You're Wrong, arXiv 2603.06604](https://arxiv.org/pdf/2603.06604); [VERDI, arXiv 2605.11334](https://arxiv.org/html/2605.11334v1); [Calibrating LLMs Using Their Generations Only, arXiv 2403.05973](https://arxiv.org/pdf/2403.05973)
- **The opposite bias also exists.** LLMs verifying code against natural-language specs show "over-correction": correct implementations are misjudged as non-conforming more often as prompt complexity rises. [preprint, 2025; snippet] — [arXiv 2508.12358](https://arxiv.org/pdf/2508.12358)
- **Path-feasibility checking.** LLM + SMT path-feasibility checking filtered 72–96% of static-analysis false alarms while keeping recall 0.93 (42/45 true bugs). [preprint; snippet] — [LLM4PFA, arXiv 2506.10322](https://arxiv.org/pdf/2506.10322)

### Inferences
- The verifier's 94% confirm rate is consistent with a TPR≈96% / TNR<25% validator. Asking the same kind of model "is this real?" again, even cross-vendor, mainly moves the criterion. That matches the observation that cross-vendor verification "only shifted the severity level", and 2608.16003's finding that context moves the criterion but not d′. **Score verifier variants with signal detection (d′ and criterion) on labeled findings, not by confirm rate.** A variant that changes only the criterion is a threshold knob, not a better discriminator.
- Judging the claim produces leniency. Asking the model to produce an artifact that can fail (a trigger, a concrete failing input, a failing test whose failure is checked against the claimed behavior) is the only intervention found with a clean precision signal.
- If a judge is used at all, the evidence favors these, in order:
  1. Calibrate it against a small labeled set and set the threshold from that.
  2. Use veto or abstain logic, not majority vote.
  3. Give it repository and tool access (agentic), not a code excerpt.
- Do not use raw verbalized confidence as the blocking threshold.

### Gaps
- No study found tests pairwise comparison (finding A vs finding B) as a discriminator for code-review findings.
- No study found compares logprob-based scores and verbalized confidence specifically for code-review findings with frontier models.
- The trigger-test result (0 false-positive witnesses, 60% TP coverage) comes from 76 C alerts on synthetic suites. It is unknown whether it transfers to TypeScript, concurrency, or design-level defects in real PRs, where witnesses are harder to write.

## 2. Multi-agent debate and adversarial verification (prosecutor/defender) for code findings

### Takeaway
Debate is not a precision win in the best peer-reviewed evidence. VulTrial raised recall at the cost of FPR. The defensible claims are narrower: a dedicated defense role reduces false accepts, and one round beats several. Evidence-grounded dialectics beat speculative debate, and unanimous agent confirmation can still be wrong.

### Cited Findings
- **VulTrial (ICSE 2026)** uses a prosecutor (security researcher), a defense (code author), a moderator and a review board, all on the same model, on PrimeVul pairs (435 test pairs).
  - GPT-4o: VulTrial P 0.53 / R 0.60 / FPR 0.52, against single-agent CoT P 0.53 / R 0.19 / FPR 0.17, and GPTLens multi-agent P 0.51 / R 0.65 / FPR 0.62.
  - GPT-3.5: VulTrial P 0.51 / R 0.25 / FPR 0.23; GPTLens R 0.94 / FPR 0.95.
  - Precision was flat. Debate traded FPR for recall. [peer: ICSE 2026] — [VulTrial, arXiv 2505.10961](https://arxiv.org/html/2505.10961)
- **VulTrial ablations (moderator-tuned GPT-4o).**
  - Removing the defense agent took correctly-identified pairs from 96 to 63 and raised "both flagged vulnerable" pairs from 154 to 277; the board "accepts researcher-identified vulnerabilities too often".
  - Removing the moderator dropped correctly-identified pairs to 32.
  - Rounds: 1 round gave 96 correct pairs, 2 rounds 87, 3 rounds 81. More rounds made the system more suspicious; one round was best. — [arXiv 2505.10961](https://arxiv.org/html/2505.10961)
- **Refute-or-Promote** (already cited by the requester): the adversarial track achieved about a 79% retrospective kill rate. A unanimous multi-agent confirmation was a false positive (a nonexistent OpenSSL vulnerability), which led the authors to add a rule. [preprint] — [arXiv 2604.19049](https://arxiv.org/html/2604.19049)
- **Aegis** argues for evidence-based dialectics grounded in a code property graph over speculative debate, and reports that more debate rounds can worsen results. [preprint; snippet] — [arXiv 2603.20637](https://arxiv.org/pdf/2603.20637)
- **VulAgent** turns each report into a hypothesis checked against code context and reports about 36% lower false-positive rate. [preprint; snippet] — [arXiv 2509.11523](https://arxiv.org/pdf/2509.11523)
- **MultiVer** had an 85% false-positive rate on patched code: the model could not tell a vulnerable function from its near-identical fixed version. [preprint; snippet] — [arXiv 2602.17875](https://arxiv.org/html/2602.17875)

### Inferences
- If prosecutor/defender is tried, use a single round, with the defender given the repository and an explicit mandate to find the precondition or guard that makes the finding impossible. Make the judge's decision depend on evidence the defender could not rebut (a cited line, a trigger), not on rhetorical balance.
- The MultiVer patched-code result is directly relevant to clean PRs. A clean PR is often the "fixed version" of code a model expects to be buggy. Same-family models share that blind spot, which helps explain why union-of-samples adds false blocks on clean PRs.
- Do not treat unanimity as evidence of truth. Refute-or-Promote's unanimous false positive and the agreeableness bias above both say so.

### Gaps
- No study found applies prosecutor/defender to general PR review (not vulnerability classification) with frontier agentic models and reports precision on clean PRs.

## 3. Learned filters and rankers on finding features; vendor "addressed rate" models

### Takeaway
Production systems with published numbers converge on the same design. A cheap grader scores each finding. Thresholds are set per category, language and assistant from developer feedback. Historically low-value categories are suppressed. Rules or filters are learned from reactions. "Addressed" is the main online metric, and it is LLM-judged and vendor-reported. No vendor publishes precision on clean PRs.

### Cited Findings
- **Uber uReview** [vendor, Aug 2025] — [Uber blog](https://www.uber.com/blog/ureview/)
  - Pipeline: generate (Standard, Best-Practices and AppSec assistants), then a secondary grading prompt with a confidence score, then a semantic-similarity dedup, then a category classifier (e.g. "correctness:null-check") that suppresses categories with historically low developer value.
  - Confidence thresholds are set **per assistant, per language and per comment category** from developer feedback and evaluations.
  - "Addressed" is measured by rerunning the review 5 times on the final commit: a comment counts as addressed if no rerun reproduces a semantically similar one.
  - About 75% of comments are rated useful, and over 65% are addressed (against 51% for human comments).
  - Best pairing: Claude 4 Sonnet as generator, o4-mini-high as grader.
- **ByteDance BitsAI-CR**: a RuleChecker followed by a fine-tuned ReviewFilter reached 75.0% precision, with 12,000+ weekly active users. [preprint/industry, Jan 2025; already cited by requester] — [arXiv 2501.15134](https://arxiv.org/pdf/2501.15134)
- **Meta MetaMateCR**: an LLM actionability classifier reached precision 0.81 and recall 0.92 for the actionable class. [preprint, Jul 2025; snippet] — [arXiv 2507.13499](https://arxiv.org/html/2507.13499v1)
- **Cursor Bugbot** [vendor, Apr 2026] — [Cursor blog](https://cursor.com/blog/bugbot-learning)
  - Resolution rate is 78.13% over 50,310 PRs, up from 52% at launch in July 2025. It is defined as flagged bugs resolved by merge, judged by an LLM, on public repositories only.
  - Cursor's comparison table: Greptile 63.49%, CodeRabbit 48.96%, Copilot 46.69%, Codex 45.07%, Gemini Code Assist 30.93%.
  - Learned rules: downvotes, replies and human-flagged misses become candidate rules, which are promoted as signal accumulates and disabled on consistent negative signal. Over 44,000 rules have been generated across 110,000+ repositories.
- **Greptile**: addressed rate rose from 30% to 43% (Agent v4, LLM-judged). [vendor, LinkedIn; snippet] — [LinkedIn post](https://www.linkedin.com/posts/dakshg_today-were-releasing-greptile-agent-v4-activity-7435353275857743872-7idK)
- **CodeRabbit**: signal-to-noise dipped at wider rollout because users found reviews pedantic. Fixes were severity tagging, stricter refactor gating and better filtering; it reports 46.3% per-comment precision for GPT-5 Codex. [vendor; snippet] — [CodeRabbit on dev.to](https://dev.to/coderabbitai/gpt-5-codex-how-it-solves-for-gpt-5s-drawbacks-2nbp)
- **Qodo**: "Relevance" scores each finding by how similar findings were handled in past PRs. Qodo notes that vendors report false discovery rate (1 − precision) while calling it "false positive rate". [vendor; snippet] — [Qodo](https://www.qodo.ai/?p=22524)
- **Other vendor claims, not comparable** [vendor; snippet]:
  - Graphite claims a 5–15% false-positive range for the best systems — [Graphite guide](https://graphite.com/guides/ai-code-review-false-positives).
  - kluster.ai's own benchmark claims false-positive rates of 22.5% for itself, 41.3% for CodeRabbit, 43.5% for Bugbot and 45.7% for Greptile — [kluster.ai](https://kluster.ai/blog/code-review-benchmark).
- **CR-Bench (Nutanix)**: on 174 verified instances, single-shot GPT-5.2 reached recall 27.0%, precision 3.56% and SNR 5.11. Reflexion raised recall to 32.8% but cut SNR to 1.95; Reflexion with GPT-5-mini fell to SNR 0.91. Pushing agents to find everything trades directly against SNR. [preprint, Mar 2026] — [arXiv 2603.11078](https://arxiv.org/html/2603.11078v1)
- **Calibrator vs raw confidence**: a learned calibrator beat verbalized confidence (AUPRC 0.867 vs 0.576). [snippet] — [arXiv 2603.06604](https://arxiv.org/pdf/2603.06604)

### Inferences
- The low-cost, evidence-backed version of a learned filter for the factory: log every candidate finding with its features and an outcome label (fixed by the author, rebutted, or adjudicated real or false), then fit per-category blocking thresholds. Features: category, reviewer and model, number of independent samples that produced a semantically equivalent finding, whether a witness exists, whether the cited lines are in the diff, and grader score.
- uReview's "rerun N times on the final commit; addressed = no longer reproduced" is a free, automatic label source that fits a factory with follow-up rounds.
- Treat vendor addressed rates as LLM-judged, public-repo-only and non-comparable. Several are false discovery rates mislabelled as false-positive rates.

### Gaps
- Nothing found for Baz, Ellipsis or Sourcery with numbers.
- No vendor publishes precision or false-block rate on PRs known to be clean. Addressed rate measures accepted comments, not false blocks avoided.
- No public study found trains a lightweight classifier (e.g. gradient boosting) on finding features such as agreement count or file churn for LLM review findings and reports precision/recall. BitsAI-CR fine-tunes an LLM filter instead.

## 4. Severity calibration: deterministic severity, category-to-blocking rules, two-tier designs

### Takeaway
The evidence supports a two-tier design. Block only on findings backed by a witness or calibrated agreement in categories whose historical precision is high; post everything else as non-blocking comments or route it to human or abstain. The production systems with numbers (uReview, CodeRabbit, CMU's abstain path) all separate "post or comment" from "high-confidence act" and set thresholds per category.

### Cited Findings
- CMU's consistency check returns "uncertain" (abstain to a human) when agreement is below threshold. That is an explicit third state between true and false positive, and it is how they reach ≥98% recall with ≥94.8% specificity. — [arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- uReview suppresses whole categories with historically low developer value and sets thresholds per category, language and assistant. — [Uber blog](https://www.uber.com/blog/ureview/)
- CodeRabbit attributes its signal-to-noise recovery partly to severity tagging and stricter gating of refactor suggestions. [vendor; snippet] — [dev.to](https://dev.to/coderabbitai/gpt-5-codex-how-it-solves-for-gpt-5s-drawbacks-2nbp)
- Bugbot deliberately avoids commenting on style, formatting and low-severity concerns, and shows per-rule acceptance rates. [vendor; snippet] — [aicodereview.cc on Bugbot](https://aicodereview.cc/tool/cursor-bugbot)
- In CR-Bench, low-severity defects have the lowest recall, and memory-bug recall was zero for all agents. Category-level recall varies a lot, so per-category thresholds matter. — [arXiv 2603.11078](https://arxiv.org/html/2603.11078v1)

### Inferences
- A blocking rule consistent with the evidence:
  - **Block** if (a) the finding has a valid executable witness (a failing test or trigger on the PR head that passes on base, or fails for the stated reason, with a validity check against precondition abuse), **or** (b) its category's measured precision at the current agreement level k is above the target.
  - Otherwise **comment** (non-blocking).
- Severity should be derived deterministically from category plus consequence (data loss, security boundary, crash, wrong result vs. maintainability), not from the model's "blocker/major" label. Asking the model's own severity just moves the criterion (see 2608.16003), which matches the cross-vendor verifier result.
- "Would you bet" framing is a verbalized-confidence intervention. The evidence suggests verbalized confidence ranks errors poorly (AUROC around 0.6–0.7) unless calibrated.

### Gaps
- No controlled study found compares deterministic consequence rubrics with model-assigned severity for blocking decisions in code review.
- No study found evaluates "would you bet" or wager framing for code findings.

## 5. Using agreement across independent samples or models without majority-vote recall loss

### Takeaway
Agreement is a usable signal when it is a threshold with an abstain path (CMU), a minority veto (Beyond Consensus), or a calibrated weighted vote. Plain majority vote is the worst option on both recall and TNR. Same-family samples share blind spots and can agree unanimously on a false positive, so agreement should be calibrated per category, not trusted as is.

### Cited Findings
- Majority consensus of 14 validators had TNR 19.2%, worse than the best single validators. Minority Veto at n=4 of 14 reached TPR 95.5% and TNR 30.9%. — [arXiv 2510.11822](https://arxiv.org/html/2510.11822v2)
- The consistency check (N=10, 80% threshold, else abstain) plus LRE for non-unanimous cases reached ≥98% recall. Plain majority vote has no abstain and no threshold to trade off errors. — [arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- Weighted voting, with each judge weighted by its false-positive and false-negative rates estimated from disagreement patterns, needs no labels. — [arXiv 2609.12002](https://arxiv.org/abs/2609.12002)
- uReview treats "reproduced across 5 reruns" as the signal that an issue persists, which is agreement used as a label, not as a vote. — [Uber blog](https://www.uber.com/blog/ureview/)
- A unanimous multi-agent confirmation was a false positive. — [Refute-or-Promote, arXiv 2604.19049](https://arxiv.org/html/2604.19049)
- Bugbot v2 dropped majority vote (already cited by the requester; not re-fetched).

### Inferences
- A recall-preserving union rule: **block if any sample produces a witnessed finding, or ≥k of n independent samples produce a semantically equivalent unwitnessed finding in a category whose calibrated precision at k is high. Otherwise comment.** This keeps the union's recall in the comment channel and restricts the blocking channel to the high-precision part.
- The union of two adversarial samples gave +17 pts recall and +3 false blocks out of 26. Under this rule those 3 extra blocks would block only if witnessed or agreed. Whether they would have been is directly testable on the stored trials.
- LRE (show the judge the conflicting rationales only when samples disagree) is a cheap, targeted use of a second call, compared with verifying every finding.

### Gaps
- No study found reports the exact precision/recall of "any-witnessed OR k-agree" against union and majority on PR review. It has to be measured on the factory's own data.

## 6. Evaluating the precision side robustly given noisy "clean" labels

### Takeaway
Report recall and specificity (prevalence-independent) with exact confidence intervals. Convert to precision at operational prevalence. Adjudicate every false block blind, because ground truth is regularly revised once a model or witness exposes a missed defect. At current sample sizes the false-block differences being measured are inside the noise.

### Cited Findings
- **Report prevalence-independent metrics.** Recall and specificity should be the primary metrics, and precision should be computed at operational prevalence. Example: o4-mini precision is about 97% at the benchmark's 64% prevalence but about 68% at 10% prevalence. Use 99% Clopper–Pearson intervals. — [arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- **Ground truth is fallible.** Several manual adjudications were revised after LLM reasoning or trigger results exposed errors. o4-mini could reconstruct sanitized Juliet filenames (memorization), so generalization claims rested on unpublished in-house adjudications. — [arXiv 2607.09979](https://arxiv.org/html/2607.09979v1)
- **Labeling protocol and agreement.** Two independent labelers with discussion-based resolution built a 100-comment gold set. Test-quality agreement between two authors was 84% on 50 instances; disagreements came from partial coverage and tests overfit to an implementation. Executable tests were used instead of LLM judges for scoring because judges are biased and unstable. [preprint, Mar 2026] — [Code Review Agent Benchmark, arXiv 2603.23448](https://arxiv.org/html/2603.23448v2)
- **Consensus is not ground truth.** Blind expert verification is preferred over human-consensus labels when consensus is not ground truth. [preprint; title-level only] — [Agreement Is Not Quality, arXiv 2607.28890](https://arxiv.org/pdf/2607.28890)
- **Calibration needs labels.** The regression calibration needed human labels (about 200 person-hours for 6 generators), and with no labels the error was 15.8%. — [arXiv 2510.11822](https://arxiv.org/html/2510.11822v2)
- **Judges can drift by examinee.** Judges are more lenient toward stronger examinee models, which biases comparisons across models. — [arXiv 2609.12002](https://arxiv.org/abs/2609.12002)

### Inferences
- My own computation, not from a source: 3 false blocks in 26 clean trials is 11.5%, with a 95% Clopper–Pearson interval of about 2.4%–30%. A +3/26 difference cannot be separated from noise at this sample size. The earlier audits found that 6/19 and 12/17 "false blocks" were real defects, so the measured false-block rate is itself biased upward by mislabelled "clean" PRs.
- A protocol consistent with the sources:
  1. Every block on a "clean" PR goes to blind adjudication (the adjudicator does not know which arm produced it) by two raters plus a tie-break, or by an executable witness where one can be produced.
  2. Relabel the PR if the defect is real.
  3. Report specificity with Clopper–Pearson intervals before and after adjudication.
  4. Convert to precision at the factory's real prevalence of defective PRs.
  5. Keep a frozen held-out clean set that has been adjudicated.
- Score verifier changes with signal-detection metrics (d′ and criterion) on adjudicated findings, so a threshold shift is not mistaken for better discrimination (2608.16003).

### Gaps
- No standard adjudication protocol for "clean PR" labels in LLM code review was found. The protocols cited come from adjacent benchmark-construction work.
- No study found estimates the label-noise rate of "clean" PR sets in public code-review benchmarks.
