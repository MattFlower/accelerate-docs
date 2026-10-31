# Change Properties, Comprehension, and Cognitive Load in Code Review

Notes compiled 2026-10-08. Setting labels used throughout: **[IND]** = industry field data or professional practitioners; **[OSS]** = open-source mining; **[LAB]** = controlled experiment; **[STU]** = participants were mostly students; **[VENDOR]** = vendor study, not peer reviewed; **[SURVEY]** = self-report. Some full texts were read directly (Bacchelli & Bird 2013; Sadowski et al. 2018; Baum et al. EMSE 2019; Baum et al. ICSME 2017; di Biase et al.; Tao & Kim 2015; Barnett et al. 2015; Bouraffa et al. 2025). For the other papers, only the abstract, metadata, or search snippets were available, and the entries say so.

## Q1. Change size: how do review effectiveness, defect detection, and review time scale with lines and files changed?

### Takeaway
Controlled and field evidence agrees that bigger changes get less effective review. Defect detection is significantly higher on small changes. Review comments thin out as files are added: each extra file cuts the odds of any comment by about 8.7%. Files later in the list get less attention. The widely quoted "200–400 LOC per review, under 500 LOC/hour, 60–90 minutes" thresholds come from a SmartBear/Cisco vendor study and should be labeled as such. The closest peer-reviewed analogue is Kemerer & Paulk's PSP finding that review rate matters, with about 200 LOC/hour recommended. At Google, most changes are already small (median 24 lines).

### Cited Findings
- **SmartBear/Cisco [VENDOR, IND].** A 10-month case study of the Cisco MeetPlace team: 2,500 reviews, 50 developers, 3.2M LOC. Recommendations: review no more than 200–400 LOC at a time, keep the inspection rate under 300–500 LOC/hour, and spend no more than 60–90 minutes. SmartBear says a 200–400 LOC review over 60–90 minutes "should yield 70-90% defect discovery", and reports a "significant drop in defect density at rates faster than 500 LOC per hour". The study is vendor-authored (Jason Cohen / SmartBear) and was not peer reviewed — [SmartBear best practices](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/); [StickyMinds summary](https://www.stickyminds.com/article/largest-case-study-code-reviews-ever)
- The same SmartBear page also says "Do not review for more than 60 minutes at a time" and that lightweight reviews take "less than 20% the time of formal reviews" while finding as many bugs. The page gives no per-condition data. [VENDOR] — [SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- **Kemerer & Paulk, "The Impact of Design and Code Reviews on Software Quality: An Empirical Study Based on PSP Data," IEEE TSE 35(4):534–550, 2009** [STU/trainee PSP class data]. Review rate is a significant factor in defect-removal effectiveness. Secondary summaries cite about 200 LOC/hour as the effective rate. I could not retrieve the abstract text to confirm the exact wording or yield percentages — [TSE index](https://ftp.math.utah.edu/pub/tex/bib/idx/ieeetranssoftweng2000/35/4/534_550.html); [PSP-related summary](https://idm.fing.edu.uy/sites/default/files/biblio/12126/analysiscodedefects-psp.pdf)
- **Baum, Schneider & Bacchelli, "Associating working memory capacity and code change ordering with code review performance," EMSE 2019** [LAB, mostly IND participants]
  - Setting: 50 participants (46 professionals). Median time was 84 minutes. Each participant reviewed one small change and two large changes from jEdit with seeded defects. Sizes as shown on screen: small = 2 files, 3 change parts, 31 LOC; large A = 7 files, 15 parts, 490 LOC; large B = 7 files, 21 parts, 233 LOC.
  - Result: effectiveness is "significantly larger for small code changes". McNemar tests on defects found in the small vs. large review gave p = 0.001–0.012 across four hypothesis variants.
  - Dropout: 24 participants dropped out during the first large review and 13 during the second, which suggests large reviews are themselves a fatigue and attrition risk.
  - Source: [arXiv/full text via figshare materials](https://figshare.com/articles/Online_Material_for_Associating_Working_Memory_Capacity_and_Code_Change_Ordering_with_Code_Review_Performance_/5808609); [ZORA record](https://www.zora.uzh.ch/entities/publication/245eb643-3ebd-476c-a613-8097ff6d9582)
- **Sadowski et al., "Modern Code Review: A Case Study at Google," ICSE-SEIP 2018** [IND]
  - Data: about 9M changes by more than 25,000 authors and reviewers (Jan 2014–Jul 2016), about 13M comments, 12 interviews, and a 44-respondent survey.
  - Change size: over 35% of changes modify a single file, about 90% modify fewer than 10 files, over 10% modify a single line, and the median is 24 lines modified. Rigby & Bird reported medians of 44 lines at AMD and 263 lines at Lucent, so Google's median is lower.
  - Latency: median time to initial feedback is under an hour for small changes and about 5 hours for very large changes. Overall median review latency is under 4 hours.
  - Reviewers: fewer than 25% of changes have more than one reviewer, and the median reviewer count is 1.
  - Time spent: developers review an average of 3.2 hours/week (median 2.6 h/week), against 6.4 h/week self-reported elsewhere.
  - The paper summarizes earlier work: the number of useful comments decreases and review latency increases as change size grows.
  - Source: [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)
- **Rigby & Bird, "Convergent Contemporary Software Peer Review Practices," ESEC/FSE 2013** [IND+OSS]
  - Projects: Android, Chrome, Bing, Office, MS SQL, and AMD, compared with Lucent inspection data and six OSS projects.
  - Convergent practices: changes are small, reviews happen early and quickly, and two reviewers find an "optimal" number of defects.
  - Peer review increases the number of distinct files a developer knows about by 66–150%.
  - Median time to approval was 14.7–19.8 h at Microsoft, 15.7 h for Chrome OS, and 17.5 h at AMD (as quoted by Sadowski et al.).
  - Source: [MSR page](https://www.microsoft.com/research/publication/convergent-software-peer-review-practices/); [Sadowski et al.](https://research.google/pubs/modern-code-review-a-case-study-at-google/)
- **Rahman, Codabux & Roy, "Does Order Matter? …File Ordering on Code Review Effectiveness," arXiv 2026** [OSS; preprint, not yet peer reviewed]
  - Data: 330,343 multi-file PRs and 756,814 file instances in 182 GitHub projects across five languages.
  - "Each additional modified file reduces the odds of receiving any review comment by about 8.7%."
  - Latent bug rates rise from 56.7% at file position 1 to 61.5% at position 30.
  - PRs with about 10 files had the lowest defect risk; very small and very large PRs had elevated risk.
  - Source: [arXiv 2609.22610](https://arxiv.org/abs/2609.22610)
- **Barnett et al., "Helping Developers Help Themselves: Automatic Decomposition of Code Review Changesets," ICSE 2015** [IND, Microsoft Bing/Office]. The median review touches 12 changed methods and 24 diff regions, and over 25% of reviews modify 23+ methods across 45+ diff regions. The authors read this as many review changes being "large and/or difficult to understand" — [Barnett et al. (MSR)](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/)
- **Kononenko et al., ICSME 2015** [OSS, Mozilla]. 54% of reviewed changes still introduced bugs (identified with SZZ). Personal factors (reviewer workload, experience) and participation factors are associated with review quality — [UWaterloo SWAG](https://swag.uwaterloo.ca/publications/investigating-code-review-quality-do-people-and-participation-matter.html)
- Sadowski et al. also cite a Mozilla survey in which developers say size-related factors have the greatest effect on review latency — [Sadowski et al.](https://research.google/pubs/modern-code-review-a-case-study-at-google/)

### Inferences
- A diff-to-review-page tool should report size in the units reviewers actually feel: files, change parts or diff hunks, and LOC visible on the new side. Baum's 233-LOC change was harder than the 490-LOC one because it was algorithmically denser, so LOC alone misleads.
- The roughly 400 LOC / 60–90 min guidance is a reasonable default for a "this PR exceeds one sitting" warning. The tool should cite it as a vendor heuristic, not a law. Peer-reviewed support exists for the direction of the effect: smaller is better, and faster is less effective.
- Files-touched is a stronger attention-dilution signal than LOC (the 8.7% per-file drop in comment odds). Triage and ordering matter more as file count grows.

### Gaps
- No peer-reviewed study replicates the specific "200–400 LOC" breakpoint with modern pull requests. The figure traces to the SmartBear/Cisco vendor study (published in Cohen's book *Best Kept Secrets of Peer Code Review*, 2006).
- I could not retrieve Kemerer & Paulk's exact abstract numbers (defect-yield percentages at 200 LOC/hour).
- Baum's other review-size papers (e.g., on the size–effectiveness relationship across companies) were not located in this pass.

## Q2. Tangled and composite changes: how common are they and what do they cost reviewers?

### Takeaway
Between 7% and 42% of changes mix multiple concerns, depending on project and definition. Practitioners at Microsoft explicitly ask for decomposition. Controlled experiments find that decomposition improves review correctness or precision: fewer false issues, and more correct answers in one student study. Neither experiment showed a gain in defect detection or speed.

### Cited Findings
- **Herzig & Zeller, "The Impact of Tangled Code Changes," MSR 2013**, and **Herzig, Just & Zeller, EMSE 2016** (tangled changes and defect prediction) [OSS, 5 Java projects]. Between 7% and 20% of bug fixes consist of multiple tangled changes. At least 16.6% of source files are incorrectly associated with bug reports. Untangling improved defect-prediction accuracy by 5% to 200% — [MSR 2013 PDF](https://www.st.cs.uni-saarland.de/publications/files/herzig-msr-2013.pdf); [EMSE 2016 (MSR page)](https://www.microsoft.com/en-us/research/publication/the-impact-of-tangled-code-changes-on-defect-prediction-models/)
- **Tao & Kim, "Partitioning Composite Code Changes to Facilitate Code Review," MSR 2015** [OSS + STU]
  - Prevalence: of 453 manually inspected changes (Ant, Commons Math, Xerces, JFreeChart), "up to 29% and on average 17% are composite."
  - User study [STU, n = 18: 2 undergraduates, 10 Master's, 6 PhD]: reviewing "by slice" (partitioned) vs. "by file" gave mean correctness 9.40 vs. 7.94 (one-tailed paired t-test p = 0.01).
  - Time did not differ significantly: 40.60 vs. 35.92 min mean, p = 0.81.
  - The partitioner produced unsatisfactory partitions for 31% of changes.
  - Source: [Tao & Kim MSR 2015](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)
- **Tao, Dang, Xie, Zhang & Kim, "How Do Software Engineers Understand Code Changes? An Exploratory Study in Industry," FSE 2012** [IND, Microsoft; survey + interviews]. Engineers find it hard to get key information about a change: its completeness, its consistency, and especially "the risk imposed by it on other software components". For composite changes, it is valuable to decompose them into sub-changes aligned with individual issues, but "such decomposition lacks tool support" — [MSR publication page](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/)
- **Barnett, Bird, Brunet & Lahiri, ICSE 2015 (ClusterChanges)** [IND, Microsoft Bing/Office]
  - Prevalence: "over 40% of changes submitted for review at Microsoft can be potentially decomposed". Only 45% of changesets have exactly one non-trivial partition, and nearly 42% have more than one.
  - Author annotations of changes in the review tool occur "less than 5% of the time in practice".
  - User study (20 developers): most agreed with the automatic partitioning and found it useful for understanding.
  - Source: [Barnett et al.](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/)
- **di Biase, Bruntink, van Deursen & Bacchelli, "The effects of change decomposition on code review — a controlled experiment," PeerJ CS 2019 (arXiv 1805.10978)** [LAB, n = 28, mix of professionals and graduate students]. Decomposition "leads to fewer wrongly reported issues" and increases context-seeking. It "impacts neither understanding the change rationale nor the number of found defects." The authors still recommend separating commits by concept — [PeerJ CS](https://peerj.com/articles/cs-193/); [arXiv](https://arxiv.org/abs/1805.10978)
- **Ram et al., FSE 2018** [IND, Mozilla]. Practitioners name "coherent commit history" as a reviewability factor — [TU Delft record](https://serg.ewi.tudelft.nl/publications/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/)
- **Bacchelli & Bird 2013** [IND]. A reviewer complained about descriptions where "people can say they are doing one thing, while they are doing many more of them." A description that hides tangling actively misleads — [ICSE 2013 PDF](https://sback.it/publications/icse2013.pdf)

### Inferences
- Detecting and visibly grouping independent concerns (refactor vs. behavior change vs. tests vs. formatting) is well supported by practitioner demand. The measured benefits are lower noise and better correctness or precision, not raw speed. Frame it as "fewer false alarms and clearer rationale," not "faster reviews."
- The tool should flag a mismatch between the PR description and the detected concerns.
- Automatic partitioning is imperfect (31% unsatisfactory in Tao & Kim). Groupings should be explainable and overridable; Baum's Principle 6 makes the same point.

### Gaps
- I did not verify the survey and interview sample sizes for Tao et al. FSE 2012. I also did not verify its specific percentages (e.g., how many respondents found composite changes hard).
- Kirinuki et al. (tangled-change detection in Japanese industry/OSS) was not retrieved.
- No study found here quantifies review time cost per extra concern in a tangled PR.

## Q3. Missing rationale or intent, and unfamiliar code, as comprehension barriers

### Takeaway
Understanding the change, and especially *why* it was made, is the main challenge reviewers report. Unfamiliarity with the touched files slows nearly everyone down: 91% of Microsoft respondents said so. Reviewers who know the code give deeper, more actionable feedback. The change description, size, and a coherent history are the top practitioner-rated reviewability factors.

### Cited Findings
- **Bacchelli & Bird, "Expectations, Outcomes, and Challenges of Modern Code Review," ICSE 2013** (2025 SIGSOFT Impact Award) [IND, Microsoft]
  - Data: 17 observed and interviewed developers across 16 teams, 570 review comments card-sorted, and surveys of 165 managers and 873 programmers (44% response rate).
  - Defect comments are only 14% of comments (4th of 9 categories), mostly small logic issues. Code-improvement comments are the most frequent at 29%.
  - Understanding is the key challenge. Interviewee quotes: "the most difficult thing when doing a code review is understanding the reason of the change" and "the biggest information need in code review: what instigated the change."
  - The survey ranks finding defects as the outcome needing the most understanding.
  - 798 respondents (91%) said reviewing unfamiliar files takes longer, because reviewers must learn the files' "purpose, invariants, APIs."
  - When the reviewer owns the changed files, feedback is "deeper," "more directed," and "more actionable," and finds "more subtle issues."
  - Source: [ICSE 2013 PDF](https://sback.it/publications/icse2013.pdf)
- **Ram, Sawant, Castelluccio & Bacchelli, "What makes a code change easier to review: an empirical investigation on code change reviewability," ESEC/FSE 2018** [IND, Mozilla]. Methods: a literature and grey-literature review, 10 interviews with professional developers, and a deployed tool with which professional developers rated the reviewability of 98 changes. Reviewability is defined by factors including the change description, size, and coherent commit history — [TU Delft](https://serg.ewi.tudelft.nl/publications/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/); [Mozilla Foundation listing](https://www.mozillafoundation.org/en/research/library/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/)
- **Pascarella, Spadini, Palomba, Bruntink & Bacchelli, "Information Needs in Contemporary Code Review," CSCW 2018** [OSS]. Manual analysis of 900 review comments from 3 large OSS projects identified seven high-level information needs. One example is knowing the uses of methods and variables declared or modified in the change — [TU Delft](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review)
- **Tao et al., FSE 2012** [IND, Microsoft]. Completeness, consistency, and risk to other components are important information needs that are hard to acquire — [MSR](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/)
- **Kononenko, Baysal & Godfrey, "Code Review Quality: How Developers See It," ICSE 2016** [SURVEY, 88 Mozilla core developers]. Review quality is mainly associated with thoroughness of feedback, the reviewer's familiarity with the code, and perceived code quality. Challenges include keeping skills up to date, managing priorities, and context switching — [UWaterloo](https://swag.uwaterloo.ca/publications/code-review-quality-how-developers-see-it.html)
- **Sadowski et al. 2018** [IND]. Often only one reviewer is needed because authors frequently hold ownership or readability for the files. Familiarity is built into Google's reviewer assignment — [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)
- **Barnett et al. 2015** [IND]. Developers say they understand composite changes better when authors annotate them, but annotation happens less than 5% of the time — [MSR](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/)

### Inferences
- The best-supported features address "why": a synthesized intent or rationale summary at the top, links to the issue, and a per-group "what this part does and why" annotation. They fill a need practitioners rank first but authors rarely meet (under 5% annotate).
- For unfamiliar reviewers, the page should surface the purpose, invariants, and APIs of touched files, plus callers and uses of modified symbols (Pascarella's need). That is the context Microsoft respondents said they spend time acquiring.
- A risk rating should include "impact on other components" (callers, dependents), since Tao et al. found this the hardest information to get.

### Gaps
- I did not verify the names and frequencies of Pascarella's seven needs. From memory they include suitability of an alternative solution, correct understanding, rationale, code context, necessity, specialized expertise, and splittability; confirm against the paper.
- I did not retrieve the ranked factor list or quantitative ratings from Ram et al. (e.g., the share of the 98 changes rated reviewable).
- Gonçalves et al. on review difficulties and competencies (e.g., "Competencies for Code Review," CSCW 2023) was not retrieved.

## Q4. Cognitive load, working memory, change-part ordering, and checklists

### Takeaway
Working memory capacity predicts finding *delocalized* defects, those whose evidence spans several places, but barely predicts other defect types. Review time is a stronger factor. Order matters. Theory says to group related parts and show needed information first. A large observational study plus an experiment show that files presented later get fewer comments, and defects in the last file were found with 64% lower odds. Developers deviate from alphabetical order in about 45% of PRs. Checklists help modestly and depend on the task: a guided checklist suits simple reviews, and a plain checklist suits complex ones.

### Cited Findings
- **Baum et al., EMSE 2019** [LAB, 50 participants, 46 professionals; working memory measured for 45]
  - There is a moderate association between working memory capacity and effectiveness at finding delocalized defects, and almost none for other defect types.
  - "Even for delocalized defects, working memory capacity is only one of several factors, of which the strongest is review time."
  - The order of presenting change parts showed "a tendency" to influence efficiency, but "cannot conclude this reliably."
  - Source: [figshare materials](https://figshare.com/articles/Online_Material_for_Associating_Working_Memory_Capacity_and_Code_Change_Ordering_with_Code_Review_Performance_/5808609); [ZORA](https://www.zora.uzh.ch/entities/publication/245eb643-3ebd-476c-a613-8097ff6d9582)
- **Baum, Schneider & Bacchelli, "On the Optimal Order of Reading Source Code Changes for Review," ICSME 2017** [IND interviews + survey of 201 reviewers; produces a theory]. "An optimal order is mainly an optimal grouping of the change parts by relatedness." Its principles:
  - (1) Group related change parts as closely as possible, to avoid context switches. 76% of survey respondents with a preference chose closeness.
  - (2) Provide information before it is needed.
  - (3) When (1) and (2) conflict, prefer grouping.
  - (4) Closely related parts form chunks.
  - (5) The closest distance is "visible on the screen at the same time."
  - (6) Use rules the reviewer can understand, and make the grouping explicit.
  - "Keep commits self-contained" is a special case of (1) plus (6).
  - Source: [Merlin UZH](https://www.merlin.uzh.ch/publication/show/15587); [figshare](https://figshare.com/articles/Online_material_for_On_the_Optimal_Order_of_Reading_Source_Code_Changes_for_Review_/5236150/1)
- **Fregnan, Braz, D'Ambros, Çalikli & Bacchelli, "First Come First Served: The Impact of File Position on Code Review," ESEC/FSE 2022** [OSS mining + LAB]
  - Mining 219,476 PRs from 138 Java projects: files earlier in the PR receive more comments, controlling for confounders.
  - Experiment (n = 106): participants had "64% lower odds to identify" a defect when the defective file was last rather than first. One defect type showed no position effect.
  - Source: [arXiv 2208.04259](https://arxiv.org/abs/2208.04259)
- **Bouraffa, Brandt, Zaidman & Maalej, "Not One to Rule Them All: Mining Meaningful Code Review Orders From GitHub," EASE 2025** [OSS]
  - Data: 23,241 PRs in 100 Java/Python repos. Reviewers comment in non-alphabetical order in 44.6% of PRs.
  - Among those, 20.6% follow largest-diff-first, 17.6% follow similarity to the PR title and description, and 29% of PRs with both production and test files follow test-first.
  - Non-alphabetical reviews covered a significantly higher proportion of files.
  - Source: [TU Delft repository PDF](https://repository.tudelft.nl/file/File_08e6d8bc-a310-418b-bf8d-e04cb000023e) (DOI 10.1145/3756681.3756961)
- **Rahman, Codabux & Roy, "Breaking the Alphabet: Rethinking File Ordering in Code Review," ICSE 2026 (arXiv 2609.04207)** [SURVEY; reported as 1,355 developers across 182 OSS projects, a figure from the fetched summary that I could not cross-check]. Only 10.2% consider alphabetical ordering optimal. 57.6% say it increases context switching and review fatigue, 63.9% worry it causes missed bugs, and 66% want customizable or dependency-aware ordering — [arXiv](https://arxiv.org/abs/2609.04207)
- **Gonçalves, Fregnan, Baum, Schneider & Bacchelli, "Do explicit review strategies improve code review performance? Towards understanding the role of cognitive load," EMSE 2022** (Registered Report at MSR 2020) [LAB, n = 70 professional developers; ad hoc vs. checklist vs. guided checklist]
  - A guided checklist (step-by-step: what, where, when) was more effective for a simple review.
  - A plain checklist supported efficiency and effectiveness on a complex task. The guided checklist constrained reviewers' own navigation there.
  - There was no strong overall relationship between guidance and performance.
  - Source: [Springer EMSE](https://link.springer.com/10.1007/s10664-022-10123-8); [MSR 2020 RR](https://2020.msrconf.org/details/msr-2020-Registered-Reports/6/Do-Explicit-Review-Strategies-Improve-Code-Review-Performance-); [GU summary](https://metrics.blogg.gu.se/?p=747)
- **Tao & Kim 2015** [STU]. Presenting slices instead of files raised correctness from a mean of 7.94 to 9.40 (p = 0.01) with no time difference — [Tao & Kim](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)

### Inferences
- Default file order should not be alphabetical. The evidence supports dependency- or relatedness-grouped order, putting needed information first (declarations or interfaces before uses; tests adjacent to the code they test), with the grouping labeled explicitly. High-risk files should go early, given the position effect.
- Delocalized defects are where working memory is the bottleneck. Showing related distant parts side by side, or "visible at the same time" (Principle 5), directly targets that load.
- Checklists should be short and contextual (tied to the change type), not a long rigid procedure, especially for complex PRs.

### Gaps
- Rong et al.'s checklist studies (which I believe used student participants) were not retrieved, so their effect sizes are unverified.
- Gonçalves et al. did not report specific effect sizes in the material I saw. Consult the EMSE paper.
- No study found here tests an *automatically generated* reading order against alphabetical order in a controlled experiment with professionals. Baum's EMSE 2019 ordering effect was inconclusive.

## Q5. Where reviewers look: eye tracking, review speed vs. defect detection, and fatigue

### Takeaway
Eye-tracking studies, mostly small lab samples, consistently find an initial "scan" of the whole code. Reviewers who scan too briefly take longer to find defects. Experts alternate between global scanning and focused inspection. Biometric studies can detect regions that were not reviewed well. Peer-reviewed evidence on fatigue over session length is thin. The 60–90 minute limit is vendor-sourced, though large-review dropout in Baum's experiment and survey reports of alphabetical-order fatigue point the same way.

### Cited Findings
- **Uwano, Nakamura, Monden & Matsumoto, "Analyzing Individual Performance of Source Code Review Using Reviewers' Eye Movement," ETRA 2006** [LAB, small sample]. They identified a "scan" pattern. Reviewers who did not spend enough time on the scan took more time to find defects on average. Later authors note that a small sample and the eye trackers of the time limited validity — [NAIST repository](https://naist.repo.nii.ac.jp/record/10579/files/R006972.pdf); [OTH Regensburg summary](https://opus4.kobv.de/opus4-oth-regensburg/frontdoor/index/index/year/2021/docId/1313)
- **Sharif, Falcone & Maletic, "An eye-tracking study on the role of scan time in finding source code defects," ETRA 2012, pp. 381–384** [LAB]. Replicated Uwano with more participants and varied expertise, testing whether the scan pattern holds and how experience affects review effectiveness and efficiency — [ACM ETRA 2012 (via search)](https://ixdf.org/literature/author/bonita-sharif)
- **Begel & Vrzakova, "Eye movements in code review," EMIP@ETRA 2018** [LAB, Microsoft Research] — [EMIP 2018 proceedings](https://ris.uni-paderborn.de/record/15588)
- **Holistic model of visual perception for code review (University of Turku), 2023** [LAB, n = 23: 15 novices, 8 experts; six short C programs]. Experts' review splits into phases, switching between global scanning and focal examination of errors — [Turku](https://research.utu.fi/converis/portal/detail/Publication/499173240?lang=en_US)
- **Hijazi et al., "Quality Evaluation of Modern Code Reviews Through Intelligent Biometric Program Comprehension," IEEE TSE (ICSE 2023 journal-first)**, and **"iReview," ISSRE 2021** [LAB]. They used heart-rate variability, task-evoked pupillary response, and a desktop eye tracker to estimate reviewer cognitive load and identify code regions that were not well reviewed — [ICSE 2023 JF](https://conf.researchr.org/details/icse-2023/icse-2023-journal-first-papers/8/Quality-Evaluation-of-Modern-Code-Reviews-Through-Intelligent-Biometric-Program-Compr); [CISUC](https://www.cisuc.uc.pt/haitham-hijazi-at-the-hannover-messe-2022)
- **"Exploring Social Signals in Code Review: An Eye-Tracking Study of Urgency and Reputation Effects," ICPC 2024** [LAB, n = 37, Java patches]. Perceived PR priority affected time spent and cognitive load, and participants were largely unaware of the effect — [ICPC 2024](https://conf.researchr.org/details/icpc-2024/icpc-2024-research/10/Exploring-Social-Signals-in-Code-Review-An-Eye-Tracking-Study-of-Urgency-and-Reputat)
- **Review speed vs. detection:** Kemerer & Paulk (TSE 2009) find review rate significant for defect removal [PSP class data]. SmartBear finds defect density drops above about 500 LOC/hour [VENDOR] — [TSE index](https://ftp.math.utah.edu/pub/tex/bib/idx/ieeetranssoftweng2000/35/4/534_550.html); [SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- **Review time as the strongest factor:** in Baum EMSE 2019, review time was the strongest predictor of finding delocalized defects, stronger than working memory capacity [LAB] — [figshare](https://figshare.com/articles/Online_Material_for_Associating_Working_Memory_Capacity_and_Code_Change_Ordering_with_Code_Review_Performance_/5808609)
- **Fatigue signals:**
  - SmartBear advises sessions of no more than 60 minutes [VENDOR].
  - In Baum EMSE 2019, 24 participants dropped out during the first large review and 13 during the second [LAB].
  - 57.6% of surveyed developers say alphabetical ordering increases context switching and fatigue [SURVEY, preprint/ICSE 2026].
  - Kononenko 2016 respondents cite context switching as a key challenge [SURVEY].
  - Sources: [SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/); [arXiv 2609.04207](https://arxiv.org/abs/2609.04207); [Kononenko 2016](https://swag.uwaterloo.ca/publications/code-review-quality-how-developers-see-it.html)

### Inferences
- An "overview first" section (map of the change, intent, groups) supports the scan phase that eye-tracking links to faster defect finding. Reading-path features should then support focused inspection of the risky parts.
- Estimates of how long a review will take ("this PR is about N minutes of focused review") and suggested split points are a reasonable response to the speed–effectiveness trade-off. Thresholds should be labeled heuristic.

### Gaps
- I did not verify participant counts and quantitative results for Uwano 2006 (I believe about 5 participants), Sharif 2012, and Begel & Vrzakova 2018.
- I found no peer-reviewed study that measures defect-detection decline as a function of minutes into a modern code review session. The 60–90 minute figure remains vendor-sourced.
- "Chandrika et al." (eye tracking in code review) was not located in a reliable venue. The search hit was a low-visibility journal listing, so I did not use it.

## Q6. Reviewer expertise and familiarity effects on speed and quality

### Takeaway
Familiarity with the changed files is consistently associated with faster, deeper, more useful review: owners give "more subtle" feedback, and 91% of respondents say unfamiliar files take longer. Reviewer workload and experience are associated with whether reviewed changes later prove buggy (Mozilla). Novices benefit more from structured guidance.

### Cited Findings
- **Bacchelli & Bird 2013** [IND]. 91% (798/873) say unfamiliar files take longer to review. When reviewers have prior knowledge of the context and code, "they complete reviews more quickly and provide more valuable feedback" — [ICSE 2013](https://sback.it/publications/icse2013.pdf)
- **Kononenko, Baysal, Guerrouj, Cao & Godfrey, ICSME 2015** [OSS, Mozilla]. 54% of reviewed changes introduced bugs. Reviewer workload and experience, and the number of participating developers, are associated with review quality — [UWaterloo](https://swag.uwaterloo.ca/publications/investigating-code-review-quality-do-people-and-participation-matter.html)
- **Kononenko et al., ICSE 2016** [SURVEY, n = 88 Mozilla]. Familiarity with the code is one of the main determinants of perceived review quality — [UWaterloo](https://swag.uwaterloo.ca/publications/code-review-quality-how-developers-see-it.html)
- **Gonçalves et al., EMSE 2022** [LAB, n = 70]. Inexperienced reviewers found more errors in simple code with a step-by-step guided checklist — [GU summary](https://metrics.blogg.gu.se/?p=747); [Springer](https://link.springer.com/10.1007/s10664-022-10123-8)
- **Turku 2023 eye-tracking** [LAB, 15 novices vs. 8 experts]. Experts show phased global/focal viewing — [Turku](https://research.utu.fi/converis/portal/detail/Publication/499173240?lang=en_US)
- **Rigby & Bird 2013** [IND+OSS]. Review spreads knowledge: developers know 66–150% more distinct files — [MSR](https://www.microsoft.com/research/publication/convergent-software-peer-review-practices/)

### Inferences
- The page should adapt to reviewer familiarity. For first-time reviewers of an area it should expand context (module purpose, invariants, owners) and offer a more guided checklist. Experts get a compact view.
- The tool can flag "reviewer unfamiliar with these files" as a risk modifier for the review, since unfamiliarity predicts slower and shallower feedback.

### Gaps
- Thongtanunam et al.'s reviewer-expertise and "Review Dynamics" papers (e.g., MSR/ICSE 2015–2017 on reviewer workload, participation, and defect-proneness) were not retrieved in this pass. Their specific numbers are unverified.
- No study found here measures the speed difference in minutes between familiar and unfamiliar reviewers. Bacchelli & Bird's 91% is self-report.
- No recent (2020–2026) systematic review numbers were extracted: Davila & Nunes JSS 2021, and Badampudi et al. TOSEM 2023, which may be the same as arXiv 2103.08777. Those SLRs would help confirm consensus.
