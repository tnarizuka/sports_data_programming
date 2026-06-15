# 運用方法

この文書は，講義ノートを更新・公開するための基本手順をまとめたものです．
公開して差し支えない手順だけを記載しています．
個別の作業記録や復旧メモは `private/` に残します．

## 環境構築

Python 仮想環境を作成し，依存パッケージをインストールします．

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ローカルビルド

Jupyter Book をビルドします．

```bash
jb build --all .
```

ビルド結果は `_build/html/` に出力されます．
`_build/` は生成物なので Git には含めません．

## 公開手順

通常の更新では，次のスクリプトを使います．

```bash
zsh build_push.sh "Update lecture notes"
```

このスクリプトは次の処理を行います．

1. `jb build --all .` で Jupyter Book をビルドする
2. 変更されたソースを stage する
3. 変更があれば指定したメッセージで commit する
4. `main` ブランチへ push する
5. `ghp-import` で `_build/html/` を `gh-pages` ブランチへ反映する

## 更新前の確認

大きな変更を行った場合は，公開前に次を確認します．

```bash
git status --short
jb build --all .
```

確認する内容は次の通りです．

- 意図しないファイルが Git 管理対象になっていないか
- `_build/` が Git 管理対象に戻っていないか
- Jupyter Book のビルドが警告なしで通るか
- `.ipynb` や `.md` のダウンロードリンクが期待通り動くか
- `requirements.txt` と本文中の依存パッケージの説明が矛盾していないか

定期的な確認には [保守チェックリスト](maintenance-checklist.md) を使います．
エラーや警告が出た場合は [トラブルシュート](troubleshooting.md) を参照します．

## 公開情報と非公開情報

公開してよい情報は `README.md` と `docs/` に置きます．
`docs/` は GitHub 上で読む公開資料であり，Jupyter Book の公開サイトには含めません．

公開してよい例:

- 講義ノートの概要
- リポジトリ構成
- 通常のビルド手順
- 公開用の変更履歴
- 利用者向けのトラブルシュート

Git に含めない例:

- 手元環境固有のパス
- 復旧用バックアップの場所
- Git 内部状態の修復記録
- 試行錯誤の詳細な作業ログ
- 認証情報，トークン，個人メモ

これらは `private/` に置きます．
