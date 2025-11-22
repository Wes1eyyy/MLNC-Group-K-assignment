# -*- coding: utf-8 -*-

import pandas as pd
import os

# Load data (relative path)
df = pd.read_csv("../data/raw/epl-training.csv")

# -------- Home statistics --------
home_stats = df.groupby("HomeTeam")["FTR"].value_counts().unstack(fill_value=0)
home_played = home_stats.sum(axis=1)
home_wins = home_stats.get("H", pd.Series(0, index=home_stats.index))
home_win_rate_percent = ((home_wins / home_played) * 100).round(2)

# -------- Away statistics --------
away_stats = df.groupby("AwayTeam")["FTR"].value_counts().unstack(fill_value=0)
away_played = away_stats.sum(axis=1)
away_wins = away_stats.get("A", pd.Series(0, index=away_stats.index))
away_win_rate_percent = ((away_wins / away_played) * 100).round(2)

# -------- Combine into a single table --------
win_rate_table = pd.DataFrame({
    "Home_Played": home_played,
    "Home_Wins": home_wins,
    "Home_WinRate(%)": home_win_rate_percent,
    "Away_Played": away_played,
    "Away_Wins": away_wins,
    "Away_WinRate(%)": away_win_rate_percent
}).sort_index()

# -------- Save output CSV --------
os.makedirs("output", exist_ok=True)
output_path = "output/win_rate_table.csv"
win_rate_table.to_csv(output_path, encoding="utf-8-sig")


print("\n================= Home & Away Win Rate Table =================\n")
print(win_rate_table)
print(f"\nCSV file saved to: {output_path}")
