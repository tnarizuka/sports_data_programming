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
plt.rcParams['font.family'] = 'Hiragino Sans'

# 表示設定
np.set_printoptions(suppress=True, precision=3)
pd.set_option('display.precision', 3)    # 小数点以下の表示桁
pd.set_option('display.max_rows', 50)   # 表示する行数の上限
pd.set_option('display.max_columns', 7)  # 表示する列数の上限
get_ipython().run_line_magic('precision', '3')


# # イベントデータの解析

# ## イベントデータ
# 
# ### Pappalardoデータセット
# 
# Pappalardoデータセットはサッカーのイベントデータをまとめた大規模データセットであり，[CC BY 4.0ライセンス](https://creativecommons.org/licenses/by/4.0/deed.ja)の下で提供されている．
# 元のデータはWyscout社によって収集されたもので，それをL. Pappalardoらが編集し2019年に公開された．
# 2023年時点で一般公開されているサッカーのイベントデータセットの中では最大級である．
# データセットの詳細については以下の付録を参照のこと：{ref}`pappalardo`

# ### 本講義で用いる加工済みデータ
# 
# Pappalardoデータセットはjson形式で提供されており，このままではデータ分析がしづらい．
# そこで，予めjson形式のデータを整形・加工し，PandasのDataFrameの形で保存しておくと便利であるが，この過程は本講義で扱った知識を総動員するだけでなく，文字列の処理などの知識も必要となる．
# **本講義ではデータの整形・加工の過程は省略し，加工済みデータ（csvファイル）のデータを提供することにする**．
# 以下では，加工済みデータの一部を使ってデータ解析の例を示すが，他のデータを解析したい場合は付録からダウンロードできる：{ref}`pappalardo`

# ## リーグ成績と順位表

# 以下のデータをダウンロードし，カレントディレクトリに保存せよ：
# - 全試合の得点データ：[game.csv](https://drive.google.com/uc?export=download&id=1gueZANYM2wOkQefKpoA_LplKkG0aXA4A)
# - チームプロフィール：[team.csv](https://drive.google.com/uc?export=download&id=1gzjVMRX3daVVFEsNlz-ipidyw-tM2zr1)
#   
# これらを用いれば，チームごとに得点，失点，得失点差，勝敗などを算出することができる．
# 各リーグの最終的な順位は勝ち点によって決まる．
# １試合で獲得する勝ち点は勝利が3，引き分けが1，負けが0である．
# よって，得点データを用いれば勝ち点を計算し，順位表を作成することができる．
# 
# 以下では，イングランド・プレミアリーグの最終成績と順位表を作成してみよう．
# なお，公式に公開されている2017年度イングランド・プレミアリーグの最終成績と順位表は以下で確認できる：
# - [https://ja.wikipedia.org/wiki/プレミアリーグ2017-2018](https://ja.wikipedia.org/wiki/%E3%83%97%E3%83%AC%E3%83%9F%E3%82%A2%E3%83%AA%E3%83%BC%E3%82%B02017-2018)
# - [Premier League Table, Form Guide & Season Archives](https://www.premierleague.com/tables?co=1&se=79&mw=-1&ha=-1)

# ### データの読み込み

# まずは [game.csv](https://drive.google.com/uc?export=download&id=1gueZANYM2wOkQefKpoA_LplKkG0aXA4A) をダウンロードしてカレントディレクトリに移動し，`GM`という名前のDataFrameに読み込む．

# In[10]:


GM = pd.read_csv('./game.csv', header=0)
GM.head(5)


# このデータの各行には2017年度ヨーロッパリーグで行われた試合の情報が収められている．
# 各列の意味は下表の通りである．
# このうち，`away_score`列と`home_score`列がアウェイチームとホームチームの得点である．
# 例えば，第0行はアーセナル（ホーム）対レイチェスターシティ（アウェイ）の試合情報を表し，得点は4-3であることが分かる．
# 
# | 変数名 | 内容 |
# | ---- | ---- |
# | game_id | 試合の一意なID |
# | league | リーグ名 |
# | section | 節（全38節）|
# | date | 日付 |
# | venue | 試合地 |
# | away | アウェイチーム名 |
# | away_id | アウェイチームID |
# | home | ホームチーム名 |
# | home_id | ホームチームID |
# | away_score | アウェイチームのスコア |
# | homw_score |  ホームチームのスコア |

# 次に [team.csv](https://drive.google.com/uc?export=download&id=1gzjVMRX3daVVFEsNlz-ipidyw-tM2zr1) をダウンロードしてカレントディレクトリに移動し，`TM`という名前のDataFrameに読み込む．

# In[12]:


TM = pd.read_csv('./team.csv', header=0)
TM.head()


# このデータの各行には2017年度ヨーロッパリーグに出場したクラブチームの情報が収められている．
# 各列の意味は下表の通りである．
# 例えば，第0行はイングランド・プレミアリーグに所属するアーセナルのチーム情報を表している．
# 
# | 変数名 | 内容 |
# | ---- | ---- |
# | name | チームの俗称 |
# | team_id | チームID|
# | city | チームの所在都市 |
# | country | チームの所在国 |
# | league | チームの所属リーグ | 

# 以下では，イングランド・プレミアリーグのデータを解析対象とする．
# そこで，条件付き抽出を用いて，`TM`と`GM`からイングランド・プレミアリーグのデータだけ抽出する．

# In[14]:


GM_E = GM.loc[GM['league']=='England']
TM_E = TM.loc[TM['league']=='England']


# ### １チームのリーグ成績

# チームプロフィール`TM_E`の先頭行のチーム（アーセナル）に対し，リーグ成績を求めてみよう．
# このチームのチームIDとチーム名を取得するには以下のように`iloc`属性を用いて先頭行を抽出すれば良い．

# In[15]:


tm_id = TM_E['team_id'].iloc[0]
tm_name = TM_E['name'].iloc[0]
print(tm_id)
print(tm_name)


# **得点・失点・得失点差**
# 
# 得点データ`GM`では，2チームをhome，awayによって区別している．
# よって，チームごとに得点と失点を集計するには，ホームゲームとアウェイゲームに分けて処理する必要がある．
# ホームゲームでは，`home_score`列が得点，`away_score`列が失点に対応し，アウェイゲームでは逆になる．
# このことに注意し，アーセナルのホームゲームの得点・失点を`S_h`，アウェイゲームの得点・失点を`S_a`に保存する．
# また，得失点差の列`diff`を追加する．

# In[16]:


# 得点と失点（ホームゲーム）
S_h = GM_E.loc[(GM_E['home_id']==tm_id), ['home_score', 'away_score']] # 対象とするチームのスコアを抽出
S_h = S_h.rename(columns={'home_score': 'goal', 'away_score': 'loss'}) # 列ラベルのリネーム
S_h.head()


# In[17]:


# 得点と失点（アウェイゲーム）
S_a = GM_E.loc[(GM_E['away_id']==tm_id), ['away_score', 'home_score']] # 対象とするチームのスコアを抽出
S_a = S_a.rename(columns={'away_score': 'goal', 'home_score': 'loss'}) # 列ラベルのリネーム
S_a.head()


# In[20]:


# 得失点差列の追加
S_h['diff'] = S_h['goal'] - S_h['loss']  # ホーム
S_a['diff'] = S_a['goal'] - S_a['loss']  # アウェイ
S_h.head()


# **試合結果**
# 
# 次に，試合結果の列`result`を追加する．
# 勝ちを1，引き分けを0，負けを-1で表すことにすると，各試合の結果は得失点差を変換することで求められる．
# 求め方は色々と考えられるが，以下では`np.sign`関数を使って正の数を1，負の数を-1に変換している．

# In[21]:


S_h['result'] = np.sign(S_h['diff']) # ホーム
S_a['result'] = np.sign(S_a['diff']) # アウェイ
S_h.head()


# **ホームゲームとアウェイゲームのデータを結合**
# 
# 次に，`pd.concat`関数を使ってホームゲームとアウェイゲームのデータを統合する．

# In[22]:


S = pd.concat([S_h, S_a])
S.head()


# **勝ち点**

# 勝ち点は勝ちの場合に3，引き分けの場合に1として計算する．

# In[23]:


S['point'] = 0
S.loc[S['result']==1, 'point'] = 3
S.loc[S['result']==0, 'point'] = 1


# **最終成績**

# 最後に各試合のデータを集計し，総得点，総失点，総得失点差，勝ち点を計算すれば，アーセナルのリーグ成績が求められる．
# 他のチームの成績を統合することを考えて，以下のようにDataFrameの形に整形しておく．

# In[43]:


pd.DataFrame([[tm_name, tm_id, S['goal'].sum(), S['loss'].sum(), S['diff'].sum(), S['point'].sum()]],
              columns=['チーム', 'ID', '得点', '失点', '得失点', '勝点'])


# ### 全チームのリーグ成績と順位表

# 全チームのリーグ成績を求めるには，`for`文を用いて上の手続きを繰り返せば良い．
# 以下では，`Rank`という名前のDataFrameに全チームのリーグ成績を保存する．

# In[40]:


Rank = pd.DataFrame(columns=['チーム', 'ID', '得点', '失点', '得失点', '勝点'])
for i in range(len(TM_E)):
    tm_id = TM_E['team_id'].iloc[i]
    tm_name = TM_E['name'].iloc[i]
    
    '''ホームゲーム'''
    # 得点と失点
    S_h = GM_E.loc[(GM_E['home_id']==tm_id), ['home_score', 'away_score']]
    S_h = S_h.rename(columns={'home_score': 'goal', 'away_score': 'loss'})

    # 得失点差
    S_h['diff'] = S_h['goal'] - S_h['loss']

    # 勝敗（勝：1，分：0，負：-1）
    S_h['result'] = np.sign(S_h['diff']) # 符号に応じて1,0,-1を返す
    
    '''アウェイゲーム'''
    # 得点と失点
    S_a = GM_E.loc[(GM_E['away_id']==tm_id), ['home_score', 'away_score']]
    S_a = S_a.rename(columns={'away_score': 'goal', 'home_score': 'loss'})

    # 得失点差
    S_a['diff'] = S_a['goal'] - S_a['loss']

    # 勝敗（勝：1，分：0，負：-1）
    S_a['result'] = np.sign(S_a['diff'])  # 符号に応じて1,0,-1を返す
    
    # 統合
    S = pd.concat([S_h, S_a])
    
    # 勝ち点
    S['point'] = 0
    S.loc[S['result']==1, 'point'] = 3
    S.loc[S['result']==0, 'point'] = 1
    
    # 順位表への統合
    gf = S['goal'].sum()  # 総得点
    ga = S['loss'].sum()  # 総失点
    gd = S['diff'].sum()  # 総得失点差
    pt = S['point'].sum()  # 勝ち点
    
    # チーム成績の結合
    df = pd.DataFrame([[tm_name, tm_id, gf, ga, gd, pt]], columns=Rank.columns)
    Rank = pd.concat([Rank, df])


# 最後に，勝ち点の順にソートし，インデックスを付け直す．

# In[41]:


# ソートと再インデックス
Rank = Rank.sort_values(['勝点'], ascending=False)
Rank = Rank.reset_index(drop=1)


# 以上により，イングランド・プレミアリーグの順位表が作成できた．
# 
# ※ [Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%97%E3%83%AC%E3%83%9F%E3%82%A2%E3%83%AA%E3%83%BC%E3%82%B02017-2018)の情報とは一部合わないが，[Premier League Table, Form Guide & Season Archives](https://www.premierleague.com/tables?co=1&se=79&mw=-1&ha=-1)とは一致している．

# In[42]:


Rank


# ### 演習問題

# - イングランド以外のリーグについて，同様の順位表を作成せよ

# ## 得点分布
# 
# サッカーは非常に得点頻度が低い競技であるが，得点がランダムに入るため常に試合から目が離せない．
# このようなランダム性はサッカーが人々を熱狂させる理由と考えられるが，一方でランダム性の裏にはきれいな法則が隠れている．

# ### ポアソン分布

# **二項分布からポアソン分布へ**
# 
# 成功確率が $ p $ の試行を独立に $ n $ 回繰り返すことを考える．
# 例えば，サイコロを振って特定の目が出ることを成功とすると，$ p=1/6 $ である．
# いま，$ n $ 回中 $ x $ 回成功する確率を $ f(x) $ とすると，$ f(x) $ は二項分布
# 
# $$
#     f(x) = \binom{n}{x}p^{x}(1-p)^{n-x}
# $$
# 
# に従う．
# この式において，$ p^{x}(1-p)^{n-x} $ は成功が $ x $回，失敗が $ n-x $ 回生じる確率を意味する．
# また，$ \binom{n}{x} $ は $ n $ 個から $ x $ 個を取り出す組み合わせの数 $ _{n}C_{x} $ を表し，$ n $ 回の中で何回目に成功するかの場合の数に対応する．

# いま，成功確率 $ p $ が小さく，かつ試行回数 $ n $ が大きい極限を考える．
# ただし，極限を取る際に発散しないように平均値が一定値 $ np=m $ になるようにする．
# このような条件で $n$ 回中 $x$ 回成功する確率 $f(x)$ は，二項分布の式に $ np=m $ を代入し，極限 $ p\to 0,\ n\to \infty $ を取ることで
# 
# $$
#     f(x) = \frac{m^{x}}{x!} \mathrm{e}^{-m}
# $$
# 
# と求まる．
# これを**ポアソン分布**と呼ぶ．
# ポアソン分布は1つのパラメータ $ m $ だけで特徴づけられ，**期待値と分散はともに $ m $ となる**．
# ポアソン分布はその導出過程より，**一定の期間内に発生確率の小さい稀な現象を多数回試行した場合に，その発生回数が従う分布である**．
# 実際，以下の現象は全てポアソン分布に従うことが知られている：
# - 1日の交通事故件数
# - 1分間の放射性元素の崩壊数
# - １ヶ月の有感地震の回数
# - プロシア陸軍で馬に蹴られて死亡した兵士の数

# **サッカーの得点分布**
# 
# チームの強さや試合展開など細かいことはひとまず無視し，サッカーにおける得点がランダムに発生すると仮定する．
# このとき，試合中のどの時点においても一定の得点確率があると見なせば，サッカーは得点確率 $ p $ の小さい試行を何度も繰り返す現象（$ n\to \infty $）と見なすことができ，1試合の得点数はポアソン分布に従うことが期待される．

# ### 得点データの要約

# まずは[game.csv](https://drive.google.com/uc?export=download&id=1gueZANYM2wOkQefKpoA_LplKkG0aXA4A)をダウンロードしてカレントディレクトリに保存し，`GM`という名前のDataFrameに読み込む．

# In[47]:


GM = pd.read_csv('./game.csv', header=0)
GM.head(2)


# この得点データを用いて，リーグごとにアウェイチームとホームチームの得点傾向を調べてみよう．
# 以下はアウェイチームとホームチームの得点の平均値および分散である．
# この結果からおおよそ以下のようなことが読み取れる
# - 1試合の得点の平均値はおおよそ1.2点くらいとなっており，サッカーが得点頻度の少ない競技であることが分かる．
# - ホームとアウェイで比べると，ホームの方がやや平均得点が高い傾向にある．
# - 得点の平均値と分散はほぼ同じ値となっており，ポアソン分布の性質をおおよそ満たしている．

# In[53]:


# England
print(GM.loc[GM['league']=='England', ['away_score', 'home_score']].mean())
print(GM.loc[GM['league']=='England', ['away_score', 'home_score']].var())


# In[54]:


# France
print(GM.loc[GM['league']=='France', ['away_score', 'home_score']].mean())
print(GM.loc[GM['league']=='France', ['away_score', 'home_score']].var())


# In[55]:


# Germany
print(GM.loc[GM['league']=='Germany', ['away_score', 'home_score']].mean())
print(GM.loc[GM['league']=='Germany', ['away_score', 'home_score']].var())


# In[57]:


# Italy
print(GM.loc[GM['league']=='Italy', ['away_score', 'home_score']].mean())
print(GM.loc[GM['league']=='Italy', ['away_score', 'home_score']].var())


# In[58]:


# Spain
print(GM.loc[GM['league']=='Spain', ['away_score', 'home_score']].mean())
print(GM.loc[GM['league']=='Spain', ['away_score', 'home_score']].var())


# ### 得点分布

# 平均値と分散の一致だけではポアソン分布に従う根拠として乏しい．
# そこで，リーグ別にホームチームの得点のヒストグラムを求めてみよう．
# 以下はイングランド・プレミアリーグのホームチームの得点分布である．

# In[70]:


data = GM.loc[GM['league']=='England', 'home_score']

fig, ax = plt.subplots(figsize=(4,3))
x = np.arange(data.max()+2)
ax.hist(data, 
        bins=x, # 階級の左端の値を指定する
        align='left',    # バーの中央を階級の左端に合わせる
        histtype='bar',  # ヒストグラムのスタイル
        color='gray',    # バーの色
        edgecolor='k',   # バーの枠線の色
        rwidth=0.2       # バーの幅
        )

ax.set_xlabel('1試合の得点', fontsize=12)
ax.set_ylabel('試合数', fontsize=12)
ax.set_xticks(x);


# 次に，上のヒストグラムがポアソン分布に従っているか調べるため，試合データから求めた平均値をパラメータとするポアソン分布を描いてみる．
# イングランド・プレミアリーグのホームチームの平均得点は1.53であったので，
# 
# $$
#     f(x) = \frac{1.53^{x}}{x!} \mathrm{e}^{-1.53}
# $$
# 
# のグラフを描けば良い．

# In[71]:


from scipy.stats import poisson

fig, ax = plt.subplots(figsize=(4,3))
x = np.arange(data.max()+2)
fx = poisson.pmf(x, data.mean())
ax.plot(x, fx, '-ok')


# 上のグラフを見比べると，確かに似た分布になっていることが分かる．
# そこで，最後に２つのグラフを合わせよう．

# In[72]:


from scipy.stats import poisson
data = GM.loc[GM['league']=='England', 'home_score']

fig, ax = plt.subplots(figsize=(4,3))
x = np.arange(data.max()+2)
ax.hist(data, 
        bins=x, # 階級の左端の値を指定する
        align='left',    # バーの中央を階級の左端に合わせる
        histtype='bar',  # ヒストグラムのスタイル
        color='gray',    # バーの色
        edgecolor='k',   # バーの枠線の色
        rwidth=0.2
        )

fx = data.size * poisson.pmf(x, data.mean())
ax.plot(x, fx, '-ok')

ax.set_xlabel('1試合の得点', fontsize=12)
ax.set_ylabel('試合数', fontsize=12)
ax.set_xticks(x);


# 実データ（棒グラフ）とポアソン分布（折れ線）の概形はおおよそ一致していることが分かる．
# これは，得点の平均値と分散が近い値になったことと共に，サッカーの得点分布がポアソン分布に従うことを裏付ける材料となる．
# もちろん，サッカーの得点分布が普遍的にポアソン分布に従うかどうかは，他のリーグのデータを調べなければわからない（確かめてみよ）．
# また，$\chi^2$検定などを用いてより定量的な検証を行うことも必要である．

# ### 演習問題

# - 他のリーグについて，ホームチーム（またはアウェイチーム）の得点分布を描画せよ．
# - 実データから求めた平均値をパラメータとするポアソン分布を同じグラフに描画せよ．

# ## イベントデータの解析

# Pappalardoデータセットのイベントデータはイベントログとイベントタグの2種類から成る：
# - イベントログ
#     - パスやシュートなどのボールに関わるイベントに対して，起きた時刻，場所，関わった選手などの基本情報が紐付けられたデータ
#     - 1試合あたり1500~2000イベント
# - イベントタグ
#     - イベントログの各イベントに対して，より詳細な付加情報が紐付けられたデータ
# 
# イベントデータにはボールに関わるほぼ全てのプレー情報が含まれているため，これを分析すれば詳細な試合展開を把握することができる．
# イベントデータは選手プロフィールや得点データに比べて格段に情報量が多いため，その扱いの難易度も高い．
# 基本的にExcelで解析するのは困難であり，Pandasの本領が最も発揮されるデータといえる．

# 以下では，イングランド・プレミアリーグのデータを解析対象とする．
# 準備として，次のファイルをダウンロードしてカレントディレクトリに移動する：
# - イベントログ：[event_England.csv](https://drive.google.com/uc?export=download&id=1783Zl4IRGmiYmo-uLA1-FsZwGesOsFhg)
# - イベントタグ：[event_tag_England.csv](https://drive.google.com/uc?export=download&id=17LhNNVGZ9nsm-d3lqfBWiKmEqGitJwVI)
# - 選手プロフィール：[player.csv](https://drive.google.com/uc?export=download&id=1rtCAL0DqW9SeslMuGFCusg8VRRWz6J_M)
# 
# これらを以下のように読み込んでおく．

# In[4]:


# イベントデータと選手プロフィールの読み込み
EV = pd.read_csv('./event_England.csv')
EV_tag = pd.read_csv('./event_tag_England.csv')
PL = pd.read_csv('./player.csv', header=0)


# ### イベントデータの詳細

# **イベントログ**

# In[5]:


EV.head()


# `EV`には380試合分のイベントログが含まれており，その行数は64万行にのぼる．
# `EV`の各行は試合中の１イベントに対応し，各列にそのイベントに関する基本情報が収められている．
# 各列の内容は下表の通りである．

# | 変数名 | 内容 |
# | ---- | ---- |
# | id | １つのイベントに付与される識別ID（１行に対して１つのIDが付与される） | 
# | game_id | 試合ID |
# | half | 1（前半），2（後半）|
# | t | イベントが起きた時間（ハーフ開始からの経過時間）．単位は秒 |
# | team_id | チームID |
# | player_id | 選手ID |
# | event | イベント名 |
# | event_id | イベントID |
# | subevent | サブイベント名 |
# | subevent_id | サブイベントID |
# | x1 | イベントの始まりの $x$ 座標（単位は\%） |
# | y1 | イベントの始まりの $y$ 座標（単位は\%） |
# | x2 | イベントの終わりの $x$ 座標（単位は\%） |
# | y2 | イベントの終わりの $y$ 座標（単位は\%） |

# **座標系**
# 
# イベントの始まりの座標 $(x_{1}, y_{1})$ と終わりの座標 $(x_{2}, y_{2})$ は以下の座標系に従う：
# - 原点は左下
# - $x,\ y$ 座標の値はフィールドの横幅と縦幅の最大値に対する割合（単位は\%）
#   - $0\le x \le 100$
#   - $0\le y \le 100$
# - 両チームの攻撃方向は右方向となるように統一されている
#   - チームや前後半に関係なく，$ x > 50 $ が相手陣，$ x < 50 $ が自陣
#   - **※ 解析内容に応じて，攻撃方向が逆になるように変換する必要がある**

# サッカーコートの公式規格は $105\mathrm{m}\times 68\mathrm{m}$ なので，コートを描く際にはアスペクト比を以下のように設定する：
# 
# ```python
# ax.set_aspect(68/105)
# ```

# In[6]:


'''サッカーコートの描画'''
fig, ax = plt.subplots(figsize=(4, 4))
ax.set_aspect(68/105)

# ハーフウェイライン
ax.plot([50, 50], [0, 100], 'k--') 

# 描画範囲と軸ラベル
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.set_xlabel('$X$'); ax.set_ylabel('$Y$')


# **イベントタグ**

# In[7]:


EV_tag.head()


# `EV_tag`はイベントログ`EV`と同じ行数のDataFrameであり，各行が試合中の１イベントを表している．
# 各列にはイベントに付与されたタグ（'goal'，'assist'など）が並んでおり，真ならば1，偽ならば0となっている．
# （このようなデータをOne-Hotエンコーディングと呼ぶ．）
# 例えば，'goal'列が1である行では，そのイベントにおいて得点が入ったことを意味する．
# 
# タグの詳細情報は[tag_list.csv](https://drive.google.com/uc?export=download&id=1o_tZ-y0eAYlgN1audJThoVBMN0Ta2x5f)にまとめられている．
# 主要なタグを下表にまとめる．
# 
# | タグ名 | 内容 |
# | ---- | ---- |
# | goal | 得点 | 
# | own_goal | オウンゴール | 
# | assist | アシスト | 
# | key_pass | パス |
# | accurate | イベントの成功 |
# | not accurate | イベントの失敗 |
# 

# ### イベントデータ解析の基本

# イベントログ`EV`とイベントタグ`EV_tag`には，ボールに関わるイベントに関するほぼ全ての情報が含まれている．
# イベントデータ解析の目的はこれらのデータから意味のある情報を抽出することである．
# イベントデータを解析する際の手順は以下のようにまとめられる：
# 1. イベントログ`EV`，イベントタグ`EV_tag`から必要な行を条件付き抽出する
# 2. 条件付き抽出したデータを集計する
# 3. 集計したデータを可視化する

# 以下では，条件付き抽出の例をいくつか示す．

# **特定の試合・時間帯の抽出**

# In[104]:


# 特定の試合を抽出
ev = EV.loc[EV['game_id']==2499719].copy()
ev_tag = EV_tag.loc[EV['game_id']==2499719].copy()


# In[9]:


ev.head()


# In[10]:


ev_tag.head()


# In[14]:


# 前半のみ抽出
ev.loc[ev['half']==1].tail()


# In[15]:


# 前半開始20秒までを抽出
ev.loc[(ev['half']==1) & (ev['t']<20)].tail()


# **特定のイベントの抽出**

# イベントログ`EV`には`'event'`列と`'subevent'`列が存在する．
# `'event'`列は`'pass'`，`'foul'`などの大分類，`'subevent'`列は`'simple_pass'`や`'high_pass'`などの小分類となっている．
# `'event'`および`'subevent'`のリストは[event_list.csv](https://drive.google.com/uc?export=download&id=1oSDUt73paDOsORVj732rGU0vwIwGHvHJ) にまとめられている．

# In[16]:


# event列が'pass'の行を抽出
ev.loc[ev['event']=='pass'].head()


# In[17]:


# subevent列が'simple_pass'の行を抽出
ev.loc[ev['subevent']=='simple_pass'].head()


# In[18]:


# event列が'shot'の行を抽出
ev.loc[(ev_tag['goal']==1)].head()


# **イベントタグを用いた抽出**

# イベントタグ`EV_tag`はイベントログ`EV`と同じ行数で共通の行ラベル（インデックス）を持つ．
# よって，`EV_tag`で取得したブールインデックスを用いて`EV`から条件付き抽出することができる．

# In[19]:


# イベント名が'pass'で，'accurate'タグが1である行（成功パス）を抽出
ev.loc[(ev['event']=='pass') & (ev_tag['accurate']==1)]


# In[20]:


# イベント名が'shot'で，'goal'タグが1である行（成功シュート）
ev.loc[(ev['event']=='shot') & (ev_tag['goal']==1)]


# ### イベント別のヒートマップ

# 条件付き抽出の応用として，イベント別にヒートマップを描いてみよう．
# まず，以下のようにヒートマップを描く`event_hmap`関数を作成する．
# この関数は，$x,\ y$座標のデータを引数として受け取り，matplotlibの`hist2d`関数を用いてヒートマップを描く．

# In[21]:


def event_hmap(x, y, cm='Greens'):
    
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # アスペクト比の変更
    ax.set_aspect(68/105)
    
    # ヒートマップの描画
    ret = ax.hist2d(x, y,\
                    bins=[50, 25], range=[[0, 100], [0, 100]], cmap=cm, cmin=0)

    # カラーバーを追加
    fig.colorbar(ret[3], orientation='vertical', 
                 shrink=0.4, aspect=10, pad=0.05)
    
    # ハーフウェイライン
    ax.plot([50, 50], [0, 100], 'k--') 

    # 描画範囲とラベル
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.set_xlabel('$X$'); ax.set_ylabel('$Y$')


# 特定のイベントだけを条件付き抽出してその$x,\ y$座標を`event_hmap`関数に渡せば，そのイベントが行われたフィールド上の位置をヒートマップで可視化することができる．
# 以下にいくつかの例を示す．

# In[22]:


# パス
cond = (EV['event']=='pass')
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y)


# In[23]:


# 特定の選手のパス
cond = (EV['event']=='pass') & (EV['player_id']==EV['player_id'].unique()[4])
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y, 'Blues')


# In[24]:


# クロス
cond = (EV['subevent']=='cross')
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y, 'Reds')


# In[25]:


# デュエル
cond = (EV['event']=='duel')
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y, 'Greys')


# In[27]:


# デュエル（攻撃時）
cond = (EV['subevent']=='ground_attacking_duel')
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y, 'jet')


# In[28]:


# シュート
cond = (EV['event']=='shot')
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y)


# In[29]:


# シュート（成功）
cond = (EV['event']=='shot') & (EV_tag['goal']==1)
x, y = EV.loc[cond, 'x1'], EV.loc[cond, 'y1']
event_hmap(x, y)


# ### 選手のランキング

# シーズンが終了すると，チームのリーグ成績と共に選手の個人成績が発表される．
# 個人成績は，シュート数やゴール数などの部門別ランキングとなっている．
# ここでは，イベントデータを用いてこれらのランキングを求めてみよう．
# なお，どのようなプレーをシュートやパスと見なすかは用いるデータセットによって異なっており，
# 以下で求めるランキングが公式発表されたものと完全に一致するわけではない．
# 2017年度プレミアリーグの個人成績は例えば，
# - https://www.premierleague.com/stats
# 
# にて確認できるが，細かい数値は本データセットから求めたものと一致しない．

# ランキングの作成方法は以下の通りである．
# - ランキング項目に応じて条件付き抽出する．
#   - 例えば，パス数の場合は'event'列が'pass'である行を抽出する
# - 条件付き抽出後のDataFrameに対し，'player_id'ごとの出現回数を求める
#   - DataFrameの`value_counts`メソッドを用いる
# - 選手プロフィール`PL`を用いて'player_id'を選手名に変換する
#   - 'player_id'と'name'が対応した辞書を作成し，`rename`メソッドを用いる

# In[97]:


# 'player_id'と'name'が対応した辞書
dict_id_name = dict(PL[['player_id', 'name']].values)


# **シュート数**

# In[99]:


cond = (EV['subevent']=='shot') | (EV['subevent']=='free_kick_shot') | (EV['subevent']=='penalty')
Rank_shot = EV.loc[cond, 'player_id'].value_counts()
Rank_shot = Rank_shot.rename(index=dict_id_name)  # 選手IDを選手名に変換する
Rank_shot.iloc[:10]


# **パス数**

# In[100]:


Rank_pass = EV.loc[(EV['event']=='pass'), 'player_id'].value_counts()
Rank_pass = Rank_pass.rename(index=dict_id_name)  # 選手IDを選手名に変換する
Rank_pass.iloc[:10]


# **アシスト数**

# In[101]:


Rank_assist = EV.loc[(EV_tag['assist']==1), 'player_id'].value_counts()
Rank_assist = Rank_assist.rename(index=dict_id_name)  # 選手IDを選手名に変換する
Rank_assist.iloc[:10]


# **ゴール数**

# In[102]:


cond = ((EV['event']=='shot') | (EV['event']=='free_kick')) & (EV_tag['goal']==1)
Rank_goal = EV.loc[cond, 'player_id'].value_counts()
Rank_goal = Rank_goal.rename(index=dict_id_name)  # 選手IDを選手名に変換する
Rank_goal.iloc[:10]


# ### 選手間のパス数

# 最後に，特定の試合における選手間のパス数を可視化してみよう．
# 本来，このような解析にはnetworkxという専用のライブラリを使うべきだが，以下ではpandasとseabornという可視化ライブラリを用いて実装する．

# **試合の抽出**

# In[128]:


# 特定の試合を抽出
ev = EV.loc[EV['game_id']==2499719].copy()
ev_tag = EV_tag.loc[EV['game_id']==2499719].copy()


# **パスリストの作成** 

# 選手間のパス数を求めるには，パスの出し手と受け手の情報が必要である．
# しかし，イベントログ`EV`にはパスの出し手の情報しかないので，受け手の情報を加える必要がある．
# イベント名が'pass'の行については，次の行の選手IDがパスの受け手に対応するので，以下のようにパスリスト`ps`を作成できる．

# In[134]:


# イベント名が'pass'の行を抽出
ev_pass = ev.loc[ev['event']=='pass', ['player_id', 'team_id']]

# パスリストの作成
ps = pd.DataFrame({'player_id': ev_pass['player_id'].values[:-1],
                   'team_id': ev_pass['team_id'].values[:-1],
                   'player_id2': ev_pass['player_id'].values[1:],
                   'team_id2': ev_pass['team_id'].values[1:]})


# **選手名の追加**

# イベントログには選手ID（'player_id'）の情報しかないので，選手プロフィール`PL`のデータを用いて選手名を追加する．
# 以下のように，`replace`メソッドを用いて，選手ID（'player_id'）を選手名（'name'）に置換すれば良い．

# In[135]:


ps['name'] = ps['player_id'].replace(PL['player_id'].values, PL['name'].values)
ps['name2'] = ps['player_id2'].replace(PL['player_id'].values, PL['name'].values)
ps.head()


# **パス数行列の作成**

# チーム内の選手 $i$ と $j$ 間のパス数を要素とする行列をパス数行列と呼ぶことにする．
# パス数行列の $(i, j)$ 成分は選手 $i$ から $j$ へのパスを表す．
# 以下は`for`文によってパス数行列を作成する例である．

# In[136]:


tm_id = ev['team_id'].unique()
pl_id0 = ps.loc[ps['team_id']==tm_id[0], 'name'].unique()
pl_id1 = ps.loc[ps['team_id']==tm_id[1], 'name'].unique()
A0 = pd.DataFrame(index=pl_id0, columns=pl_id0)
A1 = pd.DataFrame(index=pl_id1, columns=pl_id1)


# In[137]:


for i in pl_id0:
    for j in pl_id0:
        A0.loc[i, j] = len(ps.loc[(ps['name']==i) & (ps['name2']==j)])

for i in pl_id1:
    for j in pl_id1:
        A1.loc[i, j] = len(ps.loc[(ps['name']==i) & (ps['name2']==j)])
        
A0 = A0.astype(int)
A1 = A1.astype(int)


# **パス数行列の可視化**

# パス数行列を可視化する方法はいくつか考えられる．
# 例えば，選手を点，選手間のパス数を線の太さに対応させた図で表す方法がある．
# このような図はネットワーク呼ばれ，サッカーのデータ分析における標準的な手法となっている．
# しかし，ネットワークの分析と可視化にはnetworkxなどの専用ライブラリの知識が必要となるので，ここではより直接的にヒートマップを用いた可視化方法を採用する．
# 以下の`plot_corr_mat`関数は，seabornという可視化ライブラリを用いてパス数行列をヒートマップで可視化する．

# In[143]:


import seaborn
def plot_corr_mat(mat, cm='jet'):
    fig, ax = plt.subplots(figsize=(5, 5))
    seaborn.heatmap(mat, ax=ax, linewidths=0.1, cbar=True, annot=True,\
                    square=True, cmap=cm, linecolor='w', cbar_kws={"shrink": .7})
    ax.set_xticklabels(mat.columns, fontsize=8)
    ax.set_yticklabels(mat.index, fontsize=8)
    ax_clb = ax.collections[0].colorbar
    ax_clb.ax.tick_params(labelsize=8)


# In[144]:


plot_corr_mat(A0, 'Reds')


# In[140]:


plot_corr_mat(A1, 'Greens')


# ### 演習問題
# 
# - イングランド以外のリーグについて，選手のランキングを求めよ．
# - 失敗パスに対してパス数行列を作成し，可視化せよ．
# - 他のチームに対してもパス数行列を作成し，可視化せよ．
