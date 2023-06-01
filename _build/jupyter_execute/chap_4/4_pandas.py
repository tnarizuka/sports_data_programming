#!/usr/bin/env python
# coding: utf-8

# In[1]:


# （必須）モジュールのインポート
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# 日本語フォントの設定（Mac:'Hiragino Sans', Windows:'MS Gothic'）
plt.rcParams['font.family'] = 'MS Gothic'

# 表示設定
np.set_printoptions(suppress=True, precision=3)
pd.set_option('display.precision', 3)    # 小数点以下の表示桁
pd.set_option('display.max_rows', 150)   # 表示する行数の上限
pd.set_option('display.max_columns', 5)  # 表示する列数の上限
get_ipython().run_line_magic('precision', '3')


# 本章は以下の文献とウェブサイトを参考にしています：
# - 株式会社ロンバート・増田秀人，現場で使える！pandsデータ前処理入門，翔泳社，2020．
# - Wes McKinney, Pythonによるデータ分析入門，オライリー，2018
# - Jake VanderPlas, Pythonデータサイエンスハンドブック，オライリー，2018
# - note.nkmk.me: https://note.nkmk.me

# # Pandasの基礎

# ## Pandasとは？

# ### Pandasのインポート
# 
# Pandas（パンダス）は`pd`という名前でインポートするのが慣例である：

# In[2]:


import pandas as pd


# ### PandasとNumPyの違い

# 前章では，NumPyを用いて多次元配列を扱う方法を解説した．NumPyでは数値データの処理を非常に高速に実現することができた．一方，Pandas（パンダス）も基本的には多次元配列を扱うためのライブラリであり，PandasとNumPyを相互に変換することもできる．しかし，PandasにはNumPyと異なる以下のような特徴がある：
# 
# 1. 行と列にラベル（行と列の名前）が付与される
# 2. 列ごとに異なる型のデータ（数値や文字列）を混在させることができる
# 3. 欠損値の処理やデータの整形のための機能を備えている
# 4. 様々な形式のデータに対するファイル入出力機能を備えている
# 5. データの可視化機能を備えている
# 
# スポーツデータには文字列や数値など様々な型のデータが含まれるため，こうしたデータを整形したり集約したりするにはNumPyよりもPandasを用いた方が便利である．

# 例えば，以下は，典型的なサッカーのイベントデータをPandasのDataFrameという形式（後述）で表したものである．

# In[2]:


pd.DataFrame({'t':[2, 64, 350, 600],
              'player':['ozora', 'misaki', 'wakabayashi', 'hyuga'],
              'position': ['MF', 'MF', 'GK', 'FW'],
              'x':[5.0, 20.0, 10.5, 32.5],
              'y':[10.0, 1.0, 50.5, 2.5]},
             index = ['A', 'B', 'C', 'D'])


# このデータは１つの行が１イベントに対応しており，0から3までの行ラベル（**＝index**）が付与されている．
# また，各列には時刻（整数型），選手名（文字列型），位置座標（浮動小数点型），など異なるデータ型が混在しており，それぞれに`'t'`，`'player'"`，`'position'`，`'x'`，`'y'`という列ラベル（**＝columns**）が付与されている．
# このデータを処理するためには，NumPyではなくPandasを用いた方が便利そうだと直感的に分かるだろう．
# <!-- また，トラッキングデータには様々な選手の位置座標が時系列として記録されており，多くの欠損値を含む．このようなデータを処理するためには，NumPyを用いるよりも上に挙げた機能を備えたPandasを用いる方が便利である． -->
# なお，ラベルの付いていない巨大な数値データを扱いたい場合や3次元以上の数値データを扱いたい場合など，NumPyを用いた方が良い場面ももちろんある．
# また，データの可視化はPandasでもできるが，より多機能なMatplotlibを用いることを推奨する．

# ## DataFrameオブジェクト

# NumPyではデータをndarrayオブジェクト（NumPy配列）に格納し，様々な処理を行なった．
# Pandasでも2次元のデータを扱うための専用のオブジェクトDataFrameが用意されている．
# DataFrameは（Excelのような）テーブル形式の構造を持ち，以下の特徴がある：
# - 各列には数値や文字列など異なる型を持たせることができる．
# - 行と列にはラベルが付与されており，**行方向のラベルをindex（インデックス），列方向のラベルをcolumns（カラム）と呼ぶ**．
# - indexとcolumnsには数値や文字列を用いて任意のラベルを与えることができる．
# - 行と列にはNumPy配列と同じ行番号・列番号も付与されており，行番号が増える方向を`axis=0`，列番号が増える方向を`axis=1`と呼ぶ．

# ```{figure} ../figure/dataframe.png
# ---
# height: 300px
# name: fig:dataframe
# ---
# DataFrameの例
# ```

# ### DataFrameの生成
# DataFrameを生成するには，以下のように`pd.DataFrame`関数を用いる：
# 
# ```python
# pd.DataFrame(data, index=[0, 1], columns=['A', 'B', 'C'])
# ```
# 
# `pd.DataFrame`の第１引数`data`にはリスト，NumPy配列，辞書などを指定できる．
# また，オプションとして，行ラベルを表す`index`と列ラベルを表す`columns`を指定することができる．

# **リスト・NumPy配列の変換**
# 
# 

# In[3]:


# リストの変換
pd.DataFrame([[1,2,3], [4,5,6]],
             index=[0, 1],
             columns=['A', 'B', 'C'])


# In[4]:


# NumPy配列の変換
pd.DataFrame(np.full([2, 3], 5),
             index=[0, 1],
             columns=['A', 'B', 'C'])


# **辞書の変換**

# `data`として辞書を指定すると，辞書のkeyが列ラベル`columns`となる．
# 行ラベル`index`はオプションとして指定する．

# In[5]:


# 辞書データ
dict_data = {'t':[2, 64, 350, 600],
             'player':['ozora', 'misaki', 'wakabayashi', 'hyuga'],
             'x':[5.0, 20.0, 10.5, 32.5],
             'y':[10.0, 1.0, 50.5, 2.5]}
dict_data


# In[6]:


# 辞書による生成
pd.DataFrame(dict_data, index=['A', 'B', 'C', 'D'])


# ### DataFrameのファイル入出力

# Pandasでデータ分析を行う場合，外部のファイルから直接データを読み込んだり，整形したデータを改めてファイルに保存することが多い．特に，データ分析で最もよく用いられるのがcsv形式のファイルである．csvとはカンマで区切られたテキストファイルを指す略称で，Excelで編集することもできる．

# **csvファイルに保存する**
# 
# まず，DataFrameをcsvファイルに保存するには，以下のように`to_csv`メソッドを用いる：
# 
# ```python
#     df.to_csv('***.csv',  option)
# ```
# 
# 第1引数には保存先ファイルのパスを指定し，第２引数以降にオプションを指定する．

# | オプション名 | 説明 | 指定の仕方 |
# | ---- | ---- | ---- | 
# | header | 列ラベルの有無 | True/False |
# | index | 行ラベルの有無 | True/False |
# | encoding | エンコーディング | 'utf-8', 'shift-jis'など |
# | columns | 出力する列 | ['A', 'B']など |

# In[7]:


# DataFrameを生成する
df = pd.DataFrame({'t':[2, 64, 350, 600],
                   'player':['ozora', 'misaki', 'wakabayashi', 'hyuga'],
                   'x':[5.0, 20.0, 10.5, 32.5],
                   'y':[10.0, 1.0, 50.5, 2.5]},
                   index=['A', 'B', 'C', 'D'])


# In[8]:


# 相対パスを指定してカレントディレクトリに保存する
df.to_csv('./df_sample.csv', # ipynbファイルと同じフォルダに保存
          header=True, index=True, encoding='utf-8', columns=df.columns)


# **csvファイルを読み込む**
# 
# 次に，csvファイルを読み込むには`pd.read_csv`関数を用いる：
# 
# ```python
#     pd.read_csv('***.csv', option)
# ```
# 
# 第1引数にcsvファイルのパスを指定し，第２引数以降にoptionを指定する．

# | オプション名 | 説明 | 指定の仕方 |
# | ---- | ---- | ---- | 
# | header | 列ラベルに使う行 | 行番号 |
# | names | 列ラベルの指定（header=Noneとともに使用） | 列ラベル |
# | index_col | 行ラベルに使う列 | 列番号／列名 |
# | usecols | 読み込む列 | 列番号／列名 |
# | skiprows | 除外する行 | 行番号 |
# | na_values | 欠損値で置き換える値（デフォルトでは' 'や'NaN'など） | ['None', '?']など |
# | na_filter | 欠損値での置き換えの有無（デフォルトはTrue） | True/False |
# | encoding | エンコーディング | 'utf-8', 'shift-jis'など |

# In[9]:


# 相対パスを指定してcsvファイルをDataFrameに読み込む
df = pd.read_csv('./df_sample.csv',
                 header=0, index_col=0, usecols=None)
df


# ### DataFrameの属性

# DataFrameに対して，`df.属性名`とすることで，`df`の様々な情報を取得できる．

# In[22]:


# DataFrameの読み込み
df = pd.read_csv('./df_sample.csv',\
                 header=0, index_col=0, usecols=None)


# **NumPy配列を取得：`values`属性**

# `values`属性を用いると，値をNumPy配列として取り出すことができる．<br>
# ※ 複数の型が混在するDataFrameの場合，取り出したNumPy配列はobject型という特殊な型になる．

# In[23]:


# 値をNumPy配列として取り出す
df.values


# **行・列ラベルを取得：`index`属性，`columns`属性**

# DataFrameの行ラベルと列ラベルは`index`属性と`columns`属性で抽出できる．

# In[24]:


# 行ラベル
df.index


# In[25]:


# 列ラベル
df.columns


# **その他の属性**

# DataFrameにはその他に以下の属性がある．

# In[26]:


# DataFrameの要素数
df.size


# In[27]:


# DataFrameの形状
df.shape


# In[28]:


# 各列のデータ型
df.dtypes


# ### DataFrameの参照
# 
# DataFrameの一部を参照する方法として，主に以下がある：
# 
# - 行・列番号による参照：`iloc`属性（NumPyのインデックス参照と同じ）
# - 行・列ラベルによる参照：`loc`属性，角括弧`[]`
# - 先頭・末尾から数行を抽出：`head`メソッド，`tail`メソッド
# 
# 以下で説明するように，基本的には`iloc`属性と`loc`属性を用い，角括弧は列を選択する場合だけに使用することを推奨する．
# 特に`loc`属性を用いた参照方法はPandas特有であり，かつ頻繁に使用するので必ず理解したほうが良い．

# In[29]:


# csvファイルをDataFrameに読み込む
df = pd.read_csv('./df_sample.csv',\
                 header=0, index_col=0, usecols=None)
df


# **行・列番号による参照：`iloc`属性**
# 
# 0から始まる要素番号（行番号と列番号）によって参照を行うには以下のように`iloc`属性を用いる：
# ```python
# df.iloc[行番号, 列番号]
# ```
# 基本的にはNumPyのインデックス参照と同様であり，スライスにも対応している．

# In[30]:


# 第1行の参照（列番号は省略可）
df.iloc[1]


# In[31]:


# 第1列の参照（df['player']と同じ）
df.iloc[:, 1]


# In[32]:


# 第1~3行の参照
df.iloc[1:4]


# In[33]:


# 第1行と3行の参照
df.iloc[[1, 3]]


# In[34]:


# 第0列〜2列の参照
df.iloc[:, :3]


# **行・列ラベルによる参照：`loc`属性**
# 
# 行ラベルと列ラベルによって値を参照するには以下のように`loc`属性を用いる：
# ```python
# df.loc['行ラベル', '列ラベル']
# ```
# これはNumPyにはないPandas特有の方法である．
# なお，特定の行を参照する場合，列ラベルは省略できる．

# In[35]:


# 'A'行を参照（列ラベルは省略可）
df.loc['A']


# In[38]:


# 複数の行を参照（括弧を二重にする）
df.loc[['A', 'C']]


# In[39]:


# 複数の列を参照（df[['x', 'y']]と同じ）
df.loc[:, ['x', 'y']]


# In[40]:


# 行ラベルが'A'，列ラベルが't'の要素を参照
df.loc['A', 't']


# In[41]:


# 複数の行ラベルと列ラベルの指定
df.loc[['A', 'C'], ['x', 'y']]


# **角括弧`[]`による列の抽出**

# 角括弧を使って`df['t']`とすることで`'t'`というラベルの列を取り出すことができる．
# 
# ※ スライスなどにも対応しているが，`loc`属性の使用を推奨する

# In[42]:


# 't'列の参照（df.loc[:, 't']と同じ）
df['t']


# 複数の列ラベルをリストで指定すると，複数の列を取り出すことができる．

# In[43]:


# 'x'と'y'列の参照（df.loc[:, ['x', 'y']]と同じ）
df[['x', 'y']]


# **先頭から数行だけ抽出：`head`メソッド**
# 
# DataFrame`df`の先頭から`n`行だけ抽出したい場合は`df.head(n)`とする．

# In[44]:


# 先頭から2行だけ抽出
df.head(2)


# **末尾から数行だけ抽出：`tail`メソッド**
# 
# DataFrame`df`の末尾から`n`行だけ抽出したい場合は`df.tail(n)`とする．

# In[45]:


# 末尾から2行だけ抽出
df.tail(2)


# ### 演習問題

# 次のcsvファイルをダウンロードし，カレントディレクトリに保存せよ：[player_all.csv](https://drive.google.com/uc?export=download&id=1E3ahjvdekZzCu63k1oECs_GOJTS294BP) <br>
# このファイルには，2017年度にヨーロッパリーグ（イングランド，フランス，ドイツ，イタリア，スペイン）に所属していた選手のデータが保存されている．<br>
# ※ 本データはPappalardoデータセットを加工したものである（詳細は{ref}`pappalardo`）．

# まず，ダウンロードしたcsvファイルを`df`に読み込む．<br>

# In[265]:


# index_col='player_id'：選手IDを行ラベル（index）に設定
# na_values=0：身長`height`と体重`weight`が0の要素を欠損値`NaN`で置き換える
df = pd.read_csv('./player_all.csv', header=0, index_col='player_id', na_values=0)
df


# DataFrameの先頭2行を取得せよ

# In[266]:


# 解答欄


# DataFrameの末尾2行を取得せよ

# In[267]:


# 解答欄


# `index`（行ラベル）を取得せよ

# In[268]:


# 解答欄


# `columns`（列ラベル）を取得せよ

# In[269]:


# 解答欄


# `iloc`属性を用いて行番号が114の行を抽出せよ

# In[270]:


# 解答欄


# `iloc`属性を用いて行番号が1416~1936までの行を抽出せよ<br>
# ※ これはイタリアリーグのデータである

# In[271]:


# 解答欄


# `iloc`属性を用いて列番号が4の列を抽出せよ

# In[272]:


# 解答欄


# `iloc`属性を用いて列番号が4以上の列を抽出せよ

# In[273]:


# 解答欄


# 角括弧`[]`を用いて`weight`列を抽出せよ

# In[274]:


# 解答欄


# 角括弧`[]`を用いて`nationarity`列を抽出せよ

# In[275]:


# 解答欄


# 角括弧`[]`を用いて`team_id`列，`height`列，`weight`列を抽出せよ<br>
# ※ これがNumPyのレポート問題で扱ったデータである．

# In[276]:


# 解答欄


# `loc`属性を用いてindex（行ラベル）が703の行を抽出せよ

# In[277]:


# 解答欄


# `loc`属性を用いて`weight`列を抽出せよ

# In[278]:


# 解答欄


# `loc`属性を用いてindex（行ラベル）が61941，8747，283062の行を抽出せよ<br>
# ※ これは身長2m以上の選手のデータである

# In[279]:


# 解答欄


# `loc`属性を用いて`index`（行ラベル）が703で`columns`（列ラベル）が`name`，`weight`，`height`の要素を抽出せよ

# In[280]:


# 解答欄


# `index`（行ラベル）が以下の番号の選手は全て日本人である：
# ```
# 94764, 703, 14763, 94695, 94831, 254649, 14816, 14749, 391606, 94650, 14929, 365880, 14836, 94828
# ```
# これらの選手を以下の方法で抽出せよ．

# In[281]:


# 上のindexの順番で抽出


# In[282]:


# indexを昇順に並び替えた上で抽出


# In[283]:


# 上のindexの順番で`name`列だけを抽出


# In[284]:


# 上のindexの順番で`name`, `height`, `weight`列を抽出


# ## 条件付き抽出
# 
# DataFrameからある条件を満たす行や列を抽出する方法として，ブールインデックス参照がある．<br>
# ※ この他にも`where`メソッド，`query`メソッドなどがあるがここでは扱わない

# ### ブールインデックスの取得

# DataFrameにおけるブールインデックス参照は基本的にはNumPyと同様である．

# In[46]:


df = pd.read_csv('./df_sample.csv',\
                 header=0, index_col=0, usecols=None)
df


# NumPyと同様に，`==, >, <, %`などの比較演算子を用いると，ブール値のSeriesまたはDataFrameを自動的に取得することができる．

# In[286]:


# 't'列の値が64
df['t']==64


# In[287]:


# 't'列の値が64より大きい
df['t']>64


# In[288]:


# 'x'列の値が'y'列の値より大きい
df['x'] > df['y']


# 複数条件の場合は`(条件1) & (条件2)`や`（条件1）|（条件2）`のように各条件を()で囲む（and, or,  notは使えない）

# In[289]:


# 't'列が64より大きくかつ'player'列が'hyuga'
(df['t']>64) & (df['player'] == 'hyuga')


# In[290]:


# 'player'列が'misaki'または'hyuga'
(df['player']=='misaki') | (df['player']=='hyuga')


# ある条件の否定は`~条件`で実現できる．この表記は条件が多い場合に役立つ．

# In[291]:


# 't'列が64でない（df['t']!=64と同じ）
~(df['t']==64)


# ### ブールインデックス参照

# NumPyと同様，以下のようにブールインデックスが`True`の行だけを抽出することができる：
# ```python
# df.loc[条件, ['列ラベル1', '列ラベル2']]
# ```
# 特に，**条件の次に列ラベルを指定すると，条件を満たす特定の列だけを抽出できる．**

# In[292]:


# 't'列の値が64の行
df.loc[df['t']==64]


# In[293]:


# 't'列の値が64の行で，'x'，'y'列のみ抽出
df.loc[df['t']==64, ['x', 'y']]


# In[294]:


# 't'列が64でない行（df['t']!=64と同じ）
df.loc[~(df['t']==64)]


# In[295]:


# 't'列が64より大きくかつ'player'列が'hyuga'である行
df.loc[(df['t']>64) & (df['player'] == 'hyuga')]


# In[296]:


# 'player'列が'misaki'または'hyuga'である行で，'x','y'列のみ抽出
df.loc[(df['player']=='misaki') | (df['player']=='hyuga'), ['x', 'y']]


# In[297]:


# 'x'列の値が'y'列の値より大きい行
df.loc[df['x'] > df['y']]


# In[298]:


# 'x'列の値が'y'列の値より大きい行で'player'列のみ抽出
df.loc[df['x'] > df['y'], ['player']]


# ### ブールインデックス参照による値の変更

# ブールインデックス参照で抽出したDataFrameに値を代入することで，条件を満たす要素だけ変更することができる．

# In[299]:


# 't'==64の'player'を'wakashimazu'に変更
df2 = df.copy()
df2.loc[df['t']==350, 'player'] = 'wakashimazu'
df2


# In[300]:


# 't'>64の'x'と'y'を0に変更
df2 = df.copy()
df2.loc[df['t'] > 64, ['x', 'y']] = 0
df2


# ### 欠損値について

# **欠損値とは？**

# データが何らかの事情で欠落している箇所を欠損値と呼ぶ．
# Pandasにおいて，欠損値は`NaN`と表示される（'Not a Number'の略）．
# Pandasでは，空白値の他，pythonの組み込み定数である`None`や`math.nan`，`np.nan`は全て欠損値として扱われる．<br>
# ※ 無限大を表す`inf`はデフォルトでは欠損値として扱われない．

# In[ ]:


# 欠損値を含むDataFrameの作成
import math
df = pd.DataFrame([[1., None, np.nan], [math.nan, 2, 3]])
df


# **欠損値の検出**

# `NaN`の検出には`isna`メソッドまたは`pd.isnull`関数を用いる．どちらも動作は同じで，`NaN`の箇所がTrue，それ以外がFalseとなる．

# In[ ]:


df.isna()


# In[ ]:


pd.isnull(df)


# **欠損値の削除**

# 欠損値の削除には`dropna`メソッドを用いる：
# 
# ```python
# df.dropna(axis=0, how='any')
# ```
# 
# 引数に`axis=0`を指定した場合は行，`axis=1`の場合は列が削除される．
# 引数に`how='any'`を指定した場合，行／列に`NaN`が１つでも含まれれば削除される．
# 一方，`how='all'`の場合，行／列の全ての要素が`NaN`の場合に削除される．

# In[ ]:


df = pd.DataFrame(np.array([[np.nan, 1, 2], [3, np.nan, 5], [6, 7, 8], [np.nan, np.nan, np.nan]]),
                  columns=['a', 'b', 'c'])
df


# In[ ]:


# 欠損値を１つでも含む行を削除
df.dropna(axis=0, how='any')


# In[ ]:


# 欠損値を１つでも含む列を削除
df.dropna(axis=1, how='any')


# In[ ]:


# 全ての要素が欠損値である行を削除
df.dropna(axis=0, how='all')


# **欠損値の置換**

# 欠損値`NaN`を他の値で置換するには`fillna`メソッドを用いる：
# 
# ```python
#     df.fillna(value=置換後の値)
# ```
# 
# valueに数値を指定すると，全ての欠損値がその数値で置換される．

# In[ ]:


# 欠損値を0で置換
df.fillna(0)


# ### 演習問題

# 次のcsvファイルをダウンロードし，カレントディレクトリに保存せよ：[player_all.csv](https://drive.google.com/uc?export=download&id=1E3ahjvdekZzCu63k1oECs_GOJTS294BP) <br>
# このファイルには，2017年度にヨーロッパリーグ（イングランド，フランス，ドイツ，イタリア，スペイン）に所属していた選手のデータが保存されている．<br>
# ※ 本データはPappalardoデータセットを加工したものである（詳細は{ref}`pappalardo`）．

# In[ ]:


# index_col='player_id'：選手IDを行ラベル（index）に設定
# na_values=0：身長`height`と体重`weight`が0の要素を欠損値`NaN`で置き換える
df = pd.read_csv('./player_all.csv', header=0, index_col='player_id', na_values=0)
df


# 身長（`height`）が2m以上の選手を抽出せよ

# In[302]:


# 解答欄


# 国籍（`nationality`）が日本の選手を抽出せよ

# In[303]:


# 解答欄


# 国籍（`nationality`）がケニアの選手を抽出せよ

# In[304]:


# 解答欄


# 出生地（`birth_area`）がケニアの選手を抽出せよ

# In[305]:


# 解答欄


# 利き足（`foot`）が右（`right`）の選手の身長と体重を抽出せよ

# In[306]:


# 解答欄


# スペインリーグに所属し，ポジション（`role`）がフォワードの選手を抽出せよ<br>
# ※ まず`df['role'].unique()`によって，`role`列に含まれる値を確認する

# In[307]:


# まず，role列の値を確認する
df['role'].unique()


# In[308]:


# 解答欄


# 所属リーグ名（`league`）と出生地名（`birth_area`）が同じ選手を抽出し，先頭から10行だけ表示せよ

# In[309]:


# 解答欄


# `league`列内の`England`を`イングランド`に変更せよ

# In[310]:


# 解答欄


# イタリアリーグのデータだけ抽出し，`player_Italy.csv`という名前でcsvファイルに保存せよ．

# In[311]:


# 解答欄


# 自分の好きな条件でデータを抽出せよ

# In[312]:


# 解答欄


# ## データの演算と集計

# ### 演算規則
# 
# まず，NumPyの演算規則は以下のようにまとめられた：
# - NumPy配列と数値の演算は，配列の全ての要素に演算が適用される
# - 同じ形状を持つ２つの配列の演算は，**各配列の同じ要素同士で演算が行われる**．
# - 異なる形状を持つ配列の演算には特別な規則（**ブロードキャスト**）が適用される．
# 
# Pandasの基本的な演算規則はNumPyと似ているが，DataFrame（Series）にはラベルが付与されているのでやや挙動が異なる．
# 四則演算については`+`，`-`，`/`，`*`などの演算子で実現できるが，`df.add`や`df.sub`などの算術メソッドを用いると，より細かい制御が可能である．

# In[313]:


df1 = pd.DataFrame(np.arange(12).reshape(4, 3), columns=['a', 'b', 'c'], dtype='float')
df1


# In[314]:


df2 = pd.DataFrame(2*np.ones(15).reshape(5, 3), columns=['a', 'b', 'd'])
df2


# **数値との演算**

# DataFrame（およびSeries）と数値の演算は全ての要素に演算が適用される．

# In[315]:


# 1を足す
df1 + 1


# In[316]:


# 1を足す（addメソッドを用いる）
df1.add(1)


# In[317]:


# 2を掛ける
df1 * 2


# In[318]:


# 2を掛ける（mulメソッドを用いる）
df1.mul(2)


# **列（Series）同士の演算**

# In[319]:


# 'a'列と'b'列の和
df1['a'] + df1['b']


# In[320]:


# 'a'列と'b'列の積
df1['a'] * df1['b']


# In[321]:


# 'a'列と'b'列の割り算
df1['a'] / df1['b']


# In[322]:


# 'c'列を２乗する
df1['c']**2


# In[323]:


# 'a'列から5を引いて2乗する
(df1['a'] - 5)**2


# **DataFrame同士の演算**

# 行ラベル（index）と列ラベル（columns）が同じ要素同士で演算が行われる．
# 異なるラベルが存在する場合は列と行が拡張され，欠損値`NaN`となる．

# In[324]:


# ラベルが同じDataFrame同士の足し算
df1+df1


# In[325]:


# ラベルが異なるDataFrame間の足し算
df1+df2


# **DataFrameとSeries（特定の列）の演算**

# In[326]:


df1


# In[327]:


s1 = df1['c']
s1


# DataFrameの各列とSeriesの演算を行いたい場合は算術メソッドを用いて`axis=0`を指定する．<br>
# ※ 各種算術メソッドでは，デフォルトで`axis=1`となっているので注意．

# In[328]:


# 各列にs1を加える
df1.add(s1, axis=0)


# In[329]:


# 各列からs1を引く
df1.sub(s1, axis=0)


# In[330]:


# 各列をs1で割る
df1.div(s1, axis=0)


# In[331]:


# 各列にs1を掛ける
df1.mul(s1, axis=0)


# ### データの集計
# 
# PandasにもNumPyと同様にデータの集計を行う様々なメソッドが用意されている．
# 各メソッドで集計の方向を指定するには`axis`引数を用いる．
# 列ごとに集計したい場合は`axis=0`，行ごとの場合は`axis=1`を指定する．
# 

# | メソッド  | 説明  | option |
# |:--|:--| :-- |
# | min | 最小値|
# | max | 最大値|
# | sum | 合計 |
# | mean | 平均値 |
# | median | 中央値 |
# | mode | 最頻値 |
# | var | 分散| ddof（不偏：1，標本：0） |
# | std | 標準偏差| ddof（不偏：1，標本：0）|
# | count | NA値ではない要素数 |
# | diff | 階差 | periods（何行前との差を取るか） |
# | cumusum | 累積和 |

# In[332]:


df = pd.DataFrame(np.random.randint(0, 100, [5, 4]),
                  columns=list('abcd'))
df


# In[333]:


# 各列の最大値
df.max(axis=0)


# In[334]:


# 各行の最大値
df.max(axis=1)


# In[335]:


# 各列の和
df.sum(axis=0)


# In[336]:


# 各行の和
df.sum(axis=1)


# In[337]:


# 各列の平均
df.mean(axis=0)


# In[338]:


# 各行の平均
df.mean(axis=1)


# In[339]:


# 各列の標本標準偏差
df.std(ddof=0, axis=0)


# In[340]:


# 1行前との差分
df.diff(periods=1, axis=0)


# **条件付き抽出したデータの集計**
# 
# まず，演習問題で扱った`"player_all.csv"`を`df`に読み込む

# In[341]:


df = pd.read_csv('./player_all.csv', header=0, index_col='player_id', na_values=0)
df


# In[342]:


# 国籍が'Japan'の選手の平均身長
df.loc[df['nationality']=='Japan', ['height']].mean()


# In[343]:


# 国籍が'England'の選手の平均身長
df.loc[df['nationality']=='England', ['height']].mean()


# In[344]:


# 右利きの選手の平均身長と平均体重
df.loc[df['foot']=='right', ['height', 'weight']].mean()


# In[345]:


# 左利きの選手の平均身長と平均体重
df.loc[df['foot']=='left', ['height', 'weight']].mean()


# In[346]:


# 身長が最大の選手
df.loc[df['height']==df['height'].max()]


# In[347]:


# 体重が最大の選手
df.loc[df['weight']==df['weight'].max()]


# ## データの整形

# In[47]:


df = pd.read_csv('./df_sample.csv',\
                 header=0, index_col=0, usecols=None)
df


# ### 行・列の追加と削除

# **行・列の追加：拡張代入**
# 
# DataFrameに値を代入する際に存在しない行ラベルや列ラベルを指定すると，新たな行や列が追加される．
# これを拡張代入と呼ぶ．
# 拡張代入は`loc`属性と角括弧による参照が対応している（`iloc`属性は対応していない）．
# 
# ※ この他に，列を追加する`assin`メソッド，行を追加する`append`メソッドがあるがここでは触れない．

# In[349]:


# loc属性による'z'列の追加
df2 = df.copy()
df2.loc[:, 'z'] = 5
df2


# In[350]:


# 角括弧による'z'列の追加
df2 = df.copy()
df2['z'] = [1,2,3,4]
df2


# In[351]:


# loc属性による'E'行の追加
df2 = df.copy()
df2.loc['E'] = [1000, 'ishizaki', 50.0, 20.0]
df2


# **行・列の削除：`drop`メソッド**
# 
# 列を削除する場合は`df.drop(columns=['列名1', '列名2'])`とする．<br>
# 行を削除する場合は`df.drop(index=['行名1', '行名2'])`とする．<br>
# ※ バージョン0.21.0より前の場合は`axis`引数を指定する必要がある．

# In[352]:


# 'B'行の削除
df.drop(index=['B'])


# In[353]:


# 't'列の削除
df.drop(columns=['t'])


# In[354]:


# 't'列と'player'列の削除
df.drop(columns=['t', 'player'])


# ### データの並び替え

# Pandasには特定の列の値によってデータを並び替える`sort_values`メソッドと，行ラベル（index）によってデータを並び替える`sort_index`メソッドが用意されている．

# In[48]:


dict_data = {'t':[2, 64, 350, 600],\
             'player':['ozora', 'misaki', 'wakabayashi', 'hyuga'],\
             'x':[5.0, 20.0, 10.5, 32.5],
             'y':[10.0, 1.0, 50.5, 2.5]}
df = pd.DataFrame(dict_data, index=[2, 0, 1, 3])
df


# **値によるソート：`sort_values`メソッド**
# 
# 特定の行・列の値によってソートしたい場合は`sort_values`メソッドを用いる：
# ```python
# df.sort_values(['ラベル1', 'ラベル2', ...], axis=0, ascending=True)
# ```
# 第1引数にはソートに用いるラベル名を指定する．
# ラベル名を複数指定すると，まず1つ目のラベルでソートし，その後順に2つ目以降のラベルでソートされる．
# また，ソートの方向は`axis`引数で指定し，特定の列でソートする場合には`axis=0`，特定の行でソートする場合には`axis=1`を指定する．

# In[356]:


dict_data = {'half': [1, 2, 1, 2],
             't':[2, 64, 350, 600],    
             'player':['ozora', 'misaki', 'wakabayashi', 'hyuga'],
             'x':[5.0, 20.0, 10.5, 32.5],
             'y':[10.0, 1.0, 50.5, 2.5]}
df = pd.DataFrame(dict_data, index=[2, 0, 1, 3])
df


# In[357]:


# 'half'列，'t'列の順にソート
df.sort_values(['half', 't'], axis=0, ascending=True)


# 特定の行を用いてソートする場合，数値と文字列が混在する可能性が高いが，この場合はエラーになる．以下は'player'列を削除してから第2行の値でソートしている．

# In[358]:


# 'half'列，'t'列の順にソート
df2 = df.drop(['player'], axis=1)
df2.sort_values(by=2, axis=1, ascending=True)


# **行・列ラベルによるソート：`sort_index`メソッド**
# 
# 上の`df`は行ラベルが`[2,0,1,3]`という順になっている．このような場合に`sort_index`メソッドを用いると，行ラベル／列ラベルによってDataFrameを辞書順に並び替えることができる：
# ```python
#     df.sort_index(axis=0, ascending=True)
# ```
# 行ラベルか列ラベルかは`axis`引数で指定する．並び替えの方法（昇順か降順）は`ascending`引数に指定し，Trueの場合は昇順，Falseの場合は降順となる．

# In[359]:


# 行ラベルの昇順でソート
df.sort_index(axis=0, ascending=True)


# In[360]:


# 行ラベルの降順でソート
df.sort_index(axis=0, ascending=False)


# In[361]:


# 列ラベルの昇順でソート
df.sort_index(axis=1, ascending=True)


# ### 行ラベル・列ラベルの変更

# In[362]:


df = pd.DataFrame(np.arange(12).reshape(4, 3),
                  index=[3, 0, 2, 1],
                  columns=['b', 'c', 'a'])
df


# **`index`属性・`columns`属性への代入**

# In[363]:


df2 = df.copy()
df2.index = ['A', 'B', 'C', 'D']
df2


# In[364]:


df2 = df.copy()
df2.columns = [0, 1, 2]
df2


# **行ラベル（index）を連番で振り直す：`reset_index`メソッド**
# 
# `reset_index`メソッドを用いると，行ラベル（index）を0から始まる連番で振り直すことができる．
# デフォルトでは`drop`引数が0になっており，元のindexが新たな列としてDataFrameに残る．
# 元のindexを削除したい場合は`drop=1`を指定する．

# In[365]:


# 元のindexを残す
df.reset_index(drop=0)


# In[366]:


# 元のindexを削除
df.reset_index(drop=1)


# ## 演習問題

# 次のcsvファイルをダウンロードし，カレントディレクトリに保存せよ：[player_all.csv](https://drive.google.com/uc?export=download&id=1E3ahjvdekZzCu63k1oECs_GOJTS294BP)  <br>
# このファイルには，2017年度にヨーロッパリーグ（イングランド，フランス，ドイツ，イタリア，スペイン）に所属していた選手のデータが保存されている．<br>
# ※ 本データはPappalardoデータセットを加工したものである（詳細は[イベントデータの解析](https://rtwqzpj5uefb1pvzmprbnq-on.drv.tw/document/講義/立正/スポーツデータ分析のためのプログラミング/6_event.html)）．

# - `player_all.csv`ファイルを`df`に読み込め

# In[391]:


# 解答欄


# - `df`の先頭から2行を表示せよ

# In[392]:


# 解答欄


# - 肥満度を表す指標としてBMIが知られている．BMIは身長と体重を用いて以下で定義される：
#     
#     $$
#     \mathrm{BMI} = \frac{体重 [kg]}{(身長 [m])^2}
#     $$
# 
#     - 身長（`height`）の単位をcmからmに変換せよ．
#     - 身長（`height`）と体重（`weight`）からBMIを求め，`BMI`列を作成せよ．
#     - BMIが18.5未満の選手を抽出せよ．<br>
#     ※ この選手はRekeem Jordan Harper選手である．<br>
#     ※ 日本肥満学会の基準では，BMIが18.5未満の場合を痩せ型と定義している．

# In[393]:


# 'height'の単位をcm->m


# In[394]:


# BMIを求めて'BMI'列を作成


# In[395]:


# BMIが18.5未満の選手を抽出


#  - ポジション（`role`）ごとに，身長，体重，BMIの平均値を計算せよ．<br>

# In[396]:


# ディフェンダー（'DF'）


# In[397]:


# ミッドフィルダー（'MF'）


# In[398]:


# フォワード（'FW'）


# In[399]:


# キーパー（'GK'）

