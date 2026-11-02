#!/usr/bin/env bash
# Refresh the lab home from the daemon's: an online SQLite backup of the database plus the repo cache.
# The lab never shares a file with the daemon; its results stay in the lab database.
set -euo pipefail
LAB=${LAB_HOME:-$HOME/limitless-orch/lab/home}
mkdir -p "$LAB"
rm -f "$LAB/limitless.db" "$LAB/limitless.db-wal" "$LAB/limitless.db-shm"
bun -e 'import { Database } from "bun:sqlite"; const db = new Database(process.argv[1], { readonly: true }); db.run(`VACUUM INTO ${JSON.stringify(process.argv[2])}`); db.close();' "$HOME/.limitless/limitless.db" "$LAB/limitless.db"
rm -rf "$LAB/repos"; cp -R "$HOME/.limitless/repos" "$LAB/repos"
echo "lab home refreshed: $LAB ($(du -sh "$LAB/limitless.db" | cut -f1))"
