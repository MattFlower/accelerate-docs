#!/usr/bin/env bash
# Usage: p1_checkout.sh <key> <repo-name> <head>  -> phase1/wt/<key> (detached, deps installed)
set -eu
P=~/limitless-orch/review-research/phase1
key=$1; repo=$2; head=$3
wt="$P/wt/$key"
if [ ! -d "$wt" ]; then
  git -C "$P/repos/MattFlower__$repo.git" worktree add -q --detach "$wt" "$head"
fi
if [ -f "$wt/package.json" ] && [ ! -d "$wt/node_modules" ]; then
  (cd "$wt" && bun install --frozen-lockfile >/dev/null 2>&1 || bun install >/dev/null 2>&1)
fi
echo "$key ready"
