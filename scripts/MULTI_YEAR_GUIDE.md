# Multi-Year Premier League Data Scraping Guide

## 🎯 Updated Features

Both `age.py` and `value.py` scripts have been updated to collect data from **2020-2025** (6 years) for all Premier League teams that participated during this period.

## 📁 Output Files

### Age Data:
- `premier_league_team_ages_2020_2025.csv` - Complete age data for all years
- `premier_league_ages_yearly_summary.csv` - Summary statistics by year

### Value Data:
- `premier_league_team_values_2020_2025.csv` - Complete value data for all years  
- `premier_league_values_yearly_summary.csv` - Summary statistics by year

## 📊 Data Structure

### Main CSV Files Format:
```csv
year,team_name,total_market_value_millions,average_market_value_millions,number_of_players
2020,Arsenal,450.5,22.53,20
2021,Arsenal,520.2,26.01,20
...
```

### Summary Files Format:
```csv
year,total_market_value_millions,average_market_value_millions,number_of_players
2020,8500.0,25.5,340
2021,9200.0,27.1,350
...
```

## 🚀 Usage

### Run Age Scraping:
```bash
cd scripts
python age.py
```

### Run Value Scraping:
```bash
cd scripts  
python value.py
```

### Test First (Recommended):
```bash
python test_multi_year.py
```

## ⏱️ Runtime Information

- **Per Script**: ~8 minutes (156 requests × 3 seconds delay)
- **Both Scripts**: ~16 minutes total
- **Teams Covered**: 26 teams (includes promoted/relegated teams)
- **Years Covered**: 2020, 2021, 2022, 2023, 2024, 2025

## 🔧 Key Updates

1. **Historical URLs**: Automatically constructs correct Transfermarkt URLs for past seasons
2. **Age Calculation**: Calculates player ages relative to each specific year
3. **Extended Team List**: Includes teams that were in Premier League during 2020-2025
4. **Year-based Grouping**: Provides both detailed and summary data by year
5. **Error Handling**: Graceful handling of missing data or page structure changes

## 📈 Teams Included

All teams that played in Premier League 2020-2025:
- Core teams (Arsenal, Chelsea, Liverpool, etc.)
- Promoted teams (Brentford, Luton Town, etc.)  
- Relegated teams (Norwich, Watford, etc.)

## ⚠️ Important Notes

- Scripts use 3-second delays to be respectful to Transfermarkt
- Some teams may have missing data for years they weren't in Premier League
- Historical data accuracy depends on Transfermarkt's archive completeness
- URLs are constructed to match Transfermarkt's season archive format