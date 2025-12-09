"""
Script to merge the latest EPL data (2025 May-Nov) into the training dataset
This script combines epl-training.csv with epl-latest-2025.csv
"""

import pandas as pd
import os

def merge_datasets():
    """
    Merge the latest EPL data with the existing training data
    """
    # Define file paths
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    training_file = os.path.join(data_dir, 'epl-training.csv')
    latest_file = os.path.join(data_dir, 'epl-latest-2025.csv')
    backup_file = os.path.join(data_dir, 'epl-training-backup.csv')
    
    print("="*70)
    print("Merging Latest EPL Data into Training Dataset")
    print("="*70)
    
    # Check if files exist
    if not os.path.exists(training_file):
        print(f"Error: Training file not found: {training_file}")
        return
    
    if not os.path.exists(latest_file):
        print(f"Error: Latest data file not found: {latest_file}")
        print("Please run fetch_latest_epl.py first to download the data.")
        return
    
    # Create backup of original training file
    print(f"\n1. Creating backup of original training file...")
    df_old = pd.read_csv(training_file)
    df_old.to_csv(backup_file, index=False)
    print(f"   Backup saved to: {backup_file}")
    print(f"   Original dataset: {len(df_old)} matches")
    
    # Load latest data
    print(f"\n2. Loading latest data...")
    df_new = pd.read_csv(latest_file)
    print(f"   Latest dataset: {len(df_new)} matches")
    
    # Display date ranges
    print(f"\n3. Date ranges:")
    print(f"   Original data: {df_old['Date'].min()} to {df_old['Date'].max()}")
    print(f"   New data: {df_new['Date'].min()} to {df_new['Date'].max()}")
    
    # Check for duplicates based on Date and teams
    print(f"\n4. Checking for duplicate matches...")
    df_old['match_key'] = df_old['Date'] + '_' + df_old['HomeTeam'] + '_' + df_old['AwayTeam']
    df_new['match_key'] = df_new['Date'] + '_' + df_new['HomeTeam'] + '_' + df_new['AwayTeam']
    
    duplicates = df_new[df_new['match_key'].isin(df_old['match_key'])]
    if len(duplicates) > 0:
        print(f"   Warning: Found {len(duplicates)} duplicate matches that already exist in training data")
        print(f"   These will be skipped to avoid duplication.")
        # Remove duplicates from new data
        df_new = df_new[~df_new['match_key'].isin(df_old['match_key'])]
        print(f"   After removing duplicates: {len(df_new)} new matches to add")
    else:
        print(f"   No duplicates found. All {len(df_new)} matches are new.")
    
    # Remove temporary match_key column
    df_old = df_old.drop('match_key', axis=1)
    df_new = df_new.drop('match_key', axis=1)
    
    # Merge datasets
    print(f"\n5. Merging datasets...")
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    print(f"   Combined dataset: {len(df_combined)} matches")
    
    # Sort by date
    print(f"\n6. Sorting by date...")
    try:
        # Try multiple date formats
        date_formats = ['%d/%m/%Y', '%d/%m/%y']
        for fmt in date_formats:
            try:
                df_combined['Date_temp'] = pd.to_datetime(df_combined['Date'], format=fmt)
                break
            except:
                continue
        
        if 'Date_temp' in df_combined.columns:
            df_combined = df_combined.sort_values('Date_temp')
            df_combined = df_combined.drop('Date_temp', axis=1)
            print(f"   Successfully sorted by date")
        else:
            print(f"   Warning: Could not parse dates for sorting")
    except Exception as e:
        print(f"   Warning: Error during sorting: {e}")
    
    # Save merged dataset
    print(f"\n7. Saving merged dataset...")
    df_combined.to_csv(training_file, index=False)
    print(f"   Saved to: {training_file}")
    
    # Display summary
    print("\n" + "="*70)
    print("MERGE SUMMARY")
    print("="*70)
    print(f"Original matches:     {len(df_old)}")
    print(f"New matches added:    {len(df_new)}")
    print(f"Total matches:        {len(df_combined)}")
    print(f"Date range:           {df_combined['Date'].min()} to {df_combined['Date'].max()}")
    print(f"\nBackup file:          {backup_file}")
    print("="*70)
    
    # Show sample of new data
    if len(df_new) > 0:
        print("\nSample of newly added matches:")
        print(df_new[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].head(10).to_string(index=False))
    
    print("\n✓ Merge completed successfully!")
    print("\nThe training dataset has been updated with the latest matches.")
    print("You can now use the updated dataset for model training.")

if __name__ == "__main__":
    merge_datasets()
