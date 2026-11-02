# Recall levers for agentic LLM code reviewers (not yet tried by Limitless)

Scope note: research done 2026-10-29. Evidence labels: **[PR]** peer-reviewed venue, **[pre]** arXiv preprint, **[vendor]** vendor blog or vendor-run benchmark, **[2nd]** secondary coverage. Sources after 2026-10-14 are marked **(post-10-14)**. Two 2026 benchmarks anchor most of this: CRBugBench (Microsoft Research, arXiv 2610.13668, 9 Oct 2026, just before the cutoff) and SecPRBench (UIUC, arXiv 2610.33509, 24 Oct 2026, **post-10-14**). **Neither measures precision.** Where they are the only evidence, the precision risk below reads "unmeasured".

Limitless baseline for comparison: 34% blocking-defect recall (46% with the adversarial prompt), about 1.1 findings per review, about 2 of 20 minutes used. Misses: 13/30 needed out-of-diff context, 9/30 needed execution with an adversarial input, 7/30 were visible in the diff. Security 0/12, spec mismatch 0/6.

## Forcing longer or more exhaustive search (continuation, find-N-more, budget forcing, test-time compute; evidence that agents under-explore)

### Takeaway
There is direct 2026 evidence that review agents under-explore and self-censor, and that this varies by model: GPT-family reviewers stop earlier and report fewer findings than Claude. The cheapest measured lever is a "comprehensiveness" or exploration-nudging prompt, which differs from an adversarial prompt: +5 to 6 points top-5 recall for gpt-5.6-sol and opus-4.8 at roughly equal cost, about 0 for opus-5. Separating "report every candidate" discovery from verification is the second strong lever. Reasoning effort helps, but at very high cost, and Limitless already rejected it.

### Cited Findings
- **Agents stop early, and the model matters.** In CRBugBench, half of gpt-5.6-sol review runs end by turn 17 and only 3.5% reach turn 50. Opus-5's half-life is turn 35 [pre] — [CRBugBench, arXiv 2610.13668](https://arxiv.org/html/2610.13668)
- **Agents rarely run code.** About 75% of turns are reading and searching and about 8% are code execution (opus-5 9.7%, gpt-5.6-sol 6.9%) — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Comprehensiveness / exploration-nudging prompt (Table 2):**
  - gpt-5.6-sol: pre-merge top-5 recall 65.6 → 71.3 (+5.6), post-merge 49.0 → 54.0 (+5.0), at "roughly the same cost".
  - claude-opus-4.8: 70.0 → 75.5 (+5.5) and 46.6 → 52.6 (+6.0).
  - claude-opus-5: +0.3 and −1.8.
  - The abstract claims "up to 5.8% at ~10% higher cost". It calls the intervention "exploration-nudging" in one place and "comprehensiveness" in another, and the 5.8 figure doesn't exactly match Table 2 (an internal inconsistency).
  - Conclusion: comprehensive prompting is more cost-effective than multi-agent setups, and its benefit depends on the model [pre] — [CRBugBench](https://arxiv.org/html/2610.13668)
  - The exact prompt text was not in the fetched HTML; the open benchmark repo may have it — [CRBugBench repo](https://github.com/malusamayo/CRBugBench)
- **Reasoning effort:** gpt-5.6-luna went from about 36% (low) to 57% (max) detection at 23.22x cost — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Self-refine** (gpt-5.6-sol reviewing its own review again): +1.4 pre-merge and +3.0 post-merge top-5 recall, at about 2x cost — [CRBugBench Table 3](https://arxiv.org/html/2610.13668)
- **GPT reviewers drop bugs they have already found.** Greptile reports that GPT models "search depth-first and comment less (about 1–2 per review)" and can drop real bugs they have already identified, while Claude models comment about 7–8 times per review. "Adding guidance to target more comments improved its recall" (no number given) [vendor, 21 Jul 2026] — [Greptile, "Models are worse at reviewing their own code"](https://www.greptile.com/blog/model-inversion)
- **Cursor Bugbot reversed its restraint prompt.** After the switch to a fully agentic design, the agent was "too cautious", so prompts were changed to push it to investigate suspicious patterns and flag issues more readily. Bugs flagged per run went from 0.4 to 0.7, and resolution rate from 52% to over 70% across 40 experiments, without a comparable rise in false positives [vendor, 15 Jan 2026] — [Cursor, Building Bugbot](https://cursor.com/blog/building-bugbot)
- **Discovery vs verification.** Anthropic's Defending Code guidance: "Discovery optimizes for recall, verification for precision". Combining them in one agent made agents self-censor real true positives. Unreproducible findings are still reported, flagged as unproven, to keep recall high. Long prescriptive checklists reduced novel findings; goal plus context worked better [vendor, 2026] — [Anthropic defending-code-reference-harness blog post](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)
- **Repeated runs keep finding new bugs.** The same harness says even unchanged code has a long tail of bugs and recommends several loop runs on a first pass — [Defending Code blog post](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)
- **Codex low recall attributed to early termination.** A third-party benchmark measured Codex (GPT-5.5) at 4.92% recall and 27.8% precision on AACR-Bench. The authors guess this is "likely because its single-agent loop terminates early on most PRs", which is a hypothesis, not measured [pre, Aug 2026] — [OpenCodeReview, arXiv 2608.09290](https://arxiv.org/html/2608.09290)
- **Inference budget:** OpenAI's alignment team studied recall against inference budget on previously found bugs. More budget mostly improved calibration and reduced false alarms. Performance fell faster at low thinking budgets when reviewing model-generated code than human code [vendor, 1 Dec 2025] — [OpenAI, A Practical Approach to Verifying Code at Scale](https://alignment.openai.com/scaling-code-verification/)
- **Stop-gate (Evidence-Carrying Termination):** the agent may only declare COMPLETE when a typed certificate ties each required claim to in-scope trace evidence that replays deterministically.
  - Premature unsupported terminations: 40/66 → 0/66, with non-inferior task success (97/132 vs 92/132).
  - Tested on synthetic tool-use tasks, not code review [pre, Aug 2026] — [arXiv 2608.23623](https://arxiv.org/abs/2608.23623)
- **Model output is unstable.** Even unchanged code and harnesses give materially different findings run to run: overdispersion κ≈6.8 across 25,000 vulnerability-detection trials (see the ensembles section) — [Simecek et al., ICML 2026](https://icml.cc/virtual/2026/78010)

### Inferences
- **Limitless's profile matches the documented GPT-reviewer failure mode** (about 1.1 findings, about 2 of 20 minutes used): depth-first search, early stop, self-censorship. The levers below target that specifically and differ from what was tried:
  1. **Comprehensiveness / coverage prompt.** This is not the adversarial "assume it's broken" stance already tried. It asks the reviewer to cover every changed function, entry point and caller before stopping, and to report all plausible findings ranked. Evidence: +5 to 6 points for GPT and opus-4.8, about 0 for opus-5. Expect most of the gain on the Codex reviewer. Cost about 1.0–1.1x. Precision risk: unmeasured in CRBugBench; Bugbot reports no comparable false-positive rise.
  2. **Discovery/verification split with a finding quota.** For example, the reviewer must list at least N candidate defects with confidence before a separate pass filters them, and unproven candidates are kept and marked. This explains, as an inference, why the "reproduce each finding with a probe" prompt may have failed: Defending Code's authors saw exactly that combination suppress true positives. It differs from the multi-finder panel because recall is decided by the finder's candidate list, not by a verifier vote.
  3. **Coverage stop-gate.** The reviewer may only finish once it emits a ledger: every changed exported symbol with its callers inspected, every entry point touched, and every spec requirement mapped to code or test. The engine checks the ledger deterministically against the diff, which fits Limitless's "model claims are data" rule. Evidence of transfer is weak: ECT was tested on synthetic tasks only.
  4. **Self-refine / "find more" second round** in the same session. Modest gain (+1.4 to +3.0) at about 2x cost; cheap in wall time.
- **Ranked shortlist across all sections**, by expected value per evidence quality:
  - (a) coverage/comprehensiveness prompt;
  - (b) model inversion, i.e. a reviewer from a different vendor than the implementer (Q4);
  - (c) recall-tuned discovery plus a separate evidence-backed filter, keeping unproven findings;
  - (d) threat-model-then-partition security pass (Q7);
  - (e) spec-to-acceptance-test step before reading the diff (Q5);
  - (f) a many-sample or model-portfolio union with k≥5, not 2 (Q4);
  - (g) mutation-guided catching tests for the execution bucket (Q2/Q7).

### Gaps
- No public, controlled study found of "keep going" continuation or iterative "find N more" rounds specifically for code review. The closest are CRBugBench's self-refine and the Greptile anecdote.
- Budget forcing (appending a continuation token when the model tries to stop; the s1 paper, arXiv 2501.19393) is known from training data but was not retrieved this session, so its reasoning-benchmark numbers are unverified here and untested for review.
- The CRBugBench comprehensiveness prompt text was not retrieved (not in the fetched HTML portion).
- No source measured the precision cost of the comprehensiveness prompt.

## Decomposition (per-file / per-hunk / per-function, map-reduce, attack-surface enumeration, hypothesize-then-verify)

### Takeaway
Partitioned review with focused sub-agents is mainstream: Defending Code, OpenCodeReview, Qodo 2.0 and Anthropic Code Review all use it. The controlled evidence is mixed. CRBugBench sub-agents lost 3.7 points on one track and gained 6.0 on the other, and per-file dispatch in OpenCodeReview raised precision rather than recall. The best-supported decomposition for recall in security is enumerate attack surfaces → per-partition agents → system-level pass that uses the partition findings.

### Cited Findings
- **Defending Code discovery:**
  - A first pass partitions code by "attack surface, endpoint, or component". Parallel agents search each partition, then a system-level pass runs with partition findings as context.
  - Horizontal scaling gave "limiting returns", and more focus areas produced mostly duplicates [vendor] — [Defending Code blog](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)
  - On SecPRBench, this harness raised Opus 5.5 recall by 7.7 points (on 260 completed pairs) at about 10x median cost. It alone found all 10 concurrency targets (no direct-review agent found more than 6) and found 6 targets that all other agents missed [pre, **post-10-14**] — [SecPRBench, arXiv 2610.33509](https://arxiv.org/html/2610.33509)
- **CRBugBench sub-agents (gpt-5.6-sol):** −3.7 pre-merge and +6.0 post-merge top-5 recall at about 3.5–3.8x cost. Claude Code with opus-5 spawned about 9.0 sub-agents per run and cost much more; the copilot-cli harness with 0 sub-agents outperformed it [pre] — [CRBugBench](https://arxiv.org/html/2610.13668)
- **OpenCodeReview (Alibaba):** rule-guided dispatch, one sub-agent per file with 6 bounded tools and a 30-iteration cap, plus a diff-only reflector that can only filter.
  - Claude-4.6-Opus: P 33.9 / R 20.0, versus Claude Code at P 7.2 / R 28.9.
  - GPT-5.5: R 15.5, versus Codex at R 4.9.
  - No component ablation. The gains are mostly precision, and Claude Code had higher recall in several rows [pre] — [arXiv 2608.09290](https://arxiv.org/html/2608.09290)
- **Diff size and heterogeneity hurt detection** (CRBugBench logistic regression): larger diffs OR 0.591, heterogeneous changes OR 0.795 — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Multi-file spread hurts too:** pooled recall falls from about 70% with one root-cause file to under 40% with five or more (observational) — [SecPRBench](https://arxiv.org/html/2610.33509)
- **Structured semi-formal reasoning** (Meta): a template that forces explicit premises, execution-path tracing and a formal conclusion.
  - Patch equivalence 78 → 88% on curated examples; 93% on real agent patches.
  - Defects4J fault localization top-5 up about 5–12 points (reported inconsistently across versions).
  - Code QA +9 points.
  - About 2.8x more steps. No gain for Sonnet-4.5 on code QA [PR, PLDI 2026 workshop / arXiv 2603.01896] — [arXiv 2603.01896](https://arxiv.org/abs/2603.01896); [PLDI 2026 listing](https://pldi26.sigplan.org/details/page-2026-papers/1/Agentic-Code-Reasoning)
- **Wrong mechanism in the right file:** in 68% of SecPRBench direct-review misses, the agent reported on a root-cause file but argued the wrong mechanism — [SecPRBench](https://arxiv.org/html/2610.33509)
- **Hypothesis falsified by evidence, not voters:** Refute-or-Promote found that 10 reviewers unanimously endorsed a non-existent OpenSSL padding oracle, which only an empirical gate killed. No ablations [pre] — [arXiv 2604.19049](https://arxiv.org/html/2604.19049v1)

### Inferences
- Limitless's trace finder (a second agent told to rg for callers) resembles CRBugBench's sub-agent condition, which was mixed. Decomposition by itself is not a reliable recall lever.
- The decomposition that does help adds coverage obligations plus a synthesis pass: enumerate surfaces (entry points, persisted state, resume paths, auth/sandbox boundaries) → one focused investigation each → a system-level pass that sees all partition notes. That is a different shape from "find callers".
- **For the 68%-style "right file, wrong mechanism" misses,** a semi-formal trace template ("premises → path → conclusion") for each candidate is a cheap within-session lever with peer-reviewed support on adjacent tasks (fault localization, patch equivalence). It has not been tested on review recall.
- Partitioned pipelines cost wall time. Defending Code and Anthropic Code Review run in parallel and keep latency at about 20 minutes (see Q8), which fits a 30-minute cap if partitions run concurrently.

### Gaps
- No controlled study found of per-hunk vs per-file vs whole-diff review recall for frontier agentic reviewers.
- No measured "generate 20 failure-mode hypotheses then check each" study for code review. The closest are Defending Code (no numbers on that step) and Meta JiT tests (Q5/Q7).
- Vulnhuntr-style call-chain tracing and Big Sleep's variant-analysis seeding are known from training data but were not retrieved this session.

## Context engineering (code graph / call graph / data flow, impacted callers, static-analysis hints, LSP)

### Takeaway
"Needs context outside the diff" is the single largest documented predictor of misses: odds ratio 2.6 in favour of diff-visible bugs in CRBugBench, and industry repos have only 22.8% locally visible bugs. Yet no controlled public study isolates code-graph or impacted-caller retrieval as a recall lever for agentic reviewers. Static-analysis-as-hint has peer-reviewed support in security (IRIS), and production reviewers (Copilot, CodeRabbit) feed CodeQL, linters and graphs to the agent.

### Cited Findings
- **Diff visibility:** bugs visible in the diff have OR = 2.621 for detection relative to those needing other context.
  - Only 22.8% of industry bugs vs 46.1% of GitHub bugs are locally visible.
  - Visibility explains about 20% of the GitHub–industry recall gap (up to 25.5% lower on industry repos).
  - Recommendations: "supply repository knowledge", "steer agents with project priorities" — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Failure modes on context:** overtrusting misleading PR descriptions or code comments, and treating the defective code as the standard of correctness — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Repo access and execution:** giving GPT-5 repo access and execution "results in a stronger reviewer" with more critical issues caught and fewer false alarms than diff-only (no numbers) [vendor] — [OpenAI alignment blog](https://alignment.openai.com/scaling-code-verification/)
- **Bugbot moved from static to dynamic context** (the model pulls context at runtime) and found tool design "had a large effect on behavior" [vendor] — [Cursor](https://cursor.com/blog/building-bugbot)
- **IRIS (LLM + CodeQL):** the LLM infers taint specs (sources, sinks, sanitizers) for library APIs, then CodeQL runs.
  - CWE-Bench-Java: 55 vulnerabilities detected vs CodeQL's 27 (v1 claimed 69). Numbers differ by version.
  - False discovery rate is still about 85% [PR, ICLR 2025] — [IRIS, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/582d4e27fa24168f3af1f4582655034b-Abstract-Conference.html); [arXiv 2405.17238](https://arxiv.org/html/2405.17238v2)
- **Snyk VulnBench JS (300 repeated scans):** LLM extra findings varied heavily run to run. Deterministic SAST was better at systematically enumerating repeated data-flow sinks; the authors recommend pairing LLM review with SAST [pre, Jun 2026] — [arXiv 2606.15762](https://arxiv.org/pdf/2606.15762)
- **Copilot code review:**
  - Agentic tool calling gathers repository context (Oct 2025 preview, GA 5 Mar 2026).
  - CodeQL, ESLint and PMD can be enabled as inputs to review (CodeQL on by default per changelog; docs differ on defaults) [vendor] — [GitHub changelog 2026-03-05](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/); [GitHub changelog 2025-11-20](https://github.blog/changelog/2025-11-20-linter-integration-with-copilot-code-review-now-in-public-preview/)
- **CodeRabbit enrichment:** code-graph analysis of the cloned repo plus linter and SAST output, according to an academic description of its pipeline [pre] — [arXiv 2607.03316](https://arxiv.org/pdf/2607.03316). CodeRabbit's own guide calls its context engine the verification layer [vendor] — [CodeRabbit](https://www.coderabbit.ai/guides/what-is-context-engineering)
- **Code-graph tools:** open-source tools such as code-review-graph inject callers and blast radius and report token savings (median 65x), but publish no detection-quality measurement — [instagit summary](https://instagit.com/tirth8205/code-review-graph/how-does-code-review-graph-reduce-token-usage-compared-to-reading-the-full-codebase/)

### Inferences
- Limitless's agent can already rg and read files. CRBugBench suggests the bottleneck is not tool access but the agent choosing to look and stopping too early. A precomputed "impact pack" pushed into the prompt may help more than another agent told to search, because it removes the decision to look:
  - callers of changed exports;
  - sibling implementations of the same interface/route/command;
  - DB columns, migrations and persisted fields touched;
  - resume and restart entry points.
  This is untested; the precision risk is attention dilution.
- **For TypeScript, `tsc` type errors and biome output are already gates.** The additive hints would be:
  - CodeQL JS/TS taint queries or semgrep rules for the project's recurring defects (redaction boundaries, subprocess spawning outside `runProcess`, `sh(["git"...])` in agent-writable checkouts);
  - LSP find-references output for each changed symbol.
  Given IRIS's high false discovery rate, these should be treated as hypotheses for the agent to check, not findings.
- **The overtrust failure mode argues for withholding or de-emphasising the implementer's report** until after the reviewer forms an independent view. That is cheap and plausibly helps spec-mismatch misses (untested).

### Gaps
- No controlled ablation found (with vs without impacted-caller or code-graph context) measuring defect-detection recall for agentic reviewers.
- No evidence found on LSP-based navigation vs grep for review recall.
- No evidence on whether static-analysis hints dilute attention for frontier agents. Snyk and IRIS are vulnerability-detection settings, not PR review.

## Diverse mechanism ensembles (roles, union vs vote, samples vs recall curves)

### Takeaway
Recall from unions grows well beyond what a 2-sample union shows: SecPRBench's 8-agent oracle union reached 91.3% vs 78.1% for the best single agent. Run-to-run variance is overdispersed, so a single negative scan is unreliable. A portfolio of cheaper diverse models reached a high-reliability target far more cheaply than re-running the strongest one. Majority voting and LLM verifiers suppress recall; Bugbot dropped voting when it went agentic. Cross-vendor routing (model inversion) has direct vendor evidence of +2 to 3 points on high-severity bugs.

### Cited Findings
- **Oracle union:** 8 agents found 242/265 (91.3%) vs 78.1% for the best single agent. The top four alone reach about 90%, and 23 targets were missed by all. Single run per agent [pre, **post-10-14**] — [SecPRBench](https://arxiv.org/html/2610.33509)
- **ICML 2026 "Silent Failures"** (50 CVEs filtered for unstable detection, 50 LLMs × 10 runs = 25,000 trials):
  - Overdispersion κ≈6.8.
  - The strongest single-pass model finds an expected 26.7/50 and needs about $41 of repeated scanning to reach ≥45/50 with ≥80% probability.
  - A portfolio of cheap models reaches the same target for under $1 [PR, ICML 2026] — [ICML 2026 #78010](https://icml.cc/virtual/2026/78010)
- **CRBugBench ensembles (gpt-5.6-sol, orchestrator consolidation):**
  - Ensemble@3 same model: +2.4 / +4.6.
  - Ensemble@5 same model: +4.7 / +4.6 at about 5.4–5.6x cost.
  - Ensemble@3 different models: +1.2 / +3.8.
  - The paper also states "+2.8% on average at 3.68x cost" elsewhere (inconsistent). The orchestrator consolidation may itself drop findings; it is not a pure union [pre] — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Human + agent union:** 82.1% vs 71.9% for the best agent alone, so the two are complementary — [CRBugBench](https://arxiv.org/html/2610.13668)
- **Model inversion (Greptile, 1,000 PRs, about 1,500 verified P0/P1 bugs, 3 runs averaged):**
  - Claude-authored PRs: Opus 4.7 60.0% vs GPT 5.5 62.0%.
  - Codex-authored PRs: GPT 5.5 50.5% vs Opus 4.7 53.7%.
  - "Each model tends to miss the same bug categories it most often introduces." Greptile shipped routing to the non-authoring model [vendor, 21 Jul 2026] — [Greptile](https://www.greptile.com/blog/model-inversion)
- **Bugbot v1:** 8 parallel passes with shuffled diff order, then majority voting that dropped single-pass bugs, plus a validator. It later moved to a single agentic loop with a recall-leaning prompt, which was the largest gain [vendor] — [Cursor](https://cursor.com/blog/building-bugbot)
- **Specialist agents vs a generalist harness:** Defending Code's specialised security harness found all 10 concurrency targets vs at most 6 for generalist reviewers — [SecPRBench](https://arxiv.org/html/2610.33509). Its authors also warn that more focus areas produced mostly duplicates — [Defending Code](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)
- **Structured disagreement (reviewer + critic with constrained verdicts AGREE / DISAGREE_EVIDENCE / DISAGREE_CONCERN):** SWE-PRBench F1 0.533 vs 0.503 for two independent reviewers and 0.495 for a single reviewer; the naive version scored 0.457. F1 only, no recall breakdown, about 4.5x tokens [pre, Aug 2026] — [arXiv 2608.18167](https://arxiv.org/html/2608.18167)
- **False consensus:** unanimous LLM reviewers can endorse a non-existent bug — [Refute-or-Promote](https://arxiv.org/html/2604.19049v1)
- **Qodo 2.0:** specialist agents plus a judge that removes duplicates and low-signal items. Self-reported 56.7% recall / 60.1% F1 on its own benchmark [vendor, Feb 2026] — [Qodo blog](https://www.qodo.ai/blog/introducing-qodo-2-0/)

### Inferences
- **Why Limitless's union of 2 samples probably under-tested this lever:** overdispersion and the SecPRBench union curve suggest gains continue past k=2, and model diversity matters more than repetition. A k=4–6 portfolio (Codex sol + Opus + a different reasoning effort or prompt per member), run in parallel, fits the 30-minute budget. Pure union with dedupe and no voting is the recall-maximising aggregator. Precision risk: high, roughly linear in k, unless followed by an evidence-based filter (Q7), not a vote or an LLM opinion verifier.
- **The multi-finder panel was paired with an LLM verifier.** Bugbot's history and Defending Code's self-censorship note both suggest the verifier, not the finders, may have eaten the recall. Worth checking in the eval logs whether finder-level union recall was higher than post-verifier recall (an inference, not established).
- **Model inversion is cheap and different from "a different model".** Check whether the 34% eval had Codex reviewing Codex-implemented PRs, which is the worst cell in Greptile's data (50.5%). Limitless is Codex-first for implementation, so routing review to Opus for Codex-authored PRs (and the reverse) is directly testable.
- **Role specialisation pays off where a domain needs a different procedure,** such as concurrency or security with a threat model, more than as more generic eyes.

### Gaps
- No published head-to-head of union vs majority vote vs evidence-gated filtering on the same review candidates.
- No public recall@k-samples curve for agentic PR review specifically. The ICML and SecPRBench data are vulnerability detection.
- The CRBugBench orchestrator's consolidation logic is not described, so the ensemble numbers may understate pure-union recall.

## Spec/requirement checking that works (requirement-to-code tracing, acceptance tests from the spec)

### Takeaway
Limitless's 0/6 spec-mismatch result matches the literature: LLMs judging conformance from text are unreliable, and more detailed explain-and-fix prompts increase misjudgment. The approach with evidence is to make the spec executable: generate fail-to-pass acceptance tests from the request alone, before reading the implementation, then run them against the PR head. Issue-to-test systems reach about 31–63% fail-to-pass on public benchmarks, and test-based verification filters correct LLM overcorrection.

### Cited Findings
- **LLMs overcorrect on conformance:** they systematically flag correct code as non-conforming. Prompts that require explanations and proposed corrections raised misjudgment rates.
  - Proposed fix: a "Fix-guided Verification Filter" that validates the original and model-revised code against tests and spec-constrained augmented tests [pre, 2026] — [arXiv 2603.00539](https://arxiv.org/html/2603.00539v1)
  - The same bias appears in the earlier [ASE 2025 NIER paper, arXiv 2508.12358](https://arxiv.org/pdf/2508.12358) [PR]
- **Otter (IBM):** generates tests from the issue description plus the original code.
  - Fail-to-pass tests in 31.4% of cases; 37.0% with an ensemble of 5 (Otter++).
  - Used to rank SWE-bench Verified patches at a reported 65–92% precision and 30–41% recall (slide figures) [PR, ICML 2025] — [Otter, arXiv 2502.05368](https://arxiv.org/html/2502.05368v2); [ICML 2025 slides](https://icml.cc/media/icml-2025/Slides/44767.pdf)
- **e-Otter++:** 52.5% fail-to-pass on SWT-bench Lite and 63.0% on TDD-Bench Verified (63% seen via an aggregator) [pre, Aug 2025] — [arXiv 2508.06365](https://arxiv.org/html/2508.06365v3)
- **Issue2Test:** reproduces 32.9% of SWT-bench-lite issues [PR, ICSE 2026] — [ICSE 2026](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/87/Issue2Test-Generating-Reproducing-Test-Cases-from-Issue-Reports)
- **Meta's intent-aware JiT workflow:** generates tests from the diff's stated intent and produced weak catches on 7.9% of diffs vs 4.0% for the "dodgy diff" workflow (see Q7) [pre / FSE 2026 industry submission] — [arXiv 2601.22832](https://arxiv.org/abs/2601.22832v1)
- **Trust in descriptions:** CRBugBench lists overtrust in misleading PR descriptions and comments as a failure mode — [CRBugBench](https://arxiv.org/html/2610.13668)

### Inferences
- **Spec-first acceptance tests.** Before seeing the diff, a step reads only the request/issue (including its "Out of scope" list) and writes acceptance tests. They are run against the PR head in the sandbox, and each failure becomes a candidate finding with a reproducer. This differs from the requirement/entry-point trace finder Limitless tried, because the verdict comes from execution, not from an LLM judging text.
  - Wall-time cost: one generation pass plus targeted test runs, about 5–10 minutes.
  - Precision risk: tests can encode a misreading of the spec. Mitigate by keeping a failing acceptance test as a "spec question" finding when the test itself is doubtful.
- **Requirement-by-requirement ledger as a stop-gate (links to Q1):** each requirement maps to a code location plus a test or probe. Avoid "explain and propose a fix" phrasing, which raised misjudgment in 2603.00539.
- **Hide the implementer's report until the reviewer has checked the spec independently,** to counter overtrust (untested).

### Gaps
- No study found that measures spec-mismatch recall of PR reviewers with vs without generated acceptance tests.
- Issue-to-test results are on Python benchmarks (SWT-bench, TDD-Bench). There is no TypeScript evidence.

## Learning from history (fine-tuning / in-context past findings, lessons memory, reflexion-style reviewers)

### Takeaway
Production systems widely use history: Greptile learned rules (already cited), Gemini Code Assist memory, Qodo's recommendation agent, CodeRabbit Learnings, and past-CVE bug-shape hints. The only quantified signals for recall are vendor anecdotes; no 2025–2026 controlled study isolating project-memory effects on recall was found. The most concrete recall signal is Defending Code's "bug-shape hints from past CVEs" anecdote, plus Big Sleep-style variant analysis (internals not retrieved).

### Cited Findings
- **Bug-shape hints:** one team found 3 exploitable issues in an hour by feeding bug-shape hints from past CVEs. The threat model is bootstrapped from git history and past CVEs. Patch stage includes same-pattern and same-class variant search [vendor] — [Defending Code](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md)
- **But checklists hurt:** long prescriptive checklists reduced novel findings in the same harness — [Defending Code](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md). That is consistent with Limitless's failed item-by-item checklist.
- **Gemini Code Assist memory:** stores rules learned from review interactions and retrieves them before analysis and again to filter draft comments [vendor] — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/memory-for-ai-code-reviews-using-gemini-code-assist)
- **Qodo 2.0:** a recommendation agent draws on past PRs and earlier review feedback [vendor] — [Qodo](https://www.qodo.ai/products/qodo-merge)
- **Self-Evolving Coding Agents survey:** describes converting accepted review comments into persistent instructions and checklists, and notes evaluations should separate memory effects from added search [pre, Aug 2026] — [arXiv 2608.03392](https://arxiv.org/pdf/2608.03392)
- **Agentic code review vision paper:** proposes per-PR review summaries as retrievable repository memory; retention and decay remain open problems [pre, May 2026] — [arXiv 2605.17548](https://arxiv.org/pdf/2605.17548)
- **Retrieval of past review exemplars** improved comment generation (pre-agentic setting) [pre, Jun 2025] — [arXiv 2506.11591](https://arxiv.org/abs/2506.11591)
- **CRBugBench recommends** "steer agents with project priorities" and "supply repository knowledge" (recommendation, not an ablation) — [CRBugBench](https://arxiv.org/html/2610.13668)

### Inferences
- Limitless's recurring-defect list failed as a checklist. The evidence suggests using it differently: retrieve the 2–3 most similar past defects (by touched files/modules and change type) as worked examples, "bug shapes" with the original diff and the miss, rather than enumerating all items. That keeps the goal-plus-context framing Defending Code found works better. Untested; precision risk is low to moderate.
- **Variant analysis.** When a PR touches a module that had a past landed fix, ask "does this change reintroduce or extend that bug class?" This is cheap and directly targets "one guard, every path".
- **Fine-tuning a frontier reviewer is not available** for Codex/Opus via CLI, so in-context use is the only practical route.

### Gaps
- No controlled 2025–2026 study found that measures recall gain from project-specific review memory or reflexion-style lesson accumulation for agentic reviewers.
- Big Sleep's variant-analysis seeding (from previously fixed bugs) is known from training data but not retrieved this session.

## Recent agentic bug-finding systems (Big Sleep / CodeMender, Aardvark / Codex Security, Anthropic security agents, AIxCC, XBOW, Meta, academic multi-agent frameworks): distinguishing features

### Takeaway
High-recall systems share four features:
1. A threat model or attack-surface map built first.
2. Partitioned, fresh-context discovery agents tuned for recall.
3. A separate validator that demands executable evidence (PoC, failing test, sandbox trigger) instead of LLM opinion.
4. Repeated runs.
A security harness is not automatically better: Codex Security lowered recall by 8.3 points vs plain Codex CLI on SecPRBench by abstaining, while Defending Code raised Opus's by 7.7.

### Cited Findings
- **Defending Code (Anthropic reference harness):** threat model (THREAT_MODEL.md via bootstrap plus interview) → sandbox → partitioned parallel discovery with optional PoCs → independent adversarial verifier in a fresh container told to assume a false positive → dedupe by root cause → test-first patch plus variant search.
  - An adversarial verifier roughly halved the non-exploitable rate; requiring a PoC drove false positives to near zero.
  - One team's 40% false-positive rate came from a threat-model mismatch.
  - 1,596 vulnerabilities disclosed by 22 May 2026 [vendor] — [Defending Code blog](https://github.com/anthropics/defending-code-reference-harness/blob/main/docs/blog-post.md); [repo](https://github.com/anthropics/defending-code-reference-harness)
- **SecPRBench harness comparison** (same model, different prompts and budgets):
  - Defending Code: +7.7 recall for Opus 5.5 at about 10x cost.
  - Codex Security plugin: −8.3 recall for GPT-5.6 sol, mostly by abstaining, with fewer findings at about 5x cost.
  - 1-hour timeout, no turn limit [pre, **post-10-14**] — [SecPRBench](https://arxiv.org/html/2610.33509)
- **Aardvark / Codex Security (OpenAI):** threat model → commit-level discovery → validation sandbox that tries to trigger the bug → Codex patch → human review. It reads code, writes and runs tests and uses tools rather than fuzzing. OpenAI claims "high recall" on known and synthetic vulnerabilities but published no figures [vendor, Oct 2025] — [OpenAI, Introducing Aardvark](https://openai.com/index/introducing-aardvark); [The Hacker News](https://thehackernews.com/2025/10/openai-unveils-aardvark-gpt-5-agent.html)
- **XBOW:** a persistent coordinator directs many short-lived agents, "each starting fresh with a narrowly scoped objective", because long-running agents accumulate wrong assumptions. Deterministic validators require objective proof before a finding surfaces [vendor] — [XBOW platform](https://xbow.com/platform); [XBOW assessment guidance, Mar 2026](https://xbow.com/blog/introducing-assessment-guidance)
- **Meta JiT catching tests (FSE 2026 industry submission):** mutation-guided LLM test generators produce tests that fail on the diff but pass on the parent.
  - Across 22,126 generated tests, change-aware methods produced 4x more candidate catches than hardening tests and 20x more than coincidentally failing tests.
  - Rule-based plus LLM-judge-ensemble assessors cut human review load by about 70%.
  - In one subset, 8 of 41 reported issues were confirmed real, 4 of them serious [pre] — [arXiv 2601.22832](https://arxiv.org/abs/2601.22832v1); [InfoQ](https://infoq.com/news/2026/04/meta-jit-testing-ai-detection)
- **Meta semi-formal reasoning** (structured trace certificates) — see Q2 — [arXiv 2603.01896](https://arxiv.org/abs/2603.01896)
- **AIxCC:** Team Atlanta's ATLANTIS won the August 2025 final and documents an LLM component library, agents and an "Ensembler" component combining multiple approaches [pre] — [ATLANTIS report, arXiv 2509.14589](https://arxiv.org/pdf/2509.14589). Trail of Bits' Buttercup placed second — [DEF CON 33 talk transcript](https://media.defcon.org/DEF%20CON%2033/DEF%20CON%2033%20villages%20and%20creators/DEF%20CON%2033%20villages%20and%20creators%20captions/DEF%20CON%2033%20-%20AIxCC%20-%20Buckle%20Up%2C%20Buttercup%20-%20Our%20Experience%20Competing%20in%20AIxCC.eng.txt). AIxCC systems pair LLMs with fuzzing and other dynamic analysis, which applies to C/Java rather than TS PR review.
- **CodeMender (Google DeepMind):** described secondhand as multi-agent, with a critique agent comparing original and modified code and validation via fuzzing, differential testing and SMT solvers [2nd] — [Expert Insights](https://expertinsights.com/news/google-deepmind-unveils-ai-code-agent)
- **Big Sleep:** coverage is outcome-only (about 20 vulnerabilities in FFmpeg, ImageMagick and others; an SQLite bug found before exploitation) [2nd] — [Olhar Digital](https://olhardigital.com.br/2025/08/04/seguranca/google-usa-ia-e-identifica-falhas-de-seguranca-em-softwares/)
- **Run-to-run variance in practice:** a single researcher's repeated o3 runs on ksmbd found the known bug in 8/100 runs and a new zero-day (CVE-2025-37899) in some runs, with many false positives [2nd, May 2025] — [Linuxiac](https://linuxiac.com/chatgpt-o3-model-found-remote-zeroday-in-linux-kernel-code/); [Habr](https://habr.com/ru/post/912940)

### Inferences
- **Limitless's 0/12 security result maps onto SecPRBench's main failure** (68% wrong mechanism in the right file) and onto the absence of a threat model. A security sub-pass is the plausible fix:
  1. read the base-commit threat model, i.e. AGENTS.md trust boundaries (Seatbelt, redaction, `worktreeGit`, untrusted PR config);
  2. enumerate which boundaries the diff touches;
  3. one fresh-context agent per touched boundary, required to produce a probe (canary read, credential string through the redaction path);
  4. keep unproven findings marked.
  This differs from the adversarial prompt and from the checklist because the scope comes from a threat model and the evidence is executable.
  - Cost: Defending Code ran at about 10x the median cost of direct review; with partitions in parallel it should still fit about 20–30 minutes.
  - Precision risk: low if a PoC is required for "blocking" severity, higher for kept unproven items.
- **For the 9/30 execution-needed misses,** Meta's JiT pattern adapts well to TS with `bun test`: generate tests that pass on the base and fail on the head (behavioural deltas), then classify each delta as intended or a bug against the spec. Precision depends on the assessor; Meta needed a judge ensemble.
- **A security harness can lower recall** (Codex Security −8.3) if it is tuned to abstain. Any adopted security pass must be measured on Limitless's eval, not assumed.

### Gaps
- No primary architecture write-up retrieved for Big Sleep or CodeMender; details above are secondary.
- ATLANTIS and Buttercup lessons for LLM-only (no fuzzer) review were not extracted; the report PDF text wasn't retrieved.
- Aardvark's recall figures are not published.
- XBOW's "zero false positives over 1,060 attacks" claim was seen only secondhand and is unverified.

## What production AI reviewers disclose (architectures and measured recall)

### Takeaway
Vendors disclose architecture qualitatively and precision-flavoured metrics (resolution rate, percent incorrect, addressed comments). Recall numbers come from vendor-run or shifting third-party benchmarks and aren't comparable. Common architecture as of 2026:
- an agentic tool-calling loop (Bugbot, Copilot, Greptile v4, Codex);
- parallel specialists plus a verifier or judge (Anthropic Code Review, Qodo 2.0, CodeRabbit);
- depth scaled to PR size;
- static analysis and graphs as inputs.

### Cited Findings
- **Anthropic Claude Code Review** (research preview, 9 Mar 2026): a team of parallel agents, a verification step to filter false positives, severity ranking, and depth that scales with the PR (more agents for large PRs).
  - PRs over 1,000 lines: 84% get findings, averaging 7.5 issues. PRs under 50 lines: 31%, averaging 0.5.
  - Under 1% of findings marked incorrect. Substantive review comments rose from 16% to 54% of PRs.
  - About 20 minutes and $15–25 per review. No recall figure [vendor] — [Claude blog](https://claude.com/blog/code-review)
- **Cursor Bugbot:** v1 used 8 shuffled passes, voting and a validator; from fall 2025 an agentic loop with a recall-leaning prompt and dynamic context. Resolution rate 52% → over 70%; 0.4 → 0.7 bugs per run; over 2M PRs per month [vendor] — [Cursor](https://cursor.com/blog/building-bugbot)
- **OpenAI Codex review:** precision-first ("modestly reduced recall" accepted). It comments on 36% of Codex-generated PRs, and authors change code in response 52.7% of the time; over 100k external PRs per day (Oct 2025). Repo access, execution and dedicated training improve recall and precision; precision/recall is steerable via AGENTS.md [vendor] — [OpenAI alignment blog](https://alignment.openai.com/scaling-code-verification/). Third-party AACR-Bench measured Codex at 4.9% recall — [OpenCodeReview](https://arxiv.org/html/2608.09290)
- **Greptile v4** (5 Mar 2026): multi-hop investigation (dependencies, git history). Headline gains were 74% more addressed comments per PR and 68% more positive replies, an accuracy focus. Martian bench snapshot via Greptile: P 76.2 / R 50.6 / F1 60.8 [vendor] — [Greptile Martian page](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark); [Greptile changelog](https://www.greptile.com/changelog). Model inversion, routing to the non-authoring model — [Greptile](https://www.greptile.com/blog/model-inversion)
- **CodeRabbit:** per-review code graph, linters and SAST in enrichment, a "Learnings" knowledge base, and an independent-verifier framing — [arXiv 2607.03316](https://arxiv.org/pdf/2607.03316); [CodeRabbit guide](https://www.coderabbit.ai/guides/what-is-context-engineering)
- **GitHub Copilot code review:** agentic tool calling for repository context (GA 5 Mar 2026), plus CodeQL, ESLint and PMD as configurable deterministic inputs [vendor] — [changelog](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/)
- **Qodo 2.0** (Feb 2026): specialist agents, a judge for dedupe and low-signal filtering, and history-aware recommendations; self-reported recall 56.7% [vendor] — [Qodo](https://www.qodo.ai/blog/introducing-qodo-2-0/)
- **Third-party leaderboards are unstable.** Martian Code Review Bench snapshots variously rank Cubic, Greptile, Copilot and CodeRabbit around 61–66% F1, with recall around 50% for Greptile. Ranks shift by snapshot, and other vendor-run benchmarks disagree [2nd] — [aicodereviews.io on Martian](https://www.aicodereviews.io/blog/martians-code-review-bench-the-1-claim-rots-in-months/); [Entelligence benchmark](https://entelligence.ai/code-review-benchmark-2026)
- **Graphite Diamond, Sourcery, Ellipsis and Baz:** no architecture or recall disclosures retrieved this session. Baz has an "anatomy of code review accuracy" article that was not fetched — [Baz](https://baz.co/resources/the-anatomy-of-code-review-accuracy)

### Inferences
- **Depth that scales with PR size** (Anthropic) is a cheap policy lever. Limitless uses about 2 of 20 minutes regardless of PR, while CRBugBench shows larger and heterogeneous diffs and multi-file bugs are where recall collapses. A size- or risk-triggered escalation (partitioned security pass, ensemble k, acceptance tests) targets spend where misses concentrate.
- **Anthropic's about 20-minute reviews and opus-5's about 9.8-minute CRBugBench runs** suggest a 30-minute cap fits a parallel multi-agent design, not just a single session.
- **Vendors that went agentic all reported reining in over-caution** (Bugbot) or tuning for precision (Codex). Limitless's Codex reviewer likely inherits Codex's precision-first post-training, which an explicit recall-target instruction in the prompt or AGENTS.md can partly counter, per OpenAI's own "steerable" note.

### Gaps
- No vendor publishes recall on a held-out, independent, bug-verified set. CRBugBench (Microsoft Research) is the closest independent recall benchmark but evaluates raw harnesses (copilot-cli, claude-code), not vendor products.
- Graphite Diamond, Sourcery, Ellipsis and Baz architectures were not retrieved.
