// Lab eval: runs a review eval in-process with the code of the current directory (a checkout), against the
// lab home (a copy of the daemon's database and repo cache). No server, pollers, scheduler or deploy.
// Usage (from a checkout): bun ~/limitless-orch/lab/lab.ts <systems.json> [--replay <evalId>] [--cases a,b|@file]
//   [--k 2] [--concurrency 4] [--max-usd 50] [--judges j1,j2] [--no-judge] [--out report.json]
import { readFileSync } from "node:fs";
const code = process.cwd();
const LAB = process.env.LAB_HOME ?? `${process.env.HOME}/limitless-orch/lab/home`;
const { loadConfig } = await import(`${code}/src/config.ts`);
const { Factory } = await import(`${code}/src/app.ts`);
const { parseEvalReviewSystems } = await import(`${code}/src/pipeline/review-system.ts`);
const { formatEvalReport } = await import(`${code}/src/evals/format.ts`);

const args = process.argv.slice(2);
const systemsPath = args[0];
if (!systemsPath) throw new Error("usage: lab.ts <systems.json> [flags]");
const flag = (name: string) => {
  const i = args.indexOf(`--${name}`);
  return i < 0 ? undefined : args[i + 1];
};
const list = (value: string | undefined) =>
  value === undefined ? undefined : (value.startsWith("@") ? readFileSync(value.slice(1), "utf8") : value).trim().split(",");

const factory = new Factory(loadConfig({ home: LAB }), { bootSha: "lab" });
const request = {
  role: "review",
  systems: parseEvalReviewSystems(readFileSync(systemsPath, "utf8"), systemsPath),
  replayFinders: flag("replay"),
  caseIds: list(flag("cases")),
  k: Number(flag("k") ?? 2),
  maxUsd: Number(flag("max-usd") ?? 50),
  concurrency: Number(flag("concurrency") ?? 4),
};
const started = Date.now();
const elapsed = () => `${Math.round((Date.now() - started) / 1000)}s`;
const run = factory.evals.submit(request);
console.log(`lab eval ${run.id} started (code: ${code})`);
const wait = async (done: () => boolean, label: string) => {
  let last = "";
  while (!done()) {
    await Bun.sleep(5000);
    const r = factory.evals.report(run.id);
    const line = r ? r.summaries.map((s: { system?: { name?: string } | string; pending?: number }) => `${typeof s.system === "string" ? s.system : (s.system?.name ?? "?")}:${s.pending ?? "?"} pending`).join(" ") : "";
    if (line !== last) console.log(`[${elapsed()}] ${label} ${line}`);
    last = line;
  }
};
await wait(() => !["queued", "running"].includes(factory.store.getEvalRun(run.id)?.status ?? ""), "running");
console.log(`[${elapsed()}] eval ${factory.store.getEvalRun(run.id)?.status}`);
if (!args.includes("--no-judge")) {
  const judges = list(flag("judges")) ?? ["claude/sonnet-5.5", "codex/terra-6.1@medium"];
  factory.evals.judge(run.id, { judges, maxUsd: Number(flag("max-usd") ?? 50) });
  await wait(() => factory.evals.judgeStatus(run.id)?.status !== "running", "judging");
  const job = factory.evals.judgeStatus(run.id);
  console.log(`[${elapsed()}] judging ${job?.status}${job?.error ? `: ${job.error}` : ""}`);
}
const report = factory.evals.report(run.id, { delta: factory.evalSettings.delta });
console.log(formatEvalReport(report));
const out = flag("out");
if (out) await Bun.write(out, JSON.stringify(report));
console.log(`[${elapsed()}] done: ${run.id}`);
process.exit(0);
