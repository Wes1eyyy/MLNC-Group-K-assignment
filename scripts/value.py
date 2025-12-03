"""
Script to scrape Premier League team player values from Transfermarkt for multiple years
This script fetches total market value and average market value for each Premier League team
from 2000 to 2025
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
from datetime import datetime

# Headers to avoid being blocked by the website
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Base URL for Transfermarkt
BASE_URL = "https://www.transfermarkt.com"

# Years to scrape (2000-2025)
YEARS_TO_SCRAPE = list(range(2000, 2026))

# Premier League teams that were in the league during 2000-2025
# Note: Some teams may not have been in Premier League for all years
PREMIER_LEAGUE_TEAMS = {
    'Arsenal': '/arsenal-fc/startseite/verein/11',
    'Aston Villa': '/aston-villa/startseite/verein/405',
    'Bournemouth': '/afc-bournemouth/startseite/verein/989',
    'Brentford': '/brentford-fc/startseite/verein/1148',
    'Brighton': '/brighton-amp-hove-albion/startseite/verein/1237',
    'Burnley': '/fc-burnley/startseite/verein/1132',
    'Chelsea': '/fc-chelsea/startseite/verein/631',
    'Crystal Palace': '/crystal-palace/startseite/verein/873',
    'Everton': '/fc-everton/startseite/verein/29',
    'Fulham': '/fc-fulham/startseite/verein/931',
    'Liverpool': '/fc-liverpool/startseite/verein/31',
    'Leeds United': '/leeds-united/startseite/verein/399',
    'Leicester City': '/leicester-city/startseite/verein/1003',
    'Luton Town': '/luton-town-fc/startseite/verein/1031',
    'Manchester City': '/manchester-city/startseite/verein/281',
    'Manchester United': '/manchester-united/startseite/verein/985',
    'Newcastle': '/newcastle-united/startseite/verein/762',
    'Norwich City': '/norwich-city/startseite/verein/1123',
    'Nottingham Forest': '/nottingham-forest/startseite/verein/703',
    'Sheffield United': '/sheffield-united/startseite/verein/350',
    'Southampton': '/fc-southampton/startseite/verein/180',
    'Tottenham': '/tottenham-hotspur/startseite/verein/148',
    'Watford': '/fc-watford/startseite/verein/1010',
    'West Bromwich': '/west-bromwich-albion/startseite/verein/984',
    'West Ham': '/west-ham-united/startseite/verein/379',
    'Wolverhampton': '/wolverhampton-wanderers/startseite/verein/543'
}

def get_team_squad_url(team_url, year=None):
    """Convert team home URL to squad URL with optional year parameter"""
    if year and year < 2025:
        # For historical data, add year parameter
        return team_url.replace('/startseite/', f'/kader/verein/{team_url.split("/")[-1]}/saison_id/{year}')
    else:
        # For current season, use standard kader URL
        return team_url.replace('/startseite/', '/kader/')

def parse_market_value(value_str):
    """Parse market value string and convert to millions of euros"""
    if not value_str or value_str == '-':
        return 0
    
    # Remove currency symbols and spaces
    value_str = value_str.replace('€', '').replace('$', '').replace('£', '').strip()
    
    # Handle different value formats
    if 'm' in value_str.lower():
        # Already in millions
        return float(re.sub(r'[^\d.]', '', value_str))
    elif 'k' in value_str.lower():
        # In thousands, convert to millions
        return float(re.sub(r'[^\d.]', '', value_str)) / 1000
    else:
        # Assume it's a raw number in millions
        try:
            return float(re.sub(r'[^\d.]', '', value_str))
        except:
            return 0

def scrape_team_player_values(team_name, team_url, year=None):
    """Scrape player market values for a specific team and year"""
    year_str = f" ({year})" if year else ""
    print(f"Scraping player values for {team_name}{year_str}...")
    
    if year and year < 2025:
        # For historical data, construct URL with year parameter
        # Extract team slug and ID from URL  
        parts = team_url.strip('/').split('/')
        team_slug = parts[0]  # e.g., 'arsenal-fc'
        team_id = parts[-1]   # e.g., '11'
        squad_url = f"{BASE_URL}/{team_slug}/kader/verein/{team_id}/saison_id/{year}"
    else:
        # For current season
        squad_url = BASE_URL + get_team_squad_url(team_url)
    
    try:
        response = requests.get(squad_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        player_values = []
        
        # Find the squad table
        squad_table = soup.find('table', {'class': 'items'})
        if not squad_table:
            print(f"Could not find squad table for {team_name}{year_str}")
            return []
        
        # Find all player rows
        player_rows = squad_table.find('tbody').find_all('tr')
        
        for row in player_rows:
            # Skip header rows and empty rows
            if 'thead' in str(row) or not row.find('td'):
                continue
            
            # Extract player name
            name_cell = row.find('td', {'class': 'hauptlink'})
            if name_cell:
                name_link = name_cell.find('a')
                player_name = name_link.text.strip() if name_link else 'Unknown'
            else:
                continue
            
            # Extract market value
            value_cell = row.find('td', {'class': 'rechts hauptlink'})
            if value_cell:
                value_text = value_cell.text.strip()
                market_value = parse_market_value(value_text)
                player_values.append({
                    'player_name': player_name,
                    'market_value_millions': market_value
                })
        
        return player_values
        
    except Exception as e:
        print(f"Error scraping {team_name}{year_str}: {str(e)}")
        return []

def calculate_team_statistics(player_values):
    """Calculate total and average market value for a team"""
    if not player_values:
        return 0, 0, 0
    
    values = [player['market_value_millions'] for player in player_values]
    total_value = sum(values)
    average_value = total_value / len(values) if values else 0
    player_count = len(values)
    
    return total_value, average_value, player_count

def main():
    """Main function to scrape all Premier League teams' player values across multiple years"""
    print("Starting Premier League player value scraping for 2000-2025...")
    
    all_data = []
    
    for year in YEARS_TO_SCRAPE:
        print(f"\n{'='*50}")
        print(f"SCRAPING DATA FOR YEAR: {year}")
        print(f"{'='*50}")
        
        for team_name, team_url in PREMIER_LEAGUE_TEAMS.items():
            # Get player values for this team and year
            player_values = scrape_team_player_values(team_name, team_url, year)
            
            # Calculate team statistics
            total_value, avg_value, player_count = calculate_team_statistics(player_values)
            
            team_data = {
                'year': year,
                'team_name': team_name,
                'total_market_value_millions': round(total_value, 2),
                'average_market_value_millions': round(avg_value, 2),
                'number_of_players': player_count
            }
            
            all_data.append(team_data)
            
            print(f"{team_name} ({year}): Total = €{total_value:.2f}M, Average = €{avg_value:.2f}M, Players = {player_count}")
            
            # Add delay to be respectful to the website
            time.sleep(3)  # Increased delay for multi-year scraping
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_data)
    
    # Create output directory if it doesn't exist
    import os
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save comprehensive multi-year data
    output_file = os.path.join(output_dir, 'premier_league_team_values_2000_2025.csv')
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\nMulti-year data saved to {output_file}")
    
    # Create summary by year
    year_summary = df.groupby('year').agg({
        'total_market_value_millions': 'sum',
        'average_market_value_millions': 'mean',
        'number_of_players': 'sum'
    }).round(2)
    
    print(f"\nSummary by year:")
    print(year_summary)
    
    # Save year summary
    summary_file = os.path.join(output_dir, 'premier_league_values_yearly_summary.csv')
    year_summary.to_csv(summary_file, encoding='utf-8')
    print(f"Yearly summary saved to {summary_file}")

if __name__ == "__main__":
    main()
