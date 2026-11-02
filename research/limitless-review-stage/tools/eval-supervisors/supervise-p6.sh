#!/usr/bin/env bash
# Resume (bounded) and judge the p6 rubric mini-eval eval. Usage: supervise-p5.sh <evalId>
set -u
ID=${1:?eval id}
LOG=~/limitless-orch/evals/supervise-p6.log
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
      out=$(cli eval resume "$ID" 2>&1); echo "$out" >>"$LOG"
      new=$(echo "$out" | grep -oE 'resumed as eval-[a-z0-9]+' | head -1 | sed 's/resumed as //')
      if [ -n "$new" ]; then ID=$new; echo "$(date) now tracking $ID" >>"$LOG"; fi
      sleep 60 ;;
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
