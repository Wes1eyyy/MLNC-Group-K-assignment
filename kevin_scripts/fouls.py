# -*- coding: utf-8 -*-
"""
功能：统计每支球队的犯规数据（总犯规数 + 场均犯规数）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv("C:/Users/kevin/Desktop/epl-training.csv")

# 2️⃣ 分别统计主客场犯规数及场次
home_fouls = df.groupby("HomeTeam")["HF"].sum()       # 主队犯规总数
home_games = df["HomeTeam"].value_counts()             # 主场场次

away_fouls = df.groupby("AwayTeam")["AF"].sum()       # 客队犯规总数
away_games = df["AwayTeam"].value_counts()             # 客场场次

# 3️⃣ 合并主客场数据
total_fouls = home_fouls.add(away_fouls, fill_value=0)
total_games = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均犯规
avg_fouls = (total_fouls / total_games).round(2)

# 5️⃣ 生成整齐的结果表格
fouls_table = pd.DataFrame({
    "Total_Fouls": total_fouls.astype(int),
    "Total_Matches": total_games.astype(int),
    "Avg_Fouls_per_Match": avg_fouls
}).sort_values("Avg_Fouls_per_Match", ascending=False)

# 6️⃣ 输出结果
print("\n================= ⚠️ 每支球队的犯规统计 =================\n")
print(fouls_table)
