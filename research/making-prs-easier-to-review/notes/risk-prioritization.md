# Risk-based prioritization of reviewer attention (defect prediction, JIT, risky file/line highlighting)

*Notes compiled 2026-10-08. Throughout, **[PRED]** marks evidence about prediction accuracy only (offline, historical data). **[HUMAN]** marks evidence where predictions or attention cues were shown to people and behavior or outcomes were measured. Most of the literature is [PRED]; [HUMAN] evidence is thin and mixed.*

## 1. JIT (change-level) and line-level defect prediction as a review aid

### Takeaway
Change-level (JIT) models trained on simple change metrics (size, diffusion, history, experience) rank risky commits moderately well (about 68% accuracy and 64% recall in the canonical study; about 35% of defect-inducing changes found with 20% of inspection effort). Line-level variants (JITLine, DeepLineDP) can also point at specific lines, with a median Top-10 accuracy around 0.6. However, the models decay within about a year and must be retrained frequently, and almost all results are offline [PRED].

### Cited Findings
- **Kamei, Shihab, Adams, Hassan, Mockus, Sinha, Ubayashi, "A Large-Scale Empirical Study of Just-in-Time Quality Assurance," IEEE TSE 39(6):757–773, 2013** [PRED]. 11 projects (6 open source, 5 commercial). Change-level models predict whether a change will induce a defect with **average accuracy 68% and average recall 64%** — [SAIL PDF / search abstract](https://sail.cs.queensu.ca/data/pdfs/TSE_ALarge-ScaleEmpiricalStudyOfJust-in-TimeQualityAssurance.pdf)
- Kamei et al. introduced effort-aware JIT evaluation. Their effort-aware linear regression (EALR) **identifies 35% of all defect-inducing changes using 20% of the effort** needed to inspect all changes. "Effort" is measured as lines changed, which motivated the later "%defects found at 20% LOC" metrics — [Feature Sets in JIT Defect Prediction (arXiv 2209.13978)](https://arxiv.org/pdf/2209.13978); [Revisiting Unsupervised Learning for Defect Prediction (arXiv 1703.00132)](https://arxiv.org/pdf/1703.00132)
- **McIntosh & Kamei, "Are Fix-Inducing Changes a Moving Target? A Longitudinal Case Study of Just-In-Time Defect Prediction," IEEE TSE 44(5):412–428, 2018** [PRED]. 37,524 changes from Qt and OpenStack. **AUC and calibration (Brier) drop considerably one year after training.** The importance of change properties fluctuates over time, which over- or underestimates their future impact. The authors recommend **retraining on recent data (within 3 months)**, and say quality-improvement plans should rest on **≥6 months** of history — [Rebels lab page](https://rebels.cs.uwaterloo.ca/journalpaper/2017/04/04/are-fix-inducing-changes-a-moving-target.html)
- **Pornprasit & Tantithamthavorn, "JITLine: A Simpler, Better, Faster, Finer-grained Just-In-Time Defect Prediction," MSR 2021** [PRED]. 37,524 commits from OpenStack and Qt. Results:
  - 8–10% higher AUC than prior work.
  - **17–51% more cost-effective (PCI@20%LOC)**.
  - 70–100× faster than deep-learning baselines (DeepJIT, CC2Vec).
  - Line-level predictions are **133–150% more accurate (Top-10 Accuracy)** than an NLP baseline.
  - A replication showed CC2Vec's earlier results were inflated by test-data leakage: when the leakage was removed, its F-measure fell 38.5% (OpenStack) and 45.7% (Qt).

  Sources: [arXiv 2103.07068](https://arxiv.org/abs/2103.07068v1); [MSR 2021 page](https://2021.icse-conferences.org/details/msr-2021/msr-2021-technical-papers/37/JITLine-A-Simpler-Better-Faster-Finer-grained-Just-In-Time-Defect-Prediction)
- JITLine's **median line-level Top-10 accuracy = 0.61**, i.e., roughly 6 of the top-10 flagged lines are truly defective in a typical commit — [search summary citing JITLine comparisons](https://arxiv.org/abs/2103.07068v1)
- **Pornprasit & Tantithamthavorn, "DeepLineDP: Towards a Deep Learning Approach for Line-Level Defect Prediction," IEEE TSE 49(1), Jan 2023** [PRED]. This is release-based (file + line level), not JIT. It is **14–24% more accurate** than other file-level approaches and **50–250% more cost-effective** than other line-level approaches — [Monash research portal](https://research.monash.edu/en/publications/deeplinedp-towards-a-deep-learning-approach-for-line-level-defect/)
- **Hong, Tantithamthavorn & Thongtanunam (RevSpot), SANER 2022** [PRED]. RevSpot predicts which lines will receive a comment or be revised (detail in section 4) — [Monash](https://research.monash.edu/en/publications/where-should-i-look-at-recommending-lines-that-reviewers-should-p/)
- **Explainability for JIT:** **PyExplainer (Pornprasit, Tantithamthavorn, Jiarpakdee, Fu, Thongtanunam, ASE 2021, ACM Distinguished Paper)** [PRED]. It builds local rule-based explanations of why a commit is flagged. Compared with LIME, its synthetic neighbors are 41–45% more similar, its local models 18–38% more accurate, and its explanations 69–98% more unique and 17–54% more consistent with the actual characteristics of future defect-introducing commits — [ASE 2021 page](https://www.se.cs.uni-saarland.de/conferences/ASE/ase2021/details/ase-2021/ase-2021-papers/49/PyExplainer-Explaining-the-Predictions-of-Just-In-Time-Defect-Models.html). There is also a related JITBot tool: [JITBot record](https://repository.li.mahidol.ac.th/entities/publication/abb6b766-bee4-42c2-a69b-bf5562ac0a9f/full)
- **Industrial JIT, Ubisoft: Nayrolles & Hamou-Lhadj, "CLEVER," MSR 2018** [PRED]. Across 12 Ubisoft systems it detects risky commits with **79% precision and 65% recall**, beating Commit Guru. It suggests fixes, drawn from code clones, in **66.7%** of cases — [Ubisoft La Forge](https://www.ubisoft.com/en-us/studio/laforge/news/69mh5FECbj12vBfL4HGC5C/clever-combining-code-metrics-with-clone-detection-for-justintime-fault-prevention-and-resolution-in-large-industrial-projects)
- Change-level defect prediction is reported as **adopted by industrial teams at Avaya, BlackBerry and Cisco** (secondary claim made in later JIT papers) — [search summary of arXiv 2308.13707](https://arxiv.org/pdf/2308.13707v1)
- **Amazon Prime Video, Kurup et al., "Deployment Risk Assessment Using Diff-Aware Features," arXiv 2607.06766 (2026)** [PRED]. LLMs extract multi-language features (code-level and change-level metrics, style violations, change type). The model reaches **average recall 0.83 and F1 0.81** on Prime Video data plus ApacheJIT. **Change-volume metrics were noisy, and structural code complexity was a stronger predictor** — [arXiv 2607.06766](https://arxiv.org/pdf/2607.06766)

### Inferences
- For a diff-to-review-page tool, the effort-aware framing (Kamei's "% of risky changes caught at 20% of LOC") maps directly onto a "read closely / skim / skip" split. It is the right way to evaluate a triage feature: measure what fraction of real defects lands in the "read closely" bucket, normalized by that bucket's share of the lines.
- A line-level Top-10 accuracy of about 0.6 means roughly 4 in 10 highlighted lines are false alarms. Highlights should therefore be framed as "look here first," never as "only look here."
- Any risk model needs scheduled retraining (McIntosh & Kamei: ~3 months). A static heuristic or a model trained once will quietly become miscalibrated.

### Gaps
- I could not open the full Kamei 2013 PDF (the fetch was garbled), so per-metric importance (e.g., diffusion and number of files as top factors) is not verified here.
- I could not verify the exact DeepLineDP figures for Recall@Top20%LOC or Initial False Alarm.
- I did not verify that simple or unsupervised effort-aware models (Yang et al. FSE 2016; Huang et al. ICSME 2017; Zeng et al. ISSTA 2021 "LApredict") rival complex models. This is widely cited but not confirmed in this session.
- I found no reliable public source for an Ericsson JIT deployment study.

## 2. Does showing defect predictions to developers or reviewers change behavior or outcomes?

### Takeaway
The [HUMAN] evidence is sparse and mixed:
- **Google's 2013 deployment produced no detectable behavior change.**
- A 48-person controlled experiment (Gherald, EMSE 2024) found that risk analytics **significantly improved risk awareness and review effectiveness**, but its speed-up in finding defects was not significant.
- Meta reports large operational gains from risk scores used for **gating and auto-approval** rather than for guiding human attention.
- Practitioners say they want defect prediction (over 90% willing to adopt) but demand actionable, explained output.

### Cited Findings
- **Lewis, Lin, Sadowski, Zhu, Ou, Whitehead, "Does Bug Prediction Support Human Developers? Findings from a Google Case Study," ICSE 2013** [HUMAN].
  - **Compared:** FixCache (two variants) and the Rahman algorithm, which ranks files by closed bugs, plus TWS, a time-weighted Rahman variant the authors built.
  - **Result:** After deploying TWS at Google, **"developer behavior did not change significantly before and after TWS was deployed."**
  - **Three properties needed for adoption:** (1) **actionable messages**; (2) **obvious reasoning** about why a file was flagged; (3) **bias toward the new**, i.e., files causing problems now rather than historical bug counts.
  - TWS met (2) and (3) but failed on (1), which the authors link to the lack of impact.

  Sources: [Google Research](https://research.google/pubs/does-bug-prediction-support-human-developers-findings-from-a-google-case-study/); [Never Work in Theory summary](https://neverworkintheory.org/2013/06/06/does-bug-prediction-support-human-developers-findings-from-a-google-case-study.html)
- **Yu, Cogo, McIntosh, Godfrey, "Studying the Impact of Risk Assessment Analytics on Risk Awareness and Code Review Performance," EMSE 2024** [HUMAN].
  - **Design:** Between-subjects controlled experiment, **n=48**, using **Gherald**, a prototype that scores change-set riskiness from historical data.
  - **Results:** The treatment group showed **statistically significant improvements in risk awareness and code review effectiveness** (Mann–Whitney U, one-tailed, α=0.05). It **identified known defects more quickly, but that difference was not significant.**
  - **Setting:** A lab study on prepared changes, not a field deployment.

  Sources: [Rebels lab page](https://rebels.cs.uwaterloo.ca/journalpaper/2024/01/02/studying-the-impact-of-risk-assessment-analytics-on-risk-awareness-and-code-review-performance.html); [UWSpace thesis](https://uwspace.uwaterloo.ca/items/82b078da-ffb3-42bf-8c4e-2f3405580521/full)
- **Wan, Xia, Hassan, Lo, Yin, Yang, "Perceptions, Expectations, and Challenges in Defect Prediction," IEEE TSE 2018** [HUMAN, survey only].
  - **Sample:** Interviews plus a validation survey with **395 practitioner responses**.
  - **Findings:**
    - **Over 90% are willing to adopt** defect prediction.
    - **Feature-level** granularity is most preferred.
    - Practitioners' beliefs about defect-density distribution and the size–defect relationship disagree with research evidence.
    - 7.2% showed inconsistency between their behavior and their perception.
    - Over 40% said they sometimes make "work-around" fixes.

  Source: [SMU InK](https://ink.library.smu.edu.sg/sis_research/4356). A later reply paper questions some of the developer beliefs: [Assessing Developer Beliefs (arXiv 1904.05794)](https://arxiv.org/pdf/1904.05794)
- **Jiarpakdee et al., "Practitioners' Perceptions of the Goals and Visual Explanations of Defect Prediction Models," MSR 2021** [HUMAN, perception]. A practitioner survey on which explanation visualizations are useful — [MSR 2021 page](https://2021.msrconf.org/details/msr-2021-technical-papers/43/Practitioners-Perceptions-of-the-Goals-and-Visual-Explanations-of-Defect-Prediction-) (detailed numbers not retrieved).
- **Meta, Diff Risk Score (DRS)**, engineering blog, Aug 2025 [HUMAN/operational].
  - **What it is:** A fine-tuned Llama model that predicts the likelihood that a diff causes a production incident (SEV). It **"produce[s] a risk score and highlight[s] potentially risky code snippets."**
  - **Use:** It powers about 19–20 risk-aware features, including reviewer selection for high-risk diffs and code-freeze relaxation.
  - **Outcome:** During a 2024 partner event, Meta **landed 10,000+ changes that previously couldn't ship during freeze**, with minimal production impact. This is self-reported, not peer reviewed.

  Source: [Meta Engineering](https://engineering.fb.com/2025/08/06/developer-tools/diff-risk-score-drs-ai-risk-aware-software-development-meta/)
- **Abreu, Murali, Rigby, Maddila, Sun, Ge, Chinniah, Mockus, Mehta, Nagappan, "Moving Faster and Reducing Risk: Using LLMs in Release Deployment," arXiv 2410.06351 (2024)** [PRED, Meta].
  - **Logistic-regression baseline:** gating the top **5% / 10% / 50%** riskiest diffs captures **18.7% / 27.9% / 84.6% of SEV-causing diffs**.
  - **Risk-aligned generative LLMs** (iCodeLlama-34B, iDiffLlama-13B) reach **1.40× / 1.52× / 1.05×** the baseline.
  - **StarBERT** underperforms at 0.61× / 0.85× / 0.81×.

  Source: [arXiv 2410.06351](https://arxiv.org/abs/2410.06351)
- **Meta RADAR (Risk Aware Diff Auto Review), arXiv 2605.30208 (May/June 2026), 31 authors incl. Mockus, Rigby, Nagappan** [HUMAN/operational].
  - **Pipeline:** Eligibility gates, then static heuristics, then the ML Diff Risk Score, then an LLM code review, then deterministic validation. Low-risk diffs are auto-approved.
  - **Scale:** **535K+ diffs reviewed by RADAR, 331K+ auto-approved and landed.**
  - **Safety:** RADAR diffs have **1/3 the revert rate and 1/50 the production-incident rate** of non-RADAR diffs. This is confounded, because RADAR selects low-risk diffs.
  - **Calibration lever:** Relaxing the DRS threshold from the 25th to the 50th percentile raised the approve rate to **60.31%**.
  - **Speed:** Median diff review wall time fell **35%**, and median time-to-close fell by "over 330%."

  Sources: [arXiv 2605.30208](https://arxiv.org/pdf/2605.30208); [chatpaper summary](https://chatpaper.com/paper/288052)

### Inferences
- The strongest positive real-world evidence (Meta) comes from using risk to **route** work: gating, auto-approval, choosing reviewers, freeze exceptions. Using risk to **direct a human's eyes** inside a diff has much weaker evidence. A review-page tool should expect modest awareness gains (Gherald) rather than proven defect-catch improvements.
- Google's three lessons (actionable, explained, recency-biased) amount to a spec for the risk-rating UI. Every "read closely" label should carry a human-readable reason, such as "touches auth; author's first change to this file; 3 recent bug fixes here." It should also suggest a concrete action, such as "check error path X."
- RADAR's revert and incident ratios are not causal. They compare a selected low-risk population with everything else. Treat them as evidence that the score separates risk levels, not that auto-review is safer.

### Gaps
- I found no peer-reviewed field study (A/B or before/after) showing that line- or hunk-level risk highlights in a real review tool increase the number of defects caught. Gherald is lab-based, and DRS snippet highlighting has no published outcome data.
- I did not retrieve the Gherald effect sizes or what exactly the tool displayed.
- I did not retrieve the Google study's sample size or deployment duration.
- I did not retrieve the Meta paper "Leveraging Risk Models to Improve Productivity for Effective Code Un-Freeze at Scale," which the DRS blog cites.

## 3. Which signals predict defects or review-relevant issues in a change? What do review comments actually find?

### Takeaway
The best-replicated risk signals are:
- change size and diffusion (lines, files, directories);
- author inexperience or low ownership ("minor contributors");
- file defect and fix history;
- weak review (low coverage or participation).

Vulnerability likelihood rises with lines changed and author inexperience. Most review findings (about 75%) concern maintainability or evolvability rather than functional defects. Risky files are, perversely, reviewed less rigorously.

### Cited Findings
- **Bird, Nagappan, Murphy, Gall, Devanbu, "Don't Touch My Code! Examining the Effects of Ownership on Software Quality," ESEC/FSE 2011** (Test of Time Award 2021).
  - **Setting:** Windows Vista and Windows 7.
  - **Findings:** The **number of low-expertise ("minor") contributors and the top owner's ownership share** are related to **both pre-release faults and post-release failures**. Removing minor-contributor data markedly degrades contribution-based defect prediction.

  Source: [Microsoft Research](https://www.microsoft.com/en-us/research/?p=161465)
- **McIntosh, Kamei, Adams, Hassan, "The Impact of Code Review Coverage and Code Review Participation on Software Quality," MSR 2014** (extended in EMSE 2016).
  - **Setting:** Qt, VTK, ITK.
  - **Findings:** Review coverage and participation share a significant link with post-release defects. **Low coverage and low participation are estimated to produce components with up to 2 and 5 additional post-release defects, respectively.**

  Sources: [SWAG page](https://www.swag.uwaterloo.ca/www/publications/the-impact-of-code-review-coverage-and-code-review-participation-on-software-quality-a-case-study-of-the-qt-vtk-and-itk-projects.html); [EMSE extension](https://rebels.cs.uwaterloo.ca/journalpaper/2015/03/03/an-empirical-study-of-the-impact-of-modern-code-review-practices-on-software-quality.html)
- **Thongtanunam, McIntosh, Hassan, Iida, "Investigating Code Review Practices in Defective Files," MSR 2015.**
  - **Setting:** Qt, 11,736 reviews of changes to 24,486 files.
  - **Findings:** **Future-defective files and risky files tend to be reviewed *less* rigorously** than clean files. Review concerns in both kinds of file skew toward evolvability (e.g., documentation) rather than functional logic.

  Source: [SWAG page](https://swag.uwaterloo.ca/publications/investigating-code-review-practices-in-defective-files-an-empirical-study-of-the-qt-system.html)
- **Mäntylä & Lassenius, "What Types of Defects Are Really Discovered in Code Reviews?," IEEE TSE 35(3):430–448, 2009.** **77% of reviewer-identified issues were evolvability defects** and 23% were functional — [as summarized in PMC 9489594](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9489594/)
- **Beller, Bacchelli, Zaidman, Juergens, "Modern Code Reviews in Open-Source Projects: Which Problems Do They Fix?," MSR 2014.** Over 1,400 review-induced changes in two OSS projects (ConQAT, GROMACS) show a **~75:25 ratio of maintainability to functional problems** — [FLOSShub](https://flosshub.org/node/1650)
- **Bosu, Greiler, Bird, "Characteristics of Useful Code Reviews: An Empirical Study at Microsoft," MSR 2015.**
  - **Setting:** 1.5M review comments across 5 Microsoft projects. A comment counted as "useful" if it triggered a nearby code change.
  - **Findings:** **The more files in a change, the lower the proportion of useful comments.** Reviewer usefulness rises steeply in a reviewer's first year, then plateaus.

  Source: [Microsoft Research](https://www.microsoft.com/en-us/research/?p=168510)
- **Paul, Turzo, Bosu (ICSE 2021).** Review attributes that predict missed security defects (detail in section 5) — [arXiv 2102.06909](https://arxiv.org/abs/2102.06909v1)
- **Bosu, Carver et al., "Identifying the Characteristics of Vulnerable Code Changes," FSE 2014.** 267,046 review requests across 10 OSS projects yielded 413 vulnerable code changes (VCCs). Findings:
  - Code review can find common vulnerability types.
  - Experienced contributors authored most VCCs, but **less-experienced contributors' changes were 1.8–24× more likely to be vulnerable**.
  - **Vulnerability likelihood increases with lines changed.**
  - **Modified files are more likely to contain vulnerabilities than new files.**

  Source: [Unpaywall/DOI](https://unpaywall.org/10.1145%2F2635868.2635880)
- Kurup et al. (Prime Video, 2026): change-volume metrics were noisy, and structural complexity predicted deployment risk better — [arXiv 2607.06766](https://arxiv.org/pdf/2607.06766)
- McIntosh & Kamei (2018): the importance of change-property families fluctuates over time, so no single signal is stably dominant — [Rebels](https://rebels.cs.uwaterloo.ca/journalpaper/2017/04/04/are-fix-inducing-changes-a-moving-target.html)

### Inferences
- The candidate per-file risk features for the review page are all well supported:
  - lines and hunks changed;
  - number of files and directories touched;
  - whether the author is a "minor contributor" to that file (ownership share);
  - recent bug-fix history of the file;
  - whether the file is modified rather than new (higher vulnerability rate);
  - structural complexity of touched code;
  - security-sensitive areas.
- Many review comments (about 75%) are about maintainability. A "skip" label risks suppressing exactly that kind of feedback. Consider labels like "low defect risk — skim for style" rather than implying zero value.
- Thongtanunam 2015 suggests reviewers under-attend to risky files without help. That is the strongest argument for explicit risk cues.

### Gaps
- I did not verify the specific figures in Bacchelli & Bird ICSE 2013 (defects as the top stated motivation, but a minority of comments) or Kononenko et al. (Mozilla review quality).
- I found no consolidated, cited evidence that "risky code areas" such as concurrency or error handling carry higher defect rates in this session. Only security has direct support (section 5).

## 4. Review-specific attention models: which files or lines get comments, and does file order matter?

### Takeaway
Models can predict which lines will draw reviewer comments or revisions with high Top-10 accuracy (RevSpot: 81% comment, 93% revision) [PRED]. Separately, file presentation order causally affects what reviewers catch: a defect in the last file had **64% lower odds** of detection than one in the first file [HUMAN]. JetBrains confirmed the position effect industrially. A risk-ordered reading path is therefore well motivated, and default alphabetical ordering is demonstrably harmful.

### Cited Findings
- **Hong, Tantithamthavorn, Thongtanunam, "Where Should I Look At? Recommending Lines That Reviewers Should Pay Attention To" (RevSpot), SANER 2022** [PRED].
  - **Setting:** OpenStack Nova, OpenStack Ironic, Qt Base.
  - **Task:** Predict lines that **will receive a comment** and lines that **will be revised**.
  - **Results:** **Top-10 Accuracy 81% (comment) and 93% (revision)**, which is 56% and 15% better than the baseline.
  - **Motivation:** At the median, authors wait 15–64 hours for first feedback, and large patches wait longer.

  Source: [Monash research portal](https://research.monash.edu/en/publications/where-should-i-look-at-recommending-lines-that-reviewers-should-p/)
- **Fregnan, Braz, D'Ambros, Çalıklı, Bacchelli, "First Come First Served: The Impact of File Position on Code Review," ESEC/FSE 2022.**
  - **Observational [field data]:** 219,476 PRs from 138 Java GitHub projects. **Files shown earlier receive more comments**, controlling for lines added and other confounders.
  - **Controlled experiment [HUMAN]:** n=106. For one seeded defect type, **participants had 64% lower odds of finding it when its file was last rather than first.**

  Sources: [Glasgow ePrints](https://eprints.gla.ac.uk/273443); [DeepAI](https://deepai.org/publication/first-come-first-served-the-impact-of-file-position-on-code-review)
- **Bagirov, Derakhshanfar, Kalina, Kartysheva, Kovalenko (JetBrains), "Assessing the Impact of File Ordering Strategies on Code Review Process," EASE 2023 Industry.**
  - **Setting:** IntelliJ IDEA.
  - **Findings:** **Files placed lower in the order are less likely to receive review effort.** A **code-diff-based ordering beat alphabetical ordering at placing problematic files** (those needing more effort) early.

  Source: [EASE 2023](https://conf.researchr.org/details/ease-2023/ease-2023-industry/3/Assessing-the-Impact-of-File-Ordering-Strategies-on-Code-Review-Process)
- **"Not One to Rule Them All: Mining Meaningful Code Review Orders From GitHub" (arXiv 2510.04796, 2025).**
  - **Sample:** 23,241 PRs (first review round, single non-author reviewer) from 100 Java and Python repos.
  - **Findings:**
    - Non-alphabetical navigation becomes more common as file count grows.
    - Among non-alphabetical reviews, **20.6% strictly follow "Largest-Diff First"** and 24.9% correlate with it softly.
    - Non-alphabetical reviews cover a **higher share of files (42.1% vs 39.0%)**.
    - No single alternative order dominates.

  Sources: [arXiv 2510.04796](https://arxiv.org/pdf/2510.04796v1); [Moonlight summary](https://www.themoonlight.io/en/review/not-one-to-rule-them-all-mining-meaningful-code-review-orders-from-github)
- **Gonçalves, Fregnan, Baum, Schneider, Bacchelli, "Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load," EMSE 27(4), 2022** [HUMAN].
  - **Design:** Professional developers were assigned to ad hoc review, a checklist, or a **guided checklist** (segmenting and weeding to lower cognitive load).
  - **Results:** The **guided checklist helped most on a simple review**. The plain **checklist helped efficiency and effectiveness on a complex task**.

  Source: [Springer](https://link.springer.com/10.1007/s10664-022-10123-8)

### Inferences
- A risk-ordered reading path, with the highest-risk files first, directly counters the documented position bias. Fregnan et al. show the bias is causal for at least one defect type, so ordering is arguably the single best-evidenced attention intervention available.
- Note that coverage in GitHub reviews is low: reviewers comment on only about 39–42% of files. Many files are already effectively skipped. The tool's "skip" label mostly makes this implicit behavior explicit, and the evidence argues for being careful about *which* files land there.
- RevSpot predicts where comments *will* go, which mixes defects with maintainability nits. "Lines likely to be commented on" is not the same thing as "lines likely to be defective."

### Gaps
- I found no study that measured reviewers using RevSpot-style line highlights in a live tool.
- I did not locate a specific paper titled "Which file should I review first?". The closest work is the ordering studies above.

## 5. Security-focused triage in review

### Takeaway
Security defects slip through review when the review is spread across many directories, reviewers are overloaded, or the review is rushed. Simply telling reviewers to look for security issues raised detection about **8×** in a 150-person experiment, and checklists added nothing significant on top. This makes a strong case for a "security-sensitive — check X" flag.

### Cited Findings
- **Paul, Turzo, Bosu, "Why Security Defects Go Unnoticed during Code Reviews? A Case-Control Study of the Chromium OS Project," ICSE 2021.**
  - **Sample:** **516 reviews that caught security defects vs 374 where they escaped.**
  - **Model:** Logistic regression, **AUC 0.91**, identifying nine influential attributes.
  - **Helps detection:** longer review time, mutual reviewing history between developers, bug-fix changes.
  - **Hurts detection:** **number of directories under review**, the reviewer's total review workload, and the file's prior commit count.

  Source: [arXiv 2102.06909](https://arxiv.org/abs/2102.06909v1)
- **Braz, Aeberhard, Çalıklı, Bacchelli, "Less is More: Supporting Developers in Vulnerability Detection during Code Review," ICSE 2022** [HUMAN].
  - **Sample:** Online experiment, **n=150** (71% with 3+ years professional experience).
  - **Finding:** **Explicitly asking reviewers to focus on security made vulnerability detection 8× more likely.**
  - **Checklists:** A security checklist, even one **tailored to the change and its vulnerabilities, did not significantly improve on that.**

  Sources: [arXiv 2202.04586](https://arxiv.org/abs/2202.04586v2); [ICSE 2022 page](https://conf.researchr.org/details/icse-2022/icse-2022-papers/164/Less-is-More-Supporting-Developers-in-Vulnerability-Detection-during-Code-Review)
- **Bosu et al. FSE 2014.** Inexperienced authors are 1.8–24× more likely to submit vulnerable changes, and risk grows with lines changed — [Unpaywall/DOI](https://unpaywall.org/10.1145%2F2635868.2635880)

### Inferences
- A targeted "this hunk touches input validation, auth, or crypto: review for security" cue is among the best-supported attention interventions. It works through mental set rather than extra procedure, which suggests short, specific prompts beat long checklists.
- Paul et al. indicate that changes spanning many directories should raise the risk rating, or be suggested for splitting.

### Gaps
- I did not retrieve per-vulnerability-type miss rates from Paul et al.
- I found no field study of automated security-sensitivity flags in review UIs.

## 6. Risks: miscalibration, anchoring on highlights, false sense of safety

### Takeaway
There is direct experimental evidence that automated cues **anchor** reviewers. With LLM-generated reviews, reviewers concentrated on the flagged locations, found more low-severity issues but **no more high-severity issues**, and saved no time. Models also drift out of calibration within about a year. Triage labels can therefore narrow attention and create blind spots in "skip" areas.

### Cited Findings
- **Tufano, Martin-Lopez, Tayeb, Dabić, Haiduc, Bavota, "Deep Learning-based Code Reviews: A Paradigm Shift or a Double-Edged Sword?," arXiv 2411.11401 (2024; ICSE 2025)** [HUMAN].
  - **Design:** Controlled experiment, **29 expert reviewers**, 50+ hours of recorded reviews.
  - **Anchoring:** With automated reviews, reviewers **"tend to focus on the code locations indicated by the LLM rather than searching for additional issues in other parts of the code."**
  - **Outcomes:** They found more low-severity issues but **not more high-severity issues**. There was **no time saved and no confidence gain**.

  Source: [arXiv 2411.11401](https://arxiv.org/abs/2411.11401)
- Fregnan et al. (2022): attention drops for later-positioned content, with 64% lower odds of catching a defect in the last file. By the same mechanism, de-emphasized ("skip") files would plausibly get less scrutiny — [Glasgow ePrints](https://eprints.gla.ac.uk/273443)
- McIntosh & Kamei (2018): JIT models' AUC and Brier calibration degrade considerably after one year, and feature importances shift — [Rebels](https://rebels.cs.uwaterloo.ca/journalpaper/2017/04/04/are-fix-inducing-changes-a-moving-target.html)
- Lewis et al. (2013): developers distrust flags without obvious reasoning, and false positives were a concern — [Never Work in Theory](https://neverworkintheory.org/2013/06/06/does-bug-prediction-support-human-developers-findings-from-a-google-case-study.html)
- JITLine replication (2021): published deep-JIT accuracy (CC2Vec) was inflated by test-data leakage, with F-measure dropping 38.5–45.7% under a correct setup. Reported accuracies in this literature can be optimistic — [arXiv 2103.07068](https://arxiv.org/abs/2103.07068v1)
- RADAR (Meta, 2026): approval rate is a tunable calibration trade-off (approve rate 60.31% at the 50th-percentile threshold). Choosing the operating point is a policy decision, not a model property — [arXiv 2605.30208](https://arxiv.org/pdf/2605.30208)
- Meta logistic-regression baseline: gating the top 10% riskiest diffs catches only **27.9%** of SEV-causing diffs. About 72% of incident-causing diffs fall *outside* the top-risk decile — [arXiv 2410.06351](https://arxiv.org/abs/2410.06351)

### Inferences
- **Labeling.** The numbers above imply that "skip" should never be presented as "safe." Even good models leave most incidents outside the top-risk bucket. Use wording like "lower risk — skim," and show the model's recall at the chosen threshold, e.g., "historically, X% of defects were in files rated 'read closely'."
- **Calibration.** Track calibration continuously: compare predicted risk tiers with later reverts and bug-fixes, and retrain about quarterly.
- **Anchoring.** To counter anchoring, keep highlights few and justified, and prompt for an "anything else?" pass. Braz et al. suggest a short attention prompt works; Tufano et al. suggest that over-specific pointers narrow search.

### Gaps
- No study measured defects missed in tool-labeled "skip" files, i.e., the false-safety rate of a triage UI. This is an open empirical question, and the tool could instrument it itself.
- I found no peer-reviewed evaluation of risk-score calibration in human-facing review UIs (as opposed to gating).
