#!/usr/bin/env bash
# Usage: adj_codex.sh <case>  -> phase0/adj_<case>.codex.out
set -u
P=~/limitless-orch/review-research/phase0
c=$1
codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write --skip-git-repo-check --ephemeral \
  -C "$P/wt/$c" -o "$P/adj_$c.codex.out" - < "$P/adj_$c.prompt" > "$P/adj_$c.codex.trace" 2>&1
echo "$c rc=$?"
