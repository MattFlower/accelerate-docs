# External defect-labelled corpora for evaluating an LLM code reviewer

Research date: 2026-10-29. "Peer-reviewed" = accepted at a venue; "preprint" = arXiv only; "vendor" = published by a company that competes on the benchmark.

Harness needs used for scoring throughout: (1) repo + base + head commit, (2) gold defects localised to file + line (our grader is file match, line ±5), (3) clean PRs (for clean false-block rate), (4) severity mappable to blocker/major, (5) verifiability (failing test at head, or later fix commit).

## Q1. Which PR-level / commit-level review and bug-detection benchmarks exist (late 2026)?

### Takeaway
There are now about eight public PR-level review benchmarks. The most relevant to us are GitHub ReviewBench (Oct 2026, 219 PRs, 31% TypeScript), SWE-PRBench (350 PRs, base/head SHAs), c-CRAB (184 PRs with executable tests, Python), SWR-Bench (1,000 PRs incl. 500 clean, Python), AACR-Bench (200 PRs, 10 languages), Martian (50 PRs) and Qodo (100 PRs with injected defects). Only c-CRAB verifies gold issues with executable tests. Only SWR-Bench ships clean PRs. Most score with an LLM semantic judge, not file+line.

### Cited Findings

**PR-level code-review benchmarks (new, 2025-2026)**

- **GitHub ReviewBench** (vendor: GitHub/Microsoft; blog dated 2026-10-05).
  - Size and languages: 219 public PRs from 187 open-source-licensed repos, 19 languages. Sampling followed a distribution measured over 103.9M GitHub PRs. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)
  - TypeScript coverage: full set has TypeScript 68 (31.1%), JavaScript 15 (6.8%), Python 41, C# 25, Go 19, other 51. A 25-PR "test set" (5 TS, 1 JS) is part of the full set, so it is not held out. — [ReviewBench repo](https://github.com/review-bench/ReviewBench)
  - Commits and runner: base and head commits for each task are held in mirror repos named `review-bench/<owner>_<repo>`. Offline runs use `scripts/try-agent.sh` (docker, git, jq) and then `npm run judge`; leaderboard runs need a containerised agent. Licence: MIT. — [ReviewBench repo](https://github.com/review-bench/ReviewBench)
  - Gold findings: 2,623 true positives in the full set; the test set has 352 (36 High, 134 Medium, 182 Low). Findings carry severity (High/Medium/Low), category (e.g. Correctness, Security) and producer. The repo page does not state whether they carry file/line fields. — [ReviewBench repo](https://github.com/review-bench/ReviewBench)
  - How gold is made: candidates are pooled from human reviewers, issues inferred from the author's follow-up commits, static analysis and several frontier LLMs, then deduplicated and graded by Claude Sonnet 5. Senior engineers who did not build the set re-labelled every finding, agreeing 96.6% on TP/FP. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)
  - Who produced the true positives: of 4,632 golden findings, 2,623 are labelled TP. Only 39 TPs (1.5%) come from `human_review`; 1,185 (45%) come from `ccr:` producers (Copilot code review). Severity agreement with seniors is 62.9% exact; category agreement is 79.7%. — [agentpatterns.ai review](https://agentpatterns.ai/verification/open-code-review-benchmarks/)
  - Results: top grounded recall is 26.0% (Copilot Code Review "Balanced", snapshot 2026-10-01). Grounded precision is 84-90% across 28 configurations. — [agentpatterns.ai review](https://agentpatterns.ai/verification/open-code-review-benchmarks/)
  - Critiques:
    - The gold set is mostly machine-produced, and one producer dominates the TPs.
    - There is no held-out split, and the publisher ranks first on its own board. — [agentpatterns.ai review](https://agentpatterns.ai/verification/open-code-review-benchmarks/)
    - GitHub itself says the gold set is incomplete. "Augmented" recall changes its denominator per agent, so grounded recall is the headline metric. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)
    - The New Stack headline reports that an independent benchmark ordered the tools differently. — [The New Stack](https://thenewstack.io/github-reviewbench-code-review/)
  - Name collision: LangChain also published a "ReviewBench" (July 2026), but it is private and built from one team's comments. — [agentpatterns.ai review](https://agentpatterns.ai/verification/open-code-review-benchmarks/); [web search summary of The New Stack](https://thenewstack.io/github-reviewbench-code-review/)

- **SWE-PRBench** (preprint, arXiv 2603.26130, 2026-03-27).
  - Size and languages: 350 PRs, filtered from 700 by a Repository Quality Score. Python 242, JavaScript 37, Go 35, TypeScript 21, Java 15, so 58 JS+TS PRs. The paper says "6 languages" while its tables list 5. — [arXiv HTML](https://arxiv.org/html/2603.26130)
  - Gold: real human review comments on merged PRs, taken from the GitHub review API and not modified. Each PR needs at least 2 substantive human comments, and PRs with more than 30% AI-bot comments are excluded. — [arXiv HTML](https://arxiv.org/html/2603.26130)
  - Commits: base and head SHAs are stored. Tests are used only as context and are not executed. — [arXiv HTML](https://arxiv.org/html/2603.26130)
  - Data: [HF foundry-ai/swe-prbench](https://huggingface.co/datasets/foundry-ai/swe-prbench), harness at [GitHub FoundryHQ-AI/swe-prbench](https://github.com/FoundryHQ-AI/swe-prbench). The paper is CC BY 4.0; the dataset licence is not stated. — [arXiv HTML](https://arxiv.org/html/2603.26130)
  - Results: 8 models detect 15-31% of human-flagged issues (diff-only). The top four mean scores (0.147-0.153) are statistically indistinguishable. — [arXiv abs](https://arxiv.org/abs/2603.26130)
  - Detail from Table 8: detection rate ranges 0.21-0.31, e.g. Claude Sonnet 4.6 DR 0.297 with FPR 0.227.
  - Internal inconsistencies:
    - The claim that every model degrades monotonically as context grows is contradicted by Table 8 (Mistral Large 3 and Mistral Small rise from config B to C).
    - Section 3.4 difficulty percentages conflict with the counts (232/75/43). — [arXiv HTML](https://arxiv.org/html/2603.26130)
  - Contamination controls: a six-month collection window, a high-star penalty, an embedding-similarity filter (above 0.85 excluded). The authors recommend restricting evaluation to PRs merged after each model's cutoff. — [arXiv HTML](https://arxiv.org/html/2603.26130)

- **c-CRAB** (preprint, arXiv 2603.23448, v1 2026-03-24, v3 2026-04-07).
  - Size: 184 PRs and 234 validated review comments, each with at least one executable test. The repo count is reported as both 67 (Table 4) and 56 (Threats to Validity). — [arXiv HTML](https://arxiv.org/html/2603.23448)
  - Construction:
    1. Built on SWE-CARE, starting from 671 PRs and 1,313 comments.
    2. A GPT-5.2 filter keeps actionable, verifiable comments.
    3. Each PR gets a Docker image at the reviewed commit.
    4. GPT-5.2 writes a test that must fail at the PR head and pass after the human-requested fix.
    5. Claude Code (Sonnet 4.6) must be able to fix the issue from the comment alone; unsolved instances are dropped.
    6. Two authors agreed on 84% of 50 sampled tests. — [arXiv HTML](https://arxiv.org/html/2603.23448)
  - Test mix: 82.1% of tests are "structural" (inspect source text or API surface) and only 17.9% behavioural. — [arXiv HTML](https://arxiv.org/html/2603.23448)
  - Categories (10): functional correctness, testing, robustness, compatibility, documentation, design, error handling, maintainability, efficiency, security. — [arXiv HTML](https://arxiv.org/html/2603.23448)
  - Results: Claude Code 32.1%, Devin 24.8%, PR-Agent 23.1%, Codex 20.1%. The union of the four tools passes 41.5% (97/234). — [arXiv HTML](https://arxiv.org/html/2603.23448)
  - Data at [github.com/c-CRAB-Benchmark](https://github.com/c-CRAB-Benchmark). Languages are not stated explicitly; examples are Python/Django. — [arXiv HTML](https://arxiv.org/html/2603.23448)

- **SWR-Bench** (peer-reviewed: FSE 2026; arXiv 2509.01494, 2025-09-01).
  - Size: 1,000 PRs from 12 Python projects taken from SWE-bench (astropy, scikit-learn, sympy, ...). 500 "Change-PRs" have at least one ground-truth issue (1.90 change-actions on average) and 500 are "Clean-PRs". — [arXiv HTML v2](https://arxiv.org/html/2509.01494v2); [FSE 2026 listing](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/78/SWR-Bench-Assessing-LLM-Performance-in-Real-World-Code-Review-Comment-Generation)
  - Gold construction:
    - Gemini-2.5-Pro extracts change-actions from review timelines and links each to the introducing and fixing commits, with 3-run agreement.
    - SZZ removes PRs from the Clean set whose issues were fixed later.
    - Two of five graduate annotators verified each PR (Cohen's kappa 0.66). — [arXiv HTML v2](https://arxiv.org/html/2509.01494v2)
  - Snapshot: each instance captures the PR state "right before its first manual review", with a codebase checkpoint. — [arXiv HTML v2](https://arxiv.org/html/2509.01494v2)
  - Results: the best is PR-Review with Gemini-2.5-Pro at P 16.65%, R 23.18%, F1 19.38%; multi-review self-aggregation (n=5) reaches F1 23.84%. — [arXiv HTML v2](https://arxiv.org/html/2509.01494v2)
  - The LLM judge reportedly agrees with humans about 90% of the time. — [arXiv abs](https://arxiv.org/abs/2509.01494v1)
  - DOI 10.1145/3808144.

- **AACR-Bench** (preprint, arXiv 2601.19494, January 2026; Alibaba).
  - Size: 200 PRs, 1,505 comments, 50 repos, 10 languages (JS, Python, TS, Java, C#, C++, C, PHP, Go, Rust), 5 repos per language. Per-language PR counts are only in a figure. — [arXiv HTML v2](https://arxiv.org/html/2601.19494v2)
  - Gold: 391 comments are augmented from the original reviews and 1,114 are generated by LLMs and experts. About 80 engineers did double annotation. The authors say this "uncovers latent defects", giving a 285% increase in defect coverage. — [arXiv HTML v2](https://arxiv.org/html/2601.19494v2); [arXiv abs](https://arxiv.org/abs/2601.19494v1)
  - Categories: Code Defect 709, Maintainability 626, Performance 117, Security 53. There is no concurrency or compatibility category. — [arXiv HTML v2](https://arxiv.org/html/2601.19494v2)
  - Results: best F1 is 16.12% (Claude-4.5-Sonnet agent mode; P 39.9%, R 10.1%); highest recall is 47.24% at 6.7% precision. Data at [github.com/alibaba/aacr-bench](https://github.com/alibaba/aacr-bench). — [arXiv HTML v2](https://arxiv.org/html/2601.19494v2)

- **ContextCRBench** (peer-reviewed: FSE 2026 Industry; arXiv 2511.07017).
  - Size: 67,910 entries enriched with issue text and code context. Three tasks: hunk-level quality estimation, line-level defect localisation, and comment generation. — [alphaXiv](https://alphaxiv.org/abs/2511.07017); [FSE listing](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/33/Benchmarking-LLMs-for-Fine-Grained-Code-Review-with-Enriched-Context-in-Practice)
  - Results: best quality-estimation F1 is 59.54%. Used as a reward signal at ByteDance, it gave a 61.98% relative improvement. — [alphaXiv](https://alphaxiv.org/abs/2511.07017)
  - Data at github.com/kinesiatricssxilm14/ContextCRBench. — [alphaXiv](https://alphaxiv.org/abs/2511.07017)
  - It is hunk- and line-level rather than whole-PR.

- **CodeFuse-CR-Bench** (preprint 2509.14856): 601 instances from 70 Python projects, 9 PR problem domains, with the issue, PR and repo state. — [HF papers](https://huggingface.co/papers/2509.14856)

- **Martian Code Review Bench** (vendor-neutral claim: Martian says it does not sell review tools; 2026).
  - Offline set: 50 PRs from Sentry (Python), Grafana (Go), Cal.com (TypeScript), Discourse (Ruby) and Keycloak (Java). — [Martian repo](https://github.com/withmartian/code-review-benchmark)
  - Count conflict: the repo says 173 golden comments, while a third-party summary says 136. — [Martian repo](https://github.com/withmartian/code-review-benchmark); [web summary](https://agentpatterns.ai/verification/open-code-review-benchmarks/)
  - Gold: comments have severity (Low/Medium/High/Critical) and a category (bug, security, concurrency, data, api, perf, test_gap, doc_defect, style, speculative). They are "human-curated"; the process is not described, and file/line anchoring is not stated. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
  - Judging: an LLM judge (Opus 4.5, GPT-5.2, Sonnet 4.5) with Strict/Core/All category profiles and F-beta. Licence: MIT. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
  - Online track: matches bot comments to developers' later fixes on fresh PRs. Martian's own warning is that static sets risk training-data leakage. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
  - Leaderboard claims: Greptile claims #1 with 60.8% F1 (vendor blog, 2026-07-30); CodeRabbit, Cubic and Kilo also claim top placements. — [Greptile](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark); [CodeRabbit](https://www.coderabbit.ai/blog/coderabbit-tops-martian-code-review-benchmark); [Kilo](https://blog.kilo.ai/p/martians-independent-benchmark-tested)

- **Greptile benchmark** (vendor, July 2025).
  - Size: 50 PRs, 10 each from Sentry, Cal.com, Grafana, Keycloak and Discourse.
  - Construction: each bug-fix PR was traced back to its bug-introducing commit. A "before bug" branch was made, and the original change was re-opened as a new PR in clean forks. Very large or single-file changes were excluded.
  - Scoring: a catch needs a line-level comment that points at the faulty code and explains the impact.
  - Results: Greptile 82%, Bugbot 58%, Copilot 54% (per-repo cells sum to 52%), CodeRabbit 44%, Graphite 6%.
  - Availability: PRs are public in the `ai-code-review-evaluation` GitHub org; there is no packaged dataset. — [Greptile benchmarks](https://www.greptile.com/benchmarks)
  - Critique: self-run by a vendor, and the raw data was not published for verification. — [web search summary](https://gitautoreview.com/blog/ai-code-review-benchmark-2026)

- **Qodo Code Review Benchmark 1.0 / PR-Review-Bench** (vendor).
  - Size: 100 merged PRs from 8 repos with 580 injected issues. Languages: TypeScript, Python, JavaScript, C, C#, Rust, Swift.
  - Defects: LLM-injected best-practice violations plus 1-3 functional bugs per PR (edge cases, races, resource leaks, error handling). A hit needs the correct description and file+line.
  - Result: Qodo self-reports F1 60.1%. — [Qodo](https://qodo.ai/ai-code-review-benchmark/); [GitLab analysis](https://gitlab.com/gitlab-org/gitlab/-/issues/590266); [HF card](https://huggingface.co/datasets/Qodo/PR-Review-Bench/blob/main/README.md)
  - GitLab's critique:
    - The bugs are synthetic, so LLM detectors may share their patterns.
    - Most defects are single-file, with no security vulnerabilities and no full repo context.
    - GitLab recommends borrowing the methodology rather than adopting the dataset. — [GitLab analysis](https://gitlab.com/gitlab-org/gitlab/-/issues/590266)

  - HF card: licence MIT. The card names only two fields, `pr_url_to_review` and `issues` (the ground-truth list). It gives no per-language counts and no explicit base/head, file, line or severity fields; the PR URL implies the commits are recoverable from the PR. — [HF card](https://huggingface.co/datasets/Qodo/PR-Review-Bench/blob/main/README.md)
- ReviewBench judging input (`docs/JUDGING_INPUT.md`): each candidate finding has `producer`, `file` (repo-relative), `start_line`/`end_line` (at `pr.head`) and `message`. The doc does not say whether golden findings carry the same fields, or whether matching is by line or semantic. — [JUDGING_INPUT.md](https://github.com/review-bench/ReviewBench/blob/main/docs/JUDGING_INPUT.md)
- **Signal65 (Mar 2026) and AIMultiple (309 PRs, Mar 2026)**: third-party comparisons of CodeRabbit, Bugbot and others. Signal65 rewound branches to before 10 historical bug-introducing PRs per repo. Neither dataset appears to be published for reproduction. — [Signal65 PDF](https://signal65.com/wp-content/uploads/2026/03/Signal65-Insights_Evaluating-AI-Code-Review-Tools.pdf); [AIMultiple](https://aimultiple.com/ai-code-review-tools)

**Older comment-generation datasets (not defect corpora)**
- **CodeReviewer (Microsoft)**: an MSR 2025 study found only 64% of sampled training comments valid. — [Too Noisy To Learn, arXiv 2502.02757](https://arxiv.org/html/2502.02757v2)
- **CRScore**: a reference-free review-quality metric with 0.54 Spearman correlation to humans; ships a 2.9k human-rated corpus. — [arXiv 2409.19801](https://arxiv.org/html/2409.19801v2)
- **CodeReviewQA**: a comprehension benchmark with contamination mitigation, on Hugging Face. — [arXiv 2503.16167](https://arxiv.org/pdf/2503.16167.pdf)

**Bug-inducing-commit (JIT) datasets**
- **ApacheJIT** (MSR 2022 data track): 106,674 commits (28,239 bug-inducing, 78,435 clean), SZZ-labelled, 14 Apache projects (Java). — [arXiv 2203.00101](https://arxiv.org/pdf/2203.00101); [GitHub](https://github.com/harsh8398/apachejit)
- **Defectors** (2023): about 213K files (93K defective, 120K clean) from 24 Python projects, SZZ-derived. — [arXiv 2303.04738](https://www.arxiv.org/pdf/2303.04738)

**Executable bug benchmarks (JS/TS)**
- **BugsJS** (ICST 2019; STVR journal): 453 validated bugs from 10 Node.js/Mocha projects (Bower, ESLint, Express, Hessian.js, Hexo, Karma, Mongoose, Node-redis, Pencilblue, Shields). Each has a buggy revision, the fix, an exposing test and Docker infrastructure. — [ICST paper](https://people.ece.ubc.ca/amesbah/resources/papers/icst19.pdf); [dataset repo](https://github.com/ziqin/bugsjs-dataset)
- **SWE-PolyBench** (Amazon): 2,110 instances, of which TypeScript 729 and JavaScript 1,017; executable test-based issue tasks. — [HF card](https://huggingface.co/datasets/AmazonScience/SWE-PolyBench_Verified/commit/b72bb2fabd3cac2ea734d1f298fee4ac610f093f)
- **Multi-SWE-bench**: 1,632 or 2,132 instances depending on the source, including TS/JS; per-language counts not found. — [sourcepulse](https://www.sourcepulse.org/projects/15348071); [agentmarketcap](https://agentmarketcap.ai/blog/2026/04/14/multi-language-swe-bench-coding-agent-evaluation-beyond-python)
- **TSBugs** (arXiv 2601.21186): 633 bug reports from 16 TypeScript repos, with a taxonomy and bug-fix commit mining scripts. It is an empirical study, not an executable benchmark. — [arXiv](https://www.arxiv.org/pdf/2601.21186); [GitHub](https://github.com/SEatSFU/tsbugs)
- No dataset named "BugsTS" was found.

**"Review the plausible-but-wrong patch" sets**
- **Wang, Pradel & Liu** (ICSE 2026): 7.8% of plausible SWE-bench Verified patches are incorrect; PatchDiff-based extrapolation gives about 11.0%. 82.7% of suspicious patches are not caught by running developer tests. — [arXiv 2503.15223](https://arxiv.org/html/2503.15223v2); [ICSE listing](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/59/Are-Solved-Issues-in-SWE-bench-Really-Solved-Correctly-An-Empirical-Study)
- **SWE-ABS** (ICML 2026, arXiv 2603.00520): strengthened tests reject 2,184 of 11,041 (19.78%) top-30-agent patches that the original tests accepted. This is a ready-made pool of test-verified wrong patches, but Python only. — [arXiv 2603.00520](https://arxiv.org/html/2603.00520v1)

**Vulnerability datasets**
- **SecBench.js** (ICSE 2023): 600 server-side npm vulnerabilities across the 5 most common classes (e.g. prototype pollution). Each has an exploit payload, an oracle and a Jest test; needs Node 16.3+. — [GitHub](https://github.com/cristianstaicu/SecBench.js); [ICSE](https://conf.researchr.org/details/icse-2023/icse-2023-technical-track/99/SecBench-js-An-Executable-Security-Benchmark-Suite-for-Server-Side-JavaScript)
- **PrimeVul**: C/C++ only; 6,968 vulnerable and 228,800 benign functions. Its label accuracy matches the manually verified SVEN set. — [arXiv 2403.18624](https://arxiv.org/html/2403.18624v2)
- **DiverseVul and CrossVul**: label accuracy reportedly about 60% and 48%. — [arXiv 2403.18624](https://arxiv.org/pdf/2403.18624)
- **CVEfixes and CleanVul**: CVEfixes covers 27 languages; CleanVul includes JavaScript. MegaVul is C/C++. Labels from vulnerability-fixing commits are noisy because they assume all pre-fix code is vulnerable. — [SLR arXiv 2507.22659](https://arxiv.org/pdf/2507.22659); [arXiv 2508.16625](https://arxiv.org/pdf/2508.16625)

### Inferences
- **Martian and Greptile overlap.** Martian's offline set uses exactly the same five repos and 50-PR size as Greptile's July 2025 set. It is likely derived from it, or at least shares its PRs, but this is inference: no source states the lineage. If so, its gold set is effectively Greptile's backtracked bugs plus curated extras, and it has been public since mid-2025.
- **ReviewBench recall partly measures agreement with other LLMs.** Its gold set is about 45% Copilot-produced and 1.5% human-review-produced, so for an Opus or Codex-class reviewer its "recall" partly measures agreement with other frontier LLM reviewers rather than escaped-defect detection. It is still the freshest (Oct 2026, after most training cutoffs) and most TypeScript-heavy public set.
- **Results across benchmarks.** Published best recall clusters at 10-32%: ReviewBench grounded 26%, SWE-PRBench 15-31%, SWR-Bench 23%, c-CRAB 32% for the best single agent, AACR-Bench 10% at the best F1. Vendor-run sets (Greptile 82%, Qodo F1 60%, Martian F1 61%) report much higher numbers. That gap suggests the vendor sets are easier, or more favourably judged, than human-review-derived sets.

### Gaps
- No sources found for JIT-Defects4J, GHRB, VulnCode-DB, vulnerability-contributing-commit (VCC) datasets or TSSB-3M details; not researched within budget.
- ContextCRBench language mix not found.
- c-CRAB's language is Python by inference only.
- No public Graphite, CodeRabbit or Cursor Bugbot benchmark datasets were found; only vendor claims and the unpublished Signal65 and AIMultiple studies.
- Whether ReviewBench, Martian, SWR-Bench and SWE-PRBench gold items carry file+line anchors was not confirmed. ReviewBench points to `docs/JUDGING_INPUT.md`, which was not read.
- Qodo's per-language counts and schema (base/head?) are not confirmed.
- Licences for the SWE-PRBench, c-CRAB, SWR-Bench and AACR-Bench datasets are not stated; the CC BY 4.0 shown on arXiv is the paper licence.

## Q2. How does each fit our harness (base/head, file+line gold, clean PRs, severity, verifiability, TS coverage, contamination)?

### Takeaway
No external corpus meets all five harness needs. ReviewBench and SWE-PRBench supply base/head commits and real PRs with some TypeScript, but their gold needs an LLM-judge adapter. c-CRAB is the only one that verifies gold with tests, but it is Python. SWR-Bench is the only one with clean PRs, also Python. So no TypeScript-heavy external set can measure our clean false-block rate.

### Cited Findings
| Corpus | Base+head | File+line gold | Clean PRs | Severity | Verified by | TS/JS PRs | Public since | Licence |
|---|---|---|---|---|---|---|---|---|
| ReviewBench | Yes, mirror repos ([repo](https://github.com/review-bench/ReviewBench)) | Candidates submitted as file+start/end line; gold anchoring not confirmed; LLM judge (Sonnet 5) | No | High/Med/Low | LLM + seniors re-label (96.6%) | 68 TS + 15 JS of 219 | Oct 2026 | MIT |
| SWE-PRBench | SHAs ([arXiv](https://arxiv.org/html/2603.26130)) | Human review comments (inline); LLM judge kappa 0.75 | No (needs at least 2 comments) | Difficulty types, not severity | Human comments only | 21 TS + 37 JS of 350 | Mar 2026 | Paper CC BY 4.0 |
| c-CRAB | Docker image at head ([arXiv](https://arxiv.org/html/2603.23448)) | Test-based (no line grading needed) | No | 10 categories | Generated tests fail at head and pass after fix | ~0 (Python) | Mar 2026 | Unstated |
| SWR-Bench | Pre-review checkpoint ([arXiv](https://arxiv.org/html/2509.01494v2)) | Change-actions linked to fixing commits; LLM judge | **500 clean** | Taxonomy, not severity | Introducing and fixing commit + SZZ | 0 (Python) | Sep 2025 (data from SWE-bench repos) | Paper CC BY 4.0 |
| AACR-Bench | Base and target versions ([arXiv](https://arxiv.org/html/2601.19494v2)) | Fine-grained comments; LLM judge | No | 4 categories | Double human annotation | ~40 TS+JS (inferred) | Jan 2026 | Unstated |
| Martian offline | Unknown | Not stated; LLM judge | No | Low-Critical | "Human-curated" | 10 (Cal.com) | ~2025-2026 | MIT |
| Greptile | Before-bug / after-fix branches ([page](https://www.greptile.com/benchmarks)) | Line-level catch rule | No | Critical/High/Med/Low | Known historical bug + fix | 10 (Cal.com) | Jul 2025 | Unstated |
| Qodo | PR URL only (`pr_url_to_review`) | Yes, file+line required ([GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/590266)) | No | Unknown | Injected (synthetic) | Unknown subset of 100 | 2026 | MIT (HF card) |
| BugsJS | Buggy and fixed revisions ([paper](https://people.ece.ubc.ca/amesbah/resources/papers/icst19.pdf)) | Fix diff = location | No | None | Exposing test | 453 JS | 2019 | — |
| SWE-PolyBench | Base + gold patch + tests ([HF](https://huggingface.co/datasets/AmazonScience/SWE-PolyBench_Verified/commit/b72bb2fabd3cac2ea734d1f298fee4ac610f093f)) | Fix diff | No | None | Fail-to-pass tests | 729 TS + 1,017 JS | 2025 | — |
| SecBench.js | Vulnerable package version ([repo](https://github.com/cristianstaicu/SecBench.js)) | Advisory/fix | No | (security) | Exploit + oracle | 600 npm | 2023 | — |

- Contamination:
  - SWE-PRBench's authors concede contamination cannot be fully removed and advise filtering PRs by model cutoff. — [arXiv](https://arxiv.org/html/2603.26130)
  - Martian warns that static sets leak into training. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
  - SWR-Bench uses the 12 SWE-bench Python repos, which are heavily trained on. — [arXiv](https://arxiv.org/html/2509.01494v2)
- Label noise:
  - Human review comments as gold are noisy: only 64% of CodeReviewer comments were valid. — [MSR 2025](https://arxiv.org/html/2502.02757v2)
  - AACR-Bench argues that original-PR review comments miss most defects; its augmentation gave +285% coverage. — [arXiv](https://arxiv.org/abs/2601.19494v1)

### Inferences
- Integration cost is dominated by grading, not checkout. Our grader is file + line ±5; most of these corpora are graded by an LLM semantic judge. Adopting ReviewBench, SWE-PRBench or AACR-Bench means either running their judge (with an Opus or Sonnet judge cost per case) or re-anchoring each gold item to a file and line range.
- Gold sets built from human comments under-count real defects, so our "false positives" on them will include real bugs. Precision on those sets is a lower bound.
- The executable JS/TS sets (BugsJS, SWE-PolyBench, SecBench.js) can be turned into review cases by using the *reverted fix* as the "PR", with the failing test as the oracle. This is artificial: a revert has no surrounding feature work, so the defect is easier to spot than in a real bug-introducing PR. It suits a smoke test of recall, not a proxy for our gold set.
- SWE-ABS and Wang et al. offer a more realistic "review a plausible-but-wrong patch" task with test verification, but Python only. A TypeScript analogue would need generating agent patches on SWE-PolyBench TS and strengthening the tests ourselves.

### Gaps
- Not confirmed:
  - Whether ReviewBench gold findings have file/line fields.
  - Whether the Martian offline set ships base/head SHAs.
  - Qodo's schema.
- Per-language PR counts for AACR-Bench (the ~40 TS+JS is inferred from 2 of 10 languages at 5 repos each).

## Q3. Which corpora contain the defect classes we care about (security/trust boundary, multi-file/cross-entry-point omissions, compatibility/migration, concurrency/races, spec mismatch)?

### Takeaway
Category tags exist, but classes are thin. Security is present in most sets but small (AACR-Bench 53 of 1,505), and SecBench.js is the only large security set with executable oracles (npm). Concurrency is explicitly tagged only in Martian and Qodo (injected races). Compatibility is a category only in c-CRAB. Cross-file reasoning is targeted by SWE-PRBench's Type3 (12% of PRs). Spec mismatch is not a labelled category anywhere found.

### Cited Findings
- Martian's golden comments are tagged bug, security, concurrency, data, api, perf, test_gap, doc_defect, style, speculative. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
- c-CRAB categories include Compatibility, Security, Robustness and Error Handling. — [arXiv](https://arxiv.org/html/2603.23448)
- AACR-Bench: Security Vulnerability 53 of 1,505 comments; no concurrency or compatibility category. — [arXiv](https://arxiv.org/html/2601.19494v2)
- Qodo injects race conditions, resource leaks and error-handling bugs. GitLab notes there are no security vulnerabilities and most defects are single-file. — [GitLab analysis](https://gitlab.com/gitlab-org/gitlab/-/issues/590266)
- SWE-PRBench Type3_Latent_Candidate issues (43, 12.3%) are designed to need cross-file reasoning; 33.7% of its PRs are bug fixes, with "a few" security PRs. — [arXiv](https://arxiv.org/html/2603.26130)
- ReviewBench categories include Correctness and Security; the counts per category were not found. — [ReviewBench repo](https://github.com/review-bench/ReviewBench)
- SWR-Bench taxonomy: Interface, Logic, Resource, Check, Support, Larger Defects and documentation/structure classes; no explicit security or concurrency class. — [arXiv](https://arxiv.org/html/2509.01494v2)
- SecBench.js: 600 npm vulnerabilities in 5 classes (e.g. prototype pollution), each with an exploit oracle. — [GitHub](https://github.com/cristianstaicu/SecBench.js)
- The ReviewBench authors concede that "project-convention defects are hard to surface". — [agentpatterns.ai](https://agentpatterns.ai/verification/open-code-review-benchmarks/)

### Inferences
- Our highest-value classes are trust-boundary, one-guard-every-path omissions, rollback and migration compatibility, and check-then-act races (see our AGENTS.md "Defects reviews keep finding"). These are repo-specific invariants that no external corpus labels. External sets will mostly measure generic correctness; our in-house corpus remains the only measure for these classes.
- Martian's `concurrency` and `security` tags with a Strict/Core profile, and ReviewBench's Security category, are the easiest way to slice external results toward our classes.

### Gaps
- Per-category counts for ReviewBench, Martian and SWE-PRBench not found.
- No external corpus found with a labelled "spec mismatch / request not honoured" class; SWE-PolyBench-style issue tasks implicitly test spec conformance via tests.

## Q4. How have others built "escaped-defect" corpora from their own history, and how noisy is it?

### Takeaway
There are three recipes. (a) SZZ blame from fix commits: cheap, about 0.4 precision for basic SZZ, 0.66-0.73 for R-SZZ. (b) Use fix commits whose message names the inducing commit: the developer-informed oracle, high precision. (c) Replay: trace a fix to its inducing PR, rewind to just before it, and re-open the original PR for review (Greptile, Signal65, Martian online). Follow-up-commit mining is also used by ReviewBench and SWR-Bench. Recipe (b)+(c) is the actionable one for us.

### Cited Findings
- Rosa et al. (ICSE 2021) built an oracle of 1,115 bug fixes (from 1,930 validated, out of 3,585 candidates) where developers explicitly named the bug-inducing commit. — [ar5iv](https://ar5iv.arxiv.org/html/2102.03300); [ICSE](https://2021.icse-conferences.org/details/icse-2021-papers/42/Evaluating-SZZ-Implementations-Through-a-Developer-informed-Oracle)
  - SZZ precision/recall on that oracle:

    | Variant | Recall | Precision | F1 |
    |---|---|---|---|
    | B-SZZ | 0.69 | 0.39 | 0.50 |
    | AG-SZZ | 0.60 | 0.45 | 0.52 |
    | L-SZZ | 0.45 | 0.52 | 0.48 |
    | R-SZZ | 0.57 | 0.66 (0.73 with date filter) | 0.61 |
    | MA-SZZ | 0.64 | 0.36 | 0.46 |
    | PyDriller SZZ | 0.67 | 0.39 | 0.49 |
    | SZZ-unleashed | 0.72 | 0.09 | 0.16 |

  - 311 fixes defeat every variant. Causes: buggy lines not touched by the fix, reverts and history rewrites, and added lines that can't be blamed. — [ar5iv](https://ar5iv.arxiv.org/html/2102.03300)
  - The 2023 JSS extension covers 9 variants plus 2 new ones handling added lines and reverts. — [search summary of Rosa et al.](https://arxiv.org/abs/2102.03300)
- ApacheJIT and Defectors are SZZ-labelled at scale, so they inherit SZZ precision limits. — [ApacheJIT](https://arxiv.org/pdf/2203.00101); [Defectors](https://www.arxiv.org/pdf/2303.04738)
- SWR-Bench combined three steps:
  1. LLM extraction of review-timeline change-actions, linked to introducing and fixing commits.
  2. SZZ to purge "clean" PRs whose problems were fixed later.
  3. Human double verification (kappa 0.66). — [arXiv](https://arxiv.org/html/2509.01494v2)
- ReviewBench mines "issues inferred from author follow-up commits" as one gold source. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)
- Greptile replay: bug-fix PR → inducing commit → branch before the bug → re-open the original change as a PR in a clean fork. Very large or single-file changes are excluded. — [Greptile](https://www.greptile.com/benchmarks)
- Signal65 replay: rewound a branch to just before each of 10 historical bug-introducing PRs per repo. — [Signal65 PDF](https://signal65.com/wp-content/uploads/2026/03/Signal65-Insights_Evaluating-AI-Code-Review-Tools.pdf)
- Martian online track: bot suggestions are matched to developers' post-review fixes by a three-step LLM process. — [Martian repo](https://github.com/withmartian/code-review-benchmark)
- c-CRAB's test-synthesis recipe (a test fails at head and passes after the fix, validated by an agent fixing from the comment) is described as dataset-agnostic. — [arXiv](https://arxiv.org/html/2603.23448)
- Vulnerability-fix-commit labelling is noisy because it assumes all pre-fix code is vulnerable; 16.7% of CVEs map to "undecidable" patches. — [SLR](https://arxiv.org/pdf/2507.22659)

### Inferences
- Applied to our repo, recipe (b) means mining merged fix PRs and commits whose text names the inducing change ("regression from #NNN", "introduced in <sha>", "fixes a bug from #NNN"). This gives escaped defects at near-oracle precision, and the fix diff gives file+line gold. Pure SZZ (B-SZZ, PyDriller) would put roughly 6 in 10 candidates on the wrong commit.
- Our AGENTS.md already cites cause-PR numbers (e.g. "#323 broke … until #357"), which are exactly such explicit links. Re-opening each inducing PR at its original base (the Greptile/Signal65 replay) gives a corpus whose gold is verified by a later real fix. Synthesising a c-CRAB-style failing test from the fix PR's own test adds execution verification.
- Expect a selection bias: escaped defects are, by definition, ones the original review missed, which is what we want for recall. But they skew toward defects that later surfaced in behaviour, so security and compatibility issues that never fired will be under-represented.

### Gaps
- No published precision figure was found for "follow-up commit" mining (ReviewBench) or for LLM-linked change-actions (SWR-Bench) separately from their human verification.
- Industry papers (Google, Meta) on bug-introducing-diff mining were not researched within budget.

## Q5. Top-3 candidates for our use, and realistic runnable TypeScript/Node-like case counts

### Takeaway
1. **GitHub ReviewBench** gives about 83 TS/JS PRs, fresh, MIT, with base/head mirrors, but its gold is machine-heavy.
2. **SWE-PRBench** gives 58 TS/JS PRs with SHAs and human-comment gold; there is no runtime, so we would build environments.
3. **c-CRAB** gives roughly 0 TS cases but is the only test-verified set; use its method, or the Python set as an execution-verified cross-check.

Treat all three as a *complement*: none can measure clean false-block rate in TypeScript (only SWR-Bench has clean PRs, Python only). The best TypeScript-specific expansion is an in-house escaped-defect corpus built with recipe (b)+(c) above.

### Cited Findings
- ReviewBench: TS 68 + JS 15 of 219 PRs. Base/head mirrors, containerised runner, MIT, released Oct 2026, top grounded recall 26%. — [repo](https://github.com/review-bench/ReviewBench); [agentpatterns.ai](https://agentpatterns.ai/verification/open-code-review-benchmarks/)
- SWE-PRBench: TS 21 + JS 37 of 350. Base/head SHAs, human review comments, no execution, HF dataset plus harness. — [arXiv](https://arxiv.org/html/2603.26130)
- c-CRAB: 184 PRs and 234 comments with Docker and tests; Python examples. — [arXiv](https://arxiv.org/html/2603.23448)
- Other TS options:
  - Greptile/Martian Cal.com slice: 10 PRs. — [Greptile](https://www.greptile.com/benchmarks)
  - AACR-Bench: TS and JS are 2 of 10 languages across 200 PRs. — [arXiv](https://arxiv.org/html/2601.19494v2)
  - Qodo: TypeScript and JavaScript among 7 languages in 100 PRs; count unknown. — [GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/590266)
- Executable JS/TS bug pools for synthetic reverted-fix cases: BugsJS 453 ([paper](https://people.ece.ubc.ca/amesbah/resources/papers/icst19.pdf)), SWE-PolyBench 729 TS + 1,017 JS ([HF](https://huggingface.co/datasets/AmazonScience/SWE-PolyBench_Verified/commit/b72bb2fabd3cac2ea734d1f298fee4ac610f093f)), SecBench.js 600 ([repo](https://github.com/cristianstaicu/SecBench.js)).

### Inferences
Case counts below are estimates.

| Candidate | Raw TS/JS PRs | Realistically usable in our harness | Main cost |
|---|---|---|---|
| ReviewBench | 83 | ~60-80. Base/head ready; the reviewer can read and run code; tests may not install for every repo. | Judge adapter or re-anchoring; gold is ~45% Copilot-produced |
| SWE-PRBench | 58 | ~40-58 for read-only review; fewer if tests must run (no environments provided) | Build environments; gold = human comments (incomplete); judge adapter |
| c-CRAB | ~0 TS | 184 Python PRs runnable via Docker | Language mismatch; use as an execution-verified cross-check or copy the method |
| AACR-Bench (alt.) | ~40 | ~40, read-only | LLM-augmented gold; judge adapter |
| Greptile/Martian Cal.com (alt.) | 10 | 10 | Tiny; public since 2025 |
| Reverted-fix synthetic (BugsJS / SWE-PolyBench / SecBench.js) | 453 / 1,746 / 600 | Hundreds, test-verified | Artificial (revert-only diffs, no feature context); Node 16-era toolchains |

- Combined realistic external TS/JS review cases with real PRs: about 100-150 (ReviewBench + SWE-PRBench + AACR + Cal.com, minus failures). That is the same order as our in-house 135. Pooling roughly doubles N but changes the distribution, from our repo's invariants to generic OSS review issues.
- Recommended split:
  - Keep the in-house corpus as primary for blocking recall on our defect classes and for the clean false-block rate.
  - Add ReviewBench TS/JS as an external, post-cutoff generalisation check using grounded recall.
  - Grow the in-house set with explicitly-linked escaped defects (recipe b+c) rather than adopting a third-party set wholesale.

### Gaps
- The exact install success rate for ReviewBench and SWE-PRBench TS repos in a Bun/Node environment is unknown; it needs a trial run.
- Whether ReviewBench's 68 "TypeScript" PRs are by repo primary language or by changed files is not stated.
- Training-cutoff overlap per case is not computed. SWE-PRBench recommends filtering PRs merged after each model's cutoff; for Opus 5.5 (cutoff June 2026), only ReviewBench (released Oct 2026, PR dates unknown) is plausibly post-cutoff.
