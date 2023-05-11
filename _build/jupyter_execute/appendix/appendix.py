#!/usr/bin/env python
# coding: utf-8

# # 付録

# ## プログラミング環境

# ### JupyterとPythonスクリプトの使い分け
# 
#  Jupyterは短いコードを逐次実行しながら結果を確認するのには適しているが，コードが長くなると分かりにくくなる．そこで，コードが長くなってきたら関数やクラスに適宜まとめてスクリプト（`.py`ファイル）に保存すると良い．保存したスクリプトはNumPyやPandasと同じようにimportできるので，Jupyter上ではimportしたスクリプト内の関数を実行するだけにすると結果が整理しやすい．その際，以下に説明する自作モジュールの自動リロードの設定をしておくと便利である．
#  
# ※ ローカル環境で`.py`ファイルを編集するにはエディタを使用する．Windowsに標準搭載されているメモ帳を使うのが最も手軽だが，非常に使いづらいので推奨しない．まずは自分の好みに合うエディタを探すことを推奨する．よく使われるエディタは以下の通り：
# 
# - Visual Studio Code（推奨）
# - Atom
# - Sublime Text

# ### Jupyterのconfigファイル
# - ターミナルで以下を実行する
#     ```
#     jupyter notebook --generate-config
#     ```
#     - `C:\Users\username\.jupyter`の中に`jupyter_notebook_config.py`というファイルができる．
# - `jupyter_notebook_config.py`を開いて以下を追加
#     ```
#     c=get_config()
#     c.NotebookApp.notebook_dir="起動ディレクトリのパス"
#     ```
# - これにより，Jupyter Labを起動したときに指定したフォルダが開かれる

# ### Ipythonのプロファイル
# 
# Ipythonプロファイルを作成すると，jupyterの起動時に自動実行したいコマンドを設定できる．
# 
# - ターミナルで以下を実行する
#     ```
#     ipython profile create profile_name
#     ```
#     - `C:\Users\username\.ipython\prifile_name`に`startup`フォルダが作成される．
# - `startup`フォルダの中に`00.ipy`というファイル（スタートアップスクリプト）を作り，自動実行したいコマンドを記述する．
# - 例えば，以下はよく使うので自動importしておくと良い
# 
#     ```python
#     import os
#     import sys
#     import matplotlib.pyplot as plt
#     import numpy as np
#     import pandas as pd
#     ```
# - 自作のモジュール（例えば`my_module.py`）をimportして使う場合，`my_module.py`を一度jupyterでimportした後に，ローカルで`my_module.py`を変更することがよくある．このとき，ローカルで行った変更内容はjupyter側には自動で反映されない．そこで，スタートアップスクリプトに以下を加えておくと自作モジュールの変更が自動で反映される．
#   
#     ```
#     %load_ext autoreload
#     %autoreload 2
#     %matplotlib inline
#     ```

# 例として，`sport_data`フォルダの中に`module`フォルダを作り，以下のプログラムを`my_module.py`として保存する．
# 
# ```python
# def my_func():
#     for i in range(5):
#         print("test%s" % i)
# 
# if __name__ == '__main__':
#     my_func()
# ```
# つまり，このPythonスクリプトのパスは`C:\Users\username\OneDrive\sport_data\module\my_module.py`となる．

# これを単にPythonスクリプトとして実行すると，`if __name__ == '__main__':`以下のコマンドが実行される：

# ```python
# %run "./module/my_module.py"
# ```

# 一方，これをモジュールとしてインポートするには以下のようにする：

# ```python
# import module.my_module as mm
# ```

# この状態で`my_module`内の関数`my_func()`を以下のように`mm.my_func()`として実行できる：

# ```python
# mm.my_func()
# ```

# スタートアップスクリプト内にautoreloadの設定を書いている場合は，ローカルで`my_module.py`を書き換えたら即座に変更内容が反映されるはずである．

# ```python
# mm.my_func()
# ```

# ### Google Colab
# 
# Google Colab（正式名称はGoogle Colaboratoty）はgoogleが提供するPython実行環境であり，Jupyter Notebookがベースになっている．
# 実際，Google Colabで作成したノートブックは".ipynb形式"で保存されるので，相互互換性がある．
# Google Colabの特徴は以下の通りである：
# 
# - ブラウザ上で動作する
# - 基本操作はJupyter Notebookと似ている（細かい操作方法は異なる）
# - 作成したノートブックはGoogle Drive上に保存される
#     - Google Driveが必要（なのでGoogle アカウントも必要）
# - pythonの環境構築が不要（新たにモジュールをインストールすることも可能）
# - 無料でGPUを使用可能
# 
# 特に，Jupyter Notebookの場合は自分のPC上にpython環境を構築する必要があるが，Google Colabはその必要がない点がメリットである．
# また，GPUが無料で使用可能なので，重い計算を行う際にも重宝する．
# 本講義では，基本的にJupyter Labを用いるが，Google Colabを用いても問題ない．

# #### Google colabでjupyter notebookを開く
# 
# - Google Driveを開いて作業フォルダに移動
# - 既存の`.ipynbファイル`を選択するとGoogle Colabが開く
# - 新規作成作成の場合は以下
#     - ［右クリック］→［その他］→［Google Colaboratory］

# #### 必要なモジュールをimportする
# 
# - google colabにインストールされていないモジュール（japanize_matplotlibなど）
# 
#     ```python
#     !pip install japanize-matplotlib
#     import japanize_matplotlib
#     ```
# - 既にインストールされているモジュール
# 
#     ```python
#     import numpy as np
#     ```

# #### Google Driveをマウントする
# 
# Google Driveに保存した自作モジュールやファイルにアクセスしたい場合はGoogle Driveをマウントする必要がある．
# 
# - 以下を実行する
#   
#     ```python
#     from google.colab import drive
#     drive.mount('/content/drive')
#     ```
# - 「このノートブックにGoogleドライブのファイルへのアクセスを許可しますか？」と聞かれるので「Google ドライブに接続」を選択
# - 自分のGoogleアカウントを選択し，「許可」を選択

# #### 自作モジュールをimportする
# 
# ```python
# import sys
# sys.path.append('/content/drive/My Drive/***')
# 
# import ***.xxx
# ```
# ※ なお，自作モジュールの変更を反映したい場合は［ランタイムを出荷時設定にリセット］し，再度マウントする

# #### matplotlibのスタイルファイルを読み込む
# 
# ```python
# import matplotlib.pyplot as plt
# plt.style.use('/content/drive/My Drive/***/matplotlibrc')
# ```

# ## NumPy

# ### ファンシーインデックス参照
# 
# インデックス参照では1つの要素だけにしかアクセスできなかった．
# また，配列のスライスでは，複数の要素を抽出できたが，連続した要素や1つおきの要素など規則的な抽出しか実現できなかった．
# そこで，任意の要素を複数抽出する方法として，ファンシーインデックス参照がある．
# これは，複数のインデックスを配列として指定するという方法であり，NumPy配列特有の機能である．

# #### 1次元配列の場合

# In[ ]:


x = np.random.randint(100, size=10)
x


# In[ ]:


# 3番目,4番目,7番目要素
x[[3, 4, 7]]


# In[ ]:


# 3番目,7番目,4番目要素（順番が異なる）
x[[3, 7, 4]]


# In[ ]:


# 3番目要素を5個
x[[3, 3, 3, 3, 3]]


# 以下のように，インデックスを2次元配列で与えると，抽出された配列も同じ形状となる．

# In[ ]:


# 2次元のインデックス配列を与える
x[np.array([[3, 7], [4, 5]])]


# #### ２次元配列の場合

# 通常のインデックス参照と同様に，行→列の順で指定する．
# 1次元のインデックス配列を指定すると，複数の行を抽出できる．

# In[ ]:


x2 = np.array([[ 0,  1,  2,  3],
               [ 4,  5,  6,  7],
               [ 8,  9, 10, 11]])
x2


# In[ ]:


# 第0行と第2行を抽出
x2[[0, 2]]


# 複数の列を抽出するには，スライスと組み合わせる．

# In[ ]:


# 第1列と第3列を抽出
x2[:, [1, 3]]


# 2次元配列の複数の要素を一辺に抽出することもできる．
# 例えば，以下は`x2[0, 2], x2[1, 1], x2[2, 3]`を抽出する例である．

# In[ ]:


x2[[0, 1, 2], [2, 1, 3]]

