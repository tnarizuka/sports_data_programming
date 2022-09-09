#!/usr/bin/zsh

# Jupyter Bookの内容を更新
jb build --all .
git add .
git commit -m "updates"  
git push origin main

# GitHub Pagesの更新
ghp-import -n -p -f _build/html 