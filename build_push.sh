#!/usr/bin/zsh
set -euo pipefail

commit_message="${1:-updates}"

# Jupyter Bookの内容を更新
echo "== Build Jupyter Book =="
jb build --all .

echo "== Stage source changes =="
git add -A
git status --short

if ! git diff --cached --quiet; then
  git commit -m "${commit_message}"
  git push origin main
else
  echo "No source changes to commit."
fi

# GitHub Pagesの更新
echo "== Publish GitHub Pages =="
ghp-import -n -p -f _build/html
