from utils.data_utils import load_data, add_team_records_to_data

DATA_PATH = "../data/epl-training.csv"

# Load training data
print("Loading training data...")
training_data = load_data(DATA_PATH)
print(f"Loaded {len(training_data)} matches")

# Add team records to data
print("\nAdding team records to data...")
print("Warning: This may take a few minutes for the full dataset...")
enriched_data = add_team_records_to_data(training_data)
print("Done!")

# Display a sample
print("\n=== Sample enriched data (match 100) ===")
sample_match = enriched_data[100]
print(f"Date: {sample_match['Date']}")
print(f"Match: {sample_match['HomeTeam']} vs {sample_match['AwayTeam']}")
print(f"Result: {sample_match['FTR']} ({sample_match['FTHG']}-{sample_match['FTAG']})")
print(f"\nHome team ({sample_match['HomeTeam']}):")
print(f"  Season record: {sample_match['HomeTeam_Wins']}W-{sample_match['HomeTeam_Draws']}D-{sample_match['HomeTeam_Losses']}L")
print(f"  Home avg goals: {sample_match['HomeTeam_AvgGoalsScored']} scored / {sample_match['HomeTeam_AvgGoalsConceded']} conceded")
print(f"\nAway team ({sample_match['AwayTeam']}):")
print(f"  Season record: {sample_match['AwayTeam_Wins']}W-{sample_match['AwayTeam_Draws']}D-{sample_match['AwayTeam_Losses']}L")
print(f"  Away avg goals: {sample_match['AwayTeam_AvgGoalsScored']} scored / {sample_match['AwayTeam_AvgGoalsConceded']} conceded")

