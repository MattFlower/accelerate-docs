# Evaluation methodology for an LLM code reviewer on a small, single-repo, noisily-labelled corpus

Scope: how to measure review variants so that a real +10 point recall gain is detected and a false one rejected. Context (from the assignment): about 135 PR cases; about 90 gold defects in the 57-case M5.2 set, taken from what a stronger adversarial reviewer found on PRs production approved; about 48 clean PRs; matching by same file, line within ±5 and blocker/major severity, assigned one-to-one; k=2 trials; current rule = +8 points pooled dev recall and at most +1 extra clean false block, then one held-out confirmation. Audits found 6/19 and 12/17 "false blocks" were real defects. Two runs of the same system differ by about 8–10 points. About 400 unlabelled blocker/major findings from the strong reviewer exist on 136 newer PRs.

Evidence-strength key: [strong] peer-reviewed, or a primary source with formulas or data; [medium] primary vendor or preprint with a stated method but little validation; [weak] secondary, blog or search-snippet only.

## Statistical design: paired tests, clustering, trials and power (how many cases, defects and trials for +10 pts at 80% power?)

### Takeaway
Use a paired, PR-clustered comparison of per-defect detection, with each defect averaged over K trials. The cited sample-size formula, under plausible assumptions, gives about **160–200 gold defects at K=2**, about 110–130 at K=4, and a floor of about 60 even with unlimited trials. The current about 90 defects with k=2 and a +8 threshold is underpowered. Worse, the observed 8–10 point A/A gap implies a high false-accept rate. The clean-case guardrail (8 trials) carries almost no information.

### Cited Findings
- Miller (Anthropic, 2024), "Adding Error Bars to Evals", recommends paired, question-level differences. The paired SE is `SE_{A−B} = sqrt(SE_A² + SE_B² − 2·SE_A·SE_B·Corr(s_A,s_B))`. The paper says "we recommend using the paired version of the standard error estimate wherever practicable". With score correlation 0.5, pairing cuts variance by 1/3. [strong] — [Miller 2024, arXiv 2411.00640](https://arxiv.org/html/2411.00640v1)
- The same paper gives a clustered SE for questions sharing a context (Eq. 4) and a clustered paired SE (Eq. 8): `SE = (1/n)·sqrt(Σ_c Σ_i Σ_j (d_{i,c} − d̄)(d_{j,c} − d̄))`, where d is the per-item A−B difference and c the cluster. For us, the cluster is the PR and the items are defects. [strong] — [Miller 2024](https://arxiv.org/html/2411.00640v1)
- Resampling K times per question: `Var(μ̂) = (Var(x) + E[σ_i²]/K)/n`, where Var(x) is the spread of true per-item scores and σ_i² is within-item trial variance. Choose K so that E[σ_i²]/K ≪ Var(x). In the paper's example, K=2 cuts variance by 1/3, K=4 by 1/2 and K=6 by 5/9. [strong] — [Miller 2024](https://arxiv.org/html/2411.00640v1)
- Sample size (Eq. 9): `n = (z_{α/2}+z_β)² · (ω² + σ_A²/K_A + σ_B²/K_B) / δ²`, with `ω² = Var(x_A)+Var(x_B)−2Cov(x_A,x_B)`. MDE (Eq. 10): `δ = (z_{α/2}+z_β)·sqrt((ω² + σ_A²/K_A + σ_B²/K_B)/n)`. Worked examples:
  - ω²=1/9, δ=3 pts, α=.05, power .8 gives n≈969.
  - With n=198, the MDE falls from 13.2% at K=1 to 7.5% at K=10.
  [strong] — [Miller 2024](https://arxiv.org/html/2411.00640v1)
- Bowyer, Aitchison and Ivanova (ICML 2025 position paper) argue that CLT intervals under-cover with fewer than a few hundred items. In their IID simulation at N=100, nominal 95% CLT intervals covered only 92.5%. They recommend Wilson or Beta-Bernoulli Bayesian intervals for a single proportion. For clustered data, only their clustered Bayesian (Beta-Binomial) model reached correct coverage; neither the CLT nor the clustered CLT did at small N. For paired comparisons they recommend a "paired Bayes" method that models the 2x2 joint outcome table. A Python library is provided. [strong] — [Bowyer et al. 2025, arXiv 2503.01747](https://arxiv.org/pdf/2503.01747); [PMLR page](https://proceedings.mlr.press/v267/bowyer25a.html)
- Heineman et al. (AI2, NeurIPS 2025), "Signal and Noise": a benchmark's usefulness for small-scale decisions tracks its signal-to-noise ratio. Signal is the spread between models; noise is variability across random factors. The paper proposes interventions such as filtering noisy subtasks, averaging checkpoints and switching to lower-noise metrics. It covers 30 benchmarks and 375 models (the arXiv HTML says 465). [strong] — [Heineman et al. 2025, arXiv 2508.13144](https://arxiv.org/abs/2508.13144)
- SWE-PRBench reports 95% bootstrap CIs (N=300, B=10,000). Its top four models (scores 0.147–0.153) were not statistically distinguishable. This illustrates that a few points of gap are inside the noise even at hundreds of PRs. [medium] — [SWE-PRBench, arXiv 2603.26130](https://arxiv.org/html/2603.26130v1)

### Inferences
These numbers are my own calculations using the cited formulas. The parameters are assumptions, not measurements.

- **Defects needed for δ=+10 pts, α=0.05 two-sided, power 0.8** (Miller Eq. 9). Assumed: per-defect detection-probability variance Var(x)=0.08–0.12 per system, between-system correlation ρ=0.5–0.7 (so ω²≈0.07–0.08), within-defect trial variance σ²=E[q(1−q)]≈0.13–0.17:

  | K | defects needed |
  |---|---|
  | 1 | 260–330 |
  | 2 | 160–200 |
  | 4 | 110–130 |
  | 8 | 80–96 |
  | ∞ | ≈57–63 (floor) |

  Multiply by a cluster design effect `1+(m̄−1)·ICC` for defects nested in PRs. With m̄≈1.6 defects per PR and ICC≈0.3, that is about 1.2x. So about 200–240 defects at K=2, or about 130–150 at K=4.
- **McNemar alternative** (binary detected or not per defect, Connor's formula, δ=0.10). The required n depends on the discordant fraction p_d:

  | p_d | n |
  |---|---|
  | 0.15 | 115 |
  | 0.20 | 155 |
  | 0.25 | 194 |
  | 0.35 | 272 |

  This agrees in order of magnitude with the Miller estimate.
- **The observed A/A noise does not fit an IID trial-noise model.** Trial noise alone, with n=90 defects, K=2 and σ²=0.15, predicts an A/A SD of the recall difference of about 4.1 points (6.1 at n=40). That means typical gaps of 3–5 points between two runs of the same system. The reported 8–10 points is about twice that. Likely causes, in my judgement:
  1. A **run-level shared component**: model or serving drift between days, prompt-cache state, or a changed tool or environment. Pairing by case does not remove it, and adding cases does not shrink it. Only independent replicate runs do, randomized or interleaved in time.
  2. **Grading instability**: the ±5-line matcher sometimes matches and sometimes misses the same finding at a slightly different line, or one-to-one assignment flips. This adds variance unrelated to reviewer quality.
  3. A smaller effective denominator than assumed, for example dev-split defects only.
  4. Clustering by PR. At about 1.6 defects per case this alone cannot explain a 2x gap.

  Recommended diagnostic: run A/A (the same config twice, or more), and decompose the variance into per-defect, per-PR and per-run components before trusting any threshold.
- **False-accept rate of the current +8 rule.** One-sided P(diff ≥ 8 | no true difference), with diff approximately normal:

  | A/A SD of diff | P(false accept) | P(accept) if true gain is +10 |
  |---|---|---|
  | 4.1 pts | 2.6% | 69% |
  | 6.1 pts | 9.5% | 63% |
  | 8 pts | 16% | 60% |
  | 10 pts | 21% | 58% |
  | 12.5 pts | 26% | 56% |

  If the observed 8–10 point gaps reflect the true SD, the rule accepts a null variant about 1 time in 5–6 and misses a real +10 about 40% of the time. The single held-out confirmation run filters some false accepts, but it has the same noise.
- **The clean-case guardrail is uninformative at 8 trials.** With 0 extra blocks in n clean trials, the 95% upper bound on the block-rate increase is about 3/n: 37.5% at n=8, 19% at n=16, 6% at n=48, 3% at n=96. A non-inferiority test (one-sided α=.05, power .8) needs about 62 clean PR-trials for a 10-pt margin at 10% discordance, about 124 at 20% discordance, and 250–500 for a 5-pt margin. Use all about 48 clean PRs at K≥2 for both systems, paired, and state the guardrail as a non-inferiority margin on the clean-block rate rather than a count of "+1 block".
- **Concrete protocol for the statistical side:**
  - Paired design: both systems on the same cases, interleaved in time to neutralize run-level drift.
  - Unit of analysis: the per-defect detection fraction over K trials. Resample PRs, not defects, for a clustered paired bootstrap, or use Bowyer's paired or clustered Bayes.
  - K=4 for decisive comparisons; K=2 is acceptable for screening.
  - Pre-state δ, α and the guardrail margin before the run.
  - Report the paired difference with a 95% interval, the per-system scores, the between-system correlation and the A/A SD.
  - Decision: adopt only if the lower CI bound is above 0 (or above a smallest-effect-of-interest) **and** clean-block non-inferiority holds.
  - A two-stage screen-then-confirm design is fine, but the confirmation stage must be powered on its own.

### Gaps
- No primary source fetched on **sequential testing** (SPRT, group-sequential O'Brien-Fleming or alpha-spending, "always-valid" p-values) applied to LLM evals. Standard group-sequential designs would let a clear winner or loser stop early. This is a gap, not a cited recommendation.
- HELM and BetterBench guidance were not retrieved.
- The parameters Var(x), ρ and σ² are assumed. They should be estimated from the existing M5.2 trial logs, which have per-defect hits across k=2 trials and across systems, to replace the table above with measured values.

## Matching findings to gold: LLM judge vs location heuristics

### Takeaway
Current benchmarks have moved from text or location similarity to **LLM-judge semantic matching with one-to-one assignment**, validated on small human samples at about 75–95% agreement. A test-based benchmark (c-CRAB) avoids matching altogether. A pure ±5-line rule will miss root-cause findings located elsewhere. Use an LLM judge as the primary matcher, keep location only as a candidate filter or tie-breaker, and audit a stratified sample by hand.

### Cited Findings
- **SWE-PRBench** (350 PRs; ground truth = real human review comments):
  - A GPT-5.2 judge labels each agent comment CONFIRMED, PLAUSIBLE or FABRICATED.
  - One-to-one bipartite matching runs in two stages. Stage 1 is greedy assignment of judge-confirmed pairs using embeddings. Stage 2 scores the rest by affinity = cosine + 0.15·same-file + δ_line, discarding pairs below 0.30.
  - Validation: κ=0.75 (83.3% agreement) on 30 stratified items. The authors call these "rubric-derived labels", so it is not clearly human annotation.
  - A cross-judge check with Claude Sonnet 4.6 on 127 comments gave 78.7% agreement (κ=0.616), lowest for one configuration (72.5%).
  - Known failure modes: judge parse failures (hard-zeroed), judge-family bias "cannot be excluded", and non-determinism even at temperature 0.
  - Frontier models catch only 15–31% of human-flagged issues.
  [medium] — [SWE-PRBench, arXiv 2603.26130](https://arxiv.org/html/2603.26130v1)
- **SWR-Bench** (1,000 PRs: 500 with changes, 500 clean, all human-verified):
  - The judge splits a review into predicted change-points and checks whether each gold change-point is "hit" by at least one prediction.
  - Hit agreement between any two of 3 experts and 2 LLM judges was 89.2–94.9%. Type agreement was 69.4–94.8% (human-human 67.4–83.6%). Severity agreement was low even between humans, so severity is supplementary only.
  - The authors reject BLEU and exact-match as not capturing semantic identification.
  [medium] — [SWR-Bench, arXiv 2509.01494](https://arxiv.org/html/2509.01494v1)
- **c-CRAB (Code Review Agent Benchmark)** turns human review feedback into executable tests. A coding agent revises the PR from the reviewer's comments, and the review counts if the revised code passes the tests (Docker per PR). It reports that agents collectively solve only about 40% of tasks. [medium] — [c-CRAB, arXiv 2603.23448](https://arxiv.org/html/2603.23448v3). Per-agent figures (Claude Code about 32.1%, union about 41.5%) come only from a third-party blog. [weak] — [orcarouter blog](https://www.orcarouter.ai/blog/c-crab-benchmark)
- **GitHub ReviewBench** (219 PRs, 187 repos):
  - Claude Sonnet 5 is the LLM grader. The rubric, judge and matcher are versioned and published.
  - Independent senior engineers re-labelled gold findings and agreed with the labels 96.6% of the time. This compares humans with labels, not humans with the judge's matching.
  - The post does not describe the location-matching rule.
  [medium] — [GitHub blog](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)
- **Martian Code Review Bench** offline track: 50 PRs from 5 repos, 136 human-curated golden comments, an independent LLM judge, and P/R/Fβ scoring. Martian reportedly made its online (developer-action) track the headline because offline results diverged from real-world use. [weak–medium; secondary] — [Kilo blog](https://blog.kilo.ai/p/martians-independent-benchmark-tested); [The New Stack](https://thenewstack.io/github-reviewbench-code-review/)

### Inferences
- ±5 lines in the same file is a reasonable cheap first-pass filter but a poor sole criterion. A finding at the root cause (another function or file) or one describing the same defect via a different symptom gets no credit, and small line shifts add grading noise. That noise plausibly contributes to the excess A/A variance noted above.
- Suggested matcher:
  1. Generate candidate pairs (same file, or any file the gold defect's fix touched, or a judge-proposed cross-file link).
  2. An LLM judge decides "same underlying defect?" with a rubric, blind to which system produced the finding.
  3. Run one-to-one assignment (Hungarian or greedy on judge confidence).
  4. Validate on 50–100 human-adjudicated pairs, reporting κ and precision and recall of the matcher against humans.
  5. Re-validate whenever the judge model changes.
  Use a judge from a different family than either reviewer, to reduce self-preference.
- Severity gating (blocker/major) is the least reliable dimension per SWR-Bench. Consider matching on defect identity first and applying severity only to the precision side.

### Gaps
- Martian's exact matching rule and judge prompt were not retrieved; they are said to be open-sourced in its repo.
- No source measured how often location-only matching misses semantically correct findings in code review. This could be measured directly on the existing corpus by having a judge re-grade unmatched findings.

## Label noise: incomplete gold, pooling, adjudication, and precision with incomplete gold

### Takeaway
Treat the gold as **pooled and incomplete**, as TREC does. Build it from the union of all compared systems' findings plus the strong reviewer's, and adjudicate blind. Report **grounded recall** against the fixed pooled gold as the headline. Report precision only as an "augmented" or adjudicated diagnostic. A gold set defined by one reviewer structurally penalizes any variant that finds different real defects.

### Cited Findings
- Buckley and Voorhees (SIGIR 2004) found standard IR measures not robust to substantially incomplete judgments. They introduced **bpref**, which correlates with existing measures under complete judgments and is more robust when they are incomplete; it uses only judged documents. They argued that pooled collections remain viable despite incompleteness. [strong] — [NIST abstract](https://www.nist.gov/node/761376); [Webis anthology](https://ir.webis.de/anthology/2004.sigirconf_conference-2004.5/)
- Yilmaz and Aslam (CIKM 2006): bpref deviates from AP under incompleteness but ranks systems similarly. Their infAP-style estimators were more robust. [medium; secondary description] — [summary](https://datalearner.com/academic/journal-papers/0219-1377/volumes-and-issues/16/paper-detail/15917)
- Pool bias: unjudged items are treated as non-relevant, which penalizes systems that retrieve them. Webber and Park (SIGIR 2009) estimate and correct the bias against an unpooled system via leave-one-out on pooled systems. That assumes the new system resembles the pooled ones. [medium; secondary] — [search summary of Webber & Park; Lipani et al.](https://discovery-pp.ucl.ac.uk/10083262/13/Lipani_Fixed-Cost%20Pooling%20Strategies_AAM.pdf)
- Zobel (SIGIR 1998) found early TREC ad hoc tracks fairly robust to incompleteness, with pool-dependent effectiveness differences of about 0.5–3.5%. [weak; secondary] — [EIREX 2010 overview](https://arxiv.org/pdf/1201.0274)
- **ReviewBench applies pooling to code review.**
  - Candidate findings come from human reviewers, author follow-up commits, static analysis and several frontier LLMs from different families.
  - The candidates are semantically deduplicated and judged by one rubric (true, relevant, non-trivial), whatever their source.
  - It reports **grounded** P/R/F1 (gold only) and **augmented** P/R/F1, where the judge rules on findings outside the gold set.
  - Grounded recall is the headline cross-system metric. Augmented recall is per-system only, because its denominator changes with each system's findings.
  [medium] — [GitHub blog](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)
- SWE-PRBench labels unmatched but valid comments PLAUSIBLE and does not penalize them as hallucinations; only excess plausible comments above τ=0.70 are penalized. It acknowledges that human reviews are not exhaustive but does not quantify the gap. [medium] — [SWE-PRBench](https://arxiv.org/html/2603.26130v1)
- SWR-Bench: at least two annotators per PR, with five graduate students verifying about 1,000 PRs with changes and about 1,000 clean PRs. It also used **SZZ to remove "clean" PRs** whose defects were fixed later but missed in review. [medium] — [SWR-Bench](https://arxiv.org/html/2509.01494v1)

### Inferences
- The audits (6/19 and 12/17 "false blocks" were real defects) show that the clean set is contaminated and the gold is relative. Under such noise, a better reviewer can score worse on both recall (it finds different defects, earning nothing) and false blocks (its real finds on "clean" PRs count against it). This bias works against exactly the improvements being sought.
- **Concrete pooling protocol for this project:**
  1. For each comparison, pool the union of blocker/major findings from the baseline, the candidate(s) and the strong reviewer, on both defect and clean cases.
  2. Deduplicate with the LLM matcher.
  3. Adjudicate each pooled item **blind to source**: valid defect, not a defect, or duplicate. Use an LLM judge plus a human on disagreements, or two independent adjudicators on a stratified sample, and report Cohen's κ.
  4. Freeze the adjudicated pool as gold for later comparisons. Re-pool when a new variant adds many unjudged findings, a pool-bias check.
  5. Reclassify any "clean" PR that gains an adjudicated valid defect.
  - Headline: grounded recall on frozen gold.
  - Diagnostics: augmented precision (fraction of a system's blocking findings adjudicated valid) and clean-block rate on verified-clean PRs.
- The **about 400 unlabelled strong-reviewer findings on 136 newer PRs** are the natural route from about 90 to 160–240 gold defects. If roughly half survive blind adjudication, they add about 200 defects across new PRs. Hold out a slice of them as a fresh held-out set (see the last question).
- Precision with incomplete gold: define it only over adjudicated findings, in the spirit of bpref and judged-only measures. Report the fraction of each system's findings that were unjudged; a high unjudged share means the precision estimate is pool-biased.

### Gaps
- No primary source found on a specific two-annotator κ threshold or adjudication protocol for code-review findings. SWR-Bench's agreement rates (89–95% hit agreement) are the nearest benchmark.
- The Webber–Park correction details were not fetched from the primary paper.

## Building escaped-defect gold from history: SZZ and "defects that reached main"

### Takeaway
SZZ-linked defects (fix commit traced back to the introducing PR) give gold that is **independent of any reviewer**, which a single-reviewer gold set lacks. But SZZ is noisy: the best variant reached only about 66–73% precision and 57% recall against a developer-informed oracle. Use SZZ to propose candidates and confirm them by adjudication, not as gold directly.

### Cited Findings
- Rosa et al., ICSE 2021, "Evaluating SZZ Implementations Through a Developer-informed Oracle". The oracle was built from fix commits where developers explicitly name the inducing commit: 1,930 instances found, 1,115 in the filtered oracle_all, 129 in oracle_issues. Results on oracle_all without and with the issue-date filter:

  | Variant | Precision | Recall | F1 |
  |---|---|---|---|
  | R-SZZ (best F1) | 0.66 (0.73 with filter) | 0.57 | 0.61 (0.64 with filter) |
  | B-SZZ | 0.39 | 0.69 | — |
  | MA-SZZ | 0.36 | 0.64 | — |
  | SZZ@PyDriller | 0.39 | 0.67 | — |
  | SZZ Unleashed | 0.09 | 0.72 | — |

  SZZ Unleashed's low precision is driven by outlier fixes: 3 fixes produced 72 inducing candidates, only 3 correct.
  [strong] — [Rosa et al. 2021, arXiv 2102.03300](https://arxiv.org/pdf/2102.03300)
- The 2023 JSS extension reportedly grows the oracle to 2,304 instances, again finds R-SZZ best of 9 variants, and adds variants for added-lines-only fixes and reverts. [weak; search snippet only] — [Rosa et al. 2023 JSS](https://www.inf.usi.ch/lanza/Downloads/Journals/Rosa2023a.pdf)
- SWR-Bench used SZZ to remove "clean" PRs whose problems were fixed later. This is a practical use of SZZ to clean negatives. [medium] — [SWR-Bench](https://arxiv.org/html/2509.01494v1)

### Inferences
- For this repository, escaped-defect gold could be mined from:
  - Fix PRs that reference an earlier PR or issue (the developer-informed signal, the highest-precision source per Rosa et al.).
  - Reverts.
  - Factory "defects" records. The recent commit "land checks and post-merge gates record classified failure observations" suggests post-merge failure data is already being collected.
  Run R-SZZ-style blame to the introducing PR and filter by the date the issue was opened. Then **adjudicate**: was the defect visible in the introducing PR's diff? Expect about 1/3 of raw SZZ links to be wrong.
- Escaped defects are a less biased recall target than "what the strong reviewer found": they are defects the whole process missed and that mattered. But the set will be small, perhaps tens per quarter in one repo. It works best as a separate **escaped-defect recall** metric, or a held-out confirmation set, rather than the main dev set.
- Also run SZZ over the current "clean" PRs and drop or relabel any that introduced a later-fixed defect. This directly addresses the contaminated clean set.

### Gaps
- No source quantified the fraction of escaped defects that were detectable from the introducing diff alone (as opposed to needing runtime or context). That is needed to set a ceiling on escaped-defect recall.

## Online and shadow evaluation: outcome labels, addressed rate, A/B testing

### Takeaway
Vendors increasingly treat **outcome-based online metrics** (whether the author fixed the flagged issue before merge) as the headline: Cursor's "resolution rate", ReviewBench's "addressed rate", Martian's online track. These are precision proxies, not recall measures, and they are self-reported with little statistical detail. Shadow-running a candidate reviewer on production PRs, with findings adjudicated rather than shown to authors, is a practical way to grow paired evidence without affecting delivery.

### Cited Findings
- Cursor Bugbot:
  - "Resolution rate" is the share of flagged bugs the author fixed in the final code, judged by an LLM at merge time. Cursor says it spot-checked examples with PR authors and the LLM classified "nearly all" correctly.
  - It reports 40 major experiments, with resolution rate rising from 52% to over 70%, and many changes regressed the metric.
  - It also maintains an offline "BugBench" of human-annotated diffs.
  - It reports no sample sizes, CIs or A/B controls.
  [medium; self-reported] — [Cursor, Building Bugbot](https://cursor.com/blog/building-bugbot)
- ReviewBench offline-to-online check: a lite-tier ensemble predicted offline gains, and online showed addressed rate (a precision proxy) +8.0%, recall +13.6% and comment volume +61%. Offline predicted +227% critical comments versus +262% online. [medium] — [GitHub blog](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)
- Martian's online track samples fresh real PRs and records whether developers acted on each AI comment. It was made the headline partly because static datasets risk training-data leakage. [weak; secondary] — [Kilo blog](https://blog.kilo.ai/p/martians-independent-benchmark-tested); [Greptile write-up](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark)
- Independent figures are much lower than vendor resolution rates. One analysis of 22,326 AI review comments reportedly found 0.9–19.2% led to a code change, versus 60% for human comments. An Atlassian study found many LLM comments unresolved. [weak; search snippet only; definitions differ] — [arXiv 2510.05450 (related)](https://arxiv.org/html/2510.05450v1)
- A third-party caveat: resolution rate measures detected issues acted on before merge, not independent precision, recall or escaped-defect prevention. [weak] — [youngju.dev](https://www.youngju.dev/blog/2026-07-17-ai-code-review-measured-evidence.en)

### Inferences
- In this factory, findings are acted on by an implementer agent, so "addressed" is confounded: an agent may fix anything flagged. Outcome labels should therefore come from blind adjudication of shadow findings, or from later escapes (an SZZ-linked defect in a PR where the shadow reviewer flagged it and production did not), not from whether the finding was acted on.
- **Shadow protocol:**
  1. Run the candidate on every production review in shadow, with output not delivered.
  2. Pool its blocker/major findings with production's and adjudicate blind, as in the pooling question.
  3. Accumulate a **paired** dataset: same PR, both reviewers.
  4. Over weeks this yields hundreds of PRs, enough for the 160–240 defect target, with fresh data that cannot have been overfit.
  Cost is roughly one extra review per PR. Interleaving is not applicable, because there is no ranked list shown to a user; shadow pairing replaces it.
- Track escaped defects (SZZ-linked) per reviewer arm as a lagging outcome metric. It is too sparse to decide individual variants but useful as a quarterly check that offline gains translate.

### Gaps
- No public source gives the statistical design (sample sizes, CIs) behind any vendor's online A/B. All vendor numbers are self-reported.
- The 22,326-comment and Atlassian figures were not verified from primary text.

## Avoiding overfitting and contamination: dev/held-out discipline, pre-registration, held-out refresh

### Takeaway
With about 135 cases and repeated variant iteration on the same dev set, adaptive overfitting is likely. The held-out clean set is already saturated. The fix is a **fresh, periodically refreshed held-out set** built from newer PRs (the 136-PR pool and shadow traffic), used once per decision, with the decision rule and power stated in advance.

### Cited Findings
- Martian's README (as quoted secondhand) notes that static datasets risk training-data leakage, which motivated its continuously refreshed online benchmark. [weak] — [Greptile write-up](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark)
- Signal-and-Noise recommends filtering noisy subtasks to raise signal-to-noise. For us that suggests dropping or down-weighting cases whose gold is disputed or whose outcome flips across same-system trials. [strong for the general principle] — [Heineman et al. 2025](https://arxiv.org/abs/2508.13144)
- ReviewBench separates a small test set (25 PRs) from its 219-PR set, and final submissions run three rounds. [medium] — [GitHub blog](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)

### Inferences
- **Discipline:**
  - Dev set: iterate freely, but report paired CIs.
  - Held-out set: built from PRs newer than any used in prompt development, adjudicated by the pooling protocol and sized for power. A held-out set of about 50 cases cannot confirm a +10 difference; it can only catch gross regressions.
  - Each held-out set is used for at most a few decisions and then rotated into dev. Draw a new held-out set from the newest PRs or shadow traffic.
- **Pre-register each comparison** in a short file written before the run: variant, δ, α, K, guardrail margin, analysis method, and the stopping rule if sequential. This prevents threshold-shopping.
- Leave-one-PR-out or cross-fitting is relevant only if variants are tuned on gold (for example few-shot examples drawn from the corpus). Exclude any PR whose defects appear in a variant's prompt or examples from that variant's evaluation.
- Filter or flag "unstable" cases, where the same system gives different hits across trials or adjudicators disagree, and report results with and without them.

### Gaps
- No primary source on formal pre-registration practice for LLM evals was retrieved.
- No source quantified adaptive overfitting for small LLM eval sets; the risk is inferred from general practice.
