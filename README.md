# accelerate-docs

Design notes and research behind [accelerate](../accelerate), kept out of that
repo because the whole of it ships as a Claude Code plugin.

## Layout

- `research/<topic>/report.md`: the synthesized write-up, with citations.
- `research/<topic>/notes/`: the raw per-angle notes the report was built from.

## Research

- [Making PRs easier to review](research/making-prs-easier-to-review/report.md)
  (2026-10-08). What the code review literature says about making changes
  faster and easier for a human to review. It shaped `human-review`'s reading
  order, concern grouping, held-back findings, and security prompts.
