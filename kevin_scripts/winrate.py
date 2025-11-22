# -*- coding: utf-8 -*-
"""
功能：统计每支英超球队的总胜、负、平场次并计算胜率
作者：ChatGPT 助手
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ 读取数据文件
df = pd.read_csv("C:/Users/kevin/Desktop/epl-training.csv")

# 2️⃣ 打印前几行，确保列名匹配
print("数据预览：")
print(df.head(), "\n")

# 3️⃣ 创建一个包含所有球队的统计表
teams = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel('K'))
stats = pd.DataFrame(0, index=teams, columns=['Wins', 'Losses', 'Draws'])

# 4️⃣ 遍历每场比赛，更新各队统计数据
for _, row in df.iterrows():
    home = row['HomeTeam']
    away = row['AwayTeam']
    result = row['FTR']

    if result == 'H':  # 主场胜
        stats.loc[home, 'Wins'] += 1
        stats.loc[away, 'Losses'] += 1
    elif result == 'A':  # 客场胜
        stats.loc[away, 'Wins'] += 1
        stats.loc[home, 'Losses'] += 1
    elif result == 'D':  # 平局
        stats.loc[home, 'Draws'] += 1
        stats.loc[away, 'Draws'] += 1

# 5️⃣ 计算总场次与胜率
stats['TotalMatches'] = stats.sum(axis=1)
stats['WinRate(%)'] = (stats['Wins'] / stats['TotalMatches'] * 100).round(2)

# 6️⃣ 输出结果表格（按胜率排序）
print("\n球队总胜负平统计（含胜率）：")
print(stats.sort_values('WinRate(%)', ascending=False))

# 7️⃣ 可选：绘制柱状图展示胜率
stats.sort_values('WinRate(%)', ascending=False)['WinRate(%)'].plot(
    kind='bar',
    figsize=(12, 6),
    title='Premier League Team Win Rate (%)'
)
plt.ylabel('Win Rate (%)')
plt.tight_layout()
plt.show()
