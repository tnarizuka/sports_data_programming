#!/usr/bin/zsh
set -euo pipefail

# Jupyter Bookの内容を更新
jb build --all .
git add -A
if ! git diff --cached --quiet; then
  git commit -m "updates"
  git push origin main
else
  echo "No source changes to commit."
fi

# GitHub Pagesの更新
ghp-import -n -p -f _build/html 
