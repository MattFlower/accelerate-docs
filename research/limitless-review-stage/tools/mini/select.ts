// Which cases does the verifier's rating decide? Positive: a required gold defect both judges match to some finding.
// Clean: any confirmed/plausible finding at all. Uses stored judgments only.
import { Database } from "bun:sqlite";
const APP = `${process.env.HOME}/.limitless/app`;
const { judgePayload, JUDGE_PROMPT_VERSION } = await import(`${APP}/src/evals/judge.ts`);
const { blockingReviewFindings } = await import(`${APP}/src/pipeline/review.ts`);
const { parseTarget } = await import(`${APP}/src/router/targets.ts`);
const { loadRoleCases, defaultCasePath } = await import(`${APP}/src/evals/cases.ts`);
const [reportPath, system] = process.argv.slice(2);
const report = await Bun.file(reportPath).json();
const lc = loadRoleCases("review", defaultCasePath("review")); const cases = lc.cases ?? lc;
const db = new Database(`${process.env.HOME}/.limitless/limitless.db`, { readonly: true });
const hash = (v: unknown) => new Bun.CryptoHasher("sha256").update(JSON.stringify(v)).digest("hex");
const judges = ["claude/sonnet-5.5", "codex/terra-6.1@medium"];
const judgment = (j: string, item: any, out: any) => {
  const key = hash([JUDGE_PROMPT_VERSION, parseTarget(j), item.id, hash(item.defects), hash(judgePayload(item, out).findings)]);
  const row = db.query("SELECT matches_json FROM eval_judgments WHERE cache_key = ?").get(key) as any;
  return row ? JSON.parse(row.matches_json) : null;
};
const rows: Record<string, any> = {};
for (const t of report.trials) {
  if (t.details?.system !== system || t.status !== "ok" || !t.output) continue;
  const out = typeof t.output === "string" ? JSON.parse(t.output) : t.output;
  const item = cases.find((c: any) => c.id === t.caseId); if (!item) continue;
  const r = (rows[t.caseId] ??= { kind: item.defects?.length ? "pos" : "clean", detected: 0, blocked: 0, req: 0, cleanBlock: 0, findings: 0, unjudged: 0 });
  const blocking = blockingReviewFindings(out, undefined, undefined, { severityRubric: true });
  if (!item.defects?.length) { r.findings += out.findings.length; if (blocking.length) r.cleanBlock++; continue; }
  const ms = judges.map((j) => judgment(j, item, out)); if (ms.some((m) => !m)) { r.unjudged++; continue; }
  for (const [i, g] of item.defects.entries()) { if (!g.required) continue; r.req++;
    const ids = ms.map((m: any) => m.find((x: any) => x.gold === `G${i + 1}`)?.finding);
    if (ids.every(Boolean)) { r.detected++; if (ids.every((id: string) => blocking.includes(out.findings[Number(id.slice(1)) - 1]))) r.blocked++; } }
}
console.log(JSON.stringify(rows));
