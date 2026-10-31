# Order the reading, delay the AI's verdict

*Research synthesis, 2026-10-08. Written for the `human-review` skill: what the code review literature says about making changes faster and easier for a human to review, and what to build next.*

The best evidence for making pull requests easier to review favors structure over explanation. Keep changes small and single-purpose, put the riskiest or core material first, group related hunks under explicit labels, collapse mechanical edits, and state the rationale and the feedback you want. These levers reliably cut defects missed in late files: one experiment found **64% lower odds of catching a defect when its file was shown last** ([Fregnan et al., FSE 2022](https://arxiv.org/abs/2208.04259)). They also cut wrong review comments: **6 false positives fell to 1** when a tangled change was split ([di Biase et al., PeerJ CS 2019](https://peerj.com/articles/cs-193/)). But almost none of these levers has been shown in a controlled study to make review *faster*, and time spent reviewing is still the strongest predictor of finding cross-file defects. AI-generated review content carries the sharpest warning. In the only rigorous experiment with professionals, reviewers given an LLM review up front fixated on the locations it flagged, found no more high-severity issues, and took longer: **a mean of 56 minutes vs. 42** ([Tufano et al., ICSE 2025](https://arxiv.org/html/2411.11401v1)). Meta measured a **>5% review-time penalty** when AI patches were shown to reviewers by default ([Meta MetaMateCR](https://arxiv.org/abs/2507.13499v1)). `human-review` fits the evidence on three counts: its risk-first reading path, its line-anchored margin notes (the format with the best controlled comprehension result), and its split between verified and manual checks. Three of its choices are contradicted or unproven:
- **Showing the agent's annotations and risk verdict before the reviewer forms a view.** This is the setup Tufano found anchors reviewers.
- **The "skip" tier.** It hides files where most review findings and many incident-causing changes actually turn up.
- **The skill's promise to turn "a 30-minute review into a 3-minute one."** The literature on review rate says that is how defects escape.

The highest-leverage next steps are, in order:
1. Group files by concern instead of by layer.
2. Make "skip" machine-verified rather than judged.
3. Hold AI judgments behind the reviewer's own pass.
4. Attach reasons and provenance to every risk claim.
5. Add short, targeted security prompts. Telling reviewers to look for security issues made them **8× more likely to detect a vulnerability** in a 150-person experiment.
6. Instrument the page so the user can measure time and seeded-defect detection on their own PRs.

## Twelve levers, rated by how much the evidence can bear

The literature is uneven. A few findings rest on large field datasets plus a controlled experiment. Most rest on one small lab study, on surveys of what developers prefer, or on vendor or self-published industry numbers. The table below is a map for the rest of the report. "Strong" means replicated, or a large experiment with professionals. "Moderate" means one experiment or a large observational study with controls. "Weak" means perception data, proxy outcomes, or vendor claims.

| Lever | Best evidence | Key result | Strength |
|---|---|---|---|
| Put risky or core files first | Fregnan FSE 2022: 219K PRs + lab n=106; JetBrains EASE 2023 | 64% lower odds of finding a defect in the last file (1 of 2 defect types) | Strong, but modest per-file effect |
| Smaller changes | Baum EMSE 2019, n=50 | Effectiveness significantly higher on small changes (p=0.001–0.012) | Strong for quality; *null* for merge speed |
| Group related parts and label the groups | Baum ICSME 2017 (n=201 survey); Baum EMSE 2019 | 86% rate an order with no sensible rule among the worst; the experiment was directional but not significant | Moderate (theory + perception) |
| Untangle composite changes | di Biase 2019 (n=28); Tao & Kim 2015 (n=18 students) | False positives 6→1; correctness 7.94→9.40; no change in time or defects found | Moderate, small samples |
| Collapse moves and refactorings | RAID, ICPC 2021 (n=8) | Lines to review 113→55 for extractions, 14.5→2 for moves | Weak–moderate (proxy outcome) |
| Rationale and "feedback wanted" in the description | Pirouzkhah MSR 2026 (80K PRs); Xiao FSE 2024 | Merge OR ≈1.72 for stating the feedback wanted; AI-drafted descriptions −19.3 h review time | Moderate, observational |
| Targeted security prompt | Braz ICSE 2022, n=150 | 8× vulnerability detection; a checklist added nothing | Strong (one large experiment) |
| Line-anchored explanations | Ivie, CHI 2024, n=32 | 90.2% vs 65.0% comprehension accuracy compared with chat | Moderate, not review-specific |
| Risk analytics shown to reviewers | Yu EMSE 2024 (n=48); Lewis ICSE 2013 (Google) | Better risk awareness and effectiveness in the lab; no behavior change at Google | Mixed |
| AI review shown up front | Tufano ICSE 2025 (n=29 professionals); Meta trial | Anchoring, no high-severity gain, longer reviews; +5% reviewer time | Strong *warning* |
| Diagrams and UML | Arisholm TSE 2006 | Better correctness on complex tasks, no time saved; no review-specific study | Weak for review |
| Checklists and guided strategies | Gonçalves EMSE 2022; Braz ICSE 2022 | Mixed; short and targeted beats long | Moderate |

## Size, tangling, and unfamiliar code set the comprehension ceiling

**Size: bigger changes get worse reviews.** The controlled evidence is unambiguous. In Baum, Schneider and Bacchelli's experiment, 50 participants (46 professionals) reviewed one small change (2 files, 31 LOC) and two large ones (233 and 490 LOC) with seeded defects. Review effectiveness was **significantly higher for the small change** (McNemar p = 0.001–0.012) ([Baum et al., EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)). Large reviews also drove people away: **24 participants dropped out during the first large review and 13 during the second** ([replication materials](https://figshare.com/articles/Online_Material_for_Associating_Working_Memory_Capacity_and_Code_Change_Ordering_with_Code_Review_Performance_/5808609)). The denser 233-LOC change proved harder than the 490-LOC one, so line count alone misleads.

Field data says the same in terms of files. Across 1.5M Microsoft review comments, **the more files in a change, the lower the proportion of useful comments** ([Bosu et al., MSR 2015](https://www.microsoft.com/en-us/research/?p=168510)). A 2026 preprint covering 330,343 GitHub PRs estimates that **each additional file cuts the odds that a given file gets any comment by about 8.7%** ([Rahman et al., arXiv 2609.22610](https://arxiv.org/abs/2609.22610)). Google has absorbed this lesson: the median change there modifies **24 lines**, over 35% touch a single file, and about 90% touch fewer than ten ([Sadowski et al., ICSE-SEIP 2018](https://research.google/pubs/modern-code-review-a-case-study-at-google/)).

**Size: smaller changes do not merge faster.** Across 845,316 GitHub PRs plus 401,790 Gerrit and Phabricator reviews, "pull request size and composition do not relate to time-to-merge" ([Kudrjavets et al., MSR 2022](https://arxiv.org/abs/2203.05045)). Small changes buy review *quality*. Wall-clock latency is dominated by waiting.

**The popular thresholds are vendor numbers.** "200–400 LOC per review, under 500 LOC/hour, no more than 60–90 minutes" traces to a SmartBear/Cisco study of 2,500 reviews that was never peer reviewed ([SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)). The peer-reviewed analogue, Kemerer & Paulk's analysis of PSP class data, supports the direction: review rate significantly affects defect removal. The often-quoted ~200 LOC/hour figure could not be verified against the paper's text ([Kemerer & Paulk, TSE 2009](https://ftp.math.utah.edu/pub/tex/bib/idx/ieeetranssoftweng2000/35/4/534_550.html)).

**Tangled changes are common.** Many changes do several unrelated things at once:
- Up to **15% of bug fixes** in five Java projects bundle unrelated changes, and at least 16.6% of source files are wrongly linked to bug reports as a result ([Herzig & Zeller, MSR 2013](https://www.st.cs.uni-saarland.de/publications/files/herzig-msr-2013.pdf)). The journal extension puts the range at 7–20% ([Herzig, Just & Zeller, EMSE 2016](https://www.microsoft.com/en-us/research/publication/the-impact-of-tangled-code-changes-on-defect-prediction-models/)).
- On average **17%, and up to 29%**, of changes in four OSS projects are composite ([Tao & Kim, MSR 2015](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)).
- At Microsoft, **about 42% of review changesets contain more than one non-trivial partition**, yet authors annotate their changes in the review tool **less than 5% of the time** ([Barnett et al., ICSE 2015](https://cabird.com/pdfs/barnett2015helping.pdf)).

One Microsoft reviewer named the cost: descriptions in which "people can say they are doing one thing, while they are doing many more of them" ([Bacchelli & Bird, ICSE 2013](https://sback.it/publications/icse2013.pdf)). A summary that hides tangling actively misleads.

**Missing "why" and unfamiliar code are the dominant barriers.** Bacchelli & Bird's study of Microsoft reviewers (873 programmers surveyed, 570 comments card-sorted) found that understanding is the central challenge. Interviewees called "what instigated the change" the biggest information need. **91% (798 of 873) said reviewing unfamiliar files takes longer**, because they must first learn the files' purpose, invariants, and APIs. Defect-finding comments made up only **14% of review comments**. Reviewers who owned the touched files gave "deeper," "more actionable" feedback ([Bacchelli & Bird, ICSE 2013](https://sback.it/publications/icse2013.pdf)). Other studies point to the same needs:
- Microsoft engineers find a change's completeness, its consistency, and "especially the risk imposed by it on other software components" hard to obtain ([Tao et al., FSE 2012](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/)).
- Mozilla professionals rated the change description, size, and coherent commit history as top reviewability factors ([Ram et al., FSE 2018](https://serg.ewi.tudelft.nl/publications/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/)).
- Among the needs found in 900 OSS review comments is knowing where modified methods and variables are used ([Pascarella et al., CSCW 2018](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review)).

The stakes are real: **54% of reviewed Mozilla changes still introduced bugs** ([Kononenko et al., ICSME 2015](https://swag.uwaterloo.ca/publications/investigating-code-review-quality-do-people-and-participation-matter.html)). The implication for `human-review` is sobering. A page cannot make a 40-file tangled change easy. It can make the difficulty visible, supply the missing "why" and the context about unfamiliar code, and say when the change should be split.

## Rationale and a stated "feedback wanted" predict engagement better than walkthroughs

The largest study of description content compared descriptions against eight recommended elements across **80K PRs in 156 GitHub projects** ([Pirouzkhah et al., MSR 2026](https://arxiv.org/html/2602.14611v1)). The elements are purpose, reason, code explanation, issue link, type of feedback needed, file review order, test explanation, and screenshots.

**What authors actually include.** Purpose appeared in 54.5% of PRs and code explanation in 55.4%. Just **16.2% said what feedback they wanted**, 13.7% explained the tests, and 6.1% suggested a review order.

**What predicts outcomes.** Stating the feedback wanted was the strongest predictor, with **merge odds ratio ≈ 1.72**. It was also associated with more review comments and longer latency, which reads as more engagement. Code explanation came in around 1.21. Purpose and test explanation were negligible. Suggested review order was associated with *lower* merge odds (OR ≈ 0.35). That last result is almost certainly confounded, since authors add order guidance to big, hard PRs. It is a reason to measure an ordering feature, not evidence that ordering hurts.

**Many PRs have no description at all.** More than **34% of 333K GitHub PRs had empty descriptions** ([Liu et al., ASE 2019](https://ar5iv.labs.arxiv.org/html/1909.06987)). About **44% of commit messages could be improved** to say both what changed and why ([Tian et al., ICSE 2022](https://arxiv.org/abs/2202.02974)).

**Machine-drafted descriptions.** The best evidence is quasi-experimental. Xiao et al. compared 18,256 Copilot-for-PRs PRs with 54,188 controls from the same 146 repositories, weighting for 17 confounders. Copilot-assisted PRs were reviewed **19.3 hours faster** (average treatment effect; medians 12.17 h vs 16.09 h) and were **1.57× more likely to merge** (95% CI 1.35–1.84) ([Xiao et al., FSE 2024](https://arxiv.org/html/2402.08967v1)). The sample was early adopters, and the skewed distribution makes the average effect much larger than the median gap. Authors also edited heavily: of 1,437 revisions, 22.9% deleted generated content and 17.4% removed whole sections. Generated descriptions help, and they are too long or partly wrong by default.

**How reviewers use descriptions.** A think-aloud study of 25 real reviews found reviewers consulted the PR title and description in **84%** of them and the issue tracker in 44%. A short alignment conversation with the author before the review "greatly reduced" comprehension effort ([Wurzel Gonçalves et al., arXiv 2025](https://arxiv.org/html/2503.21455)).

No randomized study holds the code fixed and varies only the description. So the claim that better descriptions speed review is plausible and consistent with the evidence, not proven.

**What this means for the page.** `human-review` already has the evidence-favored element: the `questions` block, with an Answer box, is a "type of feedback needed" section. But it sits near the bottom of the page. The evidence argues for moving "What I need from you" up beside the brief, because it frames the whole review, not just the ending. The weakest part of the current brief is its sourcing. Rationale cannot be recovered from a diff. When the agent did the work, its "why" comes from its own conversation, and that is an author's account, not an independent one. The page should say where each "why" came from (issue, commit message, user prompt) and write "why: not stated" rather than reconstruct a motive.

## Reviewers read in the order you give them, so the order is the intervention

The most practically important ordering finding is behavioral. **73% of reviewers start "often or always" with whatever the tool shows first, and 66% continue in the tool's order**, even though most consider that order sub-optimal ([Baum et al., ICSME 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)). Whatever sequence `human-review` presents largely becomes the sequence of attention. The position effect is real and replicated, though modest:
- **GitHub field data.** In 219,476 PRs from 138 Java projects, files shown earlier received more comments after controlling for size and discussion.
- **Lab experiment.** With 106 participants, a defect had **64% lower odds of being found when its file was last rather than first**. This held for one of two defect types; the other showed no position effect ([Fregnan et al., FSE 2022](https://arxiv.org/abs/2208.04259)).
- **Industrial replication.** JetBrains confirmed the effect in IntelliJ IDEA reviews and found that ordering by diff size surfaced problematic files earlier than alphabetical order ([Bagirov et al., EASE 2023](https://arxiv.org/abs/2306.06956)).
- **Large-scale latent bugs.** A 2026 preprint found latent-bug rates rising from 56.7% at position 1 to 61.5% at position 30. Statistically significant, but tiny (Cohen's d = 0.044) ([Rahman et al., arXiv 2609.22610](https://arxiv.org/html/2609.22610)).

Left alone, reviewers abandon alphabetical order on larger PRs. Across 23,241 GitHub PRs, reviewers commented in non-alphabetical order in **44.6%** of them ([Bouraffa et al., EASE 2025](https://repository.tudelft.nl/file/File_08e6d8bc-a310-418b-bf8d-e04cb000023e)). Among those:
- 20.6% went largest-diff-first.
- 17.6% followed similarity to the PR description.
- 29% of PRs touching both tests and production code went test-first.

Non-alphabetical reviews covered a larger share of files, about 42% vs 39% ([arXiv 2510.04796](https://arxiv.org/pdf/2510.04796v1)). In a survey of 1,355 developers, only **10.2% considered alphabetical order optimal**, 63.9% worried it makes them miss bugs, and 66% wanted dependency-aware ordering ([Rahman et al., ICSE 2026](https://arxiv.org/abs/2609.04207)).

**What a good order looks like.** The best design guidance comes from Baum's theory, built from interviews with 12 professionals and a survey of 201 reviewers. Its central claim is that "an optimal order is mainly an optimal grouping of the change parts by relatedness" ([Baum et al., ICSME 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)):
- **Group related parts.** 102 of 123 respondents preferred related parts close together.
- **Information before it is needed.** For call flow, 85% rated callee-first (bottom-up) orders among the best.
- **When the two conflict, grouping wins.** 76% chose closeness over direction.
- **Make the rule visible.** An order with no understandable rule was rated among the worst by **86%**.

The one experiment that tested theory-optimal against worst orders found differences "in the direction predicted by theory, but subject to a lot of variation." The difference was not statistically significant ([Baum et al., EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)).

**Reading strategies trade one kind of finding for another.** In Spadini et al.'s experiment with 92 developers, reviewing tests first gave **3.49× the odds of finding test bugs** and **71% lower odds of finding production maintainability issues**. Detection of production bugs and review time did not change ([Spadini et al., ICSE 2019](https://repository.tudelft.nl/file/File_8d21a720-18e1-4621-b700-6a2b207e669d?preview=1)). Explicit guidance is similarly conditional. A step-by-step guided checklist helped on a simple review. A plain checklist helped on a complex one, where the guided version constrained reviewers' own navigation. Overall, there was no strong relationship between guidance and performance ([Gonçalves et al., EMSE 2022](https://link.springer.com/10.1007/s10664-022-10123-8)).

**How `human-review` measures up.** Its `focus` path (3–6 stops, riskiest first, each with a "why") is close to what the evidence prescribes: risk at the top to counter position bias, and an explicit rationale for each stop, per Baum's sixth principle. The "All files" list already sorts careful-first. Two gaps remain:
- **Grouping by layer.** Files are grouped by layer (Server, Web, Data, Tests). Baum's theory says group by *relatedness* (call flow, data flow, declare-and-use), with tests next to the code they exercise.
- **Order within a group.** Nothing in the skill tells the agent to put callees and declarations before callers within a group.

Because reviewers follow the tool's order, the corollary is the uncomfortable part. Whatever the path leaves out, reviewers are likely to leave out too.

## Untangling buys precision and clarity, not speed

**Outcome studies: precision up, speed unchanged.** Two controlled studies, both small, point the same way:
- **di Biase et al.** gave 28 developers either one tangled PR or the same change split into two coherent PRs ([PeerJ CS 2019](https://arxiv.org/pdf/1805.10978)). The untangled group reported **far fewer false positives (1 vs 6, p = 0.03, medium effect)** and sought more context. They did not find more defects (17 vs 20, not significant), did not understand the rationale better, and were not faster (median 759 s vs 831 s, p = 0.66).
- **Tao & Kim's** 18 student participants answered review questions more correctly when changes were presented by slice rather than by file (**9.40 vs 7.94, p = 0.01**) in a similar time (40.6 vs 35.9 min, p = 0.81). Their automatic partitioner produced unsatisfactory partitions 31% of the time ([Tao & Kim, MSR 2015](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)).

**Practitioners want decomposition, and current tools are imperfect at it.**
- At Microsoft, 16 of 20 developers judged ClusterChanges' def-use partitions of their own changes correct and complete. The misses clustered on interface usage, XML and config references, and event wiring ([Barnett et al., ICSE 2015](https://cabird.com/pdfs/barnett2015helping.pdf)).
- SmartCommit, a graph-based grouper with separate link types for refactoring and cosmetic edits, ran for nine months with 83 industrial engineers. It reached median accuracy of 70–75%, and **over 60% of its groups were accepted without adjustment** ([Shen et al., FSE 2021](https://www.cs.cmu.edu/~ckaestne/pdf/fse21_sc.pdf)).
- LLM-based multi-agent untanglers report large relative gains on synthetic benchmarks: ColaUntangle +44% on C# and +82% on Java over the best baseline ([arXiv 2507.16395](https://arxiv.org/abs/2507.16395)); Atomizer at ICSE 2026, with about 57% accuracy on C# ([arXiv 2601.01233](https://arxiv.org/html/2601.01233v1)).

None of these tools has been evaluated on downstream review outcomes. Expect roughly one in four or one in three groupings to be imperfect.

**Splitting into separate PRs carries coordination costs.** A 2026 preprint on Gerrit relation chains (stacks) found chained changes take a **median 2.6× longer to merge** than comparable solo changes, though that is confounded by feature difficulty ([Belhouchette et al., arXiv 2607.20189](https://arxiv.org/abs/2607.20189)). Wall-clock time responds to coordination interventions, not decomposition:
- Microsoft's randomized Nudge trial **cut resolution time for overdue PRs by 60%** ([Maddila et al., TOSEM 2022](https://arxiv.org/pdf/2011.12468)).
- At Meta, a "Next Reviewable Diff" feature raised review actions per day by 17%, and a stale-diff nudge bot cut time in review by 7% ([Meta Engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)).

**What this means for the page.** The product framing should change. Decomposition inside the page makes review clearer and less noisy, and the page can do it without forcing the author into stacked PRs: named concern groups, a mismatch flag when the detected concerns exceed what the brief claims, and a "this should be two PRs" recommendation when there is more than one non-trivial cluster. None of that is a speed feature, and the page should not sell it as one.

## Visual aids have the thinnest outcome evidence on the page

The visual aids with measured effects are structural, not pictorial.

**Refactoring-aware diffs.** RAID marks moves and extractions as such. With 8 professional developers, it cut median lines to review **from 113 to 55 for extractions and from 14.5 to 2 for moves**, and users reported lower cognitive effort ([Brito & Valente, ICPC 2021](https://arxiv.org/abs/2103.11453v1)). Lines-to-review is only a proxy and the sample is tiny. The detection layer underneath is mature: RefactoringMiner's AST diff reaches **99.7% precision and 98.4% recall** on its benchmark ([Alikhanifard & Tsantalis, TOSEM 2024](https://arxiv.org/pdf/2403.05939)). That makes machine-verified "this is a pure move" labels feasible, at least for Java.

**Diagrams and structured representations.** These have no review-specific outcome study. The closest classic evidence is Arisholm et al.'s controlled experiments on UML documentation in maintenance work. UML significantly improved the functional correctness and design quality of changes on *complex* tasks, **with no time saving**. On simple tasks, its costs could outweigh its benefits ([Arisholm et al., TSE 2006](https://www.simula.no/research/impact-uml-documentation-software-maintenance-experimental-evaluation)). A graph visualization of merge requests (ReviewVis) was *perceived* as helping navigation by 9 in-company developers and two survey samples (37 and 31), but outcomes were not measured ([Fregnan et al., JSS 2023](https://www.zora.uzh.ch/entities/publication/7e55e778-46a1-4a5c-8aca-b776ce1523dd/full)). Screenshots appear in the 2026 description taxonomy, but no study measures their effect ([Pirouzkhah et al.](https://arxiv.org/html/2602.14611v1)).

**Explanations anchored to code.** The strongest controlled result for a format that `human-review` uses is not from code review at all. In a within-subjects study with 32 participants, Ivie placed LLM explanations in the right margin next to code blocks and beneath hovered expressions. Compared with a chat assistant, comprehension accuracy was **90.2% vs 65.0%** (p < 0.001), responses were faster (2.8 s vs 3.6 s), and NASA-TLX workload scores were lower on every dimension ([Yan et al., CHI 2024](https://arxiv.org/html/2403.02491v1)). GILT, by contrast, put on-demand explanations in the IDE. It improved task completion over web search but showed **no significant gain in time or depth of understanding** ([Nam et al., ICSE 2024](https://arxiv.org/html/2307.08177v3)).

**What this means for the page.** Margin notes on load-bearing lines are the best-evidenced presentation choice in the skill. Wireframes, data-model and API cards, and Mermaid and architecture diagrams are reasonable navigation aids for complex, cross-cutting changes, which is where Arisholm's correctness benefit appeared. They are unproven for review speed. They also carry a fabrication risk. In a 2026 study of LLM-generated structured bug-report summaries, **47.9% omitted information and 12.3% contained fabricated content** ([arXiv 2605.24137](https://arxiv.org/pdf/2605.24137)). An inferred wireframe is exactly the kind of artifact where an omission goes unnoticed. The skill's rule that small changes get "no sections" fits the Arisholm result and should stay.

## Review time, not working memory, is the binding constraint on hard defects

**Time is what finds the hardest defects.** Baum et al. measured working memory directly. Working memory capacity correlated with finding **delocalized** defects, those whose evidence is spread across several places (Kendall τB = 0.24, p = 0.019), and essentially not with other defects. Even for delocalized defects, "the strongest [factor] is review time" ([Baum et al., EMSE 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)). A case-control study of Chromium OS (516 reviews that caught security defects vs 374 that missed them, AUC 0.91) found the same pattern. Longer review time and a history of mutual reviewing helped. **The number of directories under review** and the reviewer's overall workload hurt ([Paul et al., ICSE 2021](https://arxiv.org/abs/2102.06909v1)).

**Eye tracking: overview first, then focus.** Studies consistently observe an initial "scan" of the whole change. Reviewers who scanned too briefly took longer to find defects ([Uwano et al., ETRA 2006](https://naist.repo.nii.ac.jp/record/10579/files/R006972.pdf)). Experts alternate between global scanning and focused examination ([Turku, 2023](https://research.utu.fi/converis/portal/detail/Publication/499173240?lang=en_US)). These are small lab samples, but they support an "overview first" page design.

**Fatigue: plausible but undocumented.** Peer-reviewed evidence on how detection declines with minutes into a session is absent. The 60-minute limit is SmartBear's. The supporting signals are dropouts in Baum's large reviews and the 57.6% of surveyed developers who say alphabetical order increases context switching and fatigue ([Rahman et al., ICSE 2026](https://arxiv.org/abs/2609.04207)).

**Framing changes effort.** In a 37-person eye-tracking study, perceived PR urgency changed how long participants spent and their cognitive load, and they were largely unaware of the effect ([ICPC 2024](https://conf.researchr.org/details/icpc-2024/icpc-2024-research/10/Exploring-Social-Signals-in-Code-Review-An-Eye-Tracking-Study-of-Urgency-and-Reputat)).

**What this means for the page.** This is the core tension with the skill's stated goal. If the reviewer's time drops from 30 minutes to 3 because they read less of the core logic, the evidence predicts lower detection of exactly the cross-file defects that matter. Defensible time savings come from removing navigation cost, mechanical reading, context hunting, and waiting. The brief-plus-focus overview supports the scan phase. Showing related distant hunks side by side directly targets the working-memory load behind delocalized defects. That is Baum's principle that the closest distance is "visible on the screen at the same time." The ICPC result also suggests a hypothesis worth testing: a prominent "Risk: low" badge may act like a priority signal and quietly reduce scrutiny.

## AI explanations help comprehension, but AI verdicts shown first narrow the search

**Most AI review comments are ignored.** Industrial deployments converge on a sobering base rate. The share of generated comments acted on runs from roughly 7–8% to 40%, depending on the site and how "acted on" is defined:

| Deployment | Share acted on |
|---|---|
| Mozilla and Ubisoft, RevMate ([arXiv 2411.07091](https://alphaxiv.org/abs/2411.07091)) | 8.1% and 7.2% accepted |
| 16 open-source AI-review GitHub Actions ([arXiv 2508.18771](https://arxiv.org/html/2508.18771v1)) | under 20% led to code changes |
| Meta's best model, in production ([arXiv 2507.13499](https://arxiv.org/pdf/2507.13499)) | 19.7% applied |
| Atlassian RovoDev ([arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)) | 38.7%, vs 44.5% for human comments |
| Google AutoCommenter ([arXiv 2405.13565](https://arxiv.org/html/2405.13565)) | ~40% resolved |

Comments were more likely to cause changes when they were **concise, contained code, were hunk-level rather than whole-PR, and were manually triggered** ([arXiv 2508.18771](https://alphaxiv.org/abs/2508.18771)).

**Precision gating, not model upgrades, made comments useful.** Google raised AutoCommenter's developer-rated usefulness from 54% to its **80% target** mainly by suppressing non-actionable categories and calibrating per-category thresholds. Each comment cites the style-guide URL it relies on ([Vijayvergiya et al., AIware 2024](https://arxiv.org/html/2405.13565)). Atlassian found an actionability classifier improved alignment by 15–20 percentage points, while an LLM factual-correctness judge "had minimal impact" ([arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)). Hallucination is not rare even in production. **22% of 143 annotated RovoDev comments made claims unsupported by, or contradicting, the diff.** A judge model detecting these reached F1 0.85 at about a cent per check ([HalluJudge, arXiv 2601.19072](https://arxiv.org/html/2601.19072v2)).

**Time savings exist only in observational data.** The only randomized measurements of review time found either nothing or a slowdown:
- Google's AutoCommenter A/B test, run on about half of all developers, found **no statistically significant change in review duration or active reviewer time** ([arXiv 2405.13565](https://arxiv.org/html/2405.13565)).
- Meta's randomized safety trial found that showing AI-generated patches to *reviewers* made reviews take **more than 5% longer**. Showing them only to authors, with reviewers able to expand them, restored normal review time with no loss of acceptance ([arXiv 2507.13499](https://arxiv.org/abs/2507.13499v1)).

The claimed speed-ups are observational or self-published:
- Atlassian: 31% shorter PR cycle time, not randomized ([arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)).
- Microsoft: "10–20%" median completion-time improvement, with methodology unpublished ([Microsoft Engineering](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)).
- Beko went the other way: **average PR closure time rose from 5h52m to 8h20m** after adoption ([Cihan et al., ICSE-SEIP 2025](https://arxiv.org/html/2412.18531v2)).

When agents replace humans entirely, PRs reviewed only by code-review agents merged **45.2% of the time vs 68.4%** for human-reviewed PRs ([Chowdhury et al., MSR 2026](https://arxiv.org/abs/2604.03196)).

**The anchoring result.** Tufano et al. ran the decisive experiment for `human-review`'s design ([ICSE 2025](https://arxiv.org/html/2411.11401v1)):
- **Setup.** 29 professional developers (mean 11.4 years of experience) reviewed code with 48 injected issues under three conditions: manual review, a ChatGPT-generated review as a starting point, and an "oracle" review listing every injected issue.
- **What the AI found and what reviewers kept.** The AI review found 42% of the injected issues, and reviewers **kept 89% of what it found**. Yet the median share of injected issues found was **50% in both the manual and AI-assisted conditions**.
- **Where reviewers looked.** Reviewers "tend to focus on the code locations indicated by the LLM rather than searching for additional issues." They surfaced more low-severity issues and **no more high-severity ones**.
- **Time and confidence.** Mean review time *rose* from 42 to 56 minutes, and confidence did not change significantly.
- **The authors' recommendation.** Show automated reviews only **after** a manual inspection.

**Framing can steer AI reviewers.** An iteratively refined, benign-sounding framing of a PR's text got vulnerable code past two production AI review pipelines, one of them Claude Code, in **32 of 33 CVE cases** ([Alexopoulos et al., arXiv 2603.18740](https://arxiv.org/abs/2603.18740)).

**Explanation versus judgment.** Line-anchored *explanations* improve comprehension (Ivie's 90% vs 65%). Ericsson's senior developers disliked reviews that "merely explained code functionality" ([arXiv 2507.19115](https://arxiv.org/html/2507.19115v1)). At WirelessCar, 10 developers preferred an AI-led upfront summary over an on-demand assistant, but the preference depended on their familiarity with the codebase and the PR's severity ([Aðalsteinsson et al., arXiv 2505.16339](https://arxiv.org/abs/2505.16339)).

**The presentation rules the evidence supports:**
- **Anchor notes to lines.**
- **Make each note add judgment, not paraphrase.** Say why it matters and what could break.
- **Cite the evidence for every claim.**
- **Gate hard for precision, and stay silent rather than add noise.**
- **Collapse AI verdicts by default for the reviewer.**
- **Keep the orientation material visible, but hold back the AI's opinion of where the bugs are until the reviewer has looked.** Orientation material is the map, the groups, and the "why."

That last distinction, orientation versus verdict, is an inference from Tufano and Meta, not a tested design. No study has yet tested a delayed-reveal mitigation in code review.

## Risk scores route work well; their power to steer eyes is mostly unproven

**Offline accuracy is moderate.** Just-in-time defect prediction has been studied for over a decade:
- Kamei et al.'s change-level models reached **68% average accuracy and 64% recall** across 11 projects. Their effort-aware model found **35% of defect-inducing changes while inspecting 20% of changed lines** ([Kamei et al., TSE 2013](https://sail.cs.queensu.ca/data/pdfs/TSE_ALarge-ScaleEmpiricalStudyOfJust-in-TimeQualityAssurance.pdf); [effort-aware summary](https://arxiv.org/pdf/2209.13978)).
- Line-level JITLine has a median Top-10 accuracy around **0.61**, so about four in ten highlighted lines are false alarms ([Pornprasit & Tantithamthavorn, MSR 2021](https://arxiv.org/abs/2103.07068v1)).
- Ubisoft's CLEVER flagged risky commits with 79% precision and 65% recall ([Nayrolles & Hamou-Lhadj, MSR 2018](https://www.ubisoft.com/en-us/studio/laforge/news/69mh5FECbj12vBfL4HGC5C/clever-combining-code-metrics-with-clone-detection-for-justintime-fault-prevention-and-resolution-in-large-industrial-projects)).
- The models decay. AUC and calibration **drop considerably within a year**, and the authors recommend retraining on the most recent three months ([McIntosh & Kamei, TSE 2018](https://rebels.cs.uwaterloo.ca/journalpaper/2017/04/04/are-fix-inducing-changes-a-moving-target.html)).

**Human evidence is sparse and mixed.**
- **Google.** After deploying a bug-prediction model, Google found "developer behavior did not change significantly." The authors attributed this to messages that were not actionable. They concluded that flags need **actionable messages, obvious reasoning, and a bias toward recent problems** ([Lewis et al., ICSE 2013](https://research.google/pubs/does-bug-prediction-support-human-developers-findings-from-a-google-case-study/)).
- **Gherald.** In a 48-person controlled experiment, risk analytics produced **significant improvements in risk awareness and review effectiveness**. Participants found known defects faster, but not significantly so ([Yu et al., EMSE 2024](https://rebels.cs.uwaterloo.ca/journalpaper/2024/01/02/studying-the-impact-of-risk-assessment-analytics-on-risk-awareness-and-code-review-performance.html)).
- **Meta.** The large operational wins come from using risk to *route* work, not to steer reviewers' eyes. Meta's RADAR auto-approved over 331K low-risk diffs, with **35% lower median review wall time** and far lower revert and incident rates. Those rate comparisons are confounded, since RADAR selects low-risk diffs ([arXiv 2605.30208](https://arxiv.org/pdf/2605.30208)).

**The tail is large.** In Meta's logistic-regression baseline, gating the riskiest 10% of diffs captured only **27.9% of incident-causing diffs**. The riskiest half captured 84.6% ([Abreu et al., arXiv 2410.06351](https://arxiv.org/abs/2410.06351)).

**Which signals carry risk.** The well-replicated signals are:
- **Change size and diffusion**, meaning how many files and directories a change spreads across.
- **Low author ownership.** Minor contributors predict pre-release faults and post-release failures ([Bird et al., FSE 2011](https://www.microsoft.com/en-us/research/?p=161465)).
- **Weak review coverage and participation** ([McIntosh et al., MSR 2014](https://www.swag.uwaterloo.ca/www/publications/the-impact-of-code-review-coverage-and-code-review-participation-on-software-quality-a-case-study-of-the-qt-vtk-and-itk-projects.html)).
- **Author inexperience, for security.** Less-experienced authors' changes were **1.8–24× more likely to be vulnerable**, vulnerability likelihood grows with lines changed, and modified files are riskier than new ones ([Bosu et al., FSE 2014](https://unpaywall.org/10.1145%2F2635868.2635880)).
- **Structural complexity.** Amazon Prime Video found it predicted deployment risk better than change volume ([Kurup et al., arXiv 2607.06766](https://arxiv.org/pdf/2607.06766)).

Without help, Qt reviewers **reviewed risky and future-defective files less rigorously** than clean ones ([Thongtanunam et al., MSR 2015](https://swag.uwaterloo.ca/publications/investigating-code-review-practices-in-defective-files-an-empirical-study-of-the-qt-system.html)). That is the strongest argument for explicit risk cues at all.

**What reviews actually find.** Most findings are about maintainability, not function. **77% of reviewer-identified issues were evolvability defects** ([Mäntylä & Lassenius, TSE 2009](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9489594/)), and review-induced changes ran about **75:25 maintainability to functional** ([Beller et al., MSR 2014](https://flosshub.org/node/1650)).

**The best attention intervention is cheap.** Simply instructing reviewers to focus on security made vulnerability detection **8× more likely** among 150 developers. A security checklist, even one tailored to the change, added nothing significant on top ([Braz et al., ICSE 2022](https://arxiv.org/abs/2202.04586v2)).

**What this means for the triage tiers.** `human-review`'s careful/skim/skip triage is an effort-aware model and should be evaluated like one: what fraction of later-discovered defects lands in "careful," relative to that tier's share of the lines. The risk badge needs reasons the reviewer can check, computed from signals rather than vibes. And "skip" should be reserved for changes a machine can prove are mechanical.

## Where human-review stands against the evidence

The table audits the current design as described in its SKILL.md and renderer. "Supported" means the evidence backs the choice as built. "Risky" or "contradicted" means a finding cuts against it. "Unproven" means no relevant outcome evidence exists either way.

| Current design element | Verdict | Evidence | Adjustment |
|---|---|---|---|
| `focus` reading path: 3–6 stops, riskiest first, each with a why | **Supported** | Position effect ([Fregnan](https://arxiv.org/abs/2208.04259)); reviewers follow tool order, 73% / 66% ([Baum 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)); explicit rules | Keep. Add a "not on this path" list so omissions are visible |
| "All files" sorted careful-first | **Supported** | Diff-size and risk-first ordering beat alphabetical ([Bagirov](https://arxiv.org/abs/2306.06956)) | Keep |
| Files grouped by layer (Server, Web, Tests…) | **Partly contradicted** | Grouping by relatedness is the core of optimal order ([Baum 2017](http://tobiasbaum.github.io/rp/optimalordering.pdf)); test↔source pairing is natural ([Bouraffa](https://repository.tudelft.nl/file/File_08e6d8bc-a310-418b-bf8d-e04cb000023e)) | Group by concern or def-use cluster; pair each test with its code |
| Margin annotations, 2–5 per file, "never restate the code" | **Supported (format)** | Anchored explanations 90% vs 65% ([Ivie](https://arxiv.org/html/2403.02491v1)); concise, hunk-level comments get acted on ([arXiv 2508.18771](https://alphaxiv.org/abs/2508.18771)); paraphrase disliked ([Ericsson](https://arxiv.org/html/2507.19115v1)) | Keep the format and the cap |
| `risk` and `question` annotations, risk badge, and `focus` shown before the reviewer's own pass | **Contradicted / risky** | Anchoring, no high-severity gain, longer reviews ([Tufano](https://arxiv.org/html/2411.11401v1)); +5% time when AI output is shown to reviewers ([Meta](https://arxiv.org/abs/2507.13499v1)) | Progressive disclosure (see recommendation 3) |
| `skip` tier, excluded from the progress bar | **Risky** | ~75% of findings are maintainability ([Beller](https://flosshub.org/node/1650)); the top-risk decile catches only 27.9% of incidents ([Meta](https://arxiv.org/abs/2410.06351)); de-emphasized content gets less attention ([Fregnan](https://arxiv.org/abs/2208.04259)) | Restrict to machine-verified mechanical changes; rename the tier; never imply "safe" |
| `risk` level with a one-line why | **Partly supported** | Flags need actionable, obvious reasons ([Lewis](https://research.google/pubs/does-bug-prediction-support-human-developers-findings-from-a-google-case-study/)); risk analytics improve awareness ([Yu](https://rebels.cs.uwaterloo.ca/journalpaper/2024/01/02/studying-the-impact-of-risk-assessment-analytics-on-risk-awareness-and-code-review-performance.html)) | Itemized, checkable signals with provenance |
| Brief and summary drawn from the PR description and the agent's own conversation | **Risky** | Framing defeats AI review 97% of the time ([Alexopoulos](https://arxiv.org/abs/2603.18740)); descriptions that hide scope mislead ([Bacchelli & Bird](https://sback.it/publications/icse2013.pdf)) | Derive claims from the diff; label each "why" by source; flag mismatches with the detected concerns |
| `questions` with Answer box | **Supported, misplaced** | Stating the feedback wanted, merge OR ≈1.72 ([Pirouzkhah](https://arxiv.org/html/2602.14611v1)) | Move up beside the brief |
| `checks.verified` vs `checks.manual` | **Supported in spirit** | Cite evidence per claim ([AutoCommenter](https://arxiv.org/html/2405.13565)); 22% hallucination base rate ([HalluJudge](https://arxiv.org/html/2601.19072v2)) | Extend verified-vs-claimed labels to every annotation |
| Wireframes, data-model and API cards, diagrams | **Unproven** | Correctness gains on complex tasks only, no time saving ([Arisholm](https://www.simula.no/research/impact-uml-documentation-software-maintenance-experimental-evaluation)); perception-only for review ([ReviewVis](https://www.zora.uzh.ch/entities/publication/7e55e778-46a1-4a5c-8aca-b776ce1523dd/full)) | Gate by complexity; measure |
| "No sections" for small fixes | **Supported** | Documentation costs outweigh benefits on simple tasks ([Arisholm](https://www.simula.no/research/impact-uml-documentation-software-maintenance-experimental-evaluation)) | Keep |
| "Copy feedback for the agent" loop | **Supported in spirit** | Explicit feedback is rare when optional, ~10% at Google ([AutoCommenter](https://arxiv.org/html/2405.13565)); this loop is richer | Add timing and coverage data to the export |
| Goal: "30-minute review into a 3-minute one"; "a 40-file PR becomes a 6-file read" | **Contradicted as stated** | Review rate and review time drive detection ([Kemerer & Paulk](https://ftp.math.utah.edu/pub/tex/bib/idx/ieeetranssoftweng2000/35/4/534_550.html); [Baum 2019](https://www.ifi.uzh.ch/dam/jcr:c47671a8-3fa4-4f76-bbd1-bb352a9ac6d0/emse2019a.pdf)); no AI aid has shown randomized time savings | Reframe as cutting navigation and mechanical reading, not inspection of core logic |
| The agent recapping work it wrote itself | **Unstudied, plausible risk** | Author framing steers both humans and LLMs ([Alexopoulos](https://arxiv.org/abs/2603.18740); [Bacchelli & Bird](https://sback.it/publications/icse2013.pdf)) | Hypothesis: build the risk and annotation pass in a fresh context that sees only the diff and the repo |

## What to build next, ranked

The ranking weighs expected impact on review time *and* defect detection against the strength of the evidence and the cost to build. Items 1–4 fix places where the current design runs against the evidence or leaves well-supported gains unclaimed. Items 5–9 are additions with good support. Items 10–12 are lower-confidence bets that should ship only with measurement.

| # | Build | Tied to | Expected impact | Caveats |
|---|---|---|---|---|
| 1 | **Concern-grouped reading.** Replace layer groups with def-use, call-flow, or shared-symbol clusters, each named and with a one-line rationale. Pair each test with the code it tests. Order callees and declarations before callers inside a group. Show related cross-file hunks side by side. | Baum principles 1, 2, 5, 6; di Biase; Tao & Kim; Barnett; working memory and delocalized defects | Fewer false-positive comments; better comprehension; less context switching; targets delocalized defects | No proven speed or defect-count gain; static grouping misses config, XML, and event links (Barnett), so let the reviewer merge or split groups |
| 2 | **Machine-verified "mechanical" tier replacing "skip."** Detect pure moves, renames, formatting, generated files, and lockfiles deterministically (RefactoringMiner-style AST diff, whitespace-insensitive comparison). Show the proof ("moved verbatim, 0 tokens changed"). Rename the remaining low tier "lower risk — skim." Keep every file counted in coverage. | RAID; RefactoringMiner 99.7% precision; maintainability share of findings; Meta's tail; position effect | Large cut in lines read on refactor-heavy PRs, without hidden blind spots | Language support varies; LLM-judged "skip" should never collapse a file |
| 3 | **Independent-pass mode (progressive disclosure).** Keep the map visible: brief, groups, and the reading path *without* risk claims. Collapse `risk` and `question` annotations and the risk verdict until the reviewer marks a stop as reviewed or clicks "reveal." Then show a "the agent did not examine / not on the path" list and an "anything else?" prompt. | Tufano (anchoring, +33% mean time, no high-severity gain); Meta (collapsed by default restores time) | Protects high-severity detection; may *reduce* time lost to chasing AI-flagged nits | Untested in review; may lengthen time on easy PRs. Make it a toggle, default it on for medium and high risk, and measure (see below) |
| 4 | **Reasoned, provenance-tagged risk.** Replace the single "why" with checkable signals computed from git: files and directories touched, ownership and first-touch by the author, recent bug-fix commits to the file, modified versus new, complexity of the touched code, security-sensitive paths. Tag every claim as *verified* (test ran, grep confirmed), *from author text*, or *model inference*. | Lewis (actionable, obvious, recent); Yu; Bird; Bosu; Paul (directories); framing attack | Better-calibrated attention; resists manipulation by framing; builds trust | Signals drift (McIntosh & Kamei); show them, don't hide them behind a score |
| 5 | **Targeted security prompts.** When a hunk touches auth, input parsing, crypto, permissions, or serialization, put a one-line "review this for security: check X" cue on that hunk. No checklist. | Braz: 8× detection, checklist adds nothing | High value per pixel; cheap to build | Over-firing dilutes the effect; keep it rare and specific |
| 6 | **"What I need from you" up top**, plus a test explanation (what the tests cover and what they don't). Mark "why: not stated" when the rationale can't be sourced. | Pirouzkhah (feedback type OR ≈1.72; test explanation present in only 13.7%); Bacchelli & Bird | More directed engagement; less time reconstructing intent | Observational evidence; more engagement can mean longer latency |
| 7 | **Precision gate on annotations.** Before building the page, run a self-check pass that drops notes not supported by the diff (hallucination) or not actionable, and notes that paraphrase the code. Prefer silence over a weak note. | HalluJudge (22% base rate, F1 0.85); Atlassian actionability +15–20pp; AutoCommenter's suppression to 80% useful | Fewer wrong or noisy notes; protects trust | Atlassian found its factual-correctness judge alone did little; filter on actionability too |
| 8 | **Split and size advisor.** When there is more than one non-trivial cluster, a spread across many directories, or an estimated review exceeding one sitting, say so. Propose the split, and flag a mismatch when the detected concerns exceed what the brief claims. | Barnett (>40% decomposable); Baum 2019 (size, dropout); Paul (directories); Bacchelli & Bird quote | Better reviews on the PRs that most need it | Thresholds are vendor heuristics; stacks carry coordination cost (2.6× merge time) |
| 9 | **Impact / blast-radius card.** Callers of changed public functions, dependents of changed types, tests that exercise changed code, and config consumers. | Tao 2012 ("risk to other components" hardest to get); Pascarella (uses of modified symbols); Bacchelli & Bird (91%, unfamiliar code) | Speeds reviewers who don't know the area | Evidence is about what reviewers need, not measured outcomes |
| 10 | **Familiarity-adaptive density.** Expand module purpose, invariants, and context when the reviewer hasn't touched these files; compact the page for owners. | Bacchelli & Bird; WirelessCar (preference depends on familiarity); Gonçalves (novices benefit from guidance) | Less time spent on context for unfamiliar reviewers | Requires knowing who the reviewer is; small evidence base |
| 11 | **Visuals gated by complexity.** Show wireframes, diagrams, and data-model cards by default only for cross-cutting changes; collapse them otherwise; mark inferred layouts prominently. | Arisholm (complex tasks only, no time saved); omission and fabrication rates in generated summaries | Keeps correctness gains where they exist; trims reading cost elsewhere | No review-specific evidence either way; the strongest candidate for your own A/B test |
| 12 | **Tests-as-spec entry point as a toggle**, not the default. | Spadini (test-first trades production findings for test findings) | Useful for behavior changes | Making it the default would cut production-maintainability findings |

## Claims to validate with your own measurements

The literature leaves the most product-relevant questions open:
- Does a delayed reveal of AI notes preserve detection?
- How many defects hide in tool-labeled "skip" files?
- Do wireframes and diagrams save time?
- Does an LLM-written reading path beat the default order?

No published study answers any of them. A single-user tool is unusually well placed to answer them, because the person reviewing is the person deciding.

**Canary defects.** The most informative cheap method copies Tufano's design. On a throwaway branch, have a separate agent occasionally inject one realistic defect into a change before the page is built: an off-by-one, a missing authorization check, or a swallowed error. Record whether you catch it, in which tier and position it sat, and whether the page annotated it. Seeded defects give a detection signal in weeks, where waiting for production bugs takes months.

**Self-instrumentation.** The page already tracks which files are viewed. Adding timestamps per stop and per file, plus reveal events, to the "Copy feedback" export would yield review time, coverage by tier, and position-of-first-comment at no extra effort. Alternate conditions across PRs: annotations visible vs. revealed after your pass, and visuals on vs. off. Expect to need dozens of reviews per condition before differences stand out from noise.

| Claim to test | Metric | Evidence that motivates it |
|---|---|---|
| Revealing AI notes after your own pass preserves detection of serious defects | Canary catch rate and time, visible vs. delayed | Tufano; Meta |
| "Careful" captures most real defects | Share of canaries and post-merge fixes landing in "careful" ÷ that tier's share of lines (the Kamei effort-aware ratio) | Kamei; Meta's 27.9% top-decile figure |
| "Skip" / "mechanical" is safe | Later bug-fix commits or reverts touching files rated skip | Beller; Fregnan |
| The agent's annotations are accurate | Share of notes you mark wrong or unsupported, vs. the 22% benchmark | HalluJudge |
| Visuals save time or catch errors | Time and canary catch rate with sections on vs. off, split by PR complexity | Arisholm |
| The page cuts review time without cutting detection | Minutes per review against canary catch rate, page vs. plain diff | Kemerer & Paulk; Baum 2019 |
| The risk badge changes scrutiny | Time spent on PRs labeled "low" vs. "medium" with canaries held constant | ICPC 2024 urgency effect |

## Conclusion

The literature recasts what a review page is for. The page earns its keep as a **cartographer, not a judge**: it controls where attention goes, makes structure and omissions visible, and removes mechanical reading. Each of those has measured support. Its riskiest move is the one that feels most helpful, telling the reviewer up front where the bugs are, because the one rigorous test of that idea showed reviewers stop looking elsewhere. The 30-to-3-minute ambition is achievable only for the parts of review that are overhead: finding the entry point, reading moved code, reconstructing intent. Squeezing the time spent inspecting core logic is exactly what the review-rate evidence says lets defects through.

The most valuable thing `human-review` could add is a way to know whether it works. The open questions, delayed reveal, triage false-safety, and diagram payoff, are unanswered in the published research. Canary defects and an instrumented feedback export would let the user answer them for their own codebase. That turns a tool built on plausible design rules into one tuned by evidence from the reviews it actually serves.
