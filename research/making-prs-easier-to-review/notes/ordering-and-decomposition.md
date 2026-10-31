# Reading Order and Change Decomposition in Code Review: Effects on Speed, Understanding, and Defect Detection

Notes compiled 2026-10-08. Each finding is labeled with its evidence type: **[LAB]** controlled experiment, **[FIELD]** mining or field deployment, **[SURVEY]**/**[INTERVIEW]** perception data, **[THEORY]** theory with no direct outcome test, **[PREPRINT]** not yet peer reviewed (as far as I could verify).

---

## Q1. Does the order in which files and hunks are presented change review outcomes? (position effects, alphabetical defaults, theory of optimal order)

### Takeaway
File position has a real but modest effect, and the evidence for it is solid. Files shown earlier get more comments in the field, and in one lab experiment a defect in the last file had 64% lower odds of being found than the same defect in the first file. The best-supported theory (Baum et al. 2017) says a good order is mostly about *grouping related change parts together*, then giving information before it is needed. In the one experiment that tested this theory directly, "optimal" orders were only directionally better and the result was not statistically significant.

### Cited Findings

**Position effects (Fregnan et al., ESEC/FSE 2022)**
- Fregnan, Braz, D'Ambros, Çalikli, Bacchelli, "First Come First Served: The Impact of File Position on Code Review," ESEC/FSE 2022. They start from the observation that Gerrit and GitHub "present the files to review sorted in alphabetical order." — [arXiv 2208.04259](https://arxiv.org/abs/2208.04259)
- **[FIELD]** In 219,476 PRs from 138 popular Java projects on GitHub, files shown earlier in a PR received more review comments than files shown later. This held after controlling for confounders such as discussion threads and lines added per file. — [arXiv 2208.04259](https://arxiv.org/abs/2208.04259)
- **[LAB]** In an online experiment with 106 participants, two unrelated defects were seeded in two files, and the position of the defective files was swapped between treatments. One defect type showed no position effect. For the other, participants "have 64% lower odds to identify it when its file is last as opposed to first." — [arXiv 2208.04259](https://arxiv.org/abs/2208.04259)

**Industrial replication (Bagirov et al., EASE 2023, JetBrains)**
- **[FIELD]** In IntelliJ IDEA (a large industrial project), "reviewers leave more comments on the files shown higher in the code review." Ordering files by code-diff size placed problematic files (those needing more review effort) higher than alphabetical order did, "even with the data skewed toward Alphabetical order." The abstract gives no effect size. — [Bagirov, Derakhshanfar, Kalina, Kartysheva, Kovalenko, arXiv 2306.06956 / EASE 2023 Industry](https://arxiv.org/abs/2306.06956)

**What order reviewers actually follow (Bouraffa et al., EASE 2025)**
- **[FIELD]** In 23,241 PRs from 100 popular Java and Python GitHub repos (first review round only, bots and authors excluded), reviewers commented in **non-alphabetical order in 44.6%** of PRs. Among those:
  - **20.6%** (2,134) followed a largest-diff-first order.
  - **17.6%** (1,827) followed an order matching each file's similarity to the PR title and description.
  - **29%** (1,188) of PRs that touched both production and test files followed a **test-first** order.
  — [Bouraffa, Brandt, Zaidman, Maalej, "Not One to Rule Them All: Mining Meaningful Code Review Orders From GitHub," EASE 2025, arXiv 2506.10654](https://arxiv.org/pdf/2506.10654)
- **[FIELD]** Reviews deviate from alphabetical order more as PR size grows. From 3 reviewed files upward, non-alphabetical reviews are the majority. For 3 reviewed files, 77% of reviewers start by commenting on a file other than the alphabetically first one. For 10 files this drops to 49%. The authors read this as alphabetical order serving as a "fallback strategy" on larger reviews. — [Bouraffa et al. 2025 (TU Delft repository copy)](https://repository.tudelft.nl/file/File_08e6d8bc-a310-418b-bf8d-e04cb000023e)
- **[FIELD]** Non-alphabetical reviews covered a significantly higher share of the submitted files (reviewed files / total files) and received slightly fewer approvals on average. — [Bouraffa et al., arXiv 2506.10654](https://arxiv.org/pdf/2506.10654)

**Theory of optimal ordering (Baum, Schneider, Bacchelli, ICSME 2017)**
- **[THEORY + INTERVIEW + SURVEY]** "On the Optimal Order of Reading Source Code Changes for Review," ICSME 2017, pp. 329–340. Data: task-guided interviews with **12 professional developers** and an online survey with **201 valid respondents**. Central claim: "an optimal order is mainly an optimal grouping of the change parts by relatedness." The theory is formalized as a partial order over "tours", where a tour is a permutation of all change parts. — [Baum et al. 2017 PDF](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- **[SURVEY]** Reviewers mostly follow the tool's order even though they consider it sub-optimal. Of 132 respondents, **73%** start "often or always" with the change the tool shows first, and **66%** continue with whatever the tool shows next. 19% (32/167) review "often or always" together with the author. Experienced reviewers and users of IDE-integrated tools follow tool order less (always continuing in tool order: experienced 6/62 vs inexperienced 18/70; IDE-based 1/24 vs web-based 23/106). — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- **[INTERVIEW]** Interviewees were "neutral or negative" about alphabetical order. The review sessions analyzed had a median of 11.5 files per task, and about 54% had 10 or more files. — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- **The six principles** (verbatim headings from the paper) — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf):
  1. "Group related change parts as closely as possible." In the survey, 102 of 123 preferred related parts close together, vs 14 "not close" (Table II).
  2. "Provide information before it is needed." For call-flow (one callee, four callers), **111/130 (85%)** rated **bottom-up** (callee first) among the best tours. Top-down breadth-first: 35 best / 61 worst. Top-down depth-first: 34 best / 67 worst.
  3. "In case of conflicts between Principles 1 and 2, prefer Principle 1 (grouping)." 76% of respondents with a preference chose closeness over direction (82 vs 26).
  4. "Closely related change parts form chunks treated as elementary for further grouping and ordering." The chunking tour was preferred by 70% (35/50) in one question and 76% (38/50) in another.
  5. "The closest distance between two change parts is 'visible on the screen at the same time.'"
  6. "To satisfy the other principles, use rules that the reviewer can understand. Support this by making the grouping explicit to the reviewer." A tour with "no sensible rule" was rated among the worst by **112/130 (86%)**.
- **[INTERVIEW]** Macro structure. Start with the requirements and context, and use a usage example such as a test case for overview. Observed opening tactics:
  - T1: something easy.
  - T2: a natural entry point (GUI, servlet, CLI).
  - T3: the most important parts.
  - T4: new things.
  - T5: parts that "don't fit in."

  Endings were either a wrap-up via a test or usage example, or "the unimportant rest" at the end. Relation types reviewers cited: data flow, call flow, class hierarchy, declare & use, file order, similarity, logical dependencies, development flow. Interviewees split on top-down vs bottom-up for call flow, while survey respondents favored bottom-up. The authors conclude that "a simple global rule of 'always prefer bottom-up/top-down' probably does not exist." — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- **[THEORY]** "Keep commits self-contained" is framed as a special case of Principle 1 combined with Principle 6, since a commit is an explicit group of related change parts. — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)

**Experimental test of the theory (Baum, Schneider, Bacchelli, EMSE 2019)**
- **[LAB]** "Associating Working Memory Capacity and Code Change Ordering with Code Review Performance," *Empirical Software Engineering* 24(4):1762–1798, 2019. A confirmatory experiment with **50 participants**, mostly professional developers, reviewing one small and two larger changes with seeded defects. — [Baum et al. EMSE 2019 preprint](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)
- **[LAB]** Ordering result. They compared theory-"optimal" vs "worst" orders, each in a variant that keeps file boundaries and one that ignores them (OF, ONF, WF, WNF). Differences in median efficiency (defects/hour) went "in the direction predicted by theory, but subject to a lot of variation." Conclusion: "Strong statistically significant conclusions cannot be drawn. An effect of better change part ordering on review efficiency may exist, but its strength is highly dependent on the respective orders." Participants' qualitative comments blamed the worse orders, e.g. "pure code chaos" and "jumps between algorithm and implementation parts." — [Baum et al. EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)
- **[LAB]** Working memory: Kendall τB = 0.24 (p = 0.0186) between working memory span and **delocalized** defects found. For all defects, τB = 0.05 (p = 0.31), and for localized defects it was about −0.01. Review effectiveness was significantly higher for the small change than for the larger ones. Longer review time was associated with more defects found. — [Baum et al. EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)

**2026 work on alphabetical ordering (Rahman, Codabux, Roy)**
- **[SURVEY]** "Breaking the Alphabet: Rethinking File Ordering in Code Review," listed in the ICSE 2026 research track. Survey of **1,355 professional developers** across 182 OSS projects:
  - Only **10.2%** consider alphabetical ordering optimal.
  - **57.6%** say it increases context switching and fatigue.
  - **63.9%** worry it may make them miss bugs.
  - **66%** requested customizable ordering and dependency-aware grouping.

  — [arXiv 2609.04207](https://arxiv.org/abs/2609.04207); [ICSE 2026 listing](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/310/Breaking-the-Alphabet-Rethinking-File-Ordering-in-Code-Review). (Note: the arXiv ID format suggests a late-2026 posting, while the fetched page said "submitted May 22, 2026." Treat the venue and date as reported but unconfirmed.)
- **[FIELD][PREPRINT]** "Does Order Matter? An Empirical Investigation into the Impact of File Ordering on Code Review Effectiveness," same authors, arXiv Sept 2026. Data: 330,343 multi-file PRs, 756,814 file instances, 182 projects, 5 languages. Results:
  - The latent-bug rate rises with file position, from 56.7% at position 1 to 61.5% at position 30. This is statistically significant but very weak: Cohen's d = 0.044, Cramér's V = 0.062.
  - Each additional file in a PR lowers the odds that a given file gets any comment (OR = 0.91).
  - Buggy files receive more comments (OR = 1.17) yet still show up in later bug-fixing commits. The authors call this an "attention-effectiveness gap."

  — [arXiv 2609.22610](https://arxiv.org/html/2609.22610)

### Inferences
- Position bias is real and replicated (OSS GitHub, an industrial JetBrains project, a lab experiment), but the per-file effect is small. The 64% lower-odds result held for only one of two defect types. Moving the riskiest files to the top is a cheap mitigation the evidence supports, but it will not transform outcomes.
- Reviewers already deviate from alphabetical order on larger PRs and fall back to it as size grows. A suggested reading path is most valuable on large PRs, which is also where reviewers are least able to build one themselves.
- Baum's principles convert directly into design rules for a "where to look, in order" feature:
  - Cluster related hunks (P1).
  - Inside a cluster, order declarations and callees before uses and callers by default (P2, bottom-up preferred 85%).
  - Never break a cluster to satisfy direction (P3).
  - Treat tight clusters as units (P4).
  - Show related hunks side by side when possible (P5).
  - **Label each group and explain why it is in that position** (P6). Any order that looks arbitrary is rated worst.
- Ordering is supported mainly by perception data and weak lab evidence. It is not proven to raise defect detection on its own. Present it as reducing navigation cost and the risk of late-file neglect, not as a proven defect-finding boost.

### Gaps
- No controlled experiment I found compares alphabetical against an automated dependency-grouped or risk-first order with adequate statistical power. Baum EMSE 2019 was underpowered and inconclusive.
- Bagirov et al.'s full quantitative comparison (metric values for diff-order vs alphabetical) was not available in the abstract I accessed.
- No study I found measures *hunk-level* ordering within a file, as opposed to file-level ordering, in the field.
- The two 2026 Rahman/Codabux/Roy papers: peer-review status of "Does Order Matter?" is unverified, and its latent-bug measure (bug-fixing commits later touching the file) is an indirect proxy.

---

## Q2. Tests first, explicit strategies, and guided review: do reading strategies change outcomes?

### Takeaway
Reviewing tests first (Test-Driven Code Review) does **not** reduce production-bug detection. It roughly doubles the share of test-code bugs found, at the cost of far fewer production maintainability issues found, so it trades one kind of finding for another. Explicit checklists and guidance give mixed results: simple guidance helps on simple reviews, while heavy guidance can add cognitive load.

### Cited Findings
- **[LAB + SURVEY]** Spadini, Palomba, Baum, Hanenberg, Bruntink, Bacchelli, "Test-Driven Code Review: An Empirical Study," ICSE 2019, pp. 1061–1072. Online experiment with 92 developers after exclusions (93 recruited), 77 with at least two years of professional experience, about 180 reviews of two JPacman patches. Treatments: TF (test-first), PF (production-first), OP (only production). Plus 9 interviews and a 103-respondent survey. — [Spadini et al. 2019, TU Delft repository](https://repository.tudelft.nl/file/File_8d21a720-18e1-4621-b700-6a2b207e669d?preview=1)
- **[LAB]** Mean proportion found, by treatment (Table V). OP had no test code, so it has no test columns.

  | Treatment | Prod bugs | Prod maintainability | Test bugs | Test maintainability | Time |
  |---|---|---|---|---|---|
  | TF | 0.28 | 0.08 | **0.40** | 0.18 | 7m11s |
  | PF | 0.33 | 0.21 | 0.17 | 0.13 | 6m27s |
  | OP | 0.28 | 0.18 | n/a | n/a | 5m29s |

  Wilcoxon tests were significant (p < 0.01) only for production maintainability issues (Cliff's delta medium) and test bugs (small). Review time did not differ significantly. — [Spadini et al. 2019](https://repository.tudelft.nl/file/File_8d21a720-18e1-4621-b700-6a2b207e669d?preview=1)
- **[LAB]** Regression with controls: TF had **71% lower odds** of finding a production maintainability issue (exp(−1.25) = 0.29) and **3.49× the odds** of finding a test bug. The specific patch had a very strong effect, so code differences dominate. External raters (κ = 0.69–1.0) found no difference in review comment quality across treatments. — [Spadini et al. 2019](https://repository.tudelft.nl/file/File_8d21a720-18e1-4621-b700-6a2b207e669d?preview=1)
- **[SURVEY]** Few developers do this in practice. 5% always start from test code, 13% almost always, 42% sometimes, 27% almost never, 13% never. Developers prefer production code first "as they deem it more critical." Poor test quality and missing tool support hinder adoption. — [Spadini et al. 2019](https://repository.tudelft.nl/file/File_8d21a720-18e1-4621-b700-6a2b207e669d?preview=1); [SERG summary](https://serg.ewi.tudelft.nl/publications/test-driven-code-review-an-empirical-study/)
- **[FIELD]** Test-first appears in 29% of OSS PRs that touch both test and production files and have non-alphabetical commenting. — [Bouraffa et al. EASE 2025](https://arxiv.org/pdf/2506.10654)
- **[INTERVIEW]** Baum 2017 interviewees suggested opening and closing with a usage example, such as a test case, for overview and wrap-up. — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- **[LAB]** Gonçalves, Fregnan, Baum, Schneider, Bacchelli, "Do explicit review strategies improve code review performance? Towards understanding the role of cognitive load," *EMSE* 27(4):99, 2022 (registered report from MSR 2020). Professional developers, mostly novice reviewers, were assigned to ad hoc, checklist, or "guided checklist" (a checklist plus an explicit strategy using segmenting and weeding to lower cognitive load). Result: the guided checklist was more effective for a simple review, and the plain checklist supported efficiency and effectiveness on the complex task. However, the authors "did not identify a strong relationship between the guidance provided and code review performance." I could not retrieve the participant count or effect sizes. — [Springer DOI 10.1007/s10664-022-10123-8](https://link.springer.com/10.1007/s10664-022-10123-8); [summary via search of ZORA/UZH record](https://www.zora.uzh.ch/entities/publication/12e91b80-1a51-4659-bfaf-47727928286e)
- **[COMMENTARY]** A secondary commentary on Gonçalves et al. says guidance can raise cognitive demand and be counterproductive, shorter checklists beat longer ones, and code understanding was the dominant factor. — [Staron, metrics.blogg.gu.se](https://metrics.blogg.gu.se/?p=747) (secondary source)
- **[FIELD/LAB, industrial]** At WirelessCar, upfront AI-led reviews (summaries plus findings) were "overall more preferred" than on-demand LLM assistance, but acceptance depended on the reviewer's codebase familiarity and the PR's severity. — [Aðalsteinsson et al., "Rethinking Code Review Workflows with LLM Assistance," arXiv 2505.16339](https://arxiv.org/abs/2505.16339)

### Inferences
- "Tests first" works as an option or toggle, not as a default. It shifts attention toward test bugs and away from production maintainability. A tool could offer a "tests as spec" entry point (Baum's usage-example opening) for behavior changes, while keeping production code in the main path.
- Strategy guidance should be lightweight. Heavy checklists add load, so a reading path should be short, labeled, and skippable.

### Gaps
- Gonçalves et al. EMSE 2022: exact N, per-treatment defect rates, and cognitive-load (NASA-TLX) numbers were not retrievable (Springer paywall redirect).
- No experiment found on "interfaces before implementations" as a specific ordering. It is supported only indirectly, through Baum's Principle 2 and the bottom-up / declaration-before-use survey preferences.
- No controlled study found of LLM-generated reading paths.

---

## Q3. Does decomposing (untangling) a change into coherent parts improve review speed, understanding, or defect detection?

### Takeaway
Decomposition reliably **reduces noise** (fewer false-positive review comments) and is strongly preferred by developers. In two small lab studies it improved correctness on comprehension questions. It has **not** been shown to find more defects or to speed up review: both lab studies found no time savings.

### Cited Findings
- **[LAB]** Tao & Kim, "Partitioning Composite Code Changes to Facilitate Code Review," MSR 2015. Design: **18 CS students** (2 undergrad, 10 MSc, 6 PhD), within-subjects, 12 composite changes, reviewing either "by file" or "by slice."
  - Correctness score: mean 7.94 by file vs **9.40 by slice** (about +18%), one-tailed paired t-test **p = 0.01**.
  - Time: 35.9 min by file vs 40.6 min by slice, **p = 0.81** (no difference). The authors attribute the slight increase to learning the unfamiliar slice UI.
  - "In a similar amount of time, participants answered code review questions significantly better."

  — [Tao & Kim MSR 2015 PDF](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)
- **[FIELD]** Prevalence in the same paper: of 453 changes from Ant, Commons Math, Xerces, and JFreeChart, **17% on average and up to 29%** (JFreeChart) were composite (8–29% per project). Their heuristic partitioner matched the human partition on 54/78 (**69%**) composite changes, 53–76% per project. — [Tao & Kim 2015](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)
- **[FIELD + INTERVIEW]** Barnett, Bird, Brunet, Lahiri, "Helping Developers Help Themselves: Automatic Decomposition of Code Review Changesets," ICSE 2015 (Microsoft, Bing and Office).
  - ClusterChanges uses def-use relationships to split diff regions into "non-trivial" partitions and "trivial" partitions (in-method or single-region).
  - In 1,000 changesets, 45% had exactly one non-trivial partition and **about 42% had more than one**, so "over 40%" of review changes could potentially be decomposed.
  - On average 66% of changed lines per review fall in non-trivial partitions.
  - Authors annotating changes in the review tool happened "less than 5% of the time."

  — [Barnett et al. ICSE 2015 PDF](https://cabird.com/pdfs/barnett2015helping.pdf); [Microsoft Research copy](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/barnett2015hdh.pdf)
- **[INTERVIEW, field setting]** Barnett et al. interviewed **20 developers from 13 projects** about their *own* changes:
  - **16/20** said the non-trivial partitions were correct and complete. 2 said there should have been only one partition. 2 said some trivial partitions should be grouped.
  - 14 of the 16 would have moved up to 3 trivial changes into partitions. Missed relations were mostly interface-method usage, XML-referenced entities, and event-framework calls.
  - 7 participants said they should have split, or did split, their commits along the suggested partitions.
  - All were positive about the concept. 6 said it is especially useful for large changes. 8 suggested assigning reviewers per partition. 5 said it reduces time spent understanding across contexts.
  - One participant asked for partitions "ordered so that the most important" come first. Another complained about directory-ordered presentation.

  This is perception data only; no outcome was measured. — [Barnett et al. 2015](https://cabird.com/pdfs/barnett2015helping.pdf)
- **[FIELD replication]** JClusterChanges (an open-source Java reimplementation) replicated Barnett et al. on 1,000 GitHub Java PRs. — [Springer chapter, "Automatic Decomposition of Java Open Source Pull Requests: A Replication Study"](https://link.springer.com/chapter/10.1007/978-3-319-73117-9_18); [Freire dissertation, UFCG 2016](https://bdtd.ufcg.edu.br/jspui/bitstream/riufcg/765/3/VICTOR%20DA%20CUNHA%20LUNA%20FREIRE%20-%20DISSERTA%c3%87%c3%83O%20%28PPGCC%29%202016.pdf) (I did not retrieve the specific replication percentages.)
- **[LAB]** di Biase, Bruntink, van Deursen, Bacchelli, "The effects of change decomposition on code review — a controlled experiment," *PeerJ Computer Science* 5:e193, 2019. **28 developers** (professionals and graduate students), between-subjects 14 vs 14. One tangled PR vs the same change split into two coherent PRs, reviewed in GitHub's web UI. — [PeerJ](https://peerj.com/articles/cs-193/); [arXiv 1805.10978](https://arxiv.org/pdf/1805.10978)

  | Measure (14 vs 14) | Tangled (control) | Untangled (treatment) | p |
  |---|---|---|---|
  | Defects found, total | 20 | 17 | 0.6, not significant |
  | **False positives**, total | **6** | **1** | **0.03**, Cliff's d = 0.36 (medium) |
  | Suggested improvements, total | 7 | 19 | 0.4, not significant |
  | Review net time, median | 831 s | 759 s | 0.66, not significant |

  No difference was found in understanding of the change rationale. The untangled group showed **more context-seeking** (opening called or referenced files), and the authors link this to their higher precision. Recommendation: "commits belonging to different concepts should be separated." — [arXiv 1805.10978](https://arxiv.org/pdf/1805.10978)
- **[FIELD]** Tangling prevalence:
  - Herzig & Zeller (MSR 2013): up to **15% of bug fixes** in five Java OSS projects consist of tangled changes, and at least **16.6%** of source files are wrongly associated with bug reports because of tangling. — [Herzig & Zeller MSR 2013 PDF](https://www.st.cs.uni-saarland.de/publications/files/herzig-msr-2013.pdf)
  - SmartCommit's related work cites Nguyen et al.: 11–39% of bug-fix commits include other changes. — [Shen et al. FSE 2021](https://www.cs.cmu.edu/~ckaestne/pdf/fse21_sc.pdf)
  - Atomizer cites 11–40% across studies. — [Atomizer, arXiv 2601.01233](https://arxiv.org/html/2601.01233v1)

### Inferences
- The most reliable benefit of decomposition is **precision**: fewer wrong comments, more context-seeking, more suggestions. Recall (defects found) and speed are not improved. Pitch decomposition as "clearer, less noisy review," not "faster review."
- Both outcome studies are small (n = 18 students, n = 28) and used a single change or a few changes. The evidence is promising, not conclusive.
- Barnett et al.'s misses (interface usage, XML/config references, event wiring) show that static def-use grouping misses cross-artifact relations. A tool should add heuristics for config and code links and let users merge groups.

### Gaps
- No large-scale field study measuring defect escape or review latency with vs without automatic decomposition shown to reviewers.
- Barnett et al. did not measure review time or defects; their helpfulness evidence is interview-based.
- I did not retrieve numbers for Dias et al. EpiceaUntangler (SANER 2015), Kirinuki et al. (ICPC 2014/2016), or Kreutzer et al.'s C3 (MSR 2016); they are cited only through Atomizer's related work.

---

## Q4. Automatic untangling and clustering techniques, 2015–2026, including LLM-based

### Takeaway
Accuracy has improved from heuristic and def-use approaches (about 69% acceptable partitions), through graph clustering (Flexeme about 0.81 accuracy on C#; SmartCommit 71–84% median), to learned and LLM multi-agent methods (UTango, ColaUntangle, Atomizer at ICSE 2026). Nearly all evaluations use **synthetic tangled commits** and partition-accuracy metrics. None measures downstream review outcomes.

### Cited Findings
- **[FIELD + LAB]** Shen, Zhang, Kästner, et al., "SmartCommit: A Graph-Based Interactive Assistant for Activity-Oriented Commits," ESEC/FSE 2021.
  - Graph with 4 link types: Hard (def-use), Soft (similarity), Refactoring, and Cosmetic.
  - Field deployment with **83 engineers over 9 months** at a large international IT company, in two teams: Android music app (32 devs) and cloud platform (51 devs).
  - Median accuracy 74.70% and 70.45% in the two teams. **Over 60% of generated groups were accepted without adjustment**, with 3.41 manual operations on average.
  - On 3,000 synthetic composite commits from 10 OSS projects: median accuracy 71.00–83.50%, under 5 s in 90% of cases.

  — [Shen et al. FSE 2021 PDF](https://www.cs.cmu.edu/~ckaestne/pdf/fse21_sc.pdf)
- **[LAB, synthetic]** Pârtachi, Dash, Allamanis, Barr, "Flexeme: Untangling Commits Using Lexical Flows," ESEC/FSE 2020. Builds a δ-NFG (a multiversion graph of name flows) and clusters it with graph similarity. Accuracy **0.81** on a C# corpus. — [UCL AAM PDF](https://discovery-pp.ucl.ac.uk/10107163/2/Barr_Flexeme-%20Untangling%20Commits%20Using%20Lexical%20Flows_AAM.pdf); [FSE listing](https://2022.esec-fse.org/details/fse-2022-esec-fse-2020/11/Flexeme-Untangling-Commits-Using-Lexical-Flows)
- **[LAB, synthetic]** Li, Nguyen et al., "UTANGO: Untangling Commits with Context-Aware, Graph-Based, Code Change Clustering Learning Model," ESEC/FSE 2022. Supervised clustering over learned change embeddings. On C# (1,612) and Java (14k) tangled commits, it reports 28.6%–462.5% and 13.3%–100.0% relative accuracy gains over prior approaches. — [NJIT PDF](https://web.njit.edu/~yl622/publications/[FSE'22]UTANGO_untangling_commits_with_context-aware,graph-based,code_change_clustering_learning_model.pdf); [ACM DL](https://dl.acm.org/doi/pdf/10.1145/3540250.3549171)
- **[LAB, synthetic][LLM]** Hou, Tan, Zheng, Liu, Zhu, Zhang, "LLM-Driven Collaborative Model for Untangling Commits via Explicit and Implicit Dependency Reasoning" (ColaUntangle), arXiv 2507.16395, 2025; the search index lists a TOSEM DOI 10.1145/3822177. Multi-agent LLM design: one agent for explicit dependencies (control and data flow), one for implicit (semantic) dependencies, and a reviewer agent that reconciles them. Reports **+44% (C#) and +82% (Java)** over the best baseline on the same C# 1,612 and Java 14k datasets. — [arXiv 2507.16395](https://arxiv.org/abs/2507.16395); [CiteDrive TOSEM record](https://www.citedrive.com/en/discovery/llm-driven-collaborative-model-for-untangling-commits-via-explicit-and-implicit-dependency-reasoning/)
- **[LAB, synthetic][LLM]** Zhu, Tian, Wang, Leng, Mao, "Atomizer: An LLM-based Collaborative Multi-Agent Framework for Intent-Driven Commit Untangling," **ICSE 2026**. Uses intent-oriented chain-of-thought plus a grouper–reviewer refinement loop.
  - Beats HD-GNN, the prior graph state of the art, by about 6.0–6.5% (C#) and 5.5% (Java) on changed-statement accuracy, and by over 16% on complex commits (more than 7,000 nodes).
  - Relative gains of +11.6% over UTango and +22.2% over Flexeme on C#.
  - About 57% average accuracy on the C# dataset under its metric.

  — [arXiv 2601.01233](https://arxiv.org/html/2601.01233v1); [ICSE 2026 listing](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/245/Atomizer-An-LLM-based-Collaborative-Multi-Agent-Framework-for-Intent-Driven-Commit-U)
- **[TOOL, no evaluation]** Open-source "pr-splitter" summarizes each hunk with an LLM, embeds the hunks in a vector DB, groups similar hunks, and creates one commit and PR per group. — [scour.ing listing of github.com/DiffEnder/pr-splitter](https://scour.ing/p/https://github.com/DiffEnder/pr-splitter)
- **[TOOL]** Barnett's ClusterChanges (def-use, C#) and Tao & Kim's heuristic partitioner (formatting-only isolation, dependency, and similarity heuristics; 69% acceptable) are the review-oriented baselines. — [Barnett et al. 2015](https://cabird.com/pdfs/barnett2015helping.pdf); [Tao & Kim 2015](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)

### Inferences
- A pragmatic stack for a diff-to-review-page tool, consistent with SmartCommit's design and its 60%+ zero-edit acceptance:
  1. Start with deterministic signals: def-use/call graph, same-symbol, rename/move/refactoring detection, formatting-only isolation, test↔source pairing.
  2. Use an LLM pass only to name groups and merge "implicit/semantic" relations, as ColaUntangle and Atomizer do.
  3. Let users adjust the grouping.
- Accuracy numbers (57–84%) mean roughly 1 in 4 to 1 in 3 groupings will be imperfect. Groups should be presented as suggestions with visible rationale (Baum P6), never hiding files.

### Gaps
- No untangling paper since 2019 that I found measures the effect on *review* outcomes (defects, time). They evaluate partition accuracy on synthetic composites made by merging consecutive commits, which may not represent real tangling.
- No peer-reviewed evaluation found of LLM-based *PR splitting for reviewers* or LLM-generated reading order. Only tools and blog posts exist.

---

## Q5. Splitting large PRs, separating refactorings, and stacked diffs: measured effects

### Takeaway
Smaller and focused changes are reviewed more *effectively* in experiments (Baum 2019), and refactoring-aware diffs shrink what must be read. But a large MSR study found PR size does **not** predict time-to-merge, and the first field study of Gerrit relation chains (stacks) found that chained changes take **2.6× longer** to merge than comparable solo changes. Rigorous evidence that stacking speeds review is absent.

### Cited Findings
- **[LAB]** Review effectiveness is significantly larger for small code changes than for larger ones; this was confirmed with 50 participants. — [Baum et al. EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)
- **[FIELD]** Kudrjavets, Nagappan, Rastogi, "Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation," MSR 2022. Across 845,316 PRs from 100 GitHub projects in 10 languages, plus 401,790 Gerrit and Phabricator reviews, "pull request size and composition do not relate to time-to-merge." — [arXiv 2203.05045](https://arxiv.org/abs/2203.05045)
- **[FIELD][PREPRINT]** Belhouchette, Chouchen, Chaieb, Hamdaqa, Hamou-Lhadj, "How Developers Use Relation Chains in Gerrit-Based Review Ecosystems," arXiv July 2026. Data: 29,580 relation chains, 15 repos, OpenStack/Wikimedia/ONAP, 401,256 changes.
  - Chains make up 5–49% of changes per project and are increasing in 14 of 15 projects.
  - Chain changes take a **median 2.6× longer to merge** than comparable solo changes.
  - 33.5% of chain members change during review.
  - Review activity on the base change correlates with activity on its descendants (ρ = 0.43–0.61).

  — [arXiv 2607.20189](https://arxiv.org/abs/2607.20189)
- **[LAB]** di Biase et al. 2019: splitting one tangled PR into two coherent PRs did not change review time (median 831 s vs 759 s, p = 0.66) or defects found, but reduced false positives (6 → 1, p = 0.03). — [arXiv 1805.10978](https://arxiv.org/pdf/1805.10978)
- **[INTERVIEW]** In Barnett et al. 2015, 7 of 20 Microsoft developers said they should have split, or did split, their commits along the suggested partitions. — [Barnett et al. 2015](https://cabird.com/pdfs/barnett2015helping.pdf)
- **[FIELD]** Brito & Valente, "RAID: Tool Support for Refactoring-Aware Code Reviews," ICPC 2021. Field use by 8 professional developers over 3 months. Lines to review fell from a median of 14.5 to 2 for move refactorings and from 113 to 55 for extractions, and the authors report reduced cognitive effort for reviewing refactorings. — [arXiv 2103.11453](https://arxiv.org/abs/2103.11453v1)
- **[FIELD]** SmartCommit models "Refactoring Links" and "Cosmetic Links" as separate relation categories so they can be split off from behavioral changes. — [Shen et al. FSE 2021](https://www.cs.cmu.edu/~ckaestne/pdf/fse21_sc.pdf)
- **[INDUSTRY]** Meta, "Improving Code Review Time at Meta" (2022). This covers review routing, not decomposition:
  - "Next Reviewable Diff" raised review actions per day by 17%.
  - A stale-diff "Nudgebot" cut Time In Review by 7% and diffs waiting more than 3 days by 12%.
  - Better reviewer recommendation raised diffs reviewed within 24 h by 1.5%.

  The post gives no stacked-diff or diff-size effects. — [Meta Engineering blog](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)
- **[FIELD, industry][PREPRINT]** Meta RADAR (2026) risk-stratifies whole diffs (ML Diff Risk Score plus LLM review) to auto-approve low-risk ones.
  - Over 535K diffs reviewed and 331K landed.
  - Revert rate is 1/3 and production-incident rate 1/50 of non-RADAR diffs.
  - Median diff review wall time is 35% lower.

  This is relevant as precedent for risk-based triage, but it works at diff level, not per file. — [arXiv 2605.30208](https://arxiv.org/abs/2605.30208)
- **[VENDOR / WEAK]** Vendor blogs (Graphite and others) claim small PRs are approved about 3× faster and that defect detection drops about 70% above 1,000 lines. These are not peer-reviewed and the methodology is opaque. — [Graphite guide](https://graphite.com/guides/stacked-diffs); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/stacked-diffs)

### Inferences
- Splitting buys **review quality and comprehension**, not wall-clock merge speed. Merge time is dominated by waiting and coordination (Meta's routing gains, Kudrjavets' null result, and the stack overhead in Gerrit).
- Separating refactorings and moves has the most concrete measured payoff on reading volume (RAID: median 113 → 55 lines for extractions). A review page should collapse or flag pure moves, renames, and formatting as low-attention groups.
- "Stacked PRs" is a heavily promoted practice with very thin outcome evidence. The only quantitative field study found suggests coordination costs. Don't claim stacked diffs speed up review.

### Gaps
- No peer-reviewed study found of Phabricator or Meta stacked diffs with review-outcome measures. Meta's public posts don't quantify stacking.
- No study found where reviewers chose between a split and a single PR for the same change. di Biase is the closest, but it was between-subjects with no preference measure.
- The relation-chains preprint's 2.6× merge time is confounded: chains may correlate with harder or bigger features. Peer review is pending.

---

## Q6. Which ordering and triage heuristics are evidence-backed? (synthesis for a "where to look, in order" feature)

### Takeaway
Ranked by strength of evidence:
1. **Don't bury important files late** (position bias: field + lab).
2. **Group related hunks and label the groups** (theory + survey + decomposition lab results).
3. **Declarations and callees before uses and callers** (survey preference: 85% bottom-up).
4. **Largest-diff or risk-first for the top slot** (industrial field comparison, and what reviewers do naturally).
5. **Tests first only as an option** (lab trade-off).
6. **Separate refactorings and formatting** (field tool study).

No single global order is supported. Reviewers vary.

### Cited Findings
- Position bias exists in both field (219,476 PRs) and lab (64% lower odds for the last file on one defect type). Placing likely-defective files early is directly supported. — [Fregnan et al. 2022](https://arxiv.org/abs/2208.04259)
- Diff-size order outperformed alphabetical in placing problematic files early in IntelliJ IDEA review data. — [Bagirov et al. 2023](https://arxiv.org/abs/2306.06956)
- Reviewers naturally use largest-diff-first (20.6%), similarity to the PR description (17.6%), and test-first (29% of mixed PRs) when they leave alphabetical order. — [Bouraffa et al. 2025](https://arxiv.org/pdf/2506.10654)
- The literature-derived candidate orders are: test-first, largest-diff-first, usage example / entry point first (UI, CLI, tests), salient class / most similar to description, and defect-prone / important first. — [Bouraffa et al. 2025, Table 1](https://repository.tudelft.nl/file/File_08e6d8bc-a310-418b-bf8d-e04cb000023e)
- Grouping beats direction (76%); bottom-up along call flow is preferred (85%); arbitrary orders are rated worst (86%); make groups explicit and named. — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- Some reviewers use importance or defect-proneness as the main ordering criterion, while others don't. A lot of the variation between interviewees came from how they judged importance. — [Baum et al. 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)
- Delocalized defects depend on working memory (τB = 0.24). Keeping cross-file related parts adjacent or on screen together (Principle 5) targets exactly this defect class. — [Baum et al. EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)
- 66% of surveyed developers want customizable ordering and dependency-aware grouping. — [Rahman et al., arXiv 2609.04207](https://arxiv.org/abs/2609.04207)
- Barnett interviewees asked for partitions ordered by importance and for per-partition reviewer assignment (8/20). — [Barnett et al. 2015](https://cabird.com/pdfs/barnett2015helping.pdf)
- Graph visualization of a PR's classes and methods (ReviewVis) was perceived as helping navigation and understanding. Evidence: 9 in-company developers plus surveys of 37 and 31; perception only. — [Fregnan et al., "Graph-based visualization of merge requests for code review," JSS 2023 (ZORA record)](https://www.zora.uzh.ch/entities/publication/7e55e778-46a1-4a5c-8aca-b776ce1523dd/full)

### Inferences
A proposed default for the tool. This is design inference from the findings above, not a tested algorithm.
1. **Open with context.** Show the PR description and a short overview. Optionally show a test or usage example as the "spec," marked optional, per Spadini's trade-off.
2. **Groups, not files.** Cluster hunks by def-use/call graph, shared symbols, and test↔source pairing, then name each group (Baum P1, P4, P6; Barnett; SmartCommit).
3. **Order the groups.** Put the core or most salient group first: highest risk or largest behavioral diff, or the one most similar to the description. This counters position bias (Fregnan, Bagirov, Bouraffa).
4. **Order within a group.** Declarations, interfaces, and callees go before uses and callers (Baum P2, bottom-up 85%). Never split a group to satisfy direction (P3).
5. **Tail.** Put mechanical changes last and collapsed: moves, renames, formatting, generated code, lockfiles (RAID; SmartCommit cosmetic and refactoring links; Baum's "unimportant rest at the end").
6. **Per-file triage badges.** Mark each file as "core / supporting / mechanical." Show why each file is placed where it is, and allow a "switch to alphabetical/test-first" toggle, since there is "not one to rule them all" and reviewers vary.

Claims to avoid in product copy: that ordering or decomposition "finds more bugs" or "makes review faster." The evidence supports "fewer missed late files, less noise and context switching, better understanding."

### Gaps
- No study validates a combined risk + dependency ordering end to end.
- Per-file *risk* scoring for review ordering (as opposed to diff-level risk like Meta RADAR, or defect prediction generally) has no direct review-outcome evaluation that I found.
- Hunk-level ordering inside large files, and how to handle a cluster spanning many files on one screen (Principle 5), are untested.
