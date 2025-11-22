# -*- coding: utf-8 -*-
"""
功能：统计指定日期区间（2021-08-13 至 2024-05-19）内每队总胜负平
Author: ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据
df = pd.read_csv(r"C:\Users\kevin\Desktop\epl-training.csv")

# 2️⃣ 转换日期格式（很重要，否则无法筛选）
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# 3️⃣ 筛选日期范围（只保留 2021-08-13 ~ 2024-05-19 的比赛）
start_date = pd.Timestamp("2021-08-13")
end_date = pd.Timestamp("2024-05-19")
df_recent = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

print(f"\n✅ 数据筛选完成：共 {len(df_recent)} 场比赛入选。\n")

# 4️⃣ 获取所有球队
teams = pd.unique(df_recent[['HomeTeam', 'AwayTeam']].values.ravel('K'))

# 5️⃣ 创建统计表
stats = pd.DataFrame(0, index=teams, columns=["Wins", "Losses", "Draws"])

# 6️⃣ 遍历比赛记录统计胜负平
for _, row in df_recent.iterrows():
    home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]

    if result == "H":  # 主场胜
        stats.loc[home, "Wins"] += 1
        stats.loc[away, "Losses"] += 1
    elif result == "A":  # 客场胜
        stats.loc[away, "Wins"] += 1
        stats.loc[home, "Losses"] += 1
    elif result == "D":  # 平局
        stats.loc[home, "Draws"] += 1
        stats.loc[away, "Draws"] += 1

# 7️⃣ 计算总场次 & 胜率（可选）
stats["TotalMatches"] = stats.sum(axis=1)
stats["WinRate(%)"] = (stats["Wins"] / stats["TotalMatches"] * 100).round(2)

# 8️⃣ 输出结果（按胜率排序）
stats = stats.sort_values("WinRate(%)", ascending=False)

print("================= ⚽ 2021–2024 每队总胜负平统计 =================\n")
print(stats)
