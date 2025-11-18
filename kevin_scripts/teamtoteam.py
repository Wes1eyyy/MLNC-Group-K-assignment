# -*- coding: utf-8 -*-
"""
功能：统计每支球队对其他球队的胜负平矩阵（Head-to-Head Statistics）
作者：ChatGPT 助手
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1️⃣ 读取数据
df = pd.read_csv(r"C:\Users\kevin\Desktop\epl-training.csv")

# 2️⃣ 获取所有球队名称
teams = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel('K'))

# 3️⃣ 创建三个空矩阵：胜场、负场、平局
win_matrix = pd.DataFrame(0, index=teams, columns=teams)
loss_matrix = pd.DataFrame(0, index=teams, columns=teams)
draw_matrix = pd.DataFrame(0, index=teams, columns=teams)

# 4️⃣ 遍历每一场比赛，根据结果更新对应矩阵
for _, row in df.iterrows():
    home = row['HomeTeam']
    away = row['AwayTeam']
    result = row['FTR']

    if result == 'H':  # 主场胜
        win_matrix.loc[home, away] += 1
        loss_matrix.loc[away, home] += 1
    elif result == 'A':  # 客场胜
        win_matrix.loc[away, home] += 1
        loss_matrix.loc[home, away] += 1
    elif result == 'D':  # 平局
        draw_matrix.loc[home, away] += 1
        draw_matrix.loc[away, home] += 1

# 5️⃣ 打印结果到终端
print("\n================= ⚽ Head-to-Head Wins Matrix =================")
print(win_matrix)
print("\n================= ❌ Head-to-Head Losses Matrix =================")
print(loss_matrix)
print("\n================= 🤝 Head-to-Head Draws Matrix =================")
print(draw_matrix)

# 6️⃣ 可选：绘制热力图（以胜场为例）
plt.figure(figsize=(14, 10))
sns.heatmap(win_matrix, cmap="Blues", linewidths=0.5)
plt.title("Head-to-Head Wins Matrix (HomeTeam vs AwayTeam)")
plt.xlabel("Opponent (Away Team)")
plt.ylabel("Team (Home Team)")
plt.tight_layout()
plt.show()
