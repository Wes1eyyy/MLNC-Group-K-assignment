"""
Script to scrape latest Premier League match data (May 2025 - November 2025)
This script fetches match statistics from football-data.co.uk to extend the training dataset
"""

import requests
import pandas as pd
import time
from datetime import datetime
import os
import io

# Headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Football-data.co.uk base URL for Premier League data
# They provide CSV files with historical match data
FOOTBALL_DATA_URL = "https://www.football-data.co.uk/mmz4281/{season}/E0.csv"

def get_season_string(year):
    """
    Convert year to season string format (e.g., 2425 for 2024-2025 season)
    Premier League season runs from August to May
    """
    # 2025年5月属于2024-2025赛季
    # 2025年8月开始是2025-2026赛季
    if year == 2025:
        return "2425"  # 2024-2025 season
    elif year == 2026:
        return "2526"  # 2025-2026 season (for Aug-Nov 2025)
    return f"{str(year)[-2:]}{str(year+1)[-2:]}"

def fetch_season_data(season_string):
    """
    Fetch Premier League data for a specific season from football-data.co.uk
    """
    url = FOOTBALL_DATA_URL.format(season=season_string)
    print(f"Fetching data from: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Read CSV data
        df = pd.read_csv(io.StringIO(response.text))
        print(f"Successfully fetched {len(df)} matches for season {season_string}")
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for season {season_string}: {str(e)}")
        return None

def filter_date_range(df, start_date, end_date):
    """
    Filter dataframe to only include matches between start_date and end_date
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Convert date column to datetime
    # Try different date formats
    date_formats = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d']
    
    for fmt in date_formats:
        try:
            df['Date_parsed'] = pd.to_datetime(df['Date'], format=fmt)
            break
        except:
            continue
    
    if 'Date_parsed' not in df.columns:
        print("Warning: Could not parse dates, returning all data")
        return df
    
    # Filter by date range
    mask = (df['Date_parsed'] >= start_date) & (df['Date_parsed'] <= end_date)
    filtered_df = df[mask].copy()
    
    # Drop the temporary date column
    filtered_df = filtered_df.drop('Date_parsed', axis=1)
    
    print(f"Filtered to {len(filtered_df)} matches between {start_date} and {end_date}")
    
    return filtered_df

def standardize_column_names(df):
    """
    Ensure column names match the format in epl-training.csv
    Required columns: Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,Referee,HS,AS,HST,AST,HC,AC,HF,AF,HY,AY,HR,AR
    """
    required_columns = [
        'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 
        'HTHG', 'HTAG', 'HTR', 'Referee', 'HS', 'AS', 'HST', 'AST', 
        'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR'
    ]
    
    # Check which columns exist
    existing_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns: {missing_columns}")
        # Add missing columns with default values
        for col in missing_columns:
            df[col] = ''
    
    # Select only required columns in the correct order
    df_standardized = df[required_columns].copy()
    
    return df_standardized

def standardize_team_names(df):
    """
    Standardize team names to match the format in epl-training.csv
    """
    # Team name mapping from football-data.co.uk format to training data format
    team_name_mapping = {
        'Man United': 'Man United',
        'Manchester United': 'Man United',
        'Man City': 'Man City',
        'Manchester City': 'Man City',
        'Tottenham': 'Tottenham',
        'Spurs': 'Tottenham',
        'Newcastle': 'Newcastle',
        'Newcastle United': 'Newcastle',
        'West Ham': 'West Ham',
        'West Ham United': 'West Ham',
        'Wolves': 'Wolves',
        'Wolverhampton': 'Wolves',
        'Nott\'m Forest': 'Nott\'m Forest',
        'Nottingham Forest': 'Nott\'m Forest',
        'Nottingham': 'Nott\'m Forest',
        'Leicester': 'Leicester',
        'Leicester City': 'Leicester',
        'Brighton': 'Brighton',
        'Brighton & Hove Albion': 'Brighton',
        'Brighton and Hove Albion': 'Brighton',
    }
    
    # Replace team names
    for col in ['HomeTeam', 'AwayTeam']:
        if col in df.columns:
            df[col] = df[col].replace(team_name_mapping)
    
    return df

def main():
    """
    Main function to fetch and process latest EPL match data
    """
    print("Starting Premier League match data scraping (May 2025 - November 2025)...")
    print("="*70)
    
    # Define date ranges to fetch
    # May 2025 - end of 2024-2025 season
    may_2025_start = datetime(2025, 5, 26)  # Start after last date in training data (25/05/2025)
    may_2025_end = datetime(2025, 5, 31)
    
    # August 2025 - November 2025 (2025-2026 season)
    aug_nov_2025_start = datetime(2025, 8, 1)
    aug_nov_2025_end = datetime(2025, 11, 30)
    
    all_matches = []
    
    # Fetch 2024-2025 season data (for remaining May 2025 matches)
    print("\n--- Fetching 2024-2025 season data (for May 2025) ---")
    df_2425 = fetch_season_data("2425")
    if df_2425 is not None:
        df_may = filter_date_range(df_2425, may_2025_start, may_2025_end)
        if not df_may.empty:
            all_matches.append(df_may)
    
    time.sleep(2)  # Be respectful to the server
    
    # Fetch 2025-2026 season data (for Aug-Nov 2025)
    print("\n--- Fetching 2025-2026 season data (for Aug-Nov 2025) ---")
    df_2526 = fetch_season_data("2526")
    if df_2526 is not None:
        df_aug_nov = filter_date_range(df_2526, aug_nov_2025_start, aug_nov_2025_end)
        if not df_aug_nov.empty:
            all_matches.append(df_aug_nov)
    
    # Combine all data
    if all_matches:
        combined_df = pd.concat(all_matches, ignore_index=True)
        print(f"\n{'='*70}")
        print(f"Total matches fetched: {len(combined_df)}")
        
        # Standardize team names and column names
        combined_df = standardize_team_names(combined_df)
        combined_df = standardize_column_names(combined_df)
        
        # Sort by date
        try:
            combined_df['Date_temp'] = pd.to_datetime(combined_df['Date'], format='%d/%m/%Y', errors='coerce')
            combined_df = combined_df.sort_values('Date_temp')
            combined_df = combined_df.drop('Date_temp', axis=1)
        except:
            pass
        
        # Save to CSV
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'epl-latest-2025.csv')
        combined_df.to_csv(output_file, index=False)
        
        print(f"\nData saved to: {output_file}")
        print("\nSample of fetched data:")
        print(combined_df.head(10))
        
        # Display date range
        if not combined_df.empty:
            print(f"\nDate range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
        
        # Instructions for merging
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("1. Review the fetched data in 'data/epl-latest-2025.csv'")
        print("2. If data looks correct, append it to 'data/epl-training.csv'")
        print("3. You can use the following command to merge:")
        print(f"   cat {output_file} >> data/epl-training.csv")
        print("\nAlternatively, you can use pandas to merge in Python:")
        print("   df_old = pd.read_csv('data/epl-training.csv')")
        print("   df_new = pd.read_csv('data/epl-latest-2025.csv')")
        print("   df_combined = pd.concat([df_old, df_new], ignore_index=True)")
        print("   df_combined.to_csv('data/epl-training.csv', index=False)")
        
    else:
        print("\n⚠ No data was fetched. This could mean:")
        print("  1. The season data is not yet available on football-data.co.uk")
        print("  2. There were no matches in the specified date range")
        print("  3. The website structure has changed")
        print("\nYou may need to:")
        print("  - Wait for the data to be published")
        print("  - Check alternative data sources")
        print("  - Manually scrape from the Premier League website")

if __name__ == "__main__":
    main()
