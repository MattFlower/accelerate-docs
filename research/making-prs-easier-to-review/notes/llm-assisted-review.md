# LLM/AI Assistance in Human Code Review: Empirical Evidence 2022–2026

Notes compiled 2026-10-08. Evidence grades used below: **[RCT]** = randomized/controlled experiment; **[QE]** = quasi-experimental or observational with statistical controls; **[OBS]** = descriptive production telemetry; **[SELF]** = self-reported survey/interview; **[VENDOR]** = vendor blog/marketing, not peer reviewed.

## 1. Industry deployments with measured outcomes

### Takeaway
Large deployments (Google, Meta, Microsoft, Atlassian, Beko, Mozilla/Ubisoft, GitHub) consistently show that only a minority of AI review comments are acted on (roughly 7–40% depending on how "acted on" is defined), that heavy precision filtering is necessary to reach acceptable usefulness, and that time effects are mixed. They range from no significant change (Google A/B), to slower reviews (Beko; Meta when AI patches were shown to reviewers), to faster ones (Atlassian, Microsoft; both observational or self-published).

### Cited Findings

**Google: ML-suggested edits to resolve reviewer comments (2023) [OBS, company blog]**
- Frömmgen & Kharatyan (Google Research blog, May 23, 2023): at a target precision of 50%, the model could address 52% of reviewer comments offline. Online, suggestions were produced for "around 50% of all relevant reviewer comments." — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- 40–50% of *previewed* suggested edits were applied. After UX changes, >70% of previewed edits were applied, and the share of reviewer comments addressed by an ML edit doubled from beta to full internal launch. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- UX mattered a lot: the preview rate rose from ~20% of generated suggestions to ~40% after the UI redesign. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- Productivity claim: authors spend ~60 min of active "shepherding" time between review and submit, and Google projected savings of "hundreds of thousands of hours annually." This is an estimate, not a measured outcome. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)

**Google: AutoCommenter, Vijayvergiya et al., AIware 2024 (arXiv 2405.13565) [RCT A/B + OBS + SELF]**
- An LLM (T5/T5X) learned and flagged language best-practice violations in C++, Java, Python and Go. It went from ~3,000 early adopters (Jul 2022) to a ~50%-of-developers A/B test (Jul 2023) to all Google developers (Oct 2023). — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- The usefulness target was an 80% "useful" ratio. Developer-rated usefulness plateaued at 54% early on, rose to 66% (developer) and 74% (independent raters) after suppressing non-actionable categories, and reached the 80% target before wider rollout. Only ~10% of review comments and 2% of IDE diagnostics got explicit feedback. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- An estimated ~40% of posted comments were resolved. This was measured by AST line mapping over 6,000 snapshot pairs, and 80% of the sampled pairs were confirmed as direct fixes. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- **The A/B test found no statistically significant change in total review duration, active reviewer time, or comment-response iterations**, with a slight improvement in coding speed. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- Calibration: a single global threshold of t=0.98 was too restrictive (80% false-negative rate), so the team switched to per-category (per style-guide URL) thresholds. They suppressed 22 non-actionable URLs plus 5 more. Each comment links to the style-guide URL it relies on, 330 URLs were covered in production, and the top 85 URLs produced 90% of comments. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- Failure mode: stale training data. A change in Python 3.9 type conventions made the model recommend outdated practices, which was fixed with regex-based conditional filtering rather than retraining. Raters' complaints included "overly complex guidance," missing summaries, and subjective practices. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)

**Meta: MetaMateCR, AI-assisted fixes to code review comments (arXiv 2507.13499, FSE 2026 Industry) [RCT safety trials + production]**
- Meta sees tens of thousands of review comments per week. Llama models were fine-tuned on 64k (comment, patch) pairs, and the best model produced an exact-match patch 68% of the time offline (+9pp vs GPT-4o). In production, its ActionableToApplied rate was 19.7% (+9.2pp vs GPT-4o). — [arXiv 2507.13499](https://arxiv.org/pdf/2507.13499)
- **Key presentation finding:** in a randomized safety trial, showing AI patches to *reviewers* made reviews take >5% longer. When the UI showed patches only to *authors*, with reviewers able to expand them, review time returned to normal and acceptance rates stayed the same. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499v1); summary at [RDEL #109](https://rdel.substack.com/p/rdel-109-how-do-ai-assisted-code)

**Microsoft: internal AI code review assistant (Engineering@Microsoft blog, Jul 14, 2025) [OBS/VENDOR-ish, self-published]**
- Covers >90% of PRs company-wide, more than 600K PRs/month. — [Microsoft Engineering blog](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)
- "Early experiments and data science studies" on 5,000 onboarded repos showed a **10–20% median PR completion-time improvement**. The method, controls and effect sizes are not published in peer-reviewed form. What was learned fed into GitHub Copilot code review. — [Microsoft Engineering blog](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)

**Atlassian: RovoDev Code Reviewer, Tantithamthavorn et al. (arXiv 2601.01129, ICSE-SEIP 2026) [QE + OBS + SELF]**
- 12 months (Jun 2024–Jun 2025), 1,900+ repos, 54,000+ generated comments, 86,614 PRs (43,633 with RovoDev comments vs 42,981 without). The design was observational with interrupted time series, **not randomized**. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)
- 38.70% of RovoDev comments led to code changes, vs 44.45% for human comments. Median PR cycle time was 14.35h vs 20.73h (−30.8/31%). Human comments per PR dropped from 4.45 to 2.87 (−35.6%). Both differences had p<0.001 (Mann-Whitney). — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1); [ICSE 2026 SEIP listing](https://conf.researchr.org/details/icse-2026/icse-2026-software-engineering-in-practice/2/RovoDev-Code-Reviewer-A-Large-Scale-Online-Evaluation-of-LLM-based-Code-Review-Autom)
- Filtering: a ModernBERT "actionability" filter improved alignment by 15–20pp. An LLM-as-judge "factual correctness" check had minimal impact. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)
- Prompt ablation: removing the review guidelines cost ~5pp, the largest single contribution. Persona, chain-of-thought and PR/Jira info contributed 1–3pp each. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)
- User complaints centered on a "lack of holistic understanding": wrong language identified, and missing framework, version or deprecated-API context. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)
- Atlassian also published a marketing version of these results. — [Atlassian blog](https://www.atlassian.com/blog/rovo/how-we-cut-pr-cycle-time-with-ai-code-reviews)

**Beko: Qodo PR-Agent, Cihan et al., "Automated Code Review In Practice" (arXiv 2412.18531, ICSE-SEIP 2025) [QE/OBS + SELF]**
- 3 projects, 4,335 PRs, 1,568 of them with automated review. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- 73.8% of automated comments were labelled "resolved." However, **average PR closure time rose from 5h52m to 8h20m** after adoption. Developers also reported faulty reviews, unnecessary fixes and irrelevant comments in the survey portion. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2); [RDEL #92 summary](https://rdel.substack.com/p/rdel-92-how-do-ai-code-reviews-impact)
- Caveat: "resolved" is a status developers set, so it is not proof that the code changed. Resolving a comment can just mean dismissing it.

**Mozilla + Ubisoft: RevMate (arXiv 2411.07091) [field study, OBS + SELF]**
- A 6-week live study with 59 reviewers, 587 patch reviews and ~1.6k generated comments. RevMate used an off-the-shelf LLM with RAG for code/review context plus an LLM-as-judge filter that discards irrelevant comments. — [arXiv 2411.07091](https://arxiv.org/html/2411.07091v1); [Mozilla Foundation listing](https://www.mozillafoundation.org/en/research/library/impact-of-llm-based-review-comment-generation-in-practice-a-mixed-open-closed-source-user-study/)
- Only **8.1% and 7.2% of generated comments were accepted** (the two organizations, in the order reported). Another **14.6% and 20.5%** were marked "valuable as review or development tips" without being posted. — [arXiv 2411.07091](https://alphaxiv.org/abs/2411.07091)
- Ubisoft La Forge's practitioner write-up (Sep 5, 2025). — [Ubisoft La Forge](https://www.ubisoft.com/en-us/studio/laforge/news/3SsR9KkpyUCBvy1Wyw3lTS/impact-of-an-llmbased-code-review-assistant-in-practice)

**Ericsson: experience report (arXiv 2507.19115, ICSME 2025 Industry) [SELF, tiny N]**
- LLM plus static analysis, tested with 9 senior developers: 36 pairwise model comparisons and 15 days of practical use. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v1)
- 4/9 said it saved time. Usage was regular for 2/9, sometimes for 5/9, and once only for 2/9. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v1)
- When reviews were unsatisfactory, 4 developers said the output "merely explained code functionality," 2 reported factually incorrect analyses (e.g., wrong variable types), and 3 said it focused on irrelevant areas. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v1)

**WirelessCar (Sweden): Aðalsteinsson et al., "Rethinking Code Review Workflows with LLM Assistance" (arXiv 2505.16339, 2025) [field study + small field experiment, SELF]**
- 10 developers in the field experiment, each reviewing 2 standardized PRs. Mode A (AI-led: an upfront PR summary plus potential issues) was compared with Mode B (on-demand assistant, no upfront summary). — [arXiv 2505.16339](https://arxiv.org/pdf/2505.16339v1)
- Developers preferred AI-led reviews overall, but the preference depended on how familiar they were with the codebase and how severe the PR was. Pain points included context switching and insufficient context, along with concerns about false positives and trust. — [arXiv 2505.16339](https://arxiv.org/abs/2505.16339)

**GitHub Copilot code review [VENDOR]**
- GitHub blog (Gopu & Apirian, Mar 5, 2026): 60M+ Copilot code reviews, "more than one in five code reviews on GitHub," and 12,000+ organizations. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- "In 71% of the reviews, Copilot code review surfaces actionable feedback. In the remaining 29%, the agent says nothing at all." The stated principle is "silence is better than noise." It averages ~5.1 comments per review. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- In internal A/B tests, the agentic architecture (tool calls to read repo context) gave an initial +8.1% in positive feedback, and reasoning models gave +6% positive feedback at +16% latency. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- How "actionable" is defined and measured is not disclosed, and none of this is peer reviewed.

**Independent check on agent-only review (MSR 2026) [OBS]**
- Chowdhury et al., "From Industry Claims to Empirical Reality" (arXiv 2604.03196, MSR 2026). The sample was the AIDev dataset: 19,450 PRs, 3,109 analyzed, and 13 code review agents (CRAs). PRs reviewed only by CRAs merged 45.20% of the time vs 68.37% for human-only reviews (−23.17pp). 12 of 13 CRAs had average "signal ratios" below 60%, and 60.2% of closed CRA-only PRs fell in the 0–30% signal range. — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
- The paper explicitly rebuts the vendor claim that CRAs "can manage 80% of PRs … without human involvement." — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)

### Inferences
- Across sites, the "acted-on" rate for generated review comments clusters at 7–8% (Mozilla/Ubisoft accepted), ~20% (Meta applied, GitHub Actions changed), and ~39–40% (Atlassian, Google AutoCommenter). Beko's 73.8% "resolved" counts a status flag, not code change. A tool should expect most model-generated remarks to be ignored and design for skimmability and cheap dismissal.
- The only randomized measurements of review *time* (Google AutoCommenter A/B; Meta's safety trial) found either no time savings or a slowdown when AI output was put in front of the reviewer. The speed-ups (Atlassian −31%, Microsoft 10–20%) come from observational or self-published analyses. Treat claimed time savings as unproven.
- Meta's result is direct evidence that *who* sees AI output, and whether it is collapsed by default, changes reviewer time. Default-collapsed, reviewer-optional content is the safer design.
- Precision gating (per-category thresholds, category suppression, actionability classifiers) did more for usefulness than model upgrades. Google went from 54% to 80% "useful" mainly by suppression and calibration.

### Gaps
- Meta's "AI-assisted Code Authoring at Scale" (CodeCompose, Dunay et al., FSE 2024) and the Meta Diff Risk Score work were not verified this session. I did not confirm whether either includes review-specific outcomes.
- I found no peer-reviewed Microsoft paper with the methodology behind the 10–20% PR completion claim.
- "Leveraging Reviewer Experience in Code Review Comment Generation" (Lin et al., 2024) was not verified this session, so no numbers are reported.
- Sample sizes of the RevMate field study per organization (Mozilla vs Ubisoft split) were not extracted.

## 2. Academic studies: comment quality, PR descriptions, hallucination, trust and over-reliance

### Takeaway
Generated PR descriptions are associated with faster review and higher merge rates, but in an observational early-adopter sample. ~22% of LLM review comments are hallucinated even in a production-grade system, and fewer than 20% of comments from open-source AI review bots lead to code changes. The one rigorous controlled experiment with professionals (Tufano et al., ICSE 2025) found that AI-generated reviews anchor reviewers, add low-severity findings without adding high-severity ones, and save no time.

### Cited Findings

**PR descriptions: Xiao et al., "Generative AI for Pull Request Descriptions: Adoption, Impact, and Developer Interventions" (PACM SE / FSE 2024; arXiv 2402.08967) [QE]**
- 18,256 Copilot-for-PRs PRs across 146 GitHub repos, vs 54,188 non-Copilot PRs from the same repos. Data came from beta-period early adopters, Mar–Aug 2023. — [arXiv 2402.08967](https://arxiv.org/html/2402.08967v1); [FSE 2024](https://2024.esec-fse.org/details/fse-2024-research-papers/105/Generative-AI-for-Pull-Request-Descriptions-Adoption-Impact-and-Developer-Interven)
- Average treatment effect on the treated: **−19.3 hours review time**, with medians of 12.17h (treated) vs 16.09h (control). Copilot-assisted PRs were **1.57× more likely to be merged** (95% CI 1.35–1.84): 84% vs 71% merged. The study controlled for 17 confounders, but it is quasi-experimental and the authors acknowledge possible unmeasured confounding and limited generalizability. — [arXiv 2402.08967](https://arxiv.org/html/2402.08967v1)
- Usage: the "copilot:summary" tag appeared 13,231 times and "copilot:walkthrough" 8,990 times. — [arXiv 2402.08967](https://arxiv.org/html/2402.08967v1)
- Developer edits to AI descriptions (1,437 revisions across 311 PRs): 22.9% deleted generated content, 20.8% refined phrasing, 17.4% removed entire sections, 14.7% replaced content with their own text, 22.8% added template info, and 22.7% added links. — [arXiv 2402.08967](https://arxiv.org/html/2402.08967v1)
- Note: the 19.3h ATT is much larger than the 3.9h median gap. The distribution is likely skewed, so cite the ATT with that caveat.

**AI review bots in open source: "Does AI Code Review Lead to Code Changes? A Case Study of GitHub Actions" (arXiv 2508.18771, 2025) [OBS]**
- 16 AI code-review GitHub Actions, 22,326 comments, 178 repos. **Fewer than 20% of AI review comments led to code changes.** — [arXiv 2508.18771](https://arxiv.org/html/2508.18771v1)
- Comments were more likely to cause changes when they were **concise, contained code snippets, were manually triggered, and came from hunk-level (vs whole-PR) tools**. — [arXiv 2508.18771](https://alphaxiv.org/abs/2508.18771)

**Hallucination in review comments: HalluJudge, Tantithamthavorn et al. (arXiv 2601.19072, FSE Companion 2026) [annotated sample + production feedback]**
- In 143 human-annotated RovoDev comments (97 PRs, 5 languages), **22% were hallucinated**, meaning claims "unsupported by, contradictory to, or outside the scope of" the diff. — [arXiv 2601.19072](https://arxiv.org/html/2601.19072v2)
- The detector reached F1 0.85 at ~$0.009–0.016 per judgment. On 557 production comments with developer feedback, 67–72% of comments it judged non-hallucinated received a thumbs-up, and it covered 53–65% of all thumbs-up comments. The authors recommend running it as a filter before comments reach developers. — [arXiv 2601.19072](https://arxiv.org/html/2601.19072v2)

**Related software-summary hallucination (bug reports, arXiv 2605.24137, 2026) [annotated sample]**
- In 80 LLM-generated structured bug-report summaries, ~47.9% had missing information and 12.3% had fabricated content. This is evidence that omission errors may outnumber outright fabrication in generated summaries. — [arXiv 2605.24137](https://arxiv.org/pdf/2605.24137)

**Controlled experiment on over-reliance: Tufano, Martin-Lopez, Tayeb, Dabić, Haiduc, Bavota, "Deep Learning-based Code Reviews: A Paradigm Shift or a Double-Edged Sword?" (ICSE 2025; arXiv 2411.11401) [RCT]**
- 29 professional developers (mean 11.4 years of experience), 72 reviews, 6 projects in Java and Python, 48 injected issues, and 50+ hours of recorded reviews. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1); [ICSE 2025](https://conf.researchr.org/details/icse-2025/icse-2025-research-track/72/Deep-Learning-based-Code-Reviews-A-Paradigm-Shift-or-a-Double-Edged-Sword-)
- Three treatments: manual review (MCR); a ChatGPT Plus–generated review as a starting point (ACR); and an "oracle" review listing all injected issues (CCR). — [arXiv 2411.11401](https://arxiv.org/pdf/2411.11401)
- ChatGPT's review identified 42% of the injected issues. Reviewers **kept 89% of the AI-identified issues** in their final reviews. The median share of injected issues found was **50% in both ACR and MCR**, so the AI produced no net gain. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1)
- **Reviewers focused on the code locations the AI pointed to rather than searching elsewhere.** ACR surfaced more *low-severity* issues but not more *high-severity* ones. — [arXiv 2411.11401](https://arxiv.org/pdf/2411.11401)
- Time: MCR mean 42 min (median 37), ACR mean 56 (median 42), CCR mean 57 (median 50). Confidence (1–5) was 3.5, 3.7 and 3.8 respectively, with no significant difference. So the AI review saved no time and did not raise confidence. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1)
- The authors recommend providing automated reviews **only after manual inspection** to avoid anchoring on the highlighted locations. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1)

**Manipulating AI review: Alexopoulos et al., "Measuring and Exploiting Contextual Bias in LLM-Assisted Security Code Review" (arXiv 2603.18740, 2026) [controlled]**
- 6 LLMs under 5 framing conditions, then 33 CVEs in 20 real projects run through two automated review pipelines (Claude Code, CodeRabbit). Simple template framing attacks were ineffective, but an LLM-assisted iterative refinement attack, which framed the PR or commit text so the change looked benign, got vulnerable code past review in 32/33 (97%) cases. — [arXiv 2603.18740](https://arxiv.org/abs/2603.18740)

**Background trust signal [SELF]**
- Stack Overflow 2025 Developer Survey, as reported secondhand: only 29% of developers trust AI output accuracy (down 11 points from 2024), and 46% actively distrust it. This was not verified at the primary source this session. — [WebProNews summary](https://www.webpronews.com/the-trust-deficit-why-developers-rely-on-ai-code-tools-they-wont-ship-unchecked/)

### Inferences
- The Tufano experiment and Meta's safety trial point the same way: putting AI findings in front of reviewers before they form their own view narrows where they look and can lengthen review. A tool that shows a "risk brief" first should explicitly direct attention to areas the AI did *not* flag, or let the reviewer form an independent first pass.
- The framing-attack result means an LLM-written brief that takes the author's PR description at face value can be steered. The brief should be built from the diff and verified checks, not from author-supplied claims, and it should show where a claim comes from.
- PR-description evidence (Xiao) supports auto-generated summaries, but authors routinely deleted or trimmed generated sections (≈23% deletions, 17% section removals). Summaries are likely too long or partly wrong by default.

### Gaps
- CodeReviewer (Li et al., ESEC/FSE 2022) and Tufano et al.'s TSE work on review-automation strengths and weaknesses: quality numbers were not re-verified this session.
- I found no controlled experiment isolating the effect of an AI *PR summary* (vs AI review comments) on reviewer defect detection or comprehension.
- I found no peer-reviewed study measuring "rubber-stamping" (approval without inspection) rates before and after AI review adoption.

## 3. Explanation research: do NL explanations / walkthroughs improve comprehension?

### Takeaway
Controlled HCI studies show that LLM explanations help comprehension, and that **anchored, concise, in-place explanations beat chat or sidebar explanations** on accuracy, speed and task load (Ivie, CHI 2024). On-demand in-IDE explanations improved task completion but not time or depth of understanding (GILT, ICSE 2024). None of these studies is specifically about diff review.

### Cited Findings
- **Ivie** (Yan, Hwang, Wu, Head, CHI 2024; arXiv 2403.02491) [RCT, within-subjects, N=32 grad students, unfamiliar OpenCV API]. Explanations anchored in the right margin (for code blocks) and beneath the hovered line (for expressions) were compared with a chat-based assistant. Comprehension accuracy was **90.2% vs 65.0%** (p<0.001), response time 2.8s vs 3.6s (p=0.011), and NASA-TLX scores were lower on all dimensions (p<0.001; e.g., mental demand median 2 vs 3.5). Distraction was rated 1/7 vs 3/7. Participants valued explanations being "targeted to specific places" over chat's "long paragraphs." — [arXiv 2403.02491](https://arxiv.org/html/2403.02491v1); [CHI paper PDF](https://arxiv.org/pdf/2403.02491)
- **GILT** (Nam et al., ICSE 2024; arXiv 2307.08177) [controlled user study, N=32]. An in-IDE LLM tool with prompt-free actions (explain the highlighted code, API details, domain terms, usage examples) **significantly improved task completion vs web search, but showed no significant gains in time or depth of understanding**. Benefits differed between students and professionals. — [arXiv 2307.08177](https://arxiv.org/html/2307.08177v3); [Google Research pub](https://research.google/pubs/using-an-llm-to-help-with-code-understanding/); [ICSE 2024](https://conf.researchr.org/details/icse-2024/icse-2024-research-track/187/Using-an-LLM-to-Help-With-Code-Understanding)
- Ericsson developers complained when reviews "merely explained code functionality." Explanation that restates the diff without judgment is seen as low value in a review context. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v1)
- Copilot for PRs "walkthrough" sections, which explain changes file by file, were used 8,990 times in the early-adopter sample, but the study did not separate their effect from that of summaries. — [arXiv 2402.08967](https://arxiv.org/html/2402.08967v1)

### Inferences
- Margin annotations anchored to specific lines are the presentation format with the best controlled evidence (Ivie). A separate long narrative panel is the weaker format.
- Explanations should add judgment (why this matters, what could break), not paraphrase the code.

### Gaps
- I found no controlled study measuring whether LLM explanations of *diffs* (as opposed to just-generated code or unfamiliar APIs) improve reviewers' defect detection or review speed.
- I found no study comparing inline vs sidebar placement specifically for code-review comments. Ivie's comparison is anchored-inline vs chat.

## 4. Presentation guidance: confidence, evidence/anchors, verified vs model claims, length, noise tolerance

### Takeaway
The measured levers are: precision gating and suppression of whole categories; citing a source for each claim (style-guide URLs); concise, hunk-level, code-containing comments; staying silent when there is nothing high-signal; collapsing AI output by default for reviewers; and filtering hallucinations against the diff. Developers' tolerance for noise is low: deployed systems target 50–80% precision or "useful" ratios.

### Cited Findings
- **Precision targets:** Google's comment-resolution model ran at 50% target precision. AutoCommenter required an **80% "useful" ratio** before broad rollout, using per-category thresholds and suppression of 27 non-actionable categories. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/); [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- **Cite evidence:** each AutoCommenter comment links to the specific best-practice URL it relies on, which grounds the claim in a citable source. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- **Silence beats noise:** GitHub stays silent on 29% of reviews by design. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/) [VENDOR]
- **Concise + code snippet + hunk-level + user-triggered** comments were more likely to cause code changes. — [arXiv 2508.18771](https://alphaxiv.org/abs/2508.18771)
- **Default visibility:** showing AI patches only to authors, with reviewers able to expand them, removed Meta's >5% review-time penalty without lowering acceptance. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499v1)
- **UI drives uptake:** Google's preview rate doubled (~20% to ~40%) and the apply rate rose to >70% after UX changes alone. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- **Hallucination filtering:** an LLM-as-judge check against the diff reached F1 0.85, and its "non-hallucinated" verdict correlated with developer thumbs-up. However, Atlassian found that its *factual-correctness* judge in the main pipeline had minimal effect, while the actionability classifier gave +15–20pp. — [arXiv 2601.19072](https://arxiv.org/html/2601.19072v2); [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1)
- **Context is a top complaint:** reviewers flagged missing framework, version and deprecated-API context (Atlassian) and insufficient context and context switching (WirelessCar). Retrieving repo context gave GitHub an initial +8.1% in positive feedback. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v1); [arXiv 2505.16339](https://arxiv.org/abs/2505.16339); [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- **Low engagement with feedback controls:** only ~10% of AutoCommenter review comments got explicit thumbs feedback, so feedback buttons alone are a thin signal. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565)
- **Upfront summary preference is conditional** on codebase familiarity and PR severity (WirelessCar, N=10). — [arXiv 2505.16339](https://arxiv.org/pdf/2505.16339v1)

### Inferences
- For a review page: show a confidence or verification status on every claim, separating "verified" claims (a check ran, a test passed, a grep confirmed it) from "model claim." Anchor each claim to lines. Cap the number of annotations, preferring silence to low-confidence remarks. Keep the brief short. These follow directly from the precision-gating, citation, conciseness and hallucination findings, but no study has A/B-tested a "verified vs claimed" label specifically.
- Designers should budget for roughly 1 in 5 model claims being unsupported by the diff (HalluJudge's 22%). This argues for an explicit evidence link or check result on each risk claim.

### Gaps
- I found no empirical study measuring the effect of displayed *confidence scores* on reviewer trust or calibration in code review.
- I found no study reporting an explicit developer-stated false-positive tolerance threshold for LLM review. The commonly cited ~10% "effective false positive" bar comes from Google's pre-LLM static analysis work (Sadowski et al., CACM 2018) and was not re-verified this session.
- I found no measured optimum for summary length.

## 5. Risks: anchoring, reduced vigilance, rubber-stamping, manipulation

### Takeaway
Anchoring is directly measured in one rigorous experiment: reviewers concentrate on AI-flagged locations and gain no high-severity detections. Agent-only review correlates with worse merge outcomes. AI reviewers can be manipulated by PR framing. The mitigations with evidence are giving reviewers an independent pass first, collapsing AI output by default, and keeping humans in the loop.

### Cited Findings
- Anchoring: reviewers focus on LLM-indicated locations, 89% of AI-found issues are carried into final reviews, there is no gain in high-severity detection, and no time is saved. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1)
- Slower reviews when AI content is shown: +5% reviewer time at Meta when AI patches were visible to reviewers. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499v1)
- PR closure time rose from 5h52m to 8h20m at Beko after adopting AI review. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- Replacing humans: CRA-only PRs merged at 45.2% vs 68.4% with humans, with higher abandonment. — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
- Adversarial framing slipped vulnerabilities past two production AI review pipelines in 97% of 33 CVE cases. — [arXiv 2603.18740](https://arxiv.org/abs/2603.18740)
- Practitioner commentary on "automation bias" in AI review (vendor blog, not empirical). — [Codacy blog](https://blog.codacy.com/automation-bias-in-ai-generated-code-review-why-clean-code-still-ships-broken)
- Mitigation proposed by the experimenters: show the automated review after manual inspection. — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v1)

### Inferences
- A "reading path" plus margin annotations risks reproducing the anchoring effect at larger scale. Possible countermeasures: a "not covered by AI / please inspect manually" list, prompts for the reviewer's own first impressions, or progressive disclosure where details are revealed after the reviewer engages. These are untested hypotheses derived from the Tufano and Meta findings.
- Risk ratings that come from author-supplied text are exploitable, so they should be derived from diff and verified-check evidence.

### Gaps
- I found no published measurement of rubber-stamping (approval rates or time-to-approve on AI-summarized PRs vs controls) or of long-term deskilling of reviewers.
- I found no study testing a mitigation for anchoring (e.g., delayed reveal, a "blind spots" list) in code review.
