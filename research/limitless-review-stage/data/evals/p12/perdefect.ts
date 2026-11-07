// Per (case, gold, trial) judged-caught matrix across systems of a lab eval. Usage: bun perdefect.ts <evalId> [out.json]
const code = process.cwd();
const LAB = `${process.env.HOME}/limitless-orch/lab/home`;
const { loadConfig } = await import(`${code}/src/config.ts`);
const { Store } = await import(`${code}/src/db/store.ts`);
const { loadRoleCases } = await import(`${code}/src/evals/cases.ts`);
const { judgePayload, JUDGE_PROMPT_VERSION } = await import(`${code}/src/evals/judge.ts`);
const { blockingReviewFindings } = await import(`${code}/src/pipeline/review.ts`);
const { parseTarget } = await import(`${code}/src/router/targets.ts`);
const cfg = loadConfig({ home: LAB });
const store = new Store(`${LAB}/limitless.db`);
const evalId = process.argv[2];
const run = store.getEvalRun(evalId);
const cases = loadRoleCases("review").cases;
const judges = ["claude/sonnet-5.5", "codex/terra-6.1@medium"];
const hash = (v: unknown) => new Bun.CryptoHasher("sha256").update(JSON.stringify(v)).digest("hex");
const rows: unknown[] = [];
for (const trial of store.listEvalTrials(evalId)) {
  const item = cases.find((c: { id: string }) => c.id === trial.caseId);
  if (!item || trial.status !== "ok" || !trial.output) continue;
  const output = trial.output;
  const ms = judges.map((j) => store.evalJudgment(hash([JUDGE_PROMPT_VERSION, parseTarget(j), item.id, hash(item.defects), hash(judgePayload(item, output).findings)])));
  const rules = run.systems.find((s: { name: string }) => s.name === trial.details.system);
  const blocking = blockingReviewFindings(output, undefined, undefined, rules);
  for (const [i, gold] of item.defects.entries()) {
    if (!gold.required) continue;
    const mapped = ms.map((m: { gold: string; finding: string | null }[] | undefined) => m?.find((x) => x.gold === `G${i + 1}`)?.finding ?? null);
    const fs = mapped.map((id: string | null) => (id ? output.findings[Number(id.slice(1)) - 1] : null));
    const caught = fs.every((f: unknown) => f && blocking.includes(f));
    rows.push({ system: trial.details.system, caseId: item.id, gold: `G${i + 1}`, goldSeverity: gold.severity, goldSummary: gold.summary, trial: trial.trial, caught, matched: mapped.every(Boolean),
      finding: fs[1] ?? fs[0] ? (({ title, severity, category, verification }) => ({ title, severity, category, verification }))(fs[1] ?? fs[0]) : null });
  }
}
await Bun.write(process.argv[3] ?? "/dev/stdout", JSON.stringify(rows, null, 1));
