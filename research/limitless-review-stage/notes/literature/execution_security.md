# Execution-based security review: LLM agents that run code with adversarial inputs, and the recall they reach

Scope: designs and evidence for an "attack/execution" review pass that raises recall on security and adversarial-input defects in code changes (TypeScript/Bun, read-only reviewer that may run targeted tests and write temp files). Research date 2026-10-29. Evidence-strength labels: **[peer-reviewed]**, **[preprint]**, **[vendor claim]**, **[secondary only]** (only press, newsletter or search-snippet coverage seen; not checked against the primary source).

Already cited by the requester and not repeated here: AnyPoC (2604.11950), Verify Before You Fix (2604.10800), Refute-or-Promote (2604.19049), misguidance effect (2607.22883), ChaCo, Coding Agents as Test-Suite Auditors (2608.01715).

## 1. LLM-driven fuzzing and property-based testing for changed functions: bug-finding numbers and TypeScript applicability

### Takeaway
Agents that infer properties from code and docs, write property-based tests and run them do find real bugs at scale. The best measured setup reached 56% valid reports at about $10 per valid bug across 100 Python packages, and the best model reached 83% recall on bugs planted so that random inputs rarely hit them. Property tests and example tests catch *different* bugs, so running both (the union) beats either. Rigid scaffolding helps mid-tier models but made two strong models worse. No published evaluation covers TypeScript/fast-check.

### Cited Findings
- **Agentic PBT (Maaz, DeVoe, Hatfield-Dodds, Carlini; Anthropic/MATS), arXiv 2510.09907, Oct 2025 [preprint].** Claude Code with Opus 4.1, with the agent defined as a single Markdown prompt. It runs six stages: analyze the target, understand it by introspection and reading source, propose properties, write Hypothesis tests, run pytest and triage failures with a rubric, then write a bug report. Properties must be ones the code itself claims (docstrings, comments, how callers use it). — [arXiv HTML](https://arxiv.org/html/2510.09907v1)
  - Scale: 100 packages, 933 modules, 984 bug reports; 84.2% of modules produced at least one report. Total cost $5,474 ($5.56 per report, about $9.93 per valid bug as an upper bound), 8.8 min and about 110 turns per module. — [arXiv HTML](https://arxiv.org/html/2510.09907v1)
  - Validity on a manually reviewed sample: 56.0% valid bugs (95% CI 42.2–69.8%), 32.0% valid and worth reporting. A severity/validity ranking rubric raised this to 86% valid and 81% reportable among the 21 top-scoring reports. Initial inter-rater agreement was low (κ = 0.31). — [arXiv HTML](https://arxiv.org/html/2510.09907v1)
  - Main failure mode: the agent cannot tell intended design from a bug ("intent ambiguity"). The paper has no ablations. — [arXiv HTML](https://arxiv.org/html/2510.09907v1)
  - Earlier baseline: Vikram et al. (2023) found LLM-written property tests captured at most 21% of documented properties. The best model/prompt needed about 2.4 samples to get one valid and sound test. — [arXiv 2307.04346](https://arxiv.org/pdf/2307.04346); figure as summarized in [2510.09907](https://arxiv.org/html/2510.09907v1)
  - Follow-ons: Anthropic red-team write-up — [red.anthropic.com](https://red.anthropic.com/2026/property-based-testing); a `/hypothesis` Claude Code command released by the Hypothesis maintainers — [hypothesis.works](https://hypothesis.works/articles/claude-code-plugin/)
- **PBT-Bench, arXiv 2605.15229, NeurIPS 2026 Datasets & Benchmarks track [peer-reviewed].** 100 problems across 40 real Python libraries with 365 injected semantic bugs. The bugs are built so that default random strategies rarely trigger them, and the agent must write a Hypothesis strategy that concentrates inputs in the region that triggers the bug. Eight LLMs, three runs each. — [arXiv](https://arxiv.org/abs/2605.15229)
  - Bug recall ranged from 42.1% to 83.4% with the PBT-guided prompt and 31.4% to 76.7% with an open-ended baseline. Scaffolding lifted mid-capability models by more than 20 points, gave smaller gains to the strongest models, and made two models worse. The authors say the structured prompt "can interfere with certain model behaviours." — [arXiv](https://arxiv.org/abs/2605.15229)
  - The hardest bugs differ by model, and no single model closes all the gaps. — [arXiv](https://arxiv.org/abs/2605.15229)
- **PBT vs example-based tests (Tanaka et al.), arXiv 2510.25297, Oct 2025 [preprint, small n].** Claude Sonnet 4 wrote both kinds of tests for 16 HumanEval problems whose canonical solutions fail HumanEval+. PBT caught 11/16, EBT caught 11/16, and their union caught 13/16. Each method caught 2 bugs the other missed. — [arXiv HTML](https://arxiv.org/html/2510.25297v1)
- **Property-based validation for code generation (He et al.), arXiv 2506.18315 [preprint].** Reported 23.1–37.3% relative pass@1 improvement over TDD-style validation. I saw this figure only as cited in 2510.25297. — [arXiv 2510.25297](https://arxiv.org/html/2510.25297v1)
- **Google OSS-Fuzz-gen (Nov 2024) [secondary only; Google blog not fetched].** LLM-generated fuzz targets found 26 new vulnerabilities, including OpenSSL CVE-2024-9143 (an out-of-bounds write, likely present for about 20 years), in projects that already had hundreds of thousands of fuzzing hours. Coverage went from 160 to 272 C/C++ projects, adding more than 370k lines covered. — [The Hacker News](https://thehackernews.com/2024/11/googles-ai-powered-oss-fuzz-tool-finds.html); [Google Security Blog, Nov 2024](https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html)
- **Fuzz4All (Xia et al., ICSE 2024) [peer-reviewed; numbers from my recollection of the abstract, not re-fetched this session].** LLM-as-input-generator fuzzing across 6 languages / 9 systems under test reported 98 bugs, 64 of them confirmed as previously unknown, and higher coverage than language-specific fuzzers. — [arXiv 2308.04748](https://arxiv.org/abs/2308.04748)
- **Trail of Bits Buttercup (AIxCC 2nd place) [vendor claim].** An LLM seed generator queries a program model (CodeQuery, Tree-sitter) and feeds inputs into the same shared corpus as libFuzzer/Jazzer. Trail of Bits says LLM seeds "significantly reduce" time to discovery, and its post-semifinal lessons say CWE-specific seed generation may have helped. It reported 28 vulnerabilities across 20 CWEs at 90% accuracy using only non-reasoning LLMs. — [Trail of Bits Buttercup](https://www.trailofbits.com/buttercup/); [GitHub](https://github.com/trailofbits/buttercup); [DEF CON stage talk](https://www.trailofbits.com/documents/DEFCON_AIxCC_Stage_Talk.pdf)
- **Jazzer.js:** a coverage-guided, in-process fuzzer for Node.js built on libFuzzer, with Jest integration. It is the JavaScript engine in OSS-Fuzz. — [Code Intelligence blog](https://www.code-intelligence.com/blog/jazzer-js); [OSS-Fuzz JS guide](https://google.github.io/oss-fuzz//getting-started/new-project-guide/javascript-lang/)

### Inferences
- For a TypeScript/Bun repo, **fast-check** is the practical PBT engine: a pure-JS library that works with any test runner, so it should run under `bun test`. **I did not verify Bun compatibility in this session.** The agentic-PBT recipe (infer properties the code claims, write property tests, run, triage) transfers directly. Coverage-guided fuzzing via Jazzer.js depends on a native libFuzzer addon and Node instrumentation hooks, so it probably will not run under Bun. Use fast-check with custom arbitraries plus LLM-written seed corpora instead.
- The bugs in PBT-Bench ("random inputs rarely trigger; the agent must aim the strategy at the trigger region") are structurally the same as the misses we care about: layered URL/Unicode/JSON encodings, ANSI escapes split across chunk boundaries, truncation before redaction. Recall depends on the agent writing **targeted generators** (an `encodeLayers(secret)` arbitrary, a chunk-split arbitrary), not on asking `fc.string()` to stumble on them.
- About $5–10 per module in the agentic-PBT study implies a budget of a few dollars per changed security-relevant function, and only where the diff touches a trust boundary.
- The union result (PBT 11 + EBT 11 → 13) and the "hardest bugs are model-specific" result both argue for **several diverse attack generators whose findings are unioned**, not one better-prompted generator.

### Gaps
- No study evaluates LLM-written fast-check properties or any TypeScript PBT. Searches turned up only practitioner blogs.
- Jazzer.js maintenance status and Bun support are unverified.
- No numbers on LLM-PBT recall for *security* invariants specifically (redaction, sandbox policy). All PBT evidence is functional-correctness bugs.
- Google's November 2024 OSS-Fuzz post was seen only through press coverage. No 2025–2026 OSS-Fuzz-gen update was found.

## 2. Differential and metamorphic testing by LLMs (e.g., "redact(encode(x)) never contains secret") and mutation-based adversarial inputs

### Takeaway
Nothing I found evaluates LLM-written metamorphic relations for sanitizers or redactors. The closest strong evidence comes from AIxCC: LLM components solved vulnerability paths guarded by **encoding transformations (URL encoding), Unicode normalization, regexes and compression**, which coverage-guided fuzzing could not. Multi-step transformation chains (XOR/shift, AES+Base64) defeated them end to end, and the authors note that "tool-assisted verification could help." That is the mechanism behind our layered-encoding redaction misses.

### Cited Findings
- **SoK: DARPA AIxCC (Zhang et al., incl. Taesoo Kim), arXiv 2602.07666 v5, 2026 [preprint; authored by finalist-team members].** KF3: "LLMs complement coverage-based fuzzing in directed (delta-mode) and constraint-heavy contexts." The challenges LLMs solved where fuzzers failed include paths guarded by "regex patterns ..., encoding transformations like URL encoding (cc4▲06), Unicode normalization (cc6▲07, po1□02), or zlib compression (pb1▲02), symlink-based path obfuscation (cc7▲08), and mathematical guards." "LLMs can reason about these transformations and generate constraint-satisfying inputs." — [arXiv 2602.07666](https://arxiv.org/abs/2602.07666) ([PDF](https://arxiv.org/pdf/2602.07666))
  - Limits: "Multi-step cryptographic transformations (cu3▲07: XOR/shift; cu4▲08: AES with Base64 encoding) accumulate LLM errors end-to-end, where tool-assisted verification could help." — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
  - Grammar obstacles: systems extracted format specifications from source to generate syntactically valid structured inputs (TLV, PDF with XFA, XLSX for SSRF). — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- **Anthropic Frontier Red Team, "zero-days" (Feb 2026) [vendor claim; case studies, not rates].** In the CGIF case, Claude found that the library assumes LZW output is never larger than its input, then reasoned about dictionary resets to produce an overflow. The post argues that even 100% line and branch coverage might not expose this bug, because it needs a specific sequence of operations. — [Anthropic research](https://www.anthropic.com/research/zero-days)
- Practitioner guidance on using fast-check to test LLM-generated code exists, but it reports no measured results. — [understandingdata.com](https://understandingdata.com/posts/property-based-testing/)

### Inferences
- Encode the reviewer's attack as **metamorphic/differential oracles the agent writes and runs**, not as a probe it must "reproduce":
  - `∀ secret, ∀ encoding chain E ∈ {url, url∘url, unicode-NFKC variants, JSON-escape, base64, ANSI-wrapped}: redact(E(secret)) ∌ secret and decode*(redact(E(secret))) ∌ secret`
  - `∀ split point k: redact(chunk[0..k]) + redact(chunk[k..]) ∌ secret`, which covers chunk-boundary ANSI and secret splits.
  - `redact(truncate(x)) ⊇ truncate(redact(x))` in leak terms, which covers truncation before redaction.
  - Differential: `classifyNew(x) == classifyOld(x)` on crafted file contents, plus a reference implementation (`decode, then substring`) versus the production implementation.
  The AIxCC result says LLMs can produce inputs that satisfy single transformations. The "multi-step accumulates errors" result says the *execution* of these oracles, not the LLM's mental simulation, should decide whether a deep encoding chain leaks.
- Mutation-based generation fits here: give the agent a seed attack (one encoding layer) and have it compose mutations (add a layer, split at every offset, insert an escape introducer) inside a fast-check arbitrary. This mirrors Buttercup's "LLM seeds feed the fuzzer corpus" design (§1).

### Gaps
- No paper measures LLM-generated metamorphic relations for security sanitizers, redaction or escaping functions. The design above is an inference.
- No evidence on differential testing of policy engines (e.g., sandbox profiles) by LLMs.

## 3. Security-focused agentic reviewers and systems: architecture, how they combine static hints + execution + LLM reasoning, published recall

### Takeaway
Every strong system pairs LLM *candidate generation* with *execution-based confirmation*. The best ones do **not** discard unconfirmed candidates. They label or gate them, or keep them in a separate lane. Headline recall numbers come from AIxCC (86% of 63 planted vulnerabilities found by all teams combined) or are vendor self-reports on in-house corpora (Aardvark 92%). Independent measurements on real code are much lower (CyberGym about 20–30% single-trial; Semgrep 14–18% true-positive rate with very unstable run-to-run output).

### Cited Findings
- **DARPA AIxCC final (Aug 2025) [official results].** Systems found 54 and patched 43 synthetic vulnerabilities. DARPA revised the denominator to 63, giving **86% found and 68% patched** (earlier materials say 77%/61% of 70, and those figures still circulate). Semifinals were 37% found and 25% patched. Teams also found 18 real non-synthetic vulnerabilities. Team Atlanta won (392.76 points), followed by Trail of Bits and Theori. — [DARPA](https://darpa.mil/news/2025/aixcc-results); [Trail of Bits slides (70-vuln figures)](https://www.trailofbits.com/documents/AIxCC_Main_Stage_Presentation.pdf)
- **SoK on AIxCC (arXiv 2602.07666) [preprint].** Team codes used in the paper: AT = Team Atlanta (Atlantis, 1st), TB = Trail of Bits (Buttercup, 2nd), TI = Theori (RoboDuck, 3rd), FB = Fuzzing Brain, SP = Shellphish (Artiphishell), 42 = 42-b3yond-6ug (BugBuster), LC = Lacrosse. — [arXiv](https://arxiv.org/pdf/2602.07666)
  - Baseline: parallel fuzzing alone (8,906 CPU-hours) solved 34 of 63 (54%): 30/40 in C but only 4/23 in Java. Six systems each solved **7–16 vulnerabilities that fuzzing alone could not**, "largely attributed to LLM components."
  - **Diff hints dominate:** "Delta challenges dominate non-PF-solvable CPVs solved by CRSs (15/22). Given diff-based hints about vulnerability locations, CRSs analyze code changes and generate triggering inputs directly." The two systems with classic directed fuzzing found no delta-mode bugs that the others missed. The targeted capability was "driven primarily by LLM reasoning."
  - LLM PoV pipeline (6 teams): (1) identify and filter candidates using LLMs plus CodeQL/Semgrep/Infer and sink lists, ranked by logprob confidence or weighted votes across tools and LLMs; (2) a PoV agent with call paths, coverage, runtime logs and a debugger. One team (TB) skipped the filter and let the agent judge during PoV generation.
  - **Reproduction mismatch costs recall:** "Some stateful bugs require multiple executions to trigger: sd1□05 crashes on the second execution, and the organizer runs 100 times by default. Thus, CRSs verifying with a single execution discarded valid PoVs." Using the wrong sanitizer (ASan instead of UBSan) also lost a vulnerability for all but one team.
  - **No-PoV lane:** three systems (TI = Theori, FB = Fuzzing Brain, LC = Lacrosse) generated patches for candidates *without* a PoV. They managed the risk by "limiting no-PoV patch quantities per challenge and imposing stricter submission conditions (e.g., delayed submission, gated by prior success rate)" rather than dropping them. In shadowsocks, systems patched five same-pattern overflows with no PoV by recognizing the repeated pattern.
  - Real-world zero-days: 25 distinct vulnerabilities across 10 OSS projects, of which 12 (48%) were patched.
  - Lesson: "pure-LLM pipelines still carry fundamental limitations such as hallucination and nondeterminism," so the LLM/non-LLM cooperation patterns remain a reference even with stronger models.
- **Team Atlanta ATLANTIS technical report, arXiv 2509.14589, Sep 2025 [preprint].** "Ensemble everywhere": coverage-guided and directed fuzzers, concolic execution and LLM agents (a multi-language LLM agent, an LLM-augmented mutator, a deep generator) run in parallel around a shared bug-candidate pipeline. — [arXiv](https://arxiv.org/abs/2509.14589); SoK characterization: [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- **Anthropic Frontier Red Team, Opus 4.6 zero-days (Feb 2026) [vendor claim].** "More than 500 high-severity vulnerabilities" found and validated. The setup was a VM with standard tools, debuggers and fuzzers, no special instructions or custom harness, focused on memory corruption with sanitizers. Claude critiqued, de-duplicated and re-prioritized its own crashes; human researchers validated findings. — [Anthropic research](https://www.anthropic.com/research/zero-days)
  - In 2 of 3 case studies **fuzzing was tried first and failed**:
    - GhostScript: Claude read git history, found a commit that added a bounds check, inferred the pre-fix code was vulnerable, and found **a second caller lacking the check**.
    - OpenSC: Claude searched for commonly misused functions (`strcat` chains) on a line fuzzers rarely reach.
  - Each bug was confirmed with a proof-of-concept. No false-positive rate or pre-triage candidate count was published. — [Anthropic research](https://www.anthropic.com/research/zero-days)
  - Later, Claude Mythos Preview reportedly flagged 23,019 potential vulnerabilities (6,202 estimated high/critical) [secondary only]. — [eWeek](https://www.eweek.com/news/claude-mythos-vulnerabilities-may-2026/)
- **Anthropic agentic PBT** (see §1) is the clearest published "attack by executing" agent design with measured validity rates. — [arXiv 2510.09907](https://arxiv.org/html/2510.09907v1)
- **OpenAI Aardvark (announced Oct 2025) [vendor claim].** Builds a threat model from the whole repository, scans each new commit against it, tries to trigger flagged issues in an isolated sandbox, and proposes Codex patches. Reported **92% recall** on internal "golden" repositories with known and synthetically introduced vulnerabilities. — [OpenAI](https://openai.com/index/introducing-aardvark); [VentureBeat](https://venturebeat.com/security/meet-aardvark-openais-in-house-security-agent-for-code-analysis-and-patching)
- **OpenAI Codex Security (Mar 6, 2026) [vendor claim].** Builds a project-specific, editable threat model; the model ranks likely issues; auto-validation then tries to reproduce each in a clean container, and reproduced findings are *marked* validated. Beta claims: false positives down more than 50% across repos, low-impact noise down 84% in some cases. The FAQ says it does not replace exploitability checks or human threat assessment. — [OpenAI Codex Security FAQ](https://developers.openai.com/codex/security/faq); [SiliconANGLE](https://siliconangle.com/2026/03/06/openai-introduces-codex-security-help-developers-fix-software-vulnerabilities/); [Help Net Security](https://www.helpnetsecurity.com/2026/03/09/openai-codex-security%E2%81%A0-feature/)
- **Google CodeMender (Oct 6, 2025) [vendor claim].** Gemini Deep Think agent; 72 security fixes upstreamed in six months, all reviewed by humans. Builds on Big Sleep and OSS-Fuzz. — [BetaNews](https://betanews.com/2025/10/06/google-builds-new-ai-agent-to-improve-code-security); [Infosecurity Magazine](https://www.infosecurity-magazine.com/news/google-codemender-available-ai/)
- **Semgrep study of Claude Code and Codex as vulnerability finders (2025) [secondary only; original blog not fetched].** On 11 real-world Python web apps: Claude Code made 46 findings at a 14% true-positive rate (strong on IDOR); Codex made 21 findings at 18% (strong on path traversal). Repeated runs with the identical prompt on one app found 3, then 6, then 11 distinct findings. — [Semgrep newsletter (DEV)](https://dev.to/semgrep/semgrep-newsletter-ai-code-assistant-research-security-alerts-quarterly-release-and-more-8ca)
- **PoC validity caveat: "I Can't Believe It's Not a Valid Exploit" (PoC-Gym), arXiv 2602.04165, Feb 2026 [preprint].** On 20 real Java vulnerabilities, seemingly successful LLM PoCs were often invalid. A PoC counts as valid only if it exits 0, prints the marker, *and* reaches the sink in the execution trace. — [arXiv HTML](https://arxiv.org/html/2602.04165v1)
  - A secondary summary says models printed success markers without touching the target, hardcoded a copy of the vulnerable logic, or wrote evidence files directly, and that 71.5% of "successful" PoCs were invalid. I did not verify that figure in the paper. — [Substack summary](https://it4sec.substack.com/p/hacking-using-ai-written-exploits)
- **FaultLine, arXiv 2507.15241, Jul 2025 [preprint].** A proof-of-vulnerability test agent that traces source-to-sink data flow and reasons about path conditions before writing the test. It generated PoV tests for 16 of 100 vulnerabilities (Java, C, C++), against 9 for CodeAct 2.1. — [arXiv](https://arxiv.org/html/2507.15241v1)
  - PAGENT (ISSTA 2026) adds static analysis and sanitizer feedback to PoC generation. [peer-reviewed; numbers not read] — [arXiv 2604.07624](https://arxiv.org/pdf/2604.07624); [ISSTA 2026](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/108/PAGENT-Program-Analysis-Guided-LLM-Agent-for-Proof-of-Concept-Generation)
  - PoCGen covers npm packages (directly relevant to the JS ecosystem). [preprint; numbers not read] — [arXiv 2506.04962](https://arxiv.org/pdf/2506.04962)

### Inferences
- The consistent architecture is: **(a) a broad candidate generator** (LLM reading plus static hints plus diff focus) → **(b) targeted execution to build a trigger** → **(c) validation that labels results**, with a lane for unproven candidates. Codex Security *marks* reproduced findings rather than deleting the rest. AIxCC teams *gated* no-PoV candidates rather than discarding them. Our failed prompt made (b) a filter on (a), which none of these systems does.
- The GhostScript "fix in one caller, missing in a sibling caller" pattern maps onto our misses (redaction applied on the main path but not on error, retry or truncation paths). A cheap attack step: for each guard the diff adds or touches, enumerate every other entry point to the same sink, then run the attack input through each.
- Diff hints were the single largest source of beyond-fuzzer wins in AIxCC (15/22). A diff-scoped review is the setting where LLM-directed attack generation has the best evidence.
- PoC-Gym shows that a reviewer's "reproduced" claim is not evidence either. Trust a probe only if the harness (not the model) observes the secret in real output from real production code. This matches the repo's existing rule that "a model's claim is not evidence."

### Gaps
- No published recall for Claude Code's `/security-review` or the Anthropic security-review GitHub Action. No official XBOW, Snyk/DeepCode agentic or GitHub Copilot Autofix recall on real vulnerabilities was found in this session (not searched in depth because of the tool budget).
- No Big Sleep 2025 figures were confirmed from a primary source.
- Aardvark's 92% is on OpenAI's own planted-vulnerability corpus. No external replication.
- The SoK has no ablations ("No ablation study" is one of its stated limitations), so per-technique contributions are attributions, not controlled measurements.

## 4. LLM vulnerability-detection benchmarks: realistic recall, and which methods work (execution vs reading)

### Takeaway
On realistic, execution-checked tasks, single-attempt agent success is about 18–30%, and **repeated independent attempts roughly double it** (CyberGym: Sonnet 4.5 went from 28.9% with 1 trial to 66.7% with 30). Reading-only detection benchmarks show low F1 (SecVulEval best about 24%). PR-review benchmarks now test whether reviewers *approve* vulnerability-reintroducing PRs, but I did not read their recall numbers.

### Cited Findings
- **CyberGym (Wang et al.), ICLR 2026 [peer-reviewed].** 1,507 real vulnerabilities across 188 projects; the agent must produce a PoC that reproduces the bug. The best non-thinking combination (OpenHands with Claude Sonnet 4) reached 17.9%; the ICLR abstract says top combinations reach about 20%. Thinking mode raised GPT-5 from 7.7% to 22.0%. SWE-specialized models scored ≤2.0%. — [arXiv 2506.02548](https://arxiv.org/html/2506.02548v2); [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c876a2935a90aff21874e14c07dc3e33-Abstract-Conference.html)
  - Later results (Berkeley RDI blog): top agents reach about 30% with a single trial and about 67% with 30 trials; Claude Sonnet 4.5 went from 28.9% (1 trial) to 66.7% (30 trials). — [Berkeley RDI](https://rdi.berkeley.edu/blog/cybergym/)
  - A vendor (NSFOCUS) claims 95.02% on a CyberGym level-1 leaderboard [vendor claim; setup not comparable]. — [NSFOCUS](https://nsfocusglobal.com/?p=40719)
- **SecVulEval, arXiv 2505.19828, May 2025 [preprint].** A statement-level C/C++ benchmark with added context. The best model (Claude 3.7 Sonnet) reached 23.83% F1 for detecting vulnerable statements with correct reasoning, using a five-agent pipeline (normalization, planning, context, detection, validation). — [arXiv](https://arxiv.org/pdf/2505.19828)
- **CASTLE (2025) [preprint].** 250 micro-benchmark programs covering 25 CWEs, balanced between vulnerable and safe samples so both false negatives and false positives are measured. — [arXiv 2503.09433](https://arxiv.org/html/2503.09433v1)
- **JitVul (Yildiz et al.), ACL 2025 [peer-reviewed].** Just-in-time, repo-level detection of vulnerability-introducing commits; 879 CVEs from PrimeVul (1,758 commit pairs, 91 CWEs); compares plain LLMs with agents. — [arXiv 2503.03586](https://alphaxiv.org/abs/2503.03586); [ACL 2025 PDF](https://oar.a-star.edu.sg/storage/q/qr3jn0ng6d/acl-2025-benchmarking-llms-agents-in-repo-level-vulnerability-detection.pdf)
- **SEVRA-BENCH, arXiv 2606.13757, Jun 2026 [preprint].** 1,062 malicious PRs that revert real CVE fixes from the 2025 CWE Top-25, each wrapped in one of 15 social-engineering framings with the diff held fixed. Eight LLMs evaluated as review agents. The abstract reports a sharp gap between closed and open models. I did not read per-model approval rates. — [arXiv](https://arxiv.org/pdf/2606.13757)
- **PRWeaver, arXiv 2608.02693, 2026 [preprint].** Malicious changes split across several PRs, each plausible on its own; evaluates Claude Code, Copilot Code Review and others. Numbers not read. — [arXiv](https://arxiv.org/pdf/2608.02693)
- **Confirmation-bias study, arXiv 2603.18740, Mar 2026 [preprint].** Tests whether PR-metadata framing makes LLM reviewers miss reintroduced CVEs (250 CVE pairs, 4 models). Numbers not read. — [arXiv](https://arxiv.org/abs/2603.18740)
- **Bugdar, arXiv 2503.17302 [secondary only].** Reports 39% precision and 64% recall for vulnerability classification with retrieval on real GitHub PRs (seen only in a search snippet). — [alphaXiv](https://alphaxiv.org/overview/2503.17302v1)
- **"Coding agents supersede human inspection," arXiv 2606.13175 [preprint].** Warns that a reviewer agent may share the blind spots of the generating agent and can be steered by instructions embedded in the code it reads. — [arXiv](https://arxiv.org/pdf/2606.13175)

### Inferences
- Execution-checked benchmarks (CyberGym, AIxCC) report **lower** single-shot rates than reading-based vendor claims but are trustworthy. The 1→30-trial jump (28.9% → 66.7%) and Semgrep's 3→6→11 drift together say **sampling diversity is the cheapest recall lever**: several independent attack attempts whose findings are unioned.
- SEVRA-BENCH and the confirmation-bias study suggest the PR description itself lowers security recall. The attack pass should be shown the diff and the trust boundaries, not the author's framing.

### Gaps
- PrimeVul's own headline numbers for frontier agents were not retrieved. CVE-Bench, SEC-bench and VulnLLMEval numbers were not retrieved (tool budget).
- No benchmark found that is specific to TypeScript/Node *adversarial-input* defects (redaction, escaping, confinement policy).
- I found no direct controlled comparison of "read-only review" versus "review with execution" on the same vulnerability set. The closest is AIxCC's fuzzing baseline versus the full systems (34/63 versus +7–16 per system).

## 5. Threat-model-first review: generate a threat model / attack-surface list from the diff and trust boundaries, then attack each

### Takeaway
The two most-deployed vendor security agents (OpenAI Aardvark and Codex Security) both build a repository threat model first and check commits against it. Neither publishes an ablation, so evidence that threat-model-first *raises recall* is architectural and anecdotal, not measured. AIxCC adds a related signal: CWE-specific guidance and sink lists were used by several finalists, and Trail of Bits suspected CWE-specific seed generation would have helped.

### Cited Findings
- Aardvark builds a threat model of the project's "security objectives and design," then scans new commits against it before sandbox validation. — [OpenAI](https://openai.com/index/introducing-aardvark)
- Codex Security builds a project-specific threat model that users can edit as the architecture, risks and business context change; findings are ranked against it, then auto-validated in containers. — [OpenAI Codex Security FAQ](https://developers.openai.com/codex/security/faq); [third-party walkthrough](https://codex.danielvaughan.com/2026/03/31/codex-security-agent-vulnerability-scanning-threat-modelling)
- AIxCC finalists used predefined sink lists and CWE-specific vulnerability knowledge (2 teams) to steer candidate identification and generation. — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- Trail of Bits' post-semifinal lessons noted that CWE-type-specific seed generation may have helped. — [Trail of Bits Buttercup](https://www.trailofbits.com/buttercup/)
- A cross-surface evaluation on AgentDojo found that changing the attack surface reordered 35 of 78 model pairs. Vulnerability depends on the pairing of model and surface, which argues for enumerating surfaces explicitly. — [arXiv 2605.30454](https://arxiv.org/pdf/2605.30454)

### Inferences
- For this repo, the threat model largely exists already as prose (AGENTS.md "Trust boundaries", "Isolation", "Privacy" and the "Defects reviews keep finding" list). A diff-scoped threat-model step can be deterministic: map the touched files to a fixed attack catalog. For example:
  - `redactCredentials` / output paths → encoding layers, chunk splits, truncation order, ANSI.
  - `sandbox.ts` / `command.ts` / git → crafted repositories: submodules with their own git dirs, `.gitattributes` filters, config, hooks, symlinked gitdirs.
  - Classifiers → crafted file content (binary disguised as text, extension spoofing).
  - Gate/test-output parsing → substring spoofing by untrusted output.
  The LLM then *instantiates* attacks for each applicable catalog entry. This keeps control flow deterministic (a repo rule) while the creativity happens inside the stage.
- The catalog doubles as a recall checklist. Each entry must end in "attacked: leaked / held / could not build harness," so an entry can't be silently skipped. That turns "didn't think of the attack" misses into visible coverage gaps.

### Gaps
- No controlled study compares security-review recall with and without a threat-model step. Vendors assert the design but publish no ablation.
- No evidence on whether an LLM-generated threat model from a diff alone (without whole-repo context) is accurate enough to steer attacks.

## 6. Avoiding the failure we saw (a probe mandate reduced recall): separate attack generation from filtering, keep unreproduced findings, time budgets

### Takeaway
The −10-point regression has two documented mechanisms. (1) **Reproduce-or-drop filtering loses true positives**: AIxCC systems that verified with one execution discarded valid PoVs, and the strong systems kept a gated no-PoV lane instead. (2) **Rigid procedural scaffolding interferes with strong models**: PBT-Bench scaffolding made two models worse. The evidence-backed design separates a *generative attack pass* (several diverse samples, findings unioned) from a *labeling validator* that annotates rather than deletes, and treats reproduction as a confidence upgrade, never as a prerequisite for reporting.

### Cited Findings
- Single-execution verification discarded valid PoVs for stateful bugs; the organizer ran each PoV 100 times. — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- Three AIxCC systems kept a no-PoV patch lane, managed by quantity limits and stricter gating rather than dropping it; systems also fixed repeated-pattern bugs without PoVs. — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- Pipelines differ: TB (Trail of Bits) skipped the candidate filter and let the agent judge during PoV generation, while others filtered first by logprob confidence or weighted votes across tools and LLMs. Filtering was a *ranking* step, not a reproduction gate. — [arXiv 2602.07666](https://arxiv.org/pdf/2602.07666)
- PBT-Bench: explicit scaffolding gave mid-tier models more than +20 points but "can interfere with certain model behaviours"; two models declined. — [arXiv 2605.15229](https://arxiv.org/abs/2605.15229)
- Repeated independent trials raise recall from 28.9% to 66.7% (Sonnet 4.5, 1 vs 30 trials, CyberGym). — [Berkeley RDI](https://rdi.berkeley.edu/blog/cybergym/)
- Run-to-run variance: 3, 6, then 11 distinct findings from an identical prompt on one app. — [Semgrep newsletter](https://dev.to/semgrep/semgrep-newsletter-ai-code-assistant-research-security-alerts-quarterly-release-and-more-8ca)
- PBT and example-based testing are complementary (11/16 each, 13/16 combined). — [arXiv 2510.25297](https://arxiv.org/html/2510.25297v1)
- Codex Security marks reproduced findings as "validated" rather than suppressing the rest. — [OpenAI Codex Security FAQ](https://developers.openai.com/codex/security/faq)
- Generated PoCs can fake success (marker printed, sink never reached), so validation must check the trace or real output, not the PoC's own claim. — [arXiv 2602.04165](https://arxiv.org/html/2602.04165v1)
- Agentic PBT: validity was 56% on a reviewed sample of all reports and 86% among the 21 reports that scored highest on the ranking rubric. — [arXiv 2510.09907](https://arxiv.org/html/2510.09907v1)
- Fuzzing failed first in 2 of 3 Anthropic case studies. The bugs were found by reasoning (git history, risky-pattern search) and then *confirmed* with a PoC. — [Anthropic research](https://www.anthropic.com/research/zero-days)

### Inferences
- Agentic PBT used ranking to surface its most credible reports; the paper doesn't describe deleting the lower-ranked ones. Ranking, rather than deletion, is the noise-control pattern to borrow.

Candidate design for an attack/execution pass, synthesized from the above. The numbers attached are the cited analogues, not predictions for our eval.
1. **Deterministic trigger and catalog.** The pass runs only when the diff touches a trust boundary (path map from §5). It receives the diff, the touched trust-boundary rules and the attack catalog entries, and **not** the PR's narrative description (SEVRA-BENCH and confirmation-bias framing effects).
2. **Generate, don't filter.** The prompt asks for *attacks*: for each catalog entry, write a fast-check property or example test with a targeted arbitrary (encoding chains, chunk splits, crafted repo fixtures in a temp dir) and run it against the real function. Keep the prompt goal-oriented rather than a rigid step list (PBT-Bench interference). Ask for two complementary forms per entry: one property test and one hand-picked example set (the PBT/EBT union).
3. **Several independent samples.** Run k ≥ 2–3 attack agents with different seeds or framings (e.g., one "encoding/escaping attacker," one "sibling-path hunter" that enumerates other callers of each touched sink, GhostScript-style), and union their findings. Evidence: 1→30 trials, 29%→67%; model-specific hardest bugs.
4. **Labeling validator, separate context.** A deterministic harness, or a separate checker without the generator's context (AnyPoC-style), reruns each probe several times (stateful/flaky triggers) and checks that the secret or forbidden effect appears in *real output from production code*, not in a mock (PoC-Gym failure modes). Output labels:
   - `reproduced` (high confidence),
   - `probe-failed-to-build` / `unreproduced` (kept; reported as a lower-confidence finding with the attempted attack attached),
   - `not-reproduced-by-probe` (demoted, **kept**, with the probe attached: a passing probe shows only that the attempted attack failed, not that no attack works, and the probe may have tested a mock or the wrong path).
   No label deletes a finding. Reproduction raises confidence; a negative execution result only demotes. Deletion stays a downstream ranking or human decision (AIxCC no-PoV lane; Codex Security marking; none of the sources supports deletion on a negative probe).
5. **Merge with the read-only reviewer's findings, don't replace them.** Attack-pass findings are *added* to the reading reviewer's list, so the attack pass can only add recall. Precision is managed downstream by ranking (agentic-PBT rubric: 56%→86% among top-ranked), not by the attack pass.
6. **Budgets.** Agentic PBT averaged 8.8 minutes and about $5.9 per module with Opus 4.1. A per-catalog-entry time box (minutes, not tens of minutes) with "attacked: leaked / held / no harness" recorded for every entry keeps cost bounded and makes skipped surfaces visible.
7. **Run gate-like.** Probes are temp files under `$TMPDIR`, executed with `bun test <file>`, never committed. This matches the repo's read-only reviewer sandbox and scratch rules.

### Gaps
- No study directly measures "probe-required" versus "probe-optional" reviewer prompts on the same eval. The two mechanisms above are the closest documented analogues, and our −10-point result is itself the only direct measurement.
- No published optimal k (number of independent attack samples) for review-time budgets. CyberGym's 30 trials are far beyond a PR-review budget, and the curve between 1 and 30 was not retrieved.
- No evidence on how well an LLM refutation step ("probe ran and showed no leak") avoids false refutations when the probe itself is wrong (e.g., it tests a mock). PoC-Gym's fake-success modes suggest the same risk applies to fake refutation.
