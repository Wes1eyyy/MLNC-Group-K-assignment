"""
Script to scrape Premier League team player ages from Transfermarkt for multiple years
This script fetches total age and average age for each Premier League team
from 2000 to 2025
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
from urllib.parse import urljoin

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

def parse_birth_date(date_str, reference_year=None):
    """Parse birth date string and calculate age for a specific year"""
    if not date_str or date_str == '-':
        return None
    
    if not reference_year:
        reference_year = datetime.now().year
    
    try:
        # Common date formats on Transfermarkt
        date_formats = ['%b %d, %Y', '%d.%m.%Y', '%Y-%m-%d', '%m/%d/%Y']
        
        birth_date = None
        for fmt in date_formats:
            try:
                birth_date = datetime.strptime(date_str.strip(), fmt)
                break
            except ValueError:
                continue
        
        if birth_date:
            # Calculate age as of the reference year
            age = reference_year - birth_date.year
            # For historical data, we use the year-end age
            return age
        else:
            # Try to extract just the year if full date parsing fails
            year_match = re.search(r'(\d{4})', date_str)
            if year_match:
                birth_year = int(year_match.group(1))
                return reference_year - birth_year
            
    except Exception as e:
        print(f"Error parsing date '{date_str}': {str(e)}")
    
    return None

def parse_age_directly(age_str):
    """Parse age if it's directly provided as a number"""
    if not age_str or age_str == '-':
        return None
    
    try:
        # Extract numbers from the age string
        age_match = re.search(r'(\d+)', age_str.strip())
        if age_match:
            return int(age_match.group(1))
    except:
        pass
    
    return None

def scrape_team_player_ages(team_name, team_url, year=None):
    """Scrape player ages for a specific team and year"""
    year_str = f" ({year})" if year else ""
    print(f"Scraping player ages for {team_name}{year_str}...")
    
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
        
        player_ages = []
        
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
            
            # Extract age or birth date
            age = None
            
            # Look for age column (usually has class 'zentriert' and contains age)
            age_cells = row.find_all('td', {'class': 'zentriert'})
            for cell in age_cells:
                cell_text = cell.text.strip()
                
                # Try to parse as direct age first
                age = parse_age_directly(cell_text)
                if age:
                    break
                
                # Try to parse as birth date
                age = parse_birth_date(cell_text, year)
                if age:
                    break
            
            if age and 16 <= age <= 45:  # Reasonable age range for professional footballers
                player_ages.append({
                    'player_name': player_name,
                    'age': age
                })
        
        return player_ages
        
    except Exception as e:
        print(f"Error scraping {team_name}{year_str}: {str(e)}")
        return []

def calculate_age_statistics(player_ages):
    """Calculate total and average age for a team"""
    if not player_ages:
        return 0, 0, 0
    
    ages = [player['age'] for player in player_ages]
    total_age = sum(ages)
    average_age = total_age / len(ages) if ages else 0
    player_count = len(ages)
    
    return total_age, average_age, player_count

def main():
    """Main function to scrape all Premier League teams' player ages across multiple years"""
    print("Starting Premier League player age scraping for 2000-2025...")
    
    all_data = []
    
    for year in YEARS_TO_SCRAPE:
        print(f"\n{'='*50}")
        print(f"SCRAPING DATA FOR YEAR: {year}")
        print(f"{'='*50}")
        
        for team_name, team_url in PREMIER_LEAGUE_TEAMS.items():
            # Get player ages for this team and year
            player_ages = scrape_team_player_ages(team_name, team_url, year)
            
            # Calculate team statistics
            total_age, avg_age, player_count = calculate_age_statistics(player_ages)
            
            team_data = {
                'year': year,
                'team_name': team_name,
                'total_age_years': total_age,
                'average_age_years': round(avg_age, 2),
                'number_of_players': player_count
            }
            
            all_data.append(team_data)
            
            print(f"{team_name} ({year}): Total Age = {total_age} years, Average Age = {avg_age:.2f} years, Players = {player_count}")
            
            # Add delay to be respectful to the website
            time.sleep(3)  # Increased delay for multi-year scraping
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_data)
    
    # Create output directory if it doesn't exist
    import os
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save comprehensive multi-year data
    output_file = os.path.join(output_dir, 'premier_league_team_ages_2000_2025.csv')
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\nMulti-year data saved to {output_file}")
    
    # Create summary by year
    year_summary = df.groupby('year').agg({
        'total_age_years': 'sum',
        'average_age_years': 'mean',
        'number_of_players': 'sum'
    }).round(2)
    
    print(f"\nSummary by year:")
    print(year_summary)
    
    # Save year summary
    summary_file = os.path.join(output_dir, 'premier_league_ages_yearly_summary.csv')
    year_summary.to_csv(summary_file, encoding='utf-8')
    print(f"Yearly summary saved to {summary_file}")

if __name__ == "__main__":
    main()