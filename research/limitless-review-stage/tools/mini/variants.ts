const HEAD = "(the reviewer's severity is not an input you must keep)";
const MONTH = `"would this plausibly happen in the next month of normal factory operation?" Deploys restart the daemon daily, so restart windows count unless they last milliseconds.`;
const CRIT = "a realistic trigger that loses or corrupts persisted state, leaks a secret or private data, breaks a trust or confinement boundary, or stops the factory or deploys.";
const HIGH = "a realistic trigger with real harm: a wrong result, a silent failure, lost or repeated work, a check the change claims to add that a realistic input bypasses, or a compatibility break with the previous release.";
const MED = "a real defect with a contrived trigger (an unusual input, configuration, environment or timing the request does not ask to handle), or a cost only in tests or diagnostics, such as a missing or weak test on its own, or a missing or less informative log line or error message.";
const LOW = "cosmetic, a process ask (a report, measurements, PR text), or behaviour the repository's own rules adopt.";
const OVERRIDES = "A secret or credential stored or shown unredacted is at least high whatever the trigger. A new test that fails in normal runs stops deploys, so it is at least high.";
const REQS = "Requirements: a requirement counts as undelivered only when the behaviour or protection it exists for is missing at head; then rate the missing behaviour by its trigger and harm like any other defect. Different wording, a different mechanism than the one the request preferred, log or message text, and places the request does not name are not undelivered requirements. Edits outside the request's scope are not an undelivered requirement either.";
const PATH = "Trigger evidence: rate high or critical only when you can show from the code at head how a realistic run reaches the failure: who calls the code, under which configuration and environment it runs, and what input reaches it. Quote that path in evidence. If the path depends on a state you could not find in the code or on an unusual configuration, rate medium.";
const A = `# Severity by consequence and trigger ${HEAD}
For each candidate ask: ${MONTH}
- critical: ${CRIT}
- high: ${HIGH}
- medium: ${MED}
- low: ${LOW}
${OVERRIDES}
${REQS}`;
const B = `${A}
${PATH}`;
const C = `# Severity: decide in four steps ${HEAD}
1. Path. From the code at head, find how a realistic run reaches the failure: who calls the code, under which configuration and environment it runs, and what input reaches it. Quote that path in evidence and state it in trigger.
2. Trigger. Ask: ${MONTH} The trigger is contrived if the path needs an unusual input, configuration, environment or timing that the request does not ask to handle, or a state you could not find in the code.
3. Harm. Name what goes wrong when it happens: persisted state, secrets, a trust or confinement boundary, the factory or deploys, a wrong result or silent failure, lost or repeated work, or only tests, diagnostics or appearance.
4. Severity from steps 2 and 3:
- critical: realistic trigger, and it loses or corrupts persisted state, leaks a secret or private data, breaks a trust or confinement boundary, or stops the factory or deploys.
- high: realistic trigger, and a wrong result, a silent failure, lost or repeated work, a check the change claims to add that a realistic input bypasses, or a compatibility break with the previous release.
- medium: a contrived trigger with real harm, or harm only to tests or diagnostics (a missing or weak test on its own, a missing or less informative log line or error message).
- low: ${LOW}
${OVERRIDES}
${REQS}`;
const p5 = await Bun.file(`${process.env.HOME}/limitless-orch/evals/p5-rubric-verifier-systems.json`).json();
const base = p5.systems[0];
const systems = [
  base,
  { ...base, name: "rubric-a-no-override", severityRubric: A },
  { ...base, name: "rubric-b-path", severityRubric: B },
  { ...base, name: "rubric-c-steps", severityRubric: C },
];
await Bun.write(`${process.env.HOME}/limitless-orch/evals/p6-rubric-variants-systems.json`, `${JSON.stringify({ systems }, null, 2)}\n`);
console.log(systems.map((s) => [s.name, typeof s.severityRubric === "string" ? s.severityRubric.length : s.severityRubric]));
