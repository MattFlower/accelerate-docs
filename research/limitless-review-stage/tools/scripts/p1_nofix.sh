#!/usr/bin/env bash
# Opus adjudication without the fix step: phase1/adj/<key>.nofix.prompt -> <key>.opus-nofix.out
P=~/limitless-orch/review-research/phase1; key=$1
cd "$P/wt/$key" || exit 1
claude -p --model opus --effort high \
  --allowedTools Read Grep Glob "Bash(git diff:*)" "Bash(git show:*)" "Bash(git log:*)" "Bash(bun test:*)" "Bash(bun -e:*)" \
  < "$P/adj/$key.nofix.prompt" > "$P/adj/$key.opus-nofix.out" 2> "$P/adj/$key.opus-nofix.trace"
echo "$key nofix rc=$?"
