// Per (case, trial) blocking on clean cases for a lab eval. Usage: bun cleanblocks.ts <evalId> <clean-ids-file> [out.json]
const code = process.cwd();
const LAB = `${process.env.HOME}/limitless-orch/lab/home`;
const { Store } = await import(`${code}/src/db/store.ts`);
const { blockingReviewFindings } = await import(`${code}/src/pipeline/review.ts`);
const store = new Store(`${LAB}/limitless.db`);
const [evalId, file, out] = process.argv.slice(2);
const clean = new Set((await Bun.file(file).text()).split(/[\s,]+/).filter(Boolean));
const run = store.getEvalRun(evalId);
const rows: unknown[] = [];
for (const t of store.listEvalTrials(evalId)) {
  if (!clean.has(t.caseId)) continue;
  const sys = run.systems.find((s: { name: string }) => s.name === t.details.system);
  const b = t.status === "ok" && t.output ? blockingReviewFindings(t.output, undefined, undefined, sys) : null;
  rows.push({ system: t.details.system, caseId: t.caseId, trial: t.trial ?? t.details.trial, status: t.status, blocking: b?.length ?? null, titles: b?.map((f: { title: string; severity: string }) => `${f.severity}: ${f.title}`) });
}
await Bun.write(out ?? "/dev/stdout", JSON.stringify(rows, null, 1));
