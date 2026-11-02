// Lab judge: judges an existing (stored) review eval in the lab home with the current checkout's judge code, then
// prints the report. Usage (from a checkout): bun ~/limitless-orch/lab/judge.ts <evalId> [--judges j1,j2] [--max-usd N] [--out x.json]
const code = process.cwd();
const LAB = process.env.LAB_HOME ?? `${process.env.HOME}/limitless-orch/lab/home`;
const { loadConfig } = await import(`${code}/src/config.ts`);
const { Factory } = await import(`${code}/src/app.ts`);
const { formatEvalReport } = await import(`${code}/src/evals/format.ts`);
const args = process.argv.slice(2);
const id = args[0];
if (!id) throw new Error("usage: judge.ts <evalId> [flags]");
const flag = (name: string) => {
  const i = args.indexOf(`--${name}`);
  return i < 0 ? undefined : args[i + 1];
};
const factory = new Factory(loadConfig({ home: LAB }), { bootSha: "lab" });
const judges = (flag("judges") ?? "claude/sonnet-5.5,codex/terra-6.1@medium").split(",");
factory.evals.judge(id, { judges, maxUsd: Number(flag("max-usd") ?? 20) });
while (factory.evals.judgeStatus(id)?.status === "running") await Bun.sleep(5000);
const job = factory.evals.judgeStatus(id);
console.log(`judging ${job?.status}${job?.error ? `: ${job.error}` : ""}`);
const report = factory.evals.report(id, { delta: factory.evalSettings.delta });
console.log(formatEvalReport(report));
const out = flag("out");
if (out) await Bun.write(out, JSON.stringify(report));
process.exit(0);
