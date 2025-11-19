from typing import List
import csv
from datetime import datetime

from tqdm import tqdm


def load_data(file_path: str) -> List[dict]:
    """Load data from a given file path.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries, where each dictionary represents a row

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is empty or has no header
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)

            if not data:
                raise ValueError(f"No data found in {file_path}")

            return data

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def get_season_from_date(date_str: str) -> str:
    """Get season string from a date.

    A season runs from August to May of the next year.
    For example: '2023-24' for dates from Aug 2023 to May 2024.

    Args:
        date_str: Date string in format 'DD/MM/YYYY' or 'DD Mon YY'

    Returns:
        Season string in format 'YYYY-YY' (e.g., '2023-24')
    """
    # Handle empty or None dates
    if not date_str or date_str.strip() == '':
        raise ValueError("Date string is empty")

    # Parse date
    date = datetime.strptime(date_str, '%d/%m/%Y')

    year = date.year
    month = date.month

    # Season starts in August
    # If month is Aug-Dec, season is year to year+1
    # If month is Jan-May, season is year-1 to year
    # If month is Jun-Jul, it's off-season (shouldn't happen for matches)
    if month >= 8:  # Aug-Dec
        season_start = year
        season_end = year + 1
    else:  # Jan-Jul
        season_start = year - 1
        season_end = year

    return f"{season_start}-{str(season_end)[-2:]}"


def count_home_record_in_season(data: List[dict], team: str, reference_date: str) -> tuple:
    """Count home wins, draws, and losses for a team in the current season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Tuple of (wins, draws, losses) in the season before or on the reference date
    """
    target_season = get_season_from_date(reference_date)

    # Parse reference date for comparison
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    home_wins = 0
    home_draws = 0
    home_losses = 0

    for match in data:
        # Skip matches with no date
        if not match.get('Date') or match['Date'].strip() == '':
            continue
        # Parse match date
        match_date = datetime.strptime(match['Date'], '%d/%m/%Y')

        # Skip matches after reference date
        if match_date >= ref_date:
            break

        # Check if this match is in the target season
        match_season = get_season_from_date(match['Date'])

        # Check if team is home team
        if match_season == target_season and match['HomeTeam'] == team:
            if match['FTR'] == 'H':
                home_wins += 1
            elif match['FTR'] == 'D':
                home_draws += 1
            elif match['FTR'] == 'A':
                home_losses += 1

    return home_wins, home_draws, home_losses


def count_away_record_in_season(data: List[dict], team: str, reference_date: str) -> tuple:
    """Count away wins, draws, and losses for a team in the current season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Tuple of (wins, draws, losses) in the season before or on the reference date
    """
    target_season = get_season_from_date(reference_date)

    # Parse reference date for comparison
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    away_wins = 0
    away_draws = 0
    away_losses = 0

    for match in data:
        # Skip matches with no date
        if not match.get('Date') or match['Date'].strip() == '':
            continue
        # Parse match date
        match_date = datetime.strptime(match['Date'], '%d/%m/%Y')

        # Skip matches after reference date
        if match_date >= ref_date:
            break

        # Check if this match is in the target season
        match_season = get_season_from_date(match['Date'])

        # Check if team is away team
        if match_season == target_season and match['AwayTeam'] == team:
            if match['FTR'] == 'A':  # Away team won
                away_wins += 1
            elif match['FTR'] == 'D':  # Draw
                away_draws += 1
            elif match['FTR'] == 'H':  # Home team won (away loss)
                away_losses += 1

    return away_wins, away_draws, away_losses


def count_overall_record_in_season(data: List[dict], team: str, reference_date: str) -> tuple:
    """Count overall wins, draws, and losses (both home and away) for a team in the season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Tuple of (wins, draws, losses) in the season before or on the reference date
    """
    # Get home record
    h_wins, h_draws, h_losses = count_home_record_in_season(data, team, reference_date)
    # Get away record
    a_wins, a_draws, a_losses = count_away_record_in_season(data, team, reference_date)

    # Combine
    total_wins = h_wins + a_wins
    total_draws = h_draws + a_draws
    total_losses = h_losses + a_losses

    return total_wins, total_draws, total_losses


def add_team_records_to_data(data: List[dict]) -> List[dict]:
    """Add home team and away team season records to each match.

    For each match, adds the following fields:
    - HomeTeam_Wins: Home team's total wins in season before this match
    - HomeTeam_Draws: Home team's total draws in season before this match
    - HomeTeam_Losses: Home team's total losses in season before this match
    - AwayTeam_Wins: Away team's total wins in season before this match
    - AwayTeam_Draws: Away team's total draws in season before this match
    - AwayTeam_Losses: Away team's total losses in season before this match

    Args:
        data: List of match dictionaries

    Returns:
        List of match dictionaries with added team record fields
    """
    enriched_data = []

    for match in tqdm(data):
        # Skip matches with no date
        if not match.get('Date') or match['Date'].strip() == '':
            enriched_data.append(match)
            continue

        match_date = match['Date']
        home_team = match['HomeTeam']
        away_team = match['AwayTeam']

        # Get home team's record before this match
        h_wins, h_draws, h_losses = count_overall_record_in_season(data, home_team, match_date)

        # Get away team's record before this match
        a_wins, a_draws, a_losses = count_overall_record_in_season(data, away_team, match_date)

        # Create enriched match record
        enriched_match = match.copy()
        enriched_match['HomeTeam_Wins'] = h_wins
        enriched_match['HomeTeam_Draws'] = h_draws
        enriched_match['HomeTeam_Losses'] = h_losses
        enriched_match['AwayTeam_Wins'] = a_wins
        enriched_match['AwayTeam_Draws'] = a_draws
        enriched_match['AwayTeam_Losses'] = a_losses

        enriched_data.append(enriched_match)

    return enriched_data
