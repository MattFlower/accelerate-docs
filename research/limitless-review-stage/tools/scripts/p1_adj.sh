#!/usr/bin/env bash
# Usage: p1_adj.sh <codex|opus> <key>  -> phase1/adj/<key>.<vendor>.out (skips when output exists)
# Opus runs in default permission mode with only read tools and git/bun commands allowed.
set -u
P=~/limitless-orch/review-research/phase1
v=$1; key=$2
out="$P/adj/$key.$v.out"
[ -s "$out" ] && { echo "$key $v cached"; exit 0; }
cd "$P/wt/$key" || exit 1
if [ "$v" = codex ]; then
  codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write --skip-git-repo-check --ephemeral \
    -C "$P/wt/$key" -o "$out.tmp" - < "$P/adj/$key.prompt" > "$P/adj/$key.codex.trace" 2>&1
  rc=$?
else
  claude -p --model opus --effort high \
    --allowedTools Read Grep Glob "Bash(git diff:*)" "Bash(git show:*)" "Bash(git log:*)" "Bash(bun test:*)" "Bash(bun -e:*)" \
    < "$P/adj/$key.prompt" > "$out.tmp" 2> "$P/adj/$key.opus.trace"
  rc=$?
fi
[ $rc -eq 0 ] && [ -s "$out.tmp" ] && mv "$out.tmp" "$out"
echo "$key $v rc=$rc"
