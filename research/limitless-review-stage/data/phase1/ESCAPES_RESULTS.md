# Fresh review runs on escapes-dev (2026-10-31 overnight)

51 escapes-dev cases (80 gold defects, labelled 10-30, never used to tune any reviewer), k=2, two-judge matcher
(Claude Sonnet 5.5 + GPT-6.1 Terra; "both" rule). Evals: main eval-mvw0y6v31sec2vc1agx2t1 (resumed once after a
deploy restart), cheap eval-mvvv3pum0kriw040gi0x29 (Haiku stopped partway: timeouts). Raw table: escapes_table.txt.

| System | Judged recall | 95% CI | vs production | p50 / p90 min | >20 min | Errors | $/review (API-equiv) |
|---|---|---|---|---|---|---|---|
| production sol-6.1@medium | 27/160 16.9% | 12–23 | — | 1.5 / 2.3 | 0/102 | 0 | 0.18 |
| sol-6.1@high | 49/160 30.6% | 24–38 | +13.8 | 3.7 / 5.3 | 0/102 | 0 | 0.35 |
| adversarial prompt E3 | 45/158 28.5% | 22–36 | +11.6 | 1.7 / 2.8 | 0/102 | 1 | 0.20 |
| union of 2 adversarial D | 58/160 36.2% | 29–44 | +19.4 | 3.2 / 4.7 | 0/102 | 0 | 0.39 |
| terra-6.1@medium standard | 41/160 25.6% | 19–33 | +8.7 | 0.5 / 0.7 | 0/102 | 0 | 0.03 |
| terra-6.1@medium adversarial | 46/160 28.7% | 22–36 | +11.9 | 0.5 / 0.7 | 0/102 | 0 | 0.03 |
| luna@medium standard / adversarial | 4/160, 7/160 | 1–9 | −14.4 / −12.5 | 0.5 / 0.7 | 0 | 0 | 0.01 |
| haiku-5.5@high standard / adversarial (partial) | 6/26, 4/23 | 7–42 | n/a | 22 / 36 | 17/32 | 5 | 0.38–0.45 |

Judge checks: agreement 97–100% per system; no self-preference by the Terra judge (Sonnet credits Terra-adversarial
51/160, Terra 46/160).

## Against Phase 0 (dev, old + pool gold; stored trials)
| System | Phase 0 combined dev vs prod | Fresh escapes-dev vs prod |
|---|---|---|
| sol@high | +10.6 | +13.8 |
| E3 adversarial | +11.4 | +11.6 |
| D union of 2 | +15.7 | +19.4 |
All three gains replicate on defects nobody tuned against, and the ranking holds (D > sol@high ≈ E3).

## Reading
- Production catches about 1 in 6 escape defects (these are the defects production review let through, so its
  baseline here is lower than on old dev, 31.6%).
- Terra 6.1 with the adversarial prompt matches E3 and nearly sol@high at about a sixth of production's cost and a
  third of its time. Luna is not viable. Haiku 5.5 fails the 20-minute rule (17 of 32 reviews over 20 min, 5
  timeouts/stalls) on the Claude CLI.
- Every Sol/Terra system stays far under 20 minutes (worst p90 5.3 min).

## Not measured here
- False blocks: escape cases all contain defects. Clean-case false blocks must come from the held-out clean set.
- Held-out confirmation: none of this touches escapes-heldout (57 cases, 103 defects).

## Proposed next step (decision run)
One held-out confirmation run on escapes-heldout plus the held-out clean set, shortlist: production, sol@high, E3,
Terra-adversarial, D, and a cheap union "Terra-adversarial ×2" (D's recipe on Terra, about $0.06/review).
Decision rule as agreed: ≥10 points recall over production; a >50% rise in true clean blocks needs a considerable gain.
