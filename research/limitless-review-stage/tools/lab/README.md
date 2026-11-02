# Review lab (fast eval loop, no PR or deploy)

Runs a review eval in-process with the code of whatever checkout you run it from, against a private copy
of the daemon's database and repo cache. No server, pollers, scheduler, land queue or deploy is started,
so it never acts on GitHub. Results stay in the lab database (lab-only; cite them as screens).

- Refresh the lab copy (2-3 s): `~/limitless-orch/lab/sync.sh`
- Run (from a checkout with your edits):
  `bun ~/limitless-orch/lab/lab.ts <systems.json> --replay <sourceEvalId> --cases a,b|@file --k 2 --concurrency 8 [--no-judge] --out x.json`
- Prompt/rubric text variants: put them in the systems file (`severityRubric` text, lens `focus`); no code change.
- Code variants (blocking rules, prompts in src/): edit the checkout and rerun; the lab imports src/ live.
- Free regrades of stored outputs under a different blocking rule: scratchpad gate.ts pattern (stored judgments).
- Concurrency: the lab is a separate process and doesn't see the daemon's provider usage; keep <= 8.

## Judging a stored eval
`bun ~/limitless-orch/lab/judge.ts <evalId> [--judges j1,j2] [--max-usd N] [--out x.json]` judges an eval already in the
lab DB (e.g. a stored daemon baseline) with the checkout's judge, so baselines and lab candidates share one judging.
Run it when no other lab process is running (one Factory per lab DB at a time).
