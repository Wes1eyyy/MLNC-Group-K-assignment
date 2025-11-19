from utils.data_utils import load_data, add_team_records_to_data, save_data

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

# Save enriched data
print("\nSaving enriched data...")
save_data(enriched_data, "../data/epl-features-training.csv")
