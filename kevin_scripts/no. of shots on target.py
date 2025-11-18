# -*- coding: utf-8 -*-
"""
功能：统计每支球队的场均射正数（Shots on Target per Match）
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv("C:/Users/kevin/Desktop/epl-training.csv")

# 2️⃣ 分别统计主客场射正数与场次
home_shots_on_target = df.groupby("HomeTeam")["HST"].sum()   # 主场射正总数
home_games = df["HomeTeam"].value_counts()                    # 主场场次

away_shots_on_target = df.groupby("AwayTeam")["AST"].sum()   # 客场射正总数
away_games = df["AwayTeam"].value_counts()                    # 客场场次

# 3️⃣ 合并主客场数据
total_shots_on_target = home_shots_on_target.add(away_shots_on_target, fill_value=0)
total_games = home_games.add(away_games, fill_value=0)

# 4️⃣ 计算场均射正数
avg_shots_on_target = (total_shots_on_target / total_games).round(2)

# 5️⃣ 组合成整齐表格
shot_accuracy_table = pd.DataFrame({
    "Total_Shots_on_Target": total_shots_on_target.astype(int),
    "Total_Matches": total_games.astype(int),
    "Avg_Shots_on_Target_per_Match": avg_shots_on_target
}).sort_values("Avg_Shots_on_Target_per_Match", ascending=False)

# 6️⃣ 打印结果
print("\n================= 🎯 每支球队的场均射正统计 =================\n")
print(shot_accuracy_table)
