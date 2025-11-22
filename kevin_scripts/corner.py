# -*- coding: utf-8 -*-
"""
功能：统计每支球队的场均角球数量（主客场综合）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv(r"C:\Users\kevin\Desktop\epl-training.csv")

# 2️⃣ 分别统计主场和客场的角球总数及场次
home_corners = df.groupby("HomeTeam")["HC"].sum()   # 每队主场角球总数
home_games = df["HomeTeam"].value_counts()          # 主场场次

away_corners = df.groupby("AwayTeam")["AC"].sum()   # 每队客场角球总数
away_games = df["AwayTeam"].value_counts()          # 客场场次

# 3️⃣ 合并主客场数据
total_corners = home_corners.add(away_corners, fill_value=0)
total_games = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均角球数
avg_corners_per_match = (total_corners / total_games).round(2)

# 5️⃣ 组合成整齐表格输出
corner_table = pd.DataFrame({
    "Total_Corners": total_corners.astype(int),
    "Total_Matches": total_games.astype(int),
    "Avg_Corners_per_Match": avg_corners_per_match
}).sort_values("Avg_Corners_per_Match", ascending=False)

# 6️⃣ 打印结果到终端
print("\n================= ⚽ 每支球队的场均角球数量 =================\n")
print(corner_table)
