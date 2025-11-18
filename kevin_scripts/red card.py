# -*- coding: utf-8 -*-
"""
功能：统计每支球队的场均红牌数量（主客场综合）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv(r"C:\Users\kevin\Desktop\epl-training.csv")

# 2️⃣ 分别统计主场和客场的红牌总数及场次
home_red = df.groupby("HomeTeam")["HR"].sum()      # 每个球队主场红牌总数
home_games = df["HomeTeam"].value_counts()          # 主场场次

away_red = df.groupby("AwayTeam")["AR"].sum()      # 每个球队客场红牌总数
away_games = df["AwayTeam"].value_counts()          # 客场场次

# 3️⃣ 合并主客场数据
total_red = home_red.add(away_red, fill_value=0)
total_games = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均红牌数
avg_red_per_match = (total_red / total_games).round(3)   # 红牌较少，可多保留一位小数

# 5️⃣ 组合成整齐的表格输出
red_table = pd.DataFrame({
    "Total_Red_Cards": total_red.astype(int),
    "Total_Matches": total_games.astype(int),
    "Avg_Red_Cards_per_Match": avg_red_per_match
}).sort_values("Avg_Red_Cards_per_Match", ascending=False)

# 6️⃣ 打印结果
print("\n================= 🟥 每支球队的场均红牌数量 =================\n")
print(red_table)
