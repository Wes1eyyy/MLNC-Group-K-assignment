# -*- coding: utf-8 -*-
"""
功能：统计每个球队的场均黄牌数量（主客场综合）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv(r"C:\Users\kevin\Desktop\epl-training.csv")

# 2️⃣ 分别统计主场和客场的黄牌总数及场次
home_yellow = df.groupby("HomeTeam")["HY"].sum()    # 每个球队作为主队的黄牌总数
home_games = df["HomeTeam"].value_counts()          # 主场场次

away_yellow = df.groupby("AwayTeam")["AY"].sum()    # 每个球队作为客队的黄牌总数
away_games = df["AwayTeam"].value_counts()          # 客场场次

# 3️⃣ 合并主客场数据
total_yellow = home_yellow.add(away_yellow, fill_value=0)
total_games = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均黄牌数
avg_yellow_per_match = (total_yellow / total_games).round(2)

# 5️⃣ 组合成整齐的表格输出
yellow_table = pd.DataFrame({
    "Total_Yellow_Cards": total_yellow.astype(int),
    "Total_Matches": total_games.astype(int),
    "Avg_Yellow_Cards_per_Match": avg_yellow_per_match
}).sort_values("Avg_Yellow_Cards_per_Match", ascending=False)

# 6️⃣ 打印结果
print("\n================= 🟨 每支球队的场均黄牌数量 =================\n")
print(yellow_table)
