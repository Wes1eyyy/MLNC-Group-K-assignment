# -*- coding: utf-8 -*-
"""
功能：统计每个球队的主场胜率和客场胜率
Home win rate & Away win rate for each team
"""

import pandas as pd

# 1️⃣ 读取数据（如果你已经在项目目录放了 csv，也可以改成 "epl-training.csv"）
df = pd.read_csv(r"C:\Users\kevin\Desktop/epl-training.csv")

# 2️⃣ -------- 统计主场数据 (Home statistics) --------
# 按主队分组，然后统计每种比赛结果出现的次数
# groupby HomeTeam, count each FTR (H/A/D)
home_stats = df.groupby("HomeTeam")["FTR"].value_counts().unstack(fill_value=0)

# 主场总场次 total home matches
home_played = home_stats.sum(axis=1)

# 主场胜场数 home wins = FTR 为 'H'
home_wins = home_stats.get('H', pd.Series(0, index=home_stats.index))

# 主场胜率 home win rate
home_win_rate = home_wins / home_played   # 0～1 之间
# 如果想显示百分比，可以 *100 后保留两位小数
home_win_rate_percent = (home_win_rate * 100).round(2)

# 3️⃣ -------- 统计客场数据 (Away statistics) --------
# 按客队分组，然后统计每种比赛结果出现的次数
away_stats = df.groupby("AwayTeam")["FTR"].value_counts().unstack(fill_value=0)

# 客场总场次 total away matches
away_played = away_stats.sum(axis=1)

# 客场胜场数 away wins = FTR 为 'A'
away_wins = away_stats.get('A', pd.Series(0, index=away_stats.index))

# 客场胜率 away win rate
away_win_rate = away_wins / away_played
away_win_rate_percent = (away_win_rate * 100).round(2)

# 4️⃣ -------- 合并主客场统计到一个总表 Combine home & away --------
win_rate_table = pd.DataFrame({
    "Home_Played": home_played,                # 主场场次
    "Home_Wins": home_wins,                   # 主场胜场
    "Home_WinRate(%)": home_win_rate_percent, # 主场胜率（百分比）

    "Away_Played": away_played,                # 客场场次
    "Away_Wins": away_wins,                    # 客场胜场
    "Away_WinRate(%)": away_win_rate_percent   # 客场胜率（百分比）
})

# 有些队可能只在主场或只在客场出现，统一按队名排序
win_rate_table = win_rate_table.sort_index()

# 5️⃣ -------- 打印结果到终端 Print to terminal --------
pd.set_option("display.max_rows", None)  # 如果想看所有球队就打开这一行
print("\n================= 🏟 每队主场 / 客场 胜率统计 (Home & Away Win Rate) =================\n")
print(win_rate_table)
