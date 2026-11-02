# review-111

{
 "id": "review-111",
 "kind": "clean",
 "repo": "MattFlower/limitless",
 "base": "063a46d07dc7c727a837a13ae53fedbbdf4814da",
 "head": "fc0cd9ec133b038d350c64e6cc3c281f9056a932",
 "snapshot": true,
 "source": "pr #430 fresh clean set 2026-10-16 @ fc0cd9e",
 "split": "dev",
 "input": {
  "prompt": "## Problem\nInside confinement, every zsh here-document fails with `zsh:1: can't create temp file for here document: operation not permitted`. zsh writes here-document temp files under `TMPPREFIX`, which defaults to `<tmp>`, and confined commands can't write the system temp directories (by design; AGENTS.md says not to hardcode `/tmp`). Agents on this Mac run their shell commands in zsh (`/bin/zsh -lc ...`), so any here-doc they write (`cat <<EOF`, `python3 - <<'PY'`) fails, and they lose turns working around it. The message appears repeatedly in recent runs' event logs (for example run <run-id> on 2026-10-08).\n\nProbe with `runConfined` on 2026-10-08:\n- default: `zsh -lc 'cat <<EOF ...'` → exit 1, the error above;\n- `TMPPREFIX=\"$TMPDIR/zsh\"`, set by `export` inside the command or through the environment → exit 0, the here-doc works (a login shell's profile doesn't override it).\n\n## Change\nWherever the factory points `TMPDIR` at a run's or command's private scratch, also set `TMPPREFIX` to a path inside that same scratch (for example `<scratch>/zsh`): `runConfined` in `src/harness/sandbox.ts` and the environments of the Codex and Claude agent invocations. Use one helper so the two can't drift apart.\n\n## Tests\n- A confined `zsh -lc` here-doc succeeds, and the same command without the fix fails (the probe above, skipped where zsh or Seatbelt is unavailable, using `seatbeltSkip`).\n- The agent environment builders set `TMPPREFIX` inside the scratch they set `TMPDIR` to.\n\n## Budget\nA few lines, plus tests.\n\n## Out of scope\n- Other shells' temp settings.",
  "spec": null,
  "implementerReport": "",
  "gates": []
 },
 "defects": []
}

# Blocking findings (verifier high/critical), both trials

## trial 0: Set TMPPREFIX for preview command scratch
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/preview.ts",
 "line": 174,
 "title": "Set TMPPREFIX for preview command scratch",
 "detail": "The preview pipeline also sets TMPDIR, TMP, and TEMP to private scratch, but it does not use the new helper or override TMPPREFIX. Its build, seed, and serve commands therefore inherit a parent TMPPREFIX or use zsh's default outside that scratch. This leaves one of the factory's scratch environments outside the request's stated coverage.",
 "suggestion": "Use scratchEnv when constructing the preview environment so TMPPREFIX is derived from the same scratch directory.",
 "failure_scenario": "A preview build or seed invokes zsh with a here-document while the process is confined away from the default temporary directory, or inherits a TMPPREFIX pointing to an unwritable directory. The command fails to create its here-document even though preview set TMPDIR to writable scratch.",
 "category": "correctness",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/preview.ts:172–178 sets `HOME: scratch, TMPDIR: scratch, TMP: scratch, TEMP: scratch` without TMPPREFIX. At :184–187 it executes `cmd: [\"/bin/sh\", \"-c\", commandText]` with that environment. src/util/proc.ts:576–587 preserves inherited TMPPREFIX through `env[k] = v`. The shared fix exists at src/harness/scratch.ts:83: `TMPPREFIX: join(scratchDir, \"zsh\")`, but preview does not use it.",
  "trigger": "A preview build or seed invokes zsh with a here-document and inherits an unwritable TMPPREFIX, or runs where confinement denies zsh's default temporary directory. TMPDIR points to writable scratch, but zsh still fails to create its here-document file. This misses the explicit requirement to set TMPPREFIX wherever private TMPDIR is assigned.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 0: Set TMPPREFIX for preview commands using private scratch
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/preview.ts",
 "line": 174,
 "title": "Set TMPPREFIX for preview commands using private scratch",
 "detail": "The request says, “Wherever the factory points TMPDIR at a run's or command's private scratch, also set TMPPREFIX to a path inside that same scratch.” Preview build, seed, and server commands receive TMPDIR pointing at private scratch but do not receive the corresponding TMPPREFIX from the shared helper.",
 "suggestion": "Use scratchEnv for the preview environment as well, so TMPPREFIX tracks its scratch directory.",
 "failure_scenario": "A preview build or seed command runs a zsh here-document inside an enclosing confinement that denies system temporary directories; zsh attempts to create its temporary file outside the preview scratch and the command fails.",
 "category": "correctness",
 "confidence": 0.97,
 "introduced_by_diff": false,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/preview.ts:172–178 assigns `TMPDIR: scratch, TMP: scratch, TEMP: scratch` without assigning TMPPREFIX. At :184–191 preview passes this environment directly to `runProcess`; src/util/proc.ts:313–316 forwards `...opts.env` without adding TMPPREFIX. Only callers of src/harness/scratch.ts:83 receive `TMPPREFIX: join(scratchDir, \"zsh\")`.",
  "trigger": "A preview build or seed invokes a zsh here-document under enclosing confinement that denies system temporary directories, with TMPPREFIX unset. Zsh uses its default location instead of preview scratch and the command fails. This duplicates C1 and leaves the request's explicit 'wherever' requirement incomplete.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: Apply the scratch environment helper to preview commands
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/preview.ts",
 "line": 174,
 "title": "Apply the scratch environment helper to preview commands",
 "detail": "Preview build, seed and serve processes still set TMPDIR, TMP and TEMP directly without setting TMPPREFIX. This leaves one factory-managed scratch environment outside the shared helper, despite the request to set TMPPREFIX wherever scratch is assigned. An inherited TMPPREFIX can also continue pointing at a different or removed scratch directory.",
 "suggestion": "Use scratchEnv for the preview environment and cover the resulting TMPPREFIX in the preview tests.",
 "failure_scenario": "A preview command invokes zsh with a here-document while its inherited TMPPREFIX points to an unavailable or unwritable directory; zsh cannot create the here-document file even though TMPDIR points to the preview scratch.",
 "category": "correctness",
 "confidence": 0.98,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/preview.ts:165 builds `const env = { ...reserved, ...expanded };`; lines 172–178 set `HOME: scratch, TMPDIR: scratch, TMP: scratch, TEMP: scratch` without overriding TMPPREFIX. Lines 184–187 pass that environment directly to `runProcess`. src/harness/scratch.ts:83 provides the unused helper: `{ TMPDIR: scratchDir, TMP: scratchDir, TEMP: scratchDir, TMPPREFIX: join(scratchDir, \"zsh\") }`.",
  "trigger": "A preview command invokes zsh with a here-document and inherits TMPPREFIX pointing to an unavailable or unwritable directory. The preview environment preserves that prefix, so the command fails despite having writable TMPDIR. This misses the explicit requirement to set TMPPREFIX wherever private scratch TMPDIR is set.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}

## trial 1: Set TMPPREFIX for preview commands' private scratch
{
 "severity": "major",
 "security": false,
 "file": "src/pipeline/preview.ts",
 "line": 174,
 "title": "Set TMPPREFIX for preview commands' private scratch",
 "detail": "The request says, “Wherever the factory points TMPDIR at a run's or command's private scratch, also set TMPPREFIX to a path inside that same scratch.” Preview build, seed, and server commands receive a private scratch TMPDIR here but do not receive the shared helper's TMPPREFIX. They can inherit an unrelated TMPPREFIX or use zsh's default outside the writable scratch.",
 "suggestion": "Use scratchEnv for the preview environment as well, after applying the configured environment.",
 "failure_scenario": "A preview build or seed invokes zsh with a here-document while confined and its inherited or default TMPPREFIX points outside writable scratch; zsh fails to create the here-document temp file.",
 "category": "correctness",
 "confidence": 0.96,
 "introduced_by_diff": true,
 "verification": {
  "verdict": "CONFIRMED",
  "evidence": "src/pipeline/preview.ts:172–178 assigns `TMPDIR: scratch, TMP: scratch, TEMP: scratch` but no TMPPREFIX. Lines 179–187 execute both `[\"build\", config.build]` and `[\"seed\", config.seed]` with that environment. Lines 193–195 turn a nonzero exit into `Preview ${step} ... failed`.",
  "trigger": "A preview build or seed invokes zsh with a here-document under confinement that denies its inherited or default TMPPREFIX directory. TMPPREFIX remains outside private scratch, causing the here-document and preview step to fail. This is the same missing requirement as C1.",
  "severity": "high",
  "category": "correctness"
 },
 "agreement": 1,
 "duplicates": []
}
