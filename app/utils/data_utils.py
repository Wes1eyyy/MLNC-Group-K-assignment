from typing import List
import csv
from datetime import datetime


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


def count_home_wins_in_season(data: List[dict], team: str, reference_date: str) -> int:
    """Count how many home games a team has won in the current season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY' or 'DD Mon YY')

    Returns:
        Number of home wins in the season before or on the reference date
    """
    target_season = get_season_from_date(reference_date)

    # Parse reference date for comparison
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    home_wins = 0

    for match in data:
        # Skip matches with no date
        if not match.get('Date') or match['Date'].strip() == '':
            continue
        # Parse match date
        match_date = datetime.strptime(match['Date'], '%d/%m/%Y')

        # Skip matches after reference date
        if match_date > ref_date:
            break

        # Check if this match is in the target season
        match_season = get_season_from_date(match['Date'])

        # Check if team is home team and won
        if (match_season == target_season and
                match['HomeTeam'] == team and
                match['FTR'] == 'H'):
            home_wins += 1

    return home_wins


def count_home_losses_in_season(data: List[dict], team: str, reference_date: str) -> int:
    """Count how many home games a team has lost in the current season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Number of home losses in the season before or on the reference date
    """
    target_season = get_season_from_date(reference_date)

    # Parse reference date for comparison
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    home_losses = 0

    for match in data:
        # Skip matches with no date
        if not match.get('Date') or match['Date'].strip() == '':
            continue
        # Parse match date
        match_date = datetime.strptime(match['Date'], '%d/%m/%Y')

        # Skip matches after reference date
        if match_date > ref_date:
            break

        # Check if this match is in the target season
        match_season = get_season_from_date(match['Date'])

        # Check if team is home team and lost (FTR == 'A' means away team won)
        if (match_season == target_season and
                match['HomeTeam'] == team and
                match['FTR'] == 'A'):
            home_losses += 1

    return home_losses
