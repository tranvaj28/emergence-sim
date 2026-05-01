#!/bin/bash
cd "$(dirname "$0")"
git add .
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "wip: auto-commit $TIMESTAMP" 2>/dev/null || echo "Nothing new to commit"
git push