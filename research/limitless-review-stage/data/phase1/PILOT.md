# Phase 1 pilot: escape-corpus labelling (2026-10-30)

**Generator dry run** (`scripts/review-escape-cases.ts`, no `--write`)
- 181 candidate cases (review rounds), 448 findings. Split by PR parity, as pre-registered: 89 dev, 92 held-out.
- By reviewer era (round date before or after 10-23): 108 Opus-era, 73 Sol-era.
- Excluded: 37 (33 have no delivered fix) and 27 duplicates of existing cases.

**Pilot sample:** 20 cases, 5 per split × era cell, 47 findings.

**Adjudication**
- Two adjudicators, blind to the original severity: Codex GPT-6.1 Sol@high and Claude Opus@high.
- Each worked in a checkout of the reviewed commit, reproduced where it could, then said whether the next round's
  commit fixes the claim.

**Outcomes**

| Measure | Result |
|---|---|
| Real defect, both vendors agree | 44 of 47 |
| Not real, both agree | 1 |
| Real, but split on severity (blocking vs not) | 27 |
| Reproduced (Codex / Opus) | 46 / 38 of 47 |
| Fixed by the next factory round | all 11 agreed-gold findings |

- **Severity split, both directions:** Opus called 20 of the first 30 minor, including a credential left out of
  redaction. Codex called test-only claims major.
- **Removing the fix step doesn't move Opus's severities:** 7 of 8 unchanged, 1 lower. The template stays.

**Severity method (validated on the pilot)**
- Two text-only raters, Claude Sonnet 5.5 and GPT-6.1 Terra, classify each finding.
  - *Inputs:* the two adjudicators' scenarios and evidence, labelled A/B in random order.
  - *Ratings:* consequence (10 classes) and trigger (normal / plausible / unusual).
- Code maps those two ratings to a severity under the draft rubric. A policy answer from Matt changes the mapping,
  not the ratings.
- **Raters agree with each other** on blocking-or-not for 34 of 46.
- **Against my blind rulings on the 28 adjudicator disputes:**

  | Rater | Matches my ruling |
  |---|---|
  | Sonnet | 22 |
  | Terra | 21 |
  | Both, when they agree | 18 of 21 (86%) |

- Nearly every split is on the trigger (plausible vs unusual). Terra leans plausible, Sonnet unusual.
- **Rule:** the raters' consensus sets severity; splits come to me.

**Proposed pilot labels:** 27 gold, 20 not gold.
- Severity: set by me on 33, by rater consensus on 13.
- Matt's batch 1 is 20 random labels (`spotcheck_batch1.md`).

**New policy question (Q5).**
- Redaction gaps with an unusual trigger (a credential inside a gate name, a retry command or a saved error) are
  5 of 47 findings.
- Recommend major: AGENTS.md requires redaction at every boundary.

**Stored-trial pool (Phase 1.0)**
- 1,130 findings in stored M5.2-era trials matched no gold defect (769 blocking), on 52 real cases.
- Clustered by mechanism into 352 claims. A spot-check of review-045's 26 → 4 clusters was correct.
- Its biggest cluster is one claim that 21 trials across nearly every system reported, and it isn't in the gold.
- Adjudication of all 352 claims (both vendors) is running.
