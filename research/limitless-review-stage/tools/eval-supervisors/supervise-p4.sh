#!/usr/bin/env bash
# Resume (bounded) and judge the p4 calibration eval.
set -u
ID=eval-mvx3koae1kebh1d07r3w9f
LOG=~/limitless-orch/evals/supervise-p4.log
cd ~/.limitless/app || exit 1
cli() { bun src/cli/main.ts "$@"; }
echo "start $(date): $ID" >>"$LOG"
resumes=0
while :; do
  status=$(cli eval report "$ID" 2>/dev/null | head -1 | sed -E 's/^[^:]+: ([a-z_]+).*/\1/')
  case "$status" in
    completed) break ;;
    running|queued|pending|"") sleep 120 ;;
    *)
      if [ "$resumes" -ge 4 ]; then echo "GAVE UP $(date): status=$status after $resumes resumes" >>"$LOG"; exit 1; fi
      resumes=$((resumes + 1)); echo "$(date) status=$status, resume $resumes" >>"$LOG"
      cli eval resume "$ID" >>"$LOG" 2>&1; sleep 60 ;;
  esac
done
for attempt in 1 2 3; do
  echo "$(date) judging attempt $attempt" >>"$LOG"
  out=$(cli eval judge "$ID" --judges claude/sonnet-5.5,codex/terra-6.1@medium --max-usd 100 2>&1); echo "$out" >>"$LOG"
  echo "$out" | grep -q '"unjudged":\[\]' && break
  sleep 120
done
cli eval report "$ID" >>"$LOG" 2>&1
echo "SETTLED $(date): $ID" >>"$LOG"
