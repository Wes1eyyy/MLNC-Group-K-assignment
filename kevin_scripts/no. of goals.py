# -*- coding: utf-8 -*-
"""
功能：统计每支球队的场均进球数（Goals Scored per Match）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv("C:/Users/kevin/Desktop/epl-training.csv")

# 2️⃣ 分别统计主客场进球总数与场次
home_goals = df.groupby("HomeTeam")["FTHG"].sum()   # 主场进球总数
home_games = df["HomeTeam"].value_counts()          # 主场场次

away_goals = df.groupby("AwayTeam")["FTAG"].sum()   # 客场进球总数
away_games = df["AwayTeam"].value_counts()          # 客场场次

# 3️⃣ 合并主客场数据
total_goals = home_goals.add(away_goals, fill_value=0)
total_matches = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均进球数
avg_goals_per_match = (total_goals / total_matches).round(2)

# 5️⃣ 生成整齐表格
goal_table = pd.DataFrame({
    "Total_Goals_Scored": total_goals.astype(int),
    "Total_Matches": total_matches.astype(int),
    "Avg_Goals_per_Match": avg_goals_per_match
}).sort_values("Avg_Goals_per_Match", ascending=False)

# 6️⃣ 打印结果
print("\n================= ⚽ 每支球队的场均进球统计 =================\n")
print(goal_table)
