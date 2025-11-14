# -*- coding: utf-8 -*-
"""
功能：统计每支球队的主场与客场射门数（总数 + 场均）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv("C:/Users/kevin/Desktop/epl-training.csv")

# 2️⃣ 分别统计主场与客场射门数及场次
home_shots = df.groupby("HomeTeam")["HS"].sum()       # 主场射门总数
home_games = df["HomeTeam"].value_counts()             # 主场场次

away_shots = df.groupby("AwayTeam")["AS"].sum()       # 客场射门总数
away_games = df["AwayTeam"].value_counts()             # 客场场次

# 3️⃣ 计算主场与客场场均射门数
home_avg = (home_shots / home_games).round(2)
away_avg = (away_shots / away_games).round(2)

# 4️⃣ 合并成整齐表格
shots_table = pd.DataFrame({
    "Home_Shots_Total": home_shots.astype(int),
    "Home_Matches": home_games.astype(int),
    "Home_Avg_Shots": home_avg,
    "Away_Shots_Total": away_shots.astype(int),
    "Away_Matches": away_games.astype(int),
    "Away_Avg_Shots": away_avg
}).sort_values("Home_Avg_Shots", ascending=False)

# 5️⃣ 打印结果
print("\n================= ⚽ 每支球队的主场与客场射门统计 =================\n")
print(shots_table)
