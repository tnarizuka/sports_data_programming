# トラブルシュート

この文書には，利用者や共同編集者に公開してよい範囲の対処方法をまとめます．
手元環境固有のパス，復旧用バックアップ，Git 内部状態の詳細は `private/` に記録します．

## Jupyter Book のビルドで警告が出る

まずフルビルドを実行し，警告の対象ファイルを確認します．

```bash
jb build --all .
```

よくある原因:

- Markdown の見出しレベルが飛んでいる
- `!pip install ...` などのシェルコマンドを `python` コードブロックとして書いている
- `_toc.yml` に含まれないファイルが意図せず読まれている
- 参照先の画像やデータファイルが存在しない

対処後にもう一度 `jb build --all .` を実行し，警告が解消したことを確認します．

## `.ipynb` や `.md` がダウンロードされず表示される

ソースファイルのダウンロードリンクは `_static/download.js` で補助しています．
挙動がおかしい場合は次を確認します．

- `_config.yml` の `repository.path_to_book` が現在の配置と合っているか
- `_static/download.js` がビルド後のページに読み込まれているか
- GitHub Pages に最新の `_build/html/` が反映されているか
- ブラウザのキャッシュが古い状態になっていないか

修正後は `zsh build_push.sh "..."` で GitHub Pages を再生成します．

## 日本語フォントが表示されない

このリポジトリでは，日本語フォント表示の補助として `matplotlib-fontja` を推奨します．

```python
import matplotlib.pyplot as plt
import matplotlib_fontja
```

`seaborn` を使う場合，テーマ設定によってフォント設定が上書きされることがあります．
その場合は，`seaborn` の設定後に日本語フォント設定を行います．

```python
import seaborn as sns
import matplotlib_fontja

sns.set_theme()
matplotlib_fontja.japanize()
```

## `_build/` が Git に入ってしまう

`_build/` は生成物なので Git 管理しません．
`.gitignore` に `_build/` が含まれていることを確認します．

```bash
git status --short
```

意図せず stage されている場合は，公開前に管理対象から外します．

## `ghp-import` が失敗する

まずローカルビルドが成功するか確認します．

```bash
jb build --all .
```

そのうえで次を確認します．

- GitHub への push 権限があるか
- `main` ブランチが最新か
- `gh-pages` ブランチへの push が拒否されていないか
- ネットワーク接続に問題がないか

公開前の通常手順は [運用方法](operation-guide.md) を参照します．
