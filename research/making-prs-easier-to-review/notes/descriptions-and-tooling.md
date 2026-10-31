# PR Descriptions, Rationale, and Review Tool/Visualization Support: Evidence

Notes compiled 2026-10-08. Evidence labels: **[FIELD]** = mined repositories / production deployment; **[LAB]** = controlled experiment; **[SURVEY]** / **[QUAL]** = survey, interview, think-aloud; **[TOOL-PROPOSED]** = tool built, no measured effect on review outcomes; **[TOOL-EVAL]** = tool evaluated with a measured effect. Numbers marked "(fetched summary)" came from an automated summary of the full text and should be checked against the PDF before quoting in final copy.

## (a) How PR description quality and stated rationale/intent affect review

### Takeaway
Rationale (the "why") and a clear statement of purpose are consistently among reviewers' top information needs. They are also often missing: about 34% of GitHub PRs have empty descriptions, and about 44% of commit messages could be improved. The newest large-scale evidence (MSR 2026, 80K PRs) finds that not all description elements count equally. Telling reviewers *what kind of feedback you want* is the element most predictive of merge and reviewer engagement. AI-assisted descriptions (Copilot for PRs, FSE 2024) are associated with about 19 hours less review time and 1.57x higher merge odds. All of this is observational, though: no RCT isolates the effect of description quality.

### Cited Findings

**Rationale and purpose as information needs**
- Tao, Dang, Xie, Zhang, Kim, "How Do Software Engineers Understand Code Changes? An Exploratory Study in Industry," FSE 2012 (Microsoft; large-scale survey + interviews) [SURVEY/QUAL]. Engineers find it hard to get key information about a change: its completeness, its consistency, and "especially the risk imposed by it on other software components." Breaking a composite change into sub-changes, each tied to one development issue, is valuable, but that "currently ... lacks tool support." — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/); [PDF](https://www.cse.ust.hk/%7Ehunkim/papers/tao-fse2012.pdf)
- Pascarella, Spadini, Palomba, Bruntink, Bacchelli, "Information Needs in Contemporary Code Review," PACM HCI (CSCW) 2018 [QUAL: analysis of review threads in open-source projects + interviews]. The paper studies what information reviewers need to review properly, as a basis for tool support. — [TU Delft](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review); [SERG page](https://serg.ewi.tudelft.nl/publications/information-needs-in-contemporary-code-review/)
- Ram, Sawant, Castelluccio, Bacchelli, "What Makes a Code Change Easier to Review," ESEC/FSE 2018 [literature + gray-literature review; 10 professional developer interviews; reviewability-rating tool used by professional developers on 98 changes, Mozilla]. Reviewability depends on several factors, "such as the change description, size, and coherent commit history." — [TU Delft SERG](https://serg.ewi.tudelft.nl/publications/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/); [Mozilla Foundation](https://www.mozillafoundation.org/en/research/library/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/)
- Wurzel Gonçalves, Rani, Storey, Spinellis, Bacchelli, "Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories," arXiv 2025 [QUAL: 10 experienced reviewers, 25 real reviews, think-aloud; changes from 2 to 34,520 lines; GitHub/GitLab/Phabricator/Gerrit]. Reviewers used the PR title/description in 84% of reviews, the issue tracker in 44%, and PR discussion in 40% (fetched summary). Traceability across issue, title, description and commit messages supports top-down mental-model building. Alignment meetings with the author before review greatly reduced comprehension effort. — [arXiv 2503.21455](https://arxiv.org/html/2503.21455)

**Description completeness, elements, and outcomes**
- Pirouzkhah, Wurzel Gonçalves, Bacchelli, "The Value of Effective Pull Request Description," MSR 2026 [FIELD + SURVEY]. A gray-literature review produced a taxonomy of 8 recommended elements: purpose, reason, code explanation, link to issue, type of feedback needed, file review order guidance, test explanation, screenshots. Screenshots were excluded from the quantitative analysis as context-dependent. Dataset: 80K PRs across 156 GitHub projects in 5 languages; survey of 57 valid respondents. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1); [MSR 2026 program](https://2026.msrconf.org/details/msr-2026-technical-papers/35/The-Value-of-Effective-Pull-Request-Description)
  - Prevalence (fetched summary): purpose 54.5%, code explanation 55.4%, link to issue 45.2%, feedback type 16.2%, test explanation 13.7%, file review order 6.1%. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
  - Developers value purpose and code explanation for preserving rationale and history. But *stating the desired feedback type* best predicts acceptance and reviewer engagement. Merge OR ≈ 1.72 for feedback type and ≈ 1.21 for code explanation; purpose and test explanation were negligible (fetched summary). Feedback type was also associated with more review comments and with *longer* latency, consistent with more engagement. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
  - File-review-order guidance appeared in only 6.1% of PRs and was associated with *lower* merge odds (OR ≈ 0.35, fetched summary). This is likely confounded: authors add such guidance to large or complex PRs. Treat it as a correlation, not as evidence that guidance hurts. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
  - Descriptions are more common in mature projects and complex changes, which suggests authors write them when they are most useful rather than as a formality. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
- Liu, Xia, Treude, Lo, Li, "Automatic Generation of Pull Request Descriptions," ASE 2019 (ACM SIGSOFT Distinguished Paper) [TOOL-EVAL on ROUGE + human evaluation; not on review outcomes]. More than 34% of 333K collected PRs had empty descriptions. Their pointer-generator seq2seq model with RL optimization of ROUGE, trained on 41K PRs from commit messages and added code comments, beat the baselines. — [ar5iv 1909.06987](https://ar5iv.labs.arxiv.org/html/1909.06987); [ASE 2019](https://www.se.cs.uni-saarland.de/conferences/ASE/ase2019/details/ase-2019-papers/28/Automatic-Generation-of-Pull-Request-Descriptions.html)
- Xiao, Hata, Treude, Matsumoto, "Generative AI for Pull Request Descriptions: Adoption, Impact, and Developer Interventions," FSE 2024 / PACMSE [FIELD, quasi-experimental]. Design: 18,256 Copilot-for-PRs PRs across 146 repos vs 54,188 control PRs from the same repos; propensity-score weighting with entropy balancing over 17 confounders. Result: review time down by 19.3 h (median 12.17 h treated vs 16.09 h control); merge odds ratio 1.57 (95% CI 1.35–1.84, p<0.001). — [arXiv HTML](https://arxiv.org/html/2402.08967v1); [FSE 2024](https://2024.esec-fse.org/details/fse-2024-research-papers/105/Generative-AI-for-Pull-Request-Descriptions-Adoption-Impact-and-Developer-Interven)
  - Developers frequently edit generated content. Across 1,437 revisions in 311 PRs: deletion 22.9%, refinement 20.8%, exclusion 17.4%, replacement 14.7%, rearrangement 12.3%, augmentation 6.0%. The most used tags were `copilot:summary` (13,231) and `copilot:walkthrough` (8,990). The authors recommend adding the tags to PR templates. — [arXiv HTML](https://arxiv.org/html/2402.08967v1)
- Tian, Zhang, Stol, Jiang, Liu, "What Makes a Good Commit Message?" ICSE 2022 [QUAL + classifier]. A good message explains both *what* changed and *why*. In ~1,600 messages from 5 highly active OSS projects, "circa 44% of messages could be improved." Message quality affects communication among developers, and uncurated datasets threaten commit-message generators. — [arXiv 2202.02974](https://arxiv.org/abs/2202.02974)
- An arXiv 2026 preprint, "Predicting Acceptance and Review Effort in Human and Agent Pull Requests," reports that text and metadata variables, especially body length and title length, rank above most raw diff-size measures for predicting acceptance. Weak evidence: preprint, seen in a search snippet only, full text not read. — [arXiv 2607.12057](https://arxiv.org/html/2607.12057v1)

### Inferences
- A generated "brief" should prioritize three things: (1) purpose and why, which developers value most and which preserves rationale; (2) an explicit "what feedback I want / where to look" section, the strongest outcome predictor in Pirouzkhah 2026 yet present in only 16% of PRs; (3) a test explanation, present in only 14% of PRs. These are the gaps a tool can fill.
- The Copilot-for-PRs results suggest machine-drafted descriptions are not harmful and may speed review. Authors edit about half of them, so the UI should make the generated text editable and attributable rather than final.
- Rationale cannot be recovered from the diff alone. A tool should pull it from linked issues, commit messages and the author's prompt or conversation, and should flag "why: unknown" rather than make it up.

### Gaps
- I couldn't get Pascarella 2018's full text (the PDF link 404'd), so the exact list of seven information-need categories and their frequencies is not verified here.
- I couldn't get Tao 2012's percentages (the PDF returned 403). It is commonly cited as finding rationale the most important need, but I did not verify this.
- No RCT manipulates description quality while holding the code fixed. All description-outcome links are correlational or quasi-experimental.
- I did not locate the Zanaty/Hassan or "Rahman et al." description-quality papers named in the brief. Treat those references as unverified.
- Yu et al., "Wait For It" (MSR 2015), on PR latency determinants appeared in search results ([PDF](https://cmustrudel.github.io/papers/msr15.pdf)), but I did not read its description-related coefficients.

## (b1) Author self-annotation / author-provided guidance

### Takeaway
Direct evidence on authors annotating their own diffs is thin. The best quantitative proxies are two elements from Pirouzkhah 2026. "File review order" guidance is rare (6%) and associated with worse merge odds, probably confounded. "Type of feedback needed" is strongly positive. Wurzel Gonçalves 2025 finds that pre-review alignment with the author cuts comprehension effort.

### Cited Findings
- Author guidance is rare in practice: suggested file review order 6.1% of 80K PRs, requested feedback type 16.2% (fetched summary). — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
- Requesting a specific feedback type is associated with merge OR ≈ 1.72 and more review comments (fetched summary). — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)
- In think-aloud observations, pre-alignment meetings with authors greatly reduced the comprehension effort reviewers needed. — [arXiv 2503.21455](https://arxiv.org/html/2503.21455)
- Barnett, Bird, Brunet, Lahiri, ICSE 2015 (ClusterChanges, Microsoft) is literally titled "Helping developers help themselves": more than 40% of changes submitted for review at Microsoft could be decomposed into multiple partitions using def-use relationships between diff regions. [TOOL-EVAL, partial: it measured decomposability and developer feedback, not defect detection.] — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/); [Acolyer summary](https://blog.acolyer.org/2015/06/26/helping-developers-help-themselves-automatic-decomposition-of-code-review-changes/)

### Inferences
- Machine-generated "start here / review in this order / I want feedback on X" annotations fill an element that authors rarely write. Feedback-type requests have the strongest positive association, so prompt the author to supply one, or infer a default from risk.
- The negative OR for order guidance is a reason to A/B test any "suggested reading order" feature rather than assume it helps.

### Gaps
- I found no peer-reviewed study measuring the effect of authors' inline self-comments (Gerrit/Phabricator "author notes," GitHub self-review comments) on defects found or review time.
- I did not find the Microsoft CodeFlow studies on author annotations in this pass.

## (b2) Visualization and tool support with measured effects

### Takeaway
The strongest measured effects come from *ordering and decomposition*, not from fancy visuals. File position changes defect detection: 64% lower odds of finding a defect when its file is shown last [LAB, N=106]. Decomposing tangled changes cuts false reports but not missed defects [LAB, N=28]. Refactoring-aware diffs shrink the lines a reviewer must read by roughly 2–7x [small user study, N=8]. Nudging overdue PRs cut completion time 60% [FIELD RCT, Microsoft]. Most diagram or visualization review tools are tool-proposed papers with little outcome evidence.

### Cited Findings

**Ordering and decomposition**
- Fregnan, Braz, D'Ambros, Calikli, Bacchelli, "First Come First Served: The Impact of File Position on Code Review," ESEC/FSE 2022 [FIELD + LAB].
  - FIELD: in 219,476 PRs from 138 Java GitHub projects, files shown earlier receive more comments, after controlling for confounders such as discussion threads and lines added.
  - LAB (N=106): for one seeded defect, position had no effect. For the other, participants had 64% lower odds of finding it when its file was last rather than first.
  - [arXiv 2208.04259](https://arxiv.org/abs/2208.04259)
- Rahman, Codabux, Roy, "Breaking the Alphabet: Rethinking File Ordering in Code Review," ICSE 2026 [SURVEY: 1,355 developers, 182 OSS projects]. 10.2% consider alphabetical order optimal. 57.6% say it increases context switching and fatigue, and 63.9% worry about missing bugs because of it. 66% want customizable ordering; developers ask for dependency-aware grouping (fetched summary). — [arXiv 2609.04207](https://arxiv.org/abs/2609.04207)
- Di Biase, Bruntink, van Deursen, Bacchelli, "The effects of change decomposition on code review — a controlled experiment," PeerJ CS 2019 [LAB, N=28 professionals + graduate students]. Decomposition led to fewer wrongly reported issues and more context-seeking. It did not change understanding of the change rationale or the number of defects found. — [PeerJ](https://peerj.com/articles/cs-193/); [arXiv 1805.10978](https://arxiv.org/pdf/1805.10978)
- Baum, Schneider, Bacchelli, "Associating working memory capacity and code change ordering with code review performance," EMSE 24(4):1762–1798, 2019 [LAB, N=50, confirmatory]. The study tests working memory capacity, cognitive load, and a theory-predicted ordering of change parts against review performance. — [ZORA record](https://www.zora.uzh.ch/entities/publication/245eb643-3ebd-476c-a613-8097ff6d9582); [replication package](https://figshare.com/articles/Online_Material_for_Associating_Working_Memory_Capacity_and_Code_Change_Ordering_with_Code_Review_Performance_/5808609)
- Tao et al. FSE 2012: decomposing composite changes is valuable but lacked tool support (see above). — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/)

**Refactoring-aware and semantic diffs**
- Brito & Valente, "RAID: Tool Support for Refactoring-Aware Code Reviews," ICPC 2021 [TOOL-EVAL, small field study with 8 professional developers]. RAID uses RefDiff, runs in GitHub Actions, and adds a Chrome extension. Median lines to review fell from 14.5 to 2 for move refactorings and from 113 to 55 for extractions. Developers reported reduced cognitive effort. Weak evidence: N=8, and lines-to-review is a proxy rather than defects or time. — [arXiv 2103.11453](https://arxiv.org/abs/2103.11453v1)
- Alikhanifard & Tsantalis, "A Novel Refactoring and Semantic Aware AST Differencing Tool and a Benchmark," TOSEM 2024 [TOOL-EVAL on accuracy, not on review outcomes]. RefactoringMiner's AST diff reached 99.7% precision and 98.4% recall on their benchmark. GumTree 3.0 (simple) was second-best on multi-mappings at 59% precision and 10% recall. — [ACM DL](https://dl.acm.org/doi/10.1145/3696002); [arXiv 2403.05939](https://arxiv.org/pdf/2403.05939)
- Falleri et al., GumTree, "Fine-grained and accurate source code differencing," ASE 2014: GumTree edit scripts are reported as often more comprehensible than Unix diff. That judgment rests on a small manual evaluation, not a review-outcome experiment. — [ResearchGate](https://www.researchgate.net/publication/379791136_Fine-grained_accurate_and_scalable_source_differencing)
- Zhang, Song, Pinedo, Kim, "Interactive Code Review for Systematic Changes" (Critics), ICSE 2015 [TOOL-EVAL, LAB with students]. A study with 12 students on 24 Java review tasks measured comprehension with and without the interactive approach. I could not verify the effect sizes (see Gaps). — [PeerJ citing context](https://peerj.com/articles/cs-193/)

**Process and notification tooling (field RCT)**
- Maddila, Upadrasta, Bansal, Nagappan, Gousios, van Deursen, "Nudge: Accelerating Overdue Pull Requests Towards Completion," ACM TOSEM 2022 (not FSE) [FIELD RCT, Microsoft].
  - Nudge combines ML effort estimation, activity detection and actor identification.
  - In a randomized trial on 147 repos it cut resolution time by 60% for 8,500 PRs vs. un-nudged overdue PRs, and 73% of notifications were resolved as positive.
  - At scale it ran on 8,000 repos and sent 210,000 notifications in a year.
  - [arXiv 2011.12468](https://arxiv.org/pdf/2011.12468); [DOI 10.1145/3544791](https://api.crossref.org/works/10.1145%2F3544791)

**Visual content (screenshots and UI)**
- Pirouzkhah 2026 lists "Screenshots — provides visual evidence" among the 8 recommended description elements but excluded it from the outcome regressions as context-dependent. — [arXiv 2602.14611](https://arxiv.org/html/2602.14611v1)

### Inferences
- **Order files by risk or dependency, not alphabetically.** This is the best-supported design lever: lab plus field evidence that position affects defect detection, and a large survey showing demand. A review page that leads with the riskiest or core files, and groups by dependency, rests on solid evidence.
- **Collapse refactoring and move noise.** RAID-style refactoring-aware views and RefactoringMiner AST diffs cut reviewable lines a lot. RefactoringMiner is accurate enough (~99% precision) to rely on for Java. Outcome evidence on defects or time is still small-N.
- **Split tangled changes** into issue-aligned clusters. The expected benefit is fewer false alarms and better context-seeking, not more defects found (Di Biase 2019).
- **Treat diagrams and visual cards as unproven in review.** Present them as navigation aids and plan to measure them.

### Gaps
- I couldn't verify the Critics effect sizes. I recall reports of more correct answers in less time, but this is unverified.
- I couldn't verify the Baum 2019 ordering and working-memory results.
- I found no peer-reviewed empirical study of screenshots or images in PRs (frequency or effect on review). Searches returned only blogs and agent "PR screenshots" skills.
- I found no evidence for "ReviewViz." I did not obtain CoRT (Baum) evaluation data, CodeFlow or Critique feature evaluations, or a Google study of the "nudges" for code review.
- I found no controlled comparison of whitespace or moved-code suppression on defect detection.

## (c) Context retrieval: how much beyond the diff reviewers need

### Takeaway
Reviewers routinely leave the diff: in 84% of observed reviews they use the description, in 44% the issue tracker, plus CI, docs and tests. The hardest needs to meet are risk to other components, completeness and consistency, which require dependency or impact context the diff does not show. Decomposition increases context-seeking.

### Cited Findings
- Reviewers draw on context beyond the diff: PR title/description (84% of reviews), issue tracker (44%), PR discussion (40%), CI/CD status, commit messages, docs and testing tools. The authors recommend tools that support scoped reviewing, visually separate meaningful chunks, show how complexity is distributed, and integrate navigation with test environments (fetched summary). — [arXiv 2503.21455](https://arxiv.org/html/2503.21455)
- The hard-to-get needs are completeness, consistency, and "especially the risk imposed by it on other software components" (Microsoft). — [Microsoft Research](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/)
- Decomposition increased context-seeking in a controlled experiment. — [PeerJ](https://peerj.com/articles/cs-193/)
- Developers ask for dependency-aware grouping of files. — [arXiv 2609.04207](https://arxiv.org/abs/2609.04207)
- Sadowski et al., "Modern Code Review: A Case Study at Google," ICSE-SEIP 2018, is the canonical industry case study. I did not retrieve its specific latency or size numbers. — [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)

### Inferences
- An "impact / blast radius" card (callers of changed functions, affected tests, downstream modules) targets the single hardest-to-meet need found at Microsoft. It is supported by needs evidence, not yet by outcome experiments.
- Linking issue, commits and description into one traceable brief supports the top-down mental-model building observed in reviewers.

### Gaps
- I could not identify the "Gunawardena et al." context study named in the brief.
- I found no quantitative measure of *how much* surrounding context (lines, files, call depth) helps reviewers most.
- Vendor blogs on "context-aware AI review" (cubic, Graphite) are marketing, not evidence, and I excluded them.

## (d) Structured representations (schema/API diffs, architecture diagrams): measured comprehension benefits

### Takeaway
Outside code review, the classic controlled evidence (Arisholm et al., TSE 2006) shows UML documentation improves the correctness and design quality of *complex* maintenance changes, but saves no time. I found no study measuring schema/API-diff cards or architecture diagrams inside code review.

### Cited Findings
- Arisholm, Briand, Hove, Labiche, "The Impact of UML Documentation on Software Maintenance: An Experimental Evaluation," IEEE TSE 32(6):365–381, 2006 [LAB, controlled experiments at two sites]. For complex tasks, once past a learning curve, UML documentation "may result in significant improvements of the functional correctness of changes as well as their design quality." There was no time saving. For simple tasks, the cost of updating the UML can outweigh the benefits. — [Simula](https://www.simula.no/research/impact-uml-documentation-software-maintenance-experimental-evaluation)

### Inferences
- Diagrams and data-model/API cards are most likely to pay off on complex, cross-cutting changes, and should be suppressed or collapsed for small changes, where they add reading cost. Expect correctness gains, not speed gains. Because the tool generates the diagrams automatically, the "cost of updating UML" objection from Arisholm does not apply.

### Gaps
- I found no code-review-specific experiment on schema diffs, API surface diffs, architecture diagrams, or UI wireframes. This is an open research gap and a chance for the product to run its own evaluation, for example an A/B test of time-to-approve and post-merge defect rate.
- I did not retrieve more recent program-comprehension meta-analyses on diagrams (for example, UML comprehension systematic reviews after 2015).
