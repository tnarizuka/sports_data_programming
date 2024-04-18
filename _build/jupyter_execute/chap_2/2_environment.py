#!/usr/bin/env python
# coding: utf-8

# In[4]:


# （必須）モジュールのインポート
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# 日本語フォントの設定（Mac:'Hiragino Sans', Windows:'MS Gothic'）
plt.rcParams['font.family'] = 'MS Gothic'


# # プログラミング環境の構築

# ## Anacondaのインストール
# 
# - Anacondaのアンインストール（環境再構築の場合）
#   - コントロールパネル > プログラムのアンインストール
#   - Anacondaを選択してアンインストール
#   - PC再起動
# - インストーラのダウンロード
#   - [Anaconda Distribution](https://www.anaconda.com/download) にアクセス
#   - メールアドレスを入力して，届いたメールのURLを開く
#   - Anacondaをダウンロード
# - Cドライブ直下（ユーザフォルダと同じ階層）に`anaconda3`というフォルダを作っておく
# - Anacondaのインストール
#   - Select Installation TypeでJust Meを選ぶ
#   - Choose Install LocationでCドライブ直下に作ったanaconda3フォルダを選ぶ
#     - anacondaのインストール先のパスに日本語が含まれるとうまくいかないため
#   - Advanced Installation Optionsで以下の2つに必ずチェックを入れる
#     - Add Anaconda3 to my PATH environment variable
#     - Register Anaconda3 as my default Python 3.9
# - Anaconda Navigatorを起動して，インストールが成功しているか確認する（適宜アップデートする）

# ## 作業フォルダの作成

# データ分析では，様々なファイルを扱わなければならない．
# 例えば，本講義では，Pythonのソースコード（`.py`），Jupyter NoteBook（`.ipynb`），データ（`.csv`），図（`.pdf`や`.png`）などのファイルを扱うことになる．
# これらのファイルが自分のPC内のどこに保存されているかを把握しておかないと，ファイルを探すだけで時間を取られてしまう．
# データ分析を始める際にまず行うべきことは，PC内のフォルダやファイルを整理することである．

# まず本講義専用の作業フォルダを作成する．
# フォルダ名は自分で分かれば何でも良いが，なるべく半角英数字とし，スペースは絶対に入れないこと．
# 作業フォルダの作成場所はできればクラウドストレージのフォルダ（OneDriveやGoogle Drive）の中に作ることを推奨する（こうすれば，自動的にクラウド上にバックアップされる）．
# 
# ここでは，`ローカルディスク（C:）>ユーザー>ユーザー名>OneDrive`の中に`sport_data`という作業フォルダを作ったとする：
# ```
# [OneDrive]
#     - [デスクトップ]
#     - [ドキュメント]
#     ...
#     - [sport_data]
# 
# ```

# 本講義で扱うファイルは全てこの`sport_data`の中に保存する．
# `sport_data`フォルダの中身は次のように章ごとのサブフォルダやレポート用のフォルダに分けておくと良い：
# ```
# [sport_data]
#     - [1_introduction]
#     - [2_environment]
#         - 2_environment.ipynb
#     - [3_numpy]
#     - [4_pandas]
#     - [5_matplotlib]
#     - [6_event]
#     - [7_tracking]
#     - [report]
#     - [others]
# ```

# ## Jupyter Lab
# 
# 本講義ノートは`.ipynb`ファイル形式でダウンロードしてJupyter上で実行可能である．
# Jupyterの環境構築の方法はいくつかあるので自分の好きな方法を選んで良いが，Anacondaをインストールすると，自動的にJupyter NotebookとJupyter Labが使えるようになる．
# 
# **Jupyter Labの起動**
# 
# - Anaconda Navigatorを起動
#     - ［スタートメニュー］→［すべてのアプリ］→ [Anaconda3(64-bit)] →［Anaconda Navigator］
# - ［Jupyter Lab］をLaunch
# 
# **ノートブック（.ipynbファイル）の起動**
# 
# - `.ipynb`ファイルをダウンロードし，作業フォルダに保存する．
#     - 講義ノート上部のアイコンから`.ipynb`をクリック
#     - 自動保存された場合は`ダウンロード`フォルダ内に保存される
# - Jupyter Labを起動し，左上のフォルダアイコンをクリックする．
# - .ipynbファイルを保存した作業フォルダに移動し，`.ipynb`ファイルをダブルクリックする．

# ## Maplotlibの日本語対応
# 
# Matplotlibはグラフ作成のためのライブラリである（詳しくは基礎編で解説する）．
# Matplotlibは標準で日本語が出力されないので，ここでは日本語対応する方法を2つ紹介する．

# **方法1：`rcParams`に使用するフォント名を指定する**
# 
# 以下のように，`matplotlib.pyplot`をインポートしておき，`plt.rcParams['font.family']`に日本語フォントを指定する．
# 使用可能なフォントは環境によって異なるが，Windowsの場合は`'MS Gothic'`，`'Meiryo'`などを指定する．
# Macの場合は`'Hiragino Sans'`を指定する．

# In[2]:


import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'MS Gothic'


# **方法2： japanize_matplotlib を利用する（詳しくは[こちら](https://pypi.org/project/japanize-matplotlib/)）**
# 
# japanize_matplotlibは一度インストールすれば，あとは他のモジュールと同じように`import japanize_matplotlib`とするだけで日本語が使用可能になる．
# ただし，使用可能なフォントはIPAexゴシックだけなので，フォントにこだわりたい場合は方法１をおすすめする．
# 
# - Anaconda Promptを起動
# - 以下のコマンドを実行してjapanize_matplotlibをインストールする
#     ```zsh
#     pip install japanize-matplotlib
#     ```
# - Jupyter Labを再起動して，以下のコードを実行する
#     ```python
#     import japanize_matplotlib
#     ```
# - 日本語が使用可能になる

# ## パス（Path）について
# 
# ### パスとは何か？
# Pythonプログラムの実行，ファイルの読み込み，加工したデータの保存などを行うには，ファイルやフォルダの場所（PC内のアドレス）を指定する必要がある．
# このアドレスを指定する文字列のことをパス（Path）と呼ぶ．
# Windowsの場合，パスはフォルダの階層構造を区切り文字`¥`（またはバックスラッシュ`\`）によって区切った形式で以下のように表される：
# 
# ```
# C:¥Users¥narizuka
# ```

# フォルダの階層の区切りは`¥`（またはバックスラッシュ`\\`）によって表されており，`¥`の隣にはフォルダの名前が記載されている．
# 上の例は，Cドライブ（`C:`）の中にある`Users`フォルダの中の`narizuka`フォルダのパスを表す．

# ### 絶対パスと相対パス
# パスには絶対パスと相対パスの2種類が存在する．
# パスを使用する場面の具体例として，matplotlibで描画した図を指定したフォルダ内に保存する場合を考える．
# まず，以下のプログラムを実行する．

# In[ ]:


fig, ax = plt.subplots(figsize=(3.5, 3))
x = np.arange(-np.pi, np.pi, 0.01)
ax.plot(x, np.sin(x))
ax.set_xlabel('X軸'); ax.set_ylabel('Y軸')


# 実行がうまくいけば，サイン関数が出力されるはずである．
# 
# 次に，出力された図を自分のPCの任意のフォルダに保存する．
# このためには，`fig.savefig(path)`のように保存先のパスを指定すれば良い．
# このとき，パスの指定方法には以下の２つの方法が存在する．

# #### 1. 絶対パスによる指定

# In[ ]:


# 自分の作業フォルダの絶対パスをコピーして貼り付ける
fig.savefig(r"C:\Users\narizuka\OneDrive\sport_data\2_environment\graph.pdf", bbox_inches="tight")


# この方法では，最も上の階層であるドライブ名（ここではCドライブ）から始まるパスを指定しており，これを**絶対パス**と呼ぶ．
# Windowsで絶対パスを取得するには，パスをコピーしたいファイルやフォルダを右クリックし，「パスのコピー」を選択すれば良い．
# 絶対パスを使っておけばエラーは出にくいが，PCの奥深くにあるフォルダだとパスが長くなるという問題がある．
# 
# なお，Windows環境においてパスをコピーして貼り付けると区切り文字がバックスラッシュ`\`または`¥`になるはずである．
# ところが，pythonではバックスラッシュ`\`と文字を組み合わせたエスケープシーケンスいう特別な文字列が存在し，例えば，`\n`は改行，`\t`はタブを表すエスケープシーケンスとなる．
# これにより，上の例の中にある`\t`の部分はパスの区切りではなくエスケープシーケンスとして認識され，エラーが出ることがある（特に，pythonでファイルの入出力を行うとき）．
# これを回避するにはパスの先頭に`r`を付ける
# これは，raw文字列と呼ばれ，""の中に指定した文字列をそのままの形で認識させることができる．

# #### 2. 相対パスによる指定

# In[ ]:


# 相対パスを指定する（バックスラッシュを区切り文字にすれば先頭のrは必要ない）
fig.savefig("./graph2.pdf", bbox_inches="tight")


# 2つ目の方法では，パスが`'.'`から始まっているが，これは現在の居場所（**カレントディレクトリ**と呼ぶ）のパスを意味する．
# デフォルトではカレントディレクトリは`.ipynb`ファイルが保存されているフォルダとなる．
# このように，カレントディレクトリのパス`'.'`から始まるパスを**相対パス**と呼ぶ．
# カレントディレクトリは以下のコマンドにより任意のフォルダに変更することができる．
# 
# ```python
# import os
# os.chdir(path)
# ```
# 
# 相対パスを用いると，パスが短くなるので便利であるが，カレントディレクトリがどこなのかを認識しておく必要がある．
