
# -*- coding: utf-8 -*-

"""
Aggregate team-level features and export to CSV.

Includes:
- Overall win rate
- Home & away win rate
- Goals, shots, shots on target per match
- Fouls, yellow cards, red cards, corners per match
- Recent-period win rate (2021-08-13 to 2024-05-19)
"""

import os
import pandas as pd

# Load raw data
df = pd.read_csv("../data/raw/epl-training.csv")

# Ensure Date column is in datetime format
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# ---- Total matches (home + away) ----
home_games = df["HomeTeam"].value_counts()
away_games = df["AwayTeam"].value_counts()
total_matches = home_games.add(away_games, fill_value=0).astype(int)

teams = sorted(total_matches.index)
features = pd.DataFrame(index=teams)
features["TotalMatches"] = total_matches.reindex(teams).astype(int)


# Helper: sum a home-column and away-column into team totals
def sum_home_away(df_matches, home_col, away_col):
    home = df_matches.groupby("HomeTeam")[home_col].sum()
    away = df_matches.groupby("AwayTeam")[away_col].sum()
    return home.add(away, fill_value=0)


# ---- Wins / Losses / Draws + overall win rate ----
base_stats = pd.DataFrame(0, index=teams, columns=["Wins", "Losses", "Draws"])

for _, row in df.iterrows():
    home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]
    if result == "H":
        base_stats.loc[home, "Wins"] += 1
        base_stats.loc[away, "Losses"] += 1
    elif result == "A":
        base_stats.loc[away, "Wins"] += 1
        base_stats.loc[home, "Losses"] += 1
    elif result == "D":
        base_stats.loc[home, "Draws"] += 1
        base_stats.loc[away, "Draws"] += 1

features[["Wins", "Losses", "Draws"]] = base_stats
features["WinRate(%)"] = (
    features["Wins"] / features["TotalMatches"].replace(0, float("nan")) * 100
).round(2)


# ---- Home / away win rate ----
home_results = df.groupby("HomeTeam")["FTR"].value_counts().unstack(fill_value=0)
away_results = df.groupby("AwayTeam")["FTR"].value_counts().unstack(fill_value=0)

home_played = home_results.sum(axis=1)
away_played = away_results.sum(axis=1)
home_wins = home_results.get("H", pd.Series(0, index=home_results.index))
away_wins = away_results.get("A", pd.Series(0, index=away_results.index))

features["Home_Played"] = home_played.reindex(teams, fill_value=0).astype(int)
features["Home_Wins"] = home_wins.reindex(teams, fill_value=0).astype(int)
features["Home_WinRate(%)"] = (
    features["Home_Wins"] / features["Home_Played"].replace(0, float("nan")) * 100
).round(2)

features["Away_Played"] = away_played.reindex(teams, fill_value=0).astype(int)
features["Away_Wins"] = away_wins.reindex(teams, fill_value=0).astype(int)
features["Away_WinRate(%)"] = (
    features["Away_Wins"] / features["Away_Played"].replace(0, float("nan")) * 100
).round(2)


# ---- Goals per match (FTHG + FTAG) ----
goals_total = sum_home_away(df, "FTHG", "FTAG")
features["Total_Goals_Scored"] = goals_total.reindex(teams).astype(int)
features["Avg_Goals_per_Match"] = (
    features["Total_Goals_Scored"] / features["TotalMatches"]
).round(3)


# ---- Shots per match (HS + AS) ----
shots_total = sum_home_away(df, "HS", "AS")
features["Total_Shots"] = shots_total.reindex(teams).astype(int)
features["Avg_Shots_per_Match"] = (
    features["Total_Shots"] / features["TotalMatches"]
).round(3)


# ---- Shots on target per match (HST + AST) ----
sot_total = sum_home_away(df, "HST", "AST")
features["Total_Shots_on_Target"] = sot_total.reindex(teams).astype(int)
features["Avg_SOT_per_Match"] = (
    features["Total_Shots_on_Target"] / features["TotalMatches"]
).round(3)


# ---- Fouls per match (HF + AF) ----
fouls_total = sum_home_away(df, "HF", "AF")
features["Total_Fouls"] = fouls_total.reindex(teams).astype(int)
features["Avg_Fouls_per_Match"] = (
    features["Total_Fouls"] / features["TotalMatches"]
).round(3)


# ---- Yellow cards per match (HY + AY) ----
yc_total = sum_home_away(df, "HY", "AY")
features["Total_Yellow_Cards"] = yc_total.reindex(teams).astype(int)
features["Avg_YC_per_Match"] = (
    features["Total_Yellow_Cards"] / features["TotalMatches"]
).round(3)


# ---- Red cards per match (HR + AR) ----
rc_total = sum_home_away(df, "HR", "AR")
features["Total_Red_Cards"] = rc_total.reindex(teams).astype(int)
features["Avg_RC_per_Match"] = (
    features["Total_Red_Cards"] / features["TotalMatches"]
).round(4)


# ---- Corners per match (HC + AC) ----
corner_total = sum_home_away(df, "HC", "AC")
features["Total_Corners"] = corner_total.reindex(teams).astype(int)
features["Avg_Corners_per_Match"] = (
    features["Total_Corners"] / features["TotalMatches"]
).round(3)


# ---- Recent-period win rate (2021-08-13 ~ 2024-05-19) ----
start_recent, end_recent = pd.Timestamp("2021-08-13"), pd.Timestamp("2024-05-19")
df_recent = df[(df["Date"] >= start_recent) & (df["Date"] <= end_recent)]

recent_stats = pd.DataFrame(
    0, index=teams, columns=["Recent_Wins", "Recent_Losses", "Recent_Draws"]
)
recent_matches = pd.Series(0, index=teams, dtype="int64")

for _, row in df_recent.iterrows():
    home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]
    recent_matches[home] += 1
    recent_matches[away] += 1
    if result == "H":
        recent_stats.loc[home, "Recent_Wins"] += 1
        recent_stats.loc[away, "Recent_Losses"] += 1
    elif result == "A":
        recent_stats.loc[away, "Recent_Wins"] += 1
        recent_stats.loc[home, "Recent_Losses"] += 1
    elif result == "D":
        recent_stats.loc[home, "Recent_Draws"] += 1
        recent_stats.loc[away, "Recent_Draws"] += 1

features["Recent_Matches"] = recent_matches.reindex(teams).fillna(0).astype(int)
features["Recent_Wins"] = (
    recent_stats["Recent_Wins"].reindex(teams).fillna(0).astype(int)
)
recent_ratio = features["Recent_Wins"] / features["Recent_Matches"].replace(
    0, float("nan")
)
features["Recent_WinRate(%)"] = (recent_ratio * 100).round(2)


# ---- Sort & print ----
features = features.sort_values("WinRate(%)", ascending=False)
pd.set_option("display.max_rows", None)
print("\n================= Team Feature Table =================\n")
print(features)


# ---- Export to CSV ----
os.makedirs("output", exist_ok=True)
output_path = "output/epl-output.csv"
features.to_csv(output_path, index_label="Team", encoding="utf-8-sig")

print(f"\nCSV successfully exported to: {output_path}")


# -*- coding: utf-8 -*-
"""
功能：汇总每支球队的各项“系数/特征”并导出 Excel
包含：
- 总胜率、主客场胜率
- 场均进球、射门、射正
- 场均犯规、黄牌、红牌、角球
- 最近区间（2021-08-13 ~ 2024-05-19）的胜率
作者：ChatGPT 助手
"""

import pandas as pd

# 1️⃣ 读取数据（修改为你自己的路径）
df = pd.read_csv(r"C:/Users/kevin/Desktop/epl-training.csv")

# 确保日期格式正确
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# 2️⃣ 统计总场次（主场 + 客场）
home_games = df["HomeTeam"].value_counts()
away_games = df["AwayTeam"].value_counts()
total_matches = home_games.add(away_games, fill_value=0).astype(int)

teams = sorted(total_matches.index)
features = pd.DataFrame(index=teams)
features["TotalMatches"] = total_matches.reindex(teams).astype(int)

# 🔧 辅助函数：计算主客场合计
def sum_home_away(df_matches, home_col, away_col):
    home = df_matches.groupby("HomeTeam")[home_col].sum()
    away = df_matches.groupby("AwayTeam")[away_col].sum()
    return home.add(away, fill_value=0)

# 3️⃣ 胜 / 负 / 平 + 胜率
base_stats = pd.DataFrame(0, index=teams, columns=["Wins", "Losses", "Draws"])
for _, row in df.iterrows():
    home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]
    if result == "H":
        base_stats.loc[home, "Wins"] += 1
        base_stats.loc[away, "Losses"] += 1
    elif result == "A":
        base_stats.loc[away, "Wins"] += 1
        base_stats.loc[home, "Losses"] += 1
    elif result == "D":
        base_stats.loc[home, "Draws"] += 1
        base_stats.loc[away, "Draws"] += 1

features[["Wins", "Losses", "Draws"]] = base_stats
features["WinRate(%)"] = (
    features["Wins"] / features["TotalMatches"].replace(0, float("nan")) * 100
).round(2)

# 4️⃣ 主场 / 客场胜率
home_results = df.groupby("HomeTeam")["FTR"].value_counts().unstack(fill_value=0)
away_results = df.groupby("AwayTeam")["FTR"].value_counts().unstack(fill_value=0)

home_played = home_results.sum(axis=1)
away_played = away_results.sum(axis=1)
home_wins = home_results.get("H", pd.Series(0, index=home_results.index))
away_wins = away_results.get("A", pd.Series(0, index=away_results.index))

features["Home_Played"] = home_played.reindex(teams, fill_value=0).astype(int)
features["Home_Wins"] = home_wins.reindex(teams, fill_value=0).astype(int)
features["Home_WinRate(%)"] = (
    features["Home_Wins"] / features["Home_Played"].replace(0, float("nan")) * 100
).round(2)

features["Away_Played"] = away_played.reindex(teams, fill_value=0).astype(int)
features["Away_Wins"] = away_wins.reindex(teams, fill_value=0).astype(int)
features["Away_WinRate(%)"] = (
    features["Away_Wins"] / features["Away_Played"].replace(0, float("nan")) * 100
).round(2)

# 5️⃣ 场均进球（FTHG + FTAG）
goals_total = sum_home_away(df, "FTHG", "FTAG")
features["Total_Goals_Scored"] = goals_total.reindex(teams).astype(int)
features["Avg_Goals_per_Match"] = (
    features["Total_Goals_Scored"] / features["TotalMatches"]
).round(3)

# 6️⃣ 场均射门（HS + AS）
shots_total = sum_home_away(df, "HS", "AS")
features["Total_Shots"] = shots_total.reindex(teams).astype(int)
features["Avg_Shots_per_Match"] = (
    features["Total_Shots"] / features["TotalMatches"]
).round(3)

# 7️⃣ 场均射正（HST + AST）
sot_total = sum_home_away(df, "HST", "AST")
features["Total_Shots_on_Target"] = sot_total.reindex(teams).astype(int)
features["Avg_SOT_per_Match"] = (
    features["Total_Shots_on_Target"] / features["TotalMatches"]
).round(3)

# 8️⃣ 场均犯规（HF + AF）
fouls_total = sum_home_away(df, "HF", "AF")
features["Total_Fouls"] = fouls_total.reindex(teams).astype(int)
features["Avg_Fouls_per_Match"] = (
    features["Total_Fouls"] / features["TotalMatches"]
).round(3)

# 9️⃣ 场均黄牌（HY + AY）
yc_total = sum_home_away(df, "HY", "AY")
features["Total_Yellow_Cards"] = yc_total.reindex(teams).astype(int)
features["Avg_YC_per_Match"] = (
    features["Total_Yellow_Cards"] / features["TotalMatches"]
).round(3)

# 🔟 场均红牌（HR + AR）
rc_total = sum_home_away(df, "HR", "AR")
features["Total_Red_Cards"] = rc_total.reindex(teams).astype(int)
features["Avg_RC_per_Match"] = (
    features["Total_Red_Cards"] / features["TotalMatches"]
).round(4)

# 1️⃣1️⃣ 场均角球（HC + AC）
corner_total = sum_home_away(df, "HC", "AC")
features["Total_Corners"] = corner_total.reindex(teams).astype(int)
features["Avg_Corners_per_Match"] = (
    features["Total_Corners"] / features["TotalMatches"]
).round(3)

# 1️⃣2️⃣ 最近区间胜率（2021-08-13 ~ 2024-05-19）
start_recent, end_recent = pd.Timestamp("2021-08-13"), pd.Timestamp("2024-05-19")
df_recent = df[(df["Date"] >= start_recent) & (df["Date"] <= end_recent)]

recent_stats = pd.DataFrame(0, index=teams, columns=["Recent_Wins", "Recent_Losses", "Recent_Draws"])
recent_matches = pd.Series(0, index=teams, dtype="int64")

for _, row in df_recent.iterrows():
    home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]
    recent_matches[home] += 1
    recent_matches[away] += 1
    if result == "H":
        recent_stats.loc[home, "Recent_Wins"] += 1
        recent_stats.loc[away, "Recent_Losses"] += 1
    elif result == "A":
        recent_stats.loc[away, "Recent_Wins"] += 1
        recent_stats.loc[home, "Recent_Losses"] += 1
    elif result == "D":
        recent_stats.loc[home, "Recent_Draws"] += 1
        recent_stats.loc[away, "Recent_Draws"] += 1

features["Recent_Matches"] = recent_matches.reindex(teams).fillna(0).astype(int)
features["Recent_Wins"] = recent_stats["Recent_Wins"].reindex(teams).fillna(0).astype(int)
recent_ratio = features["Recent_Wins"] / features["Recent_Matches"].replace(0, float("nan"))
features["Recent_WinRate(%)"] = (recent_ratio * 100).round(2)

# 1️⃣3️⃣ 排序并打印
features = features.sort_values("WinRate(%)", ascending=False)
pd.set_option("display.max_rows", None)
print("\n================= 📊 各球队综合系数表（features） =================\n")
print(features)

# ✅ 导出为 Excel
output_path = r"C:\Users\kevin\Desktop\team_features.xlsx"
features.to_excel(output_path, index_label="Team")
print(f"\n✅ 已成功导出到: {output_path}")

