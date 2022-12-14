#!/usr/bin/env python
# coding: utf-8

# In[1]:


# （必須）モジュールのインポート
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    import japanize_matplotlib
except:
    pass

# 表示設定
np.set_printoptions(suppress=True, precision=3)
get_ipython().run_line_magic('precision', '3')


# In[2]:


# （必須）カレントディレクトリの変更（自分の作業フォルダのパスをコピーして入力する）
os.chdir(r'/Users/narizuka/work/document/lecture/rissho/sport_programming/sport_data')


# # NumPyの基礎

# 本章は以下の文献とウェブサイトを参考にしています：
# 
# - Wes McKinney, Pythonによるデータ分析入門，オライリー，2018
# - Jake VanderPlas, Pythonデータサイエンスハンドブック，オライリー，2018
# - note.nkmk.me: https://note.nkmk.me

# ## Numpyとは？
# ---

# ### NumPyとは？

# スポーツのデータセットは画像，ドキュメント，数値測定結果，など様々なフォーマットを持つが，これらは数値や文字列を格納した配列として扱うことができる．例えば，競技を撮影した動画はフレーム単位ではデジタル画像として表されている．デジタル画像は2次元配列として表され，配列の各要素が各ピクセルの輝度（RGB値）に対応している．また，選手の位置情報は $(x, y, z)$ の時系列データとなっているので，これも実数値の2次元配列として表すことができる．

# このように，数値や文字列を効率的に格納し操作することは，データ分析において最重要項目である．Pythonには，配列を扱うためのリストが標準搭載されているが，サイズの大きいデータを扱うのには不向きである．そこで，大規模な配列を扱うための特別なツールとしてNumPyライブラリが用意されている．NumPy配列はPythonの組み込みリストと似ているが，配列のサイズが大きくなるにつれ，より効率的なデータ操作ができるように設計されている．
# 
# なお，以下ではNumPyを「ナンパイ」と読む．

# ### NumPyのimport
# NumPyは他のパッケージと同様にimportすることができる．Numpyはnpという名前でimportするのが慣例である：

# In[3]:


import numpy as np


# これにより，NumPyの関数（例えば`func`）を使うときには`np.func()`のように実行できる．

# ### Numpy配列と組み込みリストの違い
# 
# **組み込みリスト**
# 
# Pythonは何もimportせずに組み込みリスト（以下，単にリストと呼ぶ）を使うことができる．
# リストは以下のように整数と文字列など複数の型を同時に格納することができ，多次元にすることも可能である．
# また，行ごとに異なるサイズにすることも可能である．

# In[4]:


[[1, 'a', 10.0], [2, 'b']]


# **NumPy配列**
# 
# NumPy配列を作成する方法は後ほど詳しく説明するが，`np.array`関数を用いて組み込みリストを変換するのが基本である．

# In[5]:


np.array([[1, 2], [3, 4]])


# NumPy配列は組み込みリストと同様に多次元配列を実現できるが，**全ての要素が同じ型を持ち，各行のサイズも同じでなければならない**という制約がある（データ型をobjectにすれば実現できなくもないが，これは用いるべきではない）．
# 一見するとPythonの組み込みリストの方が使い勝手が良いように見えるが，Numpy配列には以下のような長所があるため，特に大規模な数値データを分析する際に用いられる．

# **1. リストに比べて高速に動作する**
# 
# これは，Numpyの内部がC言語によって実装されていることが理由であり，特に大規模なデータを扱う際に違いが顕著になる．
# 
# **2. 配列全体に対する高速な演算が可能でコードがシンプル**
# 
# この機能はユニバーサル関数と呼ばれ，配列に対して演算を行うだけでそれが各要素に適用されるので，コードがシンプルになる．
# リストで同じ結果を得るためにはfor文を用いなければならないが，pythonではループ処理が非常に遅くかつコードが煩雑になるため，二重の意味で致命的である．
# 
# **3. 高速に動作する関数やメソッドが組み込まれている**
# 
# 例えばソートを行いたいとき，NumPyや類似のパッケージを使わない場合は自分でソート関数を作る必要があるが，それが上手く高速に動く保証はない．
# 一方，NumPyには予めソート関数`np.sort`が用意されているためこれを用いるだけで済み，さらにアルゴリズムを選択することもできる．

# ### NumPy配列の型

# データ型を明示的に指定したい場合には`dtype`キーワードを用いる．`dtype`で指定できる主要なデータ型は
# - 'int'（整数）
# - 'float'（浮動小数，実数を使う場合）
# - 'complex'（複素数）
# - 'bool'（0か1）
# - 'str'（文字列）
# 
# などである．より詳しく'float64'のようにビット長を指定することもできるが省略するとデフォルトのビット長が指定される．なお，文字列を扱いたい場合はリストかPandasを用いるのが良い．

# In[6]:


x = np.array([1,2,3,4], dtype='float')


# NumPy配列のデータ型を調べたい場合は`dtype`属性を用いる．

# In[7]:


# 配列のデータ型を取得する
x.dtype


# データ型を変更したい場合は`astype`メソッドを用いる．

# In[8]:


# データ型を整数に変更
x = x.astype(int)
x.dtype


# ### NumPy配列の属性
# 
# NumPy配列は以下のような属性を持つ
# - shape：配列の形状
# - ndim：配列の次元数
# - size：配列の全要素数
# - dtype：配列のデータ型
# 
# 配列xに対して`x.shape`などとすると，対応する属性を取得することができる．

# In[10]:


# 配列の作成
x1 = np.array([1,2,3,4,5,6])
print(x1)
x2 = np.array([[1,2,3], [4,5,6]]).astype(float)
print(x2)


# In[11]:


# 配列の形状
print(x1.shape)
print(x2.shape)


# In[12]:


# 次元数
print(x1.ndim)  # 1次元
print(x2.ndim)  # 2次元


# In[13]:


# 配列の全要素数
print(x1.size)
print(x2.size)


# In[14]:


# 配列のデータ型
print(x1.dtype)
print(x2.dtype)


# ### 演習問題
# 
# - `np.array`関数を用いて様々なデータ型の配列を作成せよ
# - 作成した配列の属性を取得せよ
# - `astype`メソッドを用いて作成した配列のデータ型を変更せよ
# - `dtype`メソッドを用いて変更した配列のデータ型を確認せよ

# ## ベクトルと行列について
# ---

# 2年次には線形代数が必修科目となっている．線形代数では主にベクトルと行列を扱うが，これらはデータ分析をする上で避けて通ることができない．実は，NumPyはベクトルや行列を扱うためのパッケージといっても過言ではない．以下，ベクトルと行列について超簡単に説明する．

# ### ベクトル
# 以下のように数字を並べたものをベクトルと呼ぶ：
# 
# $$
#     \left(
# 	\begin{array}{c}
# 		 1 \\
#          2 \\
#          3
# 	\end{array}
# \right),\hspace{0.5cm}
#     (1, 2, 3, 4)
# $$
# 
# １つ目は数字が縦に並んでいるので縦ベクトル，２つ目は横ベクトルと呼ぶ．

# ベクトルを構成する数を成分と呼ぶ．例えば，上の縦ベクトルは第0成分が1，第1成分が2，第2成分が3である．NumPyでは，横ベクトルは1次元のNumPy配列，縦ベクトルは2次元のNumPy配列によって以下のように実現できる：

# In[15]:


np.array([1,2,3])


# In[16]:


np.array([[1], [2], [3]])


# $(a_{1}, a_{2})$というベクトルは，$xy$平面上の任意の点から$x$方向に$a_{1}$，$y$方向に$a_{2}$進んだ点まで引いた矢印によって可視化できる．つまり，ベクトルというのは向きと長さ（大きさ）を持った量である．ベクトルの大きさは矢印の始点から終点までの距離に対応するので
# 
# $$
#     \sqrt{a_{1}^{2} + a_{2}^{2}}
# $$
# 
# と表される．
# スポーツデータの分析では，選手の速度を求めることがよくあるが，速度というのは向きと大きさを持つ量であるので，速度ベクトルとして表すことができる．

# ### 行列

# ベクトルは数を一方向に並べたものであったが，以下のように数を縦と横に並べたものを考える：
# 
# $$
#     \left(
# 	\begin{array}{ccc}
# 		 3 & 5 & 7 \\
#          1 & 0 & 9 \\
#          2 & 4 & 3
# 	\end{array}
# \right)
# $$
# 
# これを行列と呼ぶ．
# 行列はベクトルを並べたものと捉えることもできる．

# 上の行列を横方向に切ると，
# 
# $$
#     \left(
# 	\begin{array}{c}
# 		 3 & 5 & 7
# 	\end{array}
# \right),
#     \left(
# 	\begin{array}{c}
# 		 1 & 0 & 9
# 	\end{array}
# \right),
# \left(
# 	\begin{array}{c}
# 		 2 & 4 & 3
# 	\end{array}
# \right)
# $$
# 
# に分割することができるが，**これらを行と呼び，それぞれを0から始まる行番号によって0行，1行，2行などという．
# NumPyおよびPandasでは，行番号が増減する方向を`axis=0`と表す．**

# 一方，行列を縦方向に切ると
# 
# $$
#     \left(
# 	\begin{array}{ccc}
# 		 3 \\
#          1 \\
#          2
# 	\end{array}
#     \right),\hspace{0.5cm}
#     \left(
# 	\begin{array}{ccc}
# 		 5 \\
#          0 \\
#          4
# 	\end{array}
#     \right)\hspace{0.5cm}
#     \left(
# 	\begin{array}{ccc}
# 		 7 \\
#          9 \\
#          3
# 	\end{array}
#     \right)
# $$
# 
# に分割することができるが，**これを列と呼び，それぞれを0から始まる列番号によって0列，1列，2列などという．
# NumPyおよびPandasでは，列番号が増減する方向を`axis=1`と表す．**

# 行列の形状は行数と列数の組み合わせで $ 3\times 3 $ 行列などと表す．また，行列の成分（要素）は行番号 $ i $ と列番号 $ j $ を用いて $ (i, j) $ 成分（要素）などと表す．例えば，上の行列の $(0, 1)$ 成分は2である．

# 行列は2次元のNumPy配列によって以下のように実現できる：

# In[4]:


np.array([[3, 5, 7], [1, 0, 9], [2, 4, 3]])


# ```{figure} ../figure/matrix.png
# ---
# height: 200px
# name: fig:matrix
# ---
# 行列の例
# ```

# ## NumPy配列の構築
# ---

# ### リストを変換する
# 
# リストからNumPy配列を作るには，`np.array`関数を用いる

# In[18]:


np.array([1,2,3,4])


# In[19]:


# 3x2行列
np.array([[1,2], [3, 4], [5, 6]])


# もし，各要素の型が一致しない場合，以下のように自動的に型が統一される

# In[20]:


np.array([1, 2.0, 3])


# ### 配列生成関数を使う
# 
# 配列の要素が分かっていてサイズが小さい場合には上の方法で問題ないが，サイズが大きい場合にはNumPyの配列生成関数を利用するのが良い．

# **等間隔の数列を作成する**
# 
# まず，等間隔の数列を作る関数として，`np.arange`と`np.linspace`がある．
# 前者は`np.arange(start, end, step)`でstart以上end未満の範囲でstep間隔の数列を生成する．
# 後者は`np.linspace(start, end, num)`でstartからendの間をnum等分した数列を生成する．
# この２つはNumPyの関数の中でも特に多用するので覚えたほうが良い．

# In[21]:


# 0以上20未満の範囲で2ずつ増加する数列
np.arange(0, 20, 2)


# In[22]:


# endだけを指定する
np.arange(10)


# In[23]:


# 0から1までを5分割した数列
np.linspace(0, 1, 5)


# **規則的な配列を作成する**

# In[24]:


# 要素が全て0である長さ10の整数配列
np.zeros(10, dtype=int)


# In[25]:


# 要素が全て1である3行5列の浮動小数点数配列
np.ones([3, 5], dtype=float)


# In[26]:


# 要素がすべて100である3x5配列
np.full([3, 5], 100)


# 以上の関数について，既存の配列`x`と同じ形状にしたい場合は`np.zeros_like(x)`, `np.ones_like(x)`, `np.full_like(x)`を用いる．

# In[27]:


x = np.array([[1, 2, 3], [4, 5, 6]])


# In[28]:


np.ones_like(x)


# In[29]:


np.full_like(x, 5)


# **ランダムな配列（乱数）**

# In[110]:


# 0以上1未満の一様乱数を要素とする3x4配列
np.random.random_sample([3, 4])


# In[109]:


# 10以上20未満の一様整数乱数を要素とする3x4配列
np.random.randint(10, 20, [3, 4])


# In[112]:


# 平均5，標準偏差0.5の正規乱数を要素とする3x4配列
np.random.normal(5, 0.5, [3, 4])


# ### 演習問題

# 以下の配列を作成せよ：
# ```python
# # 0から100まで2ずつ増加する数列
# [0, 2, 4, ..., 96, 98, 100]
# ```

# In[ ]:


# NumPyを使わずに


# In[10]:


# NumPyを使って


# In[11]:


# 作成した配列の要素数を取得


# 以下の配列を作成せよ：
# ```python
# # 要素が全て5である3x4配列
# [[5, 5, 5, 5],
#  [5, 5, 5, 5],
#  [5, 5, 5, 5]]
# ```

# In[12]:


# NumPyを使わずに


# In[14]:


# NumPyを使って


# In[15]:


# 作成した配列の形状を取得


# 以下の配列をNumPyを使って作成せよ

# In[18]:


# -1以上1未満の範囲で0.1ずつ増加する配列


# In[20]:


# 10から2まで2ずつ減少する配列


# In[21]:


# 0から10までを3分割した配列


# In[22]:


# 要素が全て0である5x1の浮動小数配列


# In[23]:


# 要素が全て1である2x7の整数配列


# In[24]:


# 要素が全て0.5である長さ10の1次元配列


# 以下の配列`x`と同じ形状の配列を作成せよ

# In[25]:


np.random.seed(seed=5)
x = np.random.rand(15, 7)
x


# In[26]:


# xの形状を取得


# In[27]:


# xのデータ型を取得


# In[28]:


# xと同じ形状で全ての要素が0


# In[29]:


# xと同じ形状で全ての要素が1


# In[31]:


# xと同じ形状で全ての要素が3


# ## NumPy配列の操作
# ---

# ### 配列のインデックス参照
# 
# 配列中の要素が先頭から何番目かを表すのがインデックスである．
# 1次元配列は1つのインデックス，2次元配列は2つのインデックス（行番号と列番号に対応するインデックス）によって指定する．
# Pythonでは**インデックスは0から始まる**ことに注意する．
# 
# インデックスを用いると，配列から１部分を取り出すことができる．
# これを**インデックス参照**と呼ぶ．
# NumPy配列に対するインデックス参照の方法はPythonリストの場合と同様であり，必要なインデックスを角カッコ`[]`で指定することで$i$番目要素にアクセスできる．

# **1次元配列の場合**

# In[59]:


x1 = np.array([1,2,3,4,5,6])
x1


# In[60]:


# 0番目要素
x1[0]


# In[61]:


# 1番目要素
x1[4]


# 配列の末尾からi番目の要素にアクセスするには負のインデックスを用いる．

# In[62]:


# 末尾の要素
x1[-1]


# **2次元配列の場合**

# 2次元配列では，カンマで区切ってarr[0, 0]のようにアクセスする．
# 行番号→列番号の順番で指定する．
# 
# ※ arr[0][0]のように指定することもできるが非推奨．

# In[10]:


x2 = np.array([[1,2,3], [4,5,6]]).astype(float)
x2


# In[130]:


# (0, 1)要素
x2[0, 1]


# In[12]:


# (1, 0)要素
x2[1, 0]


# ### 配列のスライス
# 
# 配列中の連続する要素を取り出す操作を**スライス**と呼ぶ．
# NumPyでは，以下のようなコロン`:`を用いた表記により配列の１部分にアクセスすることができる：
# 
# `x[i_start: i_end: step]`
# 
# ここで，`i_start`は始めのインデックス，`i_end`は終わりのインデックス，`step`は間隔を表す．
# `i_start`，`i_end`，`step`のいずれかが指定されていない場合はデフォルト値として，`i_start=0`，`i_end=その次元のsize`，`step=1`が指定される．
# 通常はstepを省略する．

# **1次元配列のスライス**

# In[131]:


x = np.arange(10)
x


# In[135]:


# インデックスが0以上5未満の要素
x[0:5]


# In[137]:


# インデックスが0以上5未満の要素（startの省略）
x[:5]


# In[134]:


# インデックスが5以上の要素（endの省略）
x[5:]


# In[140]:


# 先頭から1つおき（startとendの省略）
x[::2]


# In[139]:


# インデックス1からスタートして1つおき
x[1::2]


# `step`が負の場合，`i_start`と`i_end`のデフォルト値が入れ替わるので，配列を逆順にすることができる．

# In[141]:


# 逆順にすべての要素
x[::-1]


# **2次元配列のスライス**
# 
# 2次元配列の場合は，行番号と列番号をカンマで区切って指定する．

# In[142]:


x2 = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12], [13, 14, 15]])
x2


# In[144]:


# 0~1行かつ0~1列
x2[0:2, 0:2]


# **行の抽出**
# 
# ２次元配列で行を抽出する場合には単に行番号を指定するだけで良い．

# In[151]:


# 第1行
x2[0]


# In[43]:


# 1行おき
x2[0::2]


# In[149]:


# 1行目以降
x2[1:]


# **列の抽出**
# 
# ２次元配列で列を抽出する場合には，行方向には`：`を指定し，列方向に抽出したい列番号を指定する．

# In[153]:


# 第0列
x2[:, 0]


# In[154]:


# 1列目以降
x2[:, 1:]


# ### （参考）ファンシーインデックス参照

# インデックス参照では1つの要素だけにしかアクセスできなかった．
# また，配列のスライスでは，複数の要素を抽出できたが，連続した要素や1つおきの要素など規則的な抽出しか実現できなかった．
# そこで，任意の要素を複数抽出する方法として，ファンシーインデックス参照がある．
# これは，複数のインデックスを配列として指定するという方法であり，NumPy配列特有の機能である．

# **1次元配列の場合**

# In[155]:


x = np.random.randint(100, size=10)
x


# In[156]:


# 3番目,4番目,7番目要素
x[[3, 4, 7]]


# In[157]:


# 3番目,7番目,4番目要素（順番が異なる）
x[[3, 7, 4]]


# In[158]:


# 3番目要素を5個
x[[3, 3, 3, 3, 3]]


# 以下のように，インデックスを2次元配列で与えると，抽出された配列も同じ形状となる．

# In[160]:


# 2次元のインデックス配列を与える
x[np.array([[3, 7], [4, 5]])]


# **２次元配列の場合**

# 通常のインデックス参照と同様に，行→列の順で指定する．
# 1次元のインデックス配列を指定すると，複数の行を抽出できる．

# In[161]:


x2 = np.array([[ 0,  1,  2,  3],
               [ 4,  5,  6,  7],
               [ 8,  9, 10, 11]])
x2


# In[162]:


# 第0行と第2行を抽出
x2[[0, 2]]


# 複数の列を抽出するには，スライスと組み合わせる．

# In[163]:


# 第1列と第3列を抽出
x2[:, [1, 3]]


# 2次元配列の複数の要素を一辺に抽出することもできる．
# 例えば，以下は`x2[0, 2], x2[1, 1], x2[2, 3]`を抽出する例である．

# In[165]:


x2[[0, 1, 2], [2, 1, 3]]


# ### 配列への代入

# インデックス参照やスライスによって抽出した配列要素に代入すると，元の配列が変更される．
# この機能を用いると，NumPy配列の１部分を変更することができる．

# **1次元の場合**

# In[166]:


x1 = np.arange(10)
x1


# In[167]:


# 2番目要素を-2に変更
x1[2] = -2
x1


# In[168]:


# 0~4番目要素までを-1に変更
x1[0:5] = -1
x1


# **2次元の場合**

# In[169]:


x2 = np.array([[1,2,3], [4,5,6], [7,8,9]])
x2


# In[170]:


# (0,0)成分を12に変更
x2[0, 0] = 12
x2


# In[171]:


# 第1行を[-4, -5, -6]に変更
x2[1] = [-4, -5, -6]
x2


# In[172]:


# 第2列を[10, 20, 30]に変更
x2[:, 2] = [10, 20, 30]
x2


# ### 演習問題

# 以下の配列`x`に対し，インデックス参照とスライスを用いて指定された１部分を抽出せよ．

# In[32]:


np.random.seed(seed=10)
x = np.random.randint(0, 100, [5, 10])
x


# In[33]:


# (3,7)成分


# In[34]:


# 第1行


# In[35]:


# 第5列


# In[36]:


# 0~2行かつ5列以降


# 配列への代入によって以下の配列を作成せよ

# ```python
# # 中央だけ0
# array([[1., 1., 1.],
#        [1., 0., 1.],
#        [1., 1., 1.]])
# ```

# In[37]:





# ```python
# # 第2行だけ連番
# array([[0., 0., 0., 0., 0.],
#        [0., 0., 0., 0., 0.],
#        [1., 2., 3., 4., 5.]])
# ```

# In[41]:





# ```python
# # 第1列だけ-1で後は10
# array([[10, -1, 10],
#        [10, -1, 10],
#        [10, -1, 10],
#        [10, -1, 10],
#        [10, -1, 10]])
# ```

# In[42]:





# 以下の配列`x`を基に指定された配列を作成せよ

# In[46]:


x = np.arange(0, 25).reshape(5, 5)
x


# ```python
# # 真ん中だけ抽出
# array([[ 6,  7,  8],
#        [11, 12, 13],
#        [16, 17, 18]])
# ```

# In[44]:





# ```python
# # 逆順
# array([[24, 23, 22, 21, 20],
#        [19, 18, 17, 16, 15],
#        [14, 13, 12, 11, 10],
#        [ 9,  8,  7,  6,  5],
#        [ 4,  3,  2,  1,  0]])
# ```

# In[48]:





# ## 条件付き抽出
# ---

# ### ブールインデックス参照

# **ブールインデックス参照とは？**

# 次のような任意の配列を考える．

# In[191]:


x1 = np.random.randint(0, 100, 5)
x1


# この配列と同じ形状で各要素が`True`または`False`である以下のような配列を用意する：

# In[192]:


index_bool = np.array([False, True, False, True, False])
index_bool.dtype


# このような配列を**ブールインデックス配列**と呼び，そのデータ型は'bool'型である．
# 元の配列`x1`に対して，ブールインデックスを用いて参照すると，`True`の要素だけを抽出することができる．これを**ブールインデックス参照**と呼ぶ．

# In[193]:


# Trueの要素だけ抽出
x1[index_bool]


# **ブールインデックス参照による条件付き抽出**

# ブールインデックスは比較演算子`<`, `>`, `==`, `!=`, `%`などを用いて元の配列から自動的に取得することができる．
# 例えば，配列`x1`の中で値が50未満の要素だけ抽出したい場合には以下のようにする：

# In[194]:


x1 = np.random.randint(0, 100, 20)
x1


# In[195]:


# ブールインデックスの取得
x_bool = x1 < 50
x_bool


# In[196]:


# 50未満の要素の抽出
x1[x_bool]


# ブールインデックス参照は多次元配列でも同様の方法で実現できる．
# また，比較演算子を変えれば，以下のように様々な条件で要素を抽出することができる．

# In[198]:


x2 = np.arange(35).reshape(5, 7)
x2


# In[204]:


# 10未満
x2[x2 < 10]


# In[205]:


# 10以上
x2[x2 >= 10]


# In[206]:


# 2に等しくない
x2[x2 != 2]


# In[207]:


# 2に等しい
x2[x2 == 2]


# In[208]:


# 2で割り切れる
x2[x2 % 2 == 0]


# 以下のように複数の条件を指定することもできる．ただし，各条件は括弧`()`で囲む．

# In[212]:


# 1より大きくかつ5未満の要素
x2_bool = (x2 > 1) & (x2 < 5)
x2_bool


# In[213]:


x2[x2_bool]


# In[214]:


# 1または5
x2[(x2 == 1) | (x2 == 5)]


# **ブールインデックス参照による代入**

# ブールインデックス参照による条件抽出と代入を組み合わせれば，配列の中で条件を満たす要素だけ値を変更することができる．

# In[221]:


x1 = np.arange(-5, 10, 1)
x1


# In[222]:


# 負の値を持つ要素を0に変更
x1[x1 < 0] = 0
x1


# In[223]:


# 2で割り切れる要素を2倍
x1[x1 % 2==0] *= 2
x1


# In[244]:


x2 = np.arange(9).reshape(3, 3)
x2


# In[246]:


# 4以上の要素を10に変更
x2[x2 >= 4] = 10
x2


# ### （参考）条件を満たす要素のインデックスを取得

# `np.where`関数を用いると，配列の中で条件を満たす要素のインデックスを取得することができる．

# In[ ]:


x1 = np.random.randint(0, 100, 10)
x1


# In[ ]:


np.where(x1 > 50)


# この場合，インデックスが0,2,9の要素が条件を満たしている．ただし，上のようにタプルが返るので注意する．

# 2次元の場合には以下のようになる．

# In[ ]:


x2 = np.array([[1,2,3], [4,5,6]])
x2


# In[ ]:


np.where(x2 < 4)


# この場合，戻り値は`(行方向のインデックス配列, 列方向のインデックス配列)`となる．
# つまり，条件を満たすインデックスは`(0, 0), (0, 1), (0, 2)`である．

# ### 演習問題

# 以下の配列`x`から指定した条件を満たす要素を抽出せよ

# In[87]:


np.random.seed(seed=5)
x = np.random.randint(-100, 100, 100)
x


# In[88]:


# 負の値を持つ要素


# In[89]:


# 3の倍数


# In[90]:


# 10以上50未満


# In[91]:


# 10以下または50以上


# 以下の配列`x`から指定された配列を作成せよ．

# In[94]:


np.random.seed(seed=30)
x = np.random.randint(-10, 10, [5, 3])
x


# ```python
# # 3を20に変更
# array([[-5, -5, 20],
#        [20,  2, -8],
#        [ 7,  4, -7],
#        [-1, -3, -9],
#        [ 7, 20, -7]])
# ```

# In[93]:





# ```python
# # 3と-5を0に変更
# array([[ 0,  0,  0],
#        [ 0,  2, -8],
#        [ 7,  4, -7],
#        [-1, -3, -9],
#        [ 7,  0, -7]])
# ```

# In[57]:





# ```python
# # 負の値を全て-1に変更
# array([[-1, -1,  3],
#        [ 3,  2, -1],
#        [ 7,  4, -1],
#        [-1, -1, -1],
#        [ 7,  3, -1]])
# ```

# In[60]:





# ```python
# # 負の値を全て正に変更
# array([[5, 5, 3],
#        [3, 2, 8],
#        [7, 4, 7],
#        [1, 3, 9],
#        [7, 3, 7]])
# ```

# In[62]:





# ## 配列の形状変更
# ---

# ### 要素数を保った形状変更

# 配列のサイズ（全要素数）を保ったまま形状（次元数）を変更するには`reshape`メソッドを用いる．
# 例えば，1次元配列を3行3列の配列に変更するには次のようにする．

# In[224]:


x1 = np.arange(1, 10)
x1


# In[225]:


# 1次元配列を3行3列に変更
x2 = x1.reshape(3, 3)
x2


# ただし，元の配列と形状変更後の配列のサイズは同じでなければならない．

# In[226]:


print(x1.size)
print(x2.size)


# 配列の形状を指定する際に１つの次元だけ`-1`とすると，他の次元から自動的にサイズを補完してくれる

# In[227]:


x1.reshape((-1, 3))


# これを使うと，2次元配列を1次元配列に変更することができる．

# In[228]:


x2.reshape(-1)


# ### 配列の連結

# 複数のNumpy配列を連結するには，`concatenate`関数を用いる．
# また，同様の機能を持つ関数として，`block`関数，`vstack`関数，`hstack`関数がある．

# **concatenate関数**

# In[229]:


x = np.array([1, 2, 3])
y = np.array([3, 2, 1])
z = np.array([99, 99, 99])


# In[230]:


# 2つの1次元配列の連結
np.concatenate([x, y])


# In[231]:


# 複数の1次元配列の連結
np.concatenate([x, y, z])


# 2次元配列の場合には連結方向を指定する．
# 連結方向は縦方向（行方向）の場合`axis=0` ，横方向（列方向）の場合`axis=1`とする．

# In[270]:


x2 = np.array([[1,2,3], [4,5,6]])
y2 = np.array([[7,8,9], [10,11,12]])


# In[271]:


# 縦（行方向）に連結
np.concatenate([x2, y2], axis=0)


# In[272]:


# 横（列方向）に連結
np.concatenate([x2, y2], axis=1)


# **（参考）vstack関数／hstack関数**
# 
# - `vstack`関数は縦方向（行方向）への連結を実現し，`axis=1`とした`concatenate`関数と同じ．
# - `hstack`関数は横方向（列方向）への連結を実現し，`axis=0`とした`concatenate`関数と同じ．

# In[273]:


# 行方向（縦）に連結
np.vstack([x2, y2])


# In[238]:


# 列方向（横）に連結
np.hstack([x2, y2])


# **（参考）block関数**

# block関数は配置をリストの形で与えるので，直感的に配置を指定できる．
# 例えば，2次元配列を横に連結したい場合には以下のようにする：

# In[274]:


np.block([x2, y2])


# 一方，縦に連結したい場合には以下のようにリストを指定する：

# In[275]:


np.block([[x2], [y2]])


# ### 配列の削除
# 
# `np.delete`関数で配列から任意の行や列を削除できる．

# In[4]:


x = np.arange(12).reshape(3, 4)
x


# In[5]:


# 第1行を削除
np.delete(x, 1, axis=0)


# In[241]:


# 第0行と1行を削除
np.delete(x, [0, 1], 0)


# In[242]:


# 第1列を削除
np.delete(x, 1, axis=1)


# In[243]:


# 第1列と第3列を削除
np.delete(x, [1, 3], axis=1)


# ## NumPy配列の演算
# ---

# ### ユニバーサル関数（ufunc）

# NumPy配列の演算（加減乗除など）はリストと同じように`for`文などで実装すると非常に低速になってしまう．そこで，高速な演算が可能な**ユニバーサル関数**が用意されている．これは，**配列に対して１つの関数を実行するだけで，全ての要素に対して演算が行われる機能**である．例えば，以下のように1000万個の数値が格納された1次元のNumPy配列があるとする．

# In[6]:


np.random.seed(seed=7)
D = np.random.randint(0, 100, size=int(1e7))
D


# いま，この1000万個の数値に対して平均値を求めようと思ったとき，最も単純な方法は以下のようなfor文による実装である：

# In[9]:


get_ipython().run_cell_magic('time', '', 'M = 0\nfor i in range(len(D)):\n    M += D[i]\n    \nM / len(D)')


# 実行結果を見ると，平均を求めるという単純な演算であるにも関わらず，3秒近く時間がかかっている（実行時間はPCのスペックによって変動する）．これは，データ数が非常に大きいことが原因である．
# 
# 一方，NumPyには平均値を求めるためのユニバーサル関数`numpy.mean`が用意されている．これを用いると，上のように配列の各要素にアクセスすることなく関数を1回実行するだけで平均値を求めることができる：

# In[10]:


get_ipython().run_cell_magic('time', '', 'np.mean(D)')


# この場合の実行時間は約10msとなり，for文を用いた場合の1/100以下となっていることがわかる（実行時間はPCのスペックによって変動する）．
# 
# このように，NumPyのユニバーサル関数を使った演算は，配列のサイズが大きくなるにつれてfor文を用いた場合よりもずっと効率的になる．そこで，**Pythonのプログラムでfor文を見つけたら，まずはNumPyのユニバーサル関数で置き換えられるかどうかを検討することが重要である**．

# ### 配列の演算規則

# NumPy配列の演算規則は以下のようにまとめられる：
# - NumPy配列と数値の演算は，配列の全ての要素に演算が適用される
# - 同じ形状を持つ２つの配列の演算は，**各配列の同じ要素同士で演算が行われる**．
# - 異なる形状を持つ配列の演算には特別な規則（**ブロードキャスト**）が適用される．

# **配列と数値の演算**
# 
# まず，配列と数値の演算は，配列の全ての要素に演算が適用される．

# In[11]:


x2 = np.array([[1, 2, 3], [4, 5, 6]])
x2


# In[284]:


# 足し算
x2 + 5


# In[285]:


# 引き算
x2 - 5


# In[286]:


# 掛け算
x2 * 2 


# In[287]:


# 割り算
x2 / 2


# In[288]:


# 累乗
x2 ** 2


# In[289]:


# 余り
x2 % 2


# In[290]:


# 加減乗除
2*(x2 + 5 - 2)/3


# **同じ形状を持つ配列間の演算**
# 
# 次に，同じ形状をもつ２つの配列の演算は，**各配列の同じ要素同士で演算が行われる**．

# In[12]:


x2


# In[14]:


# 同じ要素同士の足し算
x2 + x2


# In[15]:


# 同じ要素同士の引き算
x2 - x2


# In[16]:


# 同じ要素同士の掛け算
x2 * x2


# In[17]:


# 同じ要素同士の割り算
x2 / x2


# **（参考）異なる形状の配列間での演算：ブロードキャスト**

# NumPy配列では以上の規則を含む**ブロードキャスト**と呼ばれる演算規則が存在する．
# ブロードキャストとは，異なる形状・サイズの配列同士で演算を行う場合に，一方または両方の配列の形状・サイズを自動的に変更（ブロードキャスト）する仕組みである．

# ブロードキャストは以下のルールに従う：
# - ルール1：2つの配列の次元数（ndim）を揃える
#     - ２つの配列の次元数（ndim）が異なる場合，次元数が少ない方の配列の次元を1つ増やす．
#     - 増やした次元のサイズは1とする．
# - ルール2：2つの配列の形状（shape）を揃える
#     - 2つの配列の各次元の長さが異なる場合，サイズが1の次元に限り他方の配列に合うようにサイズを引き伸ばす．
#     - これにより形状が合わない場合はエラーとなる．

# In[297]:


x2 = np.array([[1,2,3], [4,5,6]])
print('shape:', x2.shape)
print('ndim:', x2.ndim)
x2


# In[298]:


y1 = np.array([[1], [2]])
print('shape:', y1.shape)
print('ndim:', y1.ndim)
y1


# In[299]:


z1 = np.array([1, 2, 3])
print('shape:', z1.shape)
print('ndim:', z1.ndim)
z1


# In[300]:


# 形状(2, 3)と(2, 1)
x2+y1


# In[301]:


# 形状(2, 3)と(1, 3)
x2+z1


# In[302]:


# 形状(2, 1)と(1, 3)
y1+z1


# 以下はエラーになる

# In[303]:


x2_2 = np.array([[1,2,3], [4,5,6], [7,8,9]])
print('shape:', x2_2.shape)
print('ndim:', x2_2.ndim)
x2_2


# In[304]:


# 形状(3, 3)と(2, 1)：エラーが出る
x2_2 + y1


# ### 様々なユニバーサル関数

# **並び替え（ソート）：`np.sort`**

# 元の配列を変更せずにソートされた配列を得るには`np.sort`関数を使用する．

# In[391]:


x1 = np.random.randint(0, 100, 10)
x1


# In[392]:


np.sort(x1)


# 2次元配列の場合，`axis`を指定することで行ごとや列ごとのソートが実現できる．

# In[393]:


x2 = np.random.randint(0, 10, [5, 3])
x2


# In[394]:


# 行方向（列ごと）にソート
np.sort(x2, axis=0)


# In[395]:


# 列方向（行ごと）にソート
np.sort(x2, axis=1)


# **重複を除く：`np.unique`**

# In[396]:


x1 = np.random.randint(0, 10, 100)
x1


# In[397]:


np.unique(x1)


# **絶対値**
# 
# 絶対値を求めるには`np.abs`関数を用いる．

# In[398]:


x = np.array([-2, -1, 0, 1, 2])


# In[399]:


np.abs(x)


# **三角関数**

# In[400]:


# πの取得
np.pi


# In[401]:


# 角度データの生成
theta = np.array([np.pi/6, np.pi/3, np.pi/2, np.pi])


# In[406]:


# ラジアンから°への変換
np.degrees(theta)


# In[402]:


# sin
np.sin(theta)


# In[403]:


# cos
np.cos(theta)


# In[404]:


# tan
np.tan(theta)


# **指数関数**

# In[407]:


x = np.array([1, 2, 3])


# In[408]:


# 平方根
np.sqrt(x)


# In[409]:


# 2^x
np.power(2, x)


# In[410]:


# e^x
np.power(np.e, x)


# In[411]:


# e^x
np.exp(x)


# **対数関数**

# In[418]:


# 自然対数（底がe）
x = np.exp([1, 2, 3])
np.log(x)


# In[417]:


# 常用対数（底が10）
x = np.array([10**2, 10**3, 10**4])
np.log10(x)


# In[419]:


# 底が2
x = np.array([2**2, 2**3, 2**4])
np.log2(x)


# ### 配列の集計
# 
# データが格納された配列から平均値などの統計量を求めるためのさまざまな集計関数が用意されている．
# NumPyの主要な集計関数を表に示す．
# ほとんどの集計関数には欠損値（NaN値）を無視して計算を行うNaNセーフ版が用意されている．

# | 関数名 | NaNセーフ版 | 説明 |
# | ---- | ---- | ---- |
# | np.sum | np.nansum | 要素の合計を計算する |
# | np.prod | np.nanprod | 要素の積を計算する |
# | np.mean | np.nanmean | 要素の平均値を計算する |
# | np.std | np.nanstd | 要素の標準偏差を計算する |
# | np.var | np.nanvar | 要素の分散を計算する |
# | np.min | np.nanmin | 最小値を見つける |
# | np.max | np.nanmax | 最大値を見つける |
# | np.median | np.nanmedian | 要素の中央値を計算する |
# | np.percentile | np.nanpercentile | パーセンタイルを計算する |
# | np.any | N/A | いずれかの要素がTrueであるかを評価する |
# | np.all | N/A | すべての要素がTrueであるかを評価する |

# **１次元の場合**

# In[349]:


np.random.seed(seed=2)
x = np.random.randint(0, 100, 10000)
x


# In[350]:


# 合計
np.sum(x)


# In[351]:


# 最大値
np.max(x)


# In[352]:


# 最小値
np.min(x)


# In[357]:


# 中央値
np.median(x)


# In[353]:


# 平均値
np.mean(x)


# In[360]:


# 標準偏差
np.std(x)


# In[362]:


# 標本分散
np.var(x, ddof=0)


# In[361]:


# 不偏分散
np.var(x, ddof=1)


# **2次元の場合**

# 2次元の場合は`axis`を指定することで，行ごと（`axis=0`），列ごと（`axis=1`）の集計が実現できる．

# In[18]:


np.random.seed(seed=1)
x2 = np.random.randint(0, 100, [5, 5])
x2


# In[19]:


# 行方向（列ごと）
np.max(x2, axis=0)


# In[20]:


# 列方向（行ごと）
np.max(x2, axis=1)


# ## ファイル入出力
# ---

# **ファイルへの保存**
# 
# NumPy配列`x`をファイルに書き出すには`np.savetxt`関数を用いる．

# In[97]:


x = np.arange(25).reshape(5, 5)


# 絶対パス

# In[ ]:


# 絶対パスで指定する方法
np.savetxt(r"C:\Users\parar\OneDrive\sport_data\3_numpy\array_ex.csv", x, fmt='%d', delimiter=',')


# 相対パス

# In[96]:


# 相対パスで指定する方法
os.chdir(r"C:\Users\parar\OneDrive\sport_data")  # カレントディレクトリをsport_dataに変更
np.savetxt('./3_numpy/array_ex.csv', x, fmt='%d', delimiter=',')  # sport_dataからの相対パスを指定


# `np.savetxt`にはフォーマット`fmt`，区切り文字`delimiter`，エンコーディング`encoding`などを指定できる．

# **ファイルからの読み込み**

# テキスト形式のデータをNumPy配列に読み込むには`np.loadtxt`関数を用いる．

# 絶対パス

# In[ ]:


# 絶対パスで指定する方法
arr = np.loadtxt(r"C:\Users\parar\OneDrive\sport_data\3_numpy\array_ex.csv", delimiter=',', dtype='float')
arr


# 相対パス

# In[41]:


# 相対パスで指定する方法
os.chdir(r"C:\Users\parar\OneDrive\sport_data")  # カレントディレクトリをsport_dataに変更
arr = np.loadtxt('./3_numpy/array_ex.csv', delimiter=',', dtype='float')  # sport_dataからの相対パスを指定
arr


# `np.loadtxt`には引数として区切り文字`delimiter`，データ型`dtype`，エンコーディング`encoding`などが指定できる．`delimiter`を省略するとデフォルト値のスペース' 'となる．

# ## レポート問題
# ---

# **問題A**
# 
# 以下のように，母平均5，母標準偏差0.5の正規分布に従うデータから100個を抽出した．

# In[81]:


np.random.seed(seed=33)
x = np.random.normal(5, 0.5, 100)
x


# このデータに対し，`np.mean`関数と`np.std`関数を用いて標本平均と標本標準偏差を求めると以下のようになった．

# In[82]:


np.mean(x)


# In[83]:


np.std(x)


# - `np.mean`関数と`np.average`関数を使わずに`x`の標本平均を求め，上の結果と一致することを確かめよ（NumPyの他の関数は用いても良い）．
# ただし，データ$x = (x_{1}, x_{2}, \ldots, x_{n})$に対して，標本平均$\bar{x}$は以下で定義される：
# 
# $$
#     \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_{i} = \frac{x_{1}+x_{2}+\cdots+x_{n}}{n}
# $$

# In[ ]:





# - `np.std`関数と`np.var`関数を使わずに`x`の標本標準偏差を求め，上の結果と一致することを確かめよ（NumPyの他の関数は用いても良い）．
# ただし，データ$x = (x_{1}, x_{2}, \ldots, x_{n})$に対して，標本標準偏差$\bar{\sigma}$は以下で定義される：
# 
# $$
#     \bar{\sigma} 
#     = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_{i} - \bar{x})^2}
#     = \sqrt{ \frac{(x_{1}-\bar{x})^2+(x_{2}-\bar{x})^2+\cdots+(x_{n}-\bar{x})^2}{n} }
# $$

# In[ ]:





# **問題B**

# 次のcsvファイルをダウンロードし，作業フォルダ（例えば`OneDrive/sport_data/3_numpy`）に移動せよ：[player_England.csv](https://drive.google.com/uc?export=download&id=1C1jhTLnDg7ES3QClTf6LL34f8vXq-JgQ) <br>
# このファイルには，2017年度にイングランド・プレミアリーグに所属していた選手の選手ID，身長，体重のデータが保存されている．
# ただし，身長の単位はcm，体重の単位はkgである．
# 
# ※ 本データはPappalardoデータセットを加工したものである（詳細は[イベントデータの解析](https://rtwqzpj5uefb1pvzmprbnq-on.drv.tw/document/講義/立正/スポーツデータ分析のためのプログラミング/6_event.html)）．

# まず，このファイルをNumPy配列`D`に読み込む：

# In[3]:


# csvファイルのパスを指定する
D = np.loadtxt('./3_numpy/player_England.csv', delimiter=',', dtype='int')
D


# 配列`D`は第0列に選手ID，第1列に身長，第2列に体重が格納されている．
# 例えば，`D`の第0行目を見ると，選手IDが3319で身長180cm，体重76kgであることが分かる．
# このデータに対し，以下の問いに答えよ．

# - 選手IDが-1となっている要素はダミーデータである．`D`からダミーデータを削除し，改めて配列`D`とせよ．

# In[3]:


# 解答欄


# - データに含まれる選手数を調べよ．

# In[2]:


# 解答欄


# - 選手IDが703の選手の身長と体重を調べよ．<br>
# ※ この選手は吉田麻也選手である．2017年時点の体重と現在の体重を比較してみよ．

# In[4]:


# 解答欄


# - 配列Dから選手ID，身長，体重のデータを抽出し，それぞれI, H, Wという配列に格納せよ．

# In[62]:


I = 
H = 
W = 


# - 以下の方法により，身長の最小値，最大値を求めよ
#     - `H`を昇順（小→大）に並び替え，先頭と末尾の要素を抽出する
#     - `np.min`，`np.max`関数を用いる

# In[ ]:


# Hを昇順に並び替えて先頭と末尾の要素を抽出


# In[ ]:


# np.min, np.maxを用いる


# - 肥満度を表す指標としてBMIが知られている．BMIは身長と体重を用いて以下で定義される：
# \begin{align}
#     \mathrm{BMI} = \frac{体重 [kg]}{(身長 [m])^2}
# \end{align}

# - 身長の単位をcmからmに変換し，`H2`に格納せよ．

# In[ ]:


# Hの単位をcm -> m
H2 = 


# - 配列`W`と`H2`からBMIを求め，`BMI`という配列に格納せよ．

# In[ ]:


# BMIを求める
BMI = 


# - BMIが18.5未満の選手が１人いる．この選手のIDを調べよ．<br>
#   ※ この選手はRekeem Jordan Harper選手である．<br>
#   ※ 日本肥満学会の基準では，BMIが18.5未満の場合を痩せ型と定義している．

# In[ ]:


# BMIが18.5未満を抽出

