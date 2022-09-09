#!/usr/bin/env python
# coding: utf-8

# # 2022年度レポート

# ## レポートの諸注意

# **回答方法**
# 
# - プログラムはコードセル（複数のセルでもよい）に記述する
# - 問題の回答および説明はマークダウンセルに記述する

# **提出方法**
# 
# 1. このipynbファイルをhtml形式でエクスポートする
#     - File -> Export Notebook As -> HTMLをクリック
#     - 自分の分かりやすいフォルダに保存する
# 2. htmlファイルをポータルのオンライン授業から提出する
#     - ポータルサイトのオンライン授業からレポート提出場所を開く
#     - 1.で保存したhtmlファイルをアップロードする<br>
#     ※ ファイル名は「学籍番号_氏名.html」とすること

# **提出締切**
# 
# - 7/31（日），23:59

# **評価基準**
# 
# - F評価
#     - レポートに著しい不備がある／未提出
# - C評価
#     - レポートを期限内に提出し，基礎知識に関する問題がほとんどできている
# - B評価
#     - 上に加え，NumPy，Pandas，Matplotlibに関する問題の一部ができている
# - A評価
#     - 上に加え，NumPy，Pandas，Matplotlibに関する問題がほとんどできている
# - S評価
#     - 上に加え，実践編に関する課題に答えている
#     - 来年度成塚のゼミを志望する場合はここまでできることが望ましい

# ## 基礎知識に関する問題

# - 新しいマークダウンセルを下に追加し，セル内に好きな文章を記述せよ．
#     - これは解答例です．

# - 絶対パスと相対パスについて自分の言葉で説明せよ
#     - 次の講義資料を参照：**2.4.4  絶対パスと相対パス**

# - Windowsにおいて，コピーしたパスをそのまま貼り付けて使用すると，python側でエラーが出る．この原因と回避する方法を自分の言葉で説明せよ
#     - 次の講義資料を参照：**2.4.3  WindowsのPythonでパスを指定する際の注意**

# - スポーツデータ分析において，Pythonを用いるメリットを自分の言葉で説明せよ
#     - 次の講義資料を参照：**1.1.4  Pythonを用いる理由**<br>
#     - ※ ここに書かれているのはあくまでも一例

# - スポーツデータ分析において，NumPy，Pandas，Matplotlibを用いるメリットを自分の言葉で説明せよ
#     - 次の講義資料を参照：**3.1  Numpyとは？**，**4.1.2  PandasとNumPyの違い**<br>
#     - Matplotlibについては，NumPyやPandasとの連携がしやすい，対話的に実行できる，色やレイアウトを細かく調整できる，など（あくまでも一例）．

# - NumPyとPandasの違いを自分の言葉で説明せよ
#     - 次の講義資料を参照：**4.1.2  PandasとNumPyの違い**

# - モジュールをインポートする意味を自分の言葉で説明せよ
#     - [公式ドキュメント](https://docs.python.org/ja/3/reference/import.html)などを参照

# - `os`モジュールをインポートせよ

# In[1]:


import os


# - `os.chdir`を用いてカレントディレクトリを適当な作業フォルダに変更せよ

# In[2]:


os.chdir('/Users/narizuka/work/document/講義/立正/スポーツデータ分析のためのプログラミング/sport_data')


# - NumPyを`np`，Pandasを`pd`という名前でインポートせよ

# In[3]:


import numpy as np
import pandas as pd


# - matplotlib.pyplotを`plt`という名前でインポートせよ

# In[4]:


import matplotlib.pyplot as plt


# - レポートを**期限内に指定された方法で**提出せよ
#     - 『※ ファイル名は「学籍番号_氏名.html」とすること』を守ること
#     - ファイルの拡張子を手動で変更するのはNG
#     - 自分のPCで開けないファイルは他の人も開けないので，提出前に確認すること

# ## NumPyに関する問題

# **問題A**
# 
# 以下のように，母平均5，母標準偏差0.5の正規分布に従うデータから100個を抽出した．

# In[6]:


np.random.seed(seed=33)
x = np.random.normal(5, 0.5, 100)
x


# このデータに対し，`np.mean`関数と`np.std`関数を用いて標本平均と標本標準偏差を求めると以下のようになった．

# In[7]:


np.mean(x)


# In[8]:


np.std(x)


# - `np.mean`関数と`np.average`関数を使わずに`x`の標本平均を求め，上の結果と一致することを確かめよ（NumPyの他の関数は用いても良い）．
# ただし，データ$x = (x_{1}, x_{2}, \ldots, x_{n})$に対して，標本平均$\bar{x}$は以下で定義される：
# \begin{align}
#     \bar{x} &= \frac{1}{n} \sum_{i=1}^{n} x_{i} = \frac{x_{1}+x_{2}+\cdots+x_{n}}{n}
# \end{align}

# In[10]:


np.sum(x)/x.size


# - `np.std`関数と`np.var`関数を使わずに`x`の標本標準偏差を求め，上の結果と一致することを確かめよ（NumPyの他の関数は用いても良い）．
# ただし，データ$x = (x_{1}, x_{2}, \ldots, x_{n})$に対して，標本標準偏差$\bar{\sigma}$は以下で定義される：
# 
# $$
#     \bar{\sigma} 
#     = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_{i} - \bar{x})^2}
#     = \sqrt{ \frac{(x_{1}-\bar{x})^2+(x_{2}-\bar{x})^2+\cdots+(x_{n}-\bar{x})^2}{n} }
# $$

# In[11]:


np.sqrt(np.sum((x-np.mean(x))**2)/x.size)


# **問題B**

# 次のcsvファイルをダウンロードせよ：[player_England.csv](https://drive.google.com/uc?export=download&id=1C1jhTLnDg7ES3QClTf6LL34f8vXq-JgQ) <br>
# このファイルには，2017年度にイングランド・プレミアリーグに所属していた選手の選手ID，身長，体重のデータが保存されている．
# ただし，身長の単位はcm，体重の単位はkgである．
# 
# ※ 本データはPappalardoデータセットを加工したものである（詳細は[イベントデータの解析](https://rtwqzpj5uefb1pvzmprbnq-on.drv.tw/document/講義/立正/スポーツデータ分析のためのプログラミング/6_event.html)）．

# - 以下を適当に修正し，ダウンロードしたファイルをNumPy配列`D`に読み込め：

# In[13]:


# csvファイルのパスを指定する
D = np.loadtxt('./report/player_England.csv', delimiter=',', dtype='int')
D


# 配列`D`は第0列に選手ID，第1列に身長，第2列に体重が格納されている．
# 例えば，`D`の第0行目を見ると，選手IDが3319で身長180cm，体重76kgであることが分かる．
# このデータに対し，以下の問いに答えよ．

# - 選手IDが-1となっている要素はダミーデータである．`D`からダミーデータを削除し，改めて配列`D`とせよ．

# In[17]:


D = D[D[:, 0]!=-1]


# - データに含まれる選手数を調べよ．

# In[32]:


len(D)


# - 選手IDが703の選手の身長と体重を調べよ．<br>
# ※ この選手は吉田麻也選手である．2017年時点の体重と現在の体重を比較してみよ．

# In[22]:


D[D[:, 0]==703]


# - 配列Dから選手ID，身長，体重のデータを抽出し，それぞれI, H, Wという配列に格納せよ．

# In[23]:


I = D[:, 0]
H = D[:, 1]
W = D[:, 2]


# - 以下の方法により，身長の最小値，最大値を求めよ
#     - `H`を昇順（小→大）に並び替え，先頭と末尾の要素を抽出する
#     - `np.min`，`np.max`関数を用いる

# In[25]:


# Hを昇順に並び替えて先頭と末尾の要素を抽出
np.sort(H)[0], np.sort(H)[-1]


# In[26]:


# np.min, np.maxを用いる
np.min(H), np.max(H)


# - 肥満度を表す指標としてBMIが知られている．BMIは身長と体重を用いて以下で定義される：
# $$
#     \mathrm{BMI} = \frac{体重 [kg]}{(身長 [m])^2}
# $$
#     - 身長の単位をcmからmに変換し，`H2`に格納せよ．
#     - 配列`W`と`H2`からBMIを求め，`BMI`という配列に格納せよ．
#     - BMIが18.5未満の選手が１人いる．この選手のIDを調べよ．<br>
#     ※ この選手はRekeem Jordan Harper選手である．<br>
#     ※ 日本肥満学会の基準では，BMIが18.5未満の場合を痩せ型と定義している．

# In[27]:


# Hの単位をcm -> m
H2 = H/100


# In[33]:


# BMIを求める
BMI = W/(H2**2)


# In[34]:


# BMIが18.5未満を抽出
D[BMI < 18.5]


# ## Pandasに関する問題

# 次のcsvファイルをダウンロードせよ：[player_all.csv](https://drive.google.com/uc?export=download&id=1E3ahjvdekZzCu63k1oECs_GOJTS294BP) <br>
# このファイルには，2017年度にヨーロッパリーグ（イングランド，フランス，ドイツ，イタリア，スペイン）に所属していた選手のデータが保存されている．<br>
# ※ 本データはPappalardoデータセットを加工したものである（詳細は[イベントデータの解析](https://rtwqzpj5uefb1pvzmprbnq-on.drv.tw/document/講義/立正/スポーツデータ分析のためのプログラミング/6_event.html)）．

# - 以下を適当に修正し，`player_all.csv`ファイルを`df`に読み込め

# In[35]:


df = pd.read_csv('./report/player_all.csv', header=0, index_col='player_id', na_values=0)
df


# - `df`の先頭から2行を表示せよ

# In[36]:


df.head(2)


# - 肥満度を表す指標としてBMIが知られている．BMIは身長と体重を用いて以下で定義される：
# $$
#     \mathrm{BMI} = \frac{体重 [kg]}{(身長 [m])^2}
# $$
#     - 身長（`height`）の単位をcmからmに変換せよ．
#     - 身長（`height`）と体重（`weight`）からBMIを求め，`BMI`列を作成せよ．
#     - BMIが18.5未満の選手を抽出せよ．<br>
#     ※ この選手はRekeem Jordan Harper選手である．<br>
#     ※ 日本肥満学会の基準では，BMIが18.5未満の場合を痩せ型と定義している．

# In[38]:


# 'height'の単位をcm->m
df['height']/100


# In[39]:


# BMIを求めて'BMI'列を作成
df['BMI'] = df['weight']/(df['height']/100)**2


# In[41]:


# BMIが18.5未満の選手を抽出
df.loc[df['BMI'] < 18.5]


#  - ポジション（`role`）ごとに，身長，体重，BMIの平均値を計算せよ．<br>

# In[42]:


df['role'].unique()


# In[45]:


# ディフェンダー（'DF'）
df.loc[df['role']=='DF', ['height', 'weight', 'BMI']].mean()


# In[46]:


# ミッドフィルダー（'MF'）
df.loc[df['role']=='MD', ['height', 'weight', 'BMI']].mean()


# In[47]:


# フォワード（'FW'）
df.loc[df['role']=='FW', ['height', 'weight', 'BMI']].mean()


# In[48]:


# キーパー（'GK'）
df.loc[df['role']=='GK', ['height', 'weight', 'BMI']].mean()


# ※ groupbyを用いると１行で書ける

# In[98]:


df.groupby('role').mean()


# ## Matplotlibに関する問題

# 4.で用いた[player_all.csv](https://drive.google.com/uc?export=download&id=1E3ahjvdekZzCu63k1oECs_GOJTS294BP)について，次の問いに答えよ．

# **問題A：体重の箱ひげ図**
# - `England`リーグに所属する選手の体重のデータから欠損値を除外したデータは以下で取得できる．
#     ```python
#     data1 = df.loc[df['league']=='England', 'weight'].dropna()
#     ```
# - 全てのリーグに対して同様のデータを求め，以下のようなリストを作成せよ
#     ```python
#     D = [data1, data2, ...]
#     ```

# 方法１

# In[65]:


data1 = df.loc[df['league']=='England', 'weight'].dropna()
data2 = df.loc[df['league']=='France', 'weight'].dropna()
data3 = df.loc[df['league']=='Germany', 'weight'].dropna()
data4 = df.loc[df['league']=='Italy', 'weight'].dropna()
data5 = df.loc[df['league']=='Spain', 'weight'].dropna()
D = [data1, data2, data3, data3, data4, data5]


# 方法２（for文）

# In[77]:


D = []
for l in df['league'].unique():
    D.append(df.loc[df['league']==l, 'weight'].dropna())


# 方法３（リスト内包表記）

# In[79]:


D = [df.loc[df['league']==l, 'weight'].dropna() for l in df['league'].unique()]


# - リスト`D`を用いて，体重の箱ひげ図をリーグ別に作成せよ．また，グラフを分かりやすく装飾せよ．

# ※ 講義資料のコードをほぼそのまま利用できます

# In[97]:


# 箱ひげ図のプロット
fig, ax = plt.subplots(figsize=(5, 3))
ret = ax.boxplot(D, whis=1.5, widths=0.5, vert=1)

# 横軸の目盛りラベル
ax.set_xticklabels(df['league'].unique())

# 軸のラベル
ax.set_xlabel('リーグ', fontsize=12)
ax.set_ylabel('体重 [kg]', fontsize=12)


# **問題B：身長のヒストグラム**
# - `England`リーグに所属する選手の身長のヒストグラムを以下の条件で作成せよ：
#     - 横軸のラベル：`height [cm]`
#     - 縦軸のラベル：`Frequency`
#     - 階級の数：10
#     - その他の装飾は自由

# ※ 講義資料のコードをほぼそのまま利用できます

# In[99]:


H_e = df.loc[df['league']=='England', 'height'].dropna()

fig, ax = plt.subplots(figsize=(4, 3))
ret = ax.hist(H_e, 
              bins=10,
              histtype='bar',  # ヒストグラムのスタイルを棒グラフに
              color='c',       # バーの色をシアンに
              edgecolor='k',   # バーの枠線の色を黒に
              linewidth=0.5,     # バーの枠線の太さを1に
              linestyle='--',  # 枠線を点線に
              )

# 軸のラベル
ax.set_xlabel('height [cm]', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_xlim(150, 210)


# ## 実践編に関する課題

# 授業内で扱ったデータをPythonを用いて自由に解析し，解析結果をまとめよ．
# - 解析内容は些細なことでも良い
# - 既に知られていることでも良い
