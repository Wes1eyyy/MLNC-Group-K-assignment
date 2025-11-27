# Premier League Team Statistics Scraping Scripts

This directory contains scripts to scrape Premier League team statistics from Transfermarkt.

## Scripts Overview

### 1. `value.py` - Player Market Value Scraper
- Scrapes total and average market values for all Premier League teams
- Outputs data to `../data/premier_league_team_values.csv`
- Includes team name, total market value, average market value, and player count

### 2. `age.py` - Player Age Scraper  
- Scrapes total and average ages for all Premier League teams
- Outputs data to `../data/premier_league_team_ages.csv`
- Includes team name, total age, average age, and player count

### 3. `test_scraping.py` - Test Script
- Tests the parsing functions to ensure they work correctly
- Run this first to verify everything is set up properly

## Requirements

Install the required packages:
```bash
pip install beautifulsoup4 requests pandas lxml
```

## Usage

1. **Test the scripts first:**
   ```bash
   python test_scraping.py
   ```

2. **Scrape team market values:**
   ```bash
   python value.py
   ```
   
3. **Scrape team ages:**
   ```bash
   python age.py
   ```

## Output Files

- `../data/premier_league_team_values.csv` - Team market value statistics
- `../data/premier_league_team_ages.csv` - Team age statistics

## Features

- **Rate limiting**: 2-second delays between requests to be respectful to the website
- **Error handling**: Graceful handling of parsing errors and missing data
- **Data validation**: Reasonable ranges for ages and market values
- **Sorting**: Output sorted by total market value (values) and average age (ages)
- **English comments**: All code comments are in English

## Notes

- Scraping may take 5-10 minutes due to rate limiting
- The scripts target the 2023-24 Premier League season teams
- Market values are converted to millions of euros for consistency
- Age calculations handle various date formats from the website

## Data Columns

### Market Value CSV:
- `team_name`: Premier League team name
- `total_market_value_millions`: Total squad value in millions of euros
- `average_market_value_millions`: Average player value in millions of euros  
- `number_of_players`: Number of players in the squad

### Age CSV:
- `team_name`: Premier League team name
- `total_age_years`: Sum of all player ages
- `average_age_years`: Average age of squad players
- `number_of_players`: Number of players in the squad