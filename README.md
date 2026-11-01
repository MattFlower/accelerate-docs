# accelerate-docs

Design notes and research shared by [accelerate](https://github.com/MattFlower/accelerate)
and [limitless](https://github.com/MattFlower/limitless). Both build software
with agents, so the same research serves either project.

The notes live apart from the shipped repos because the whole of accelerate
ships as a Claude Code plugin, and this research is kept out of both.

## Layout

- `research/<topic>/report.md`: the synthesized write-up, with citations.
- `research/<topic>/notes/`: the raw per-angle notes the report was built from.
- A topic may also hold a `design-*.md` and a `BACKLOG.md`.

## Research

- [Making PRs easier to review](research/making-prs-easier-to-review/report.md)
  (2026-10-08). What the code review literature says about making changes
  faster and easier for a human to review. It shaped `human-review`'s reading
  order, concern grouping, held-back findings, and security prompts.
- [Automated code review](research/automated-code-review/report.md)
  (2026-10-31). Findings and sources on automated defect-finding review, plus
  a v1 design and backlog for a `bug-review` skill.
