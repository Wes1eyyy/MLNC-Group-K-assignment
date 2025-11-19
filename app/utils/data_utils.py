from typing import List
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def save_data(data: List[dict], file_path: str) -> None:
    """Save data to a CSV file.

    Args:
        data: List of dictionaries to save
        file_path: Path to save the CSV file

    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("No data to save")

    # Get all unique field names from all dictionaries
    fieldnames = list(data[0].keys())

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} rows to {file_path}")


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


def count_record_in_season(data: List[dict], team: str, reference_date: str) -> tuple:
    """Count wins, draws, and losses for a team in the current season up to the reference date.

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

    wins = 0
    draws = 0
    losses = 0

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
                wins += 1
            elif match['FTR'] == 'D':
                draws += 1
            elif match['FTR'] == 'A':
                losses += 1
        elif match_season == target_season and match['AwayTeam'] == team:
            if match['FTR'] == 'A':
                wins += 1
            elif match['FTR'] == 'D':
                draws += 1
            elif match['FTR'] == 'H':
                losses += 1

    return wins, draws, losses


def calculate_goal_averages(data: List[dict], team: str, reference_date: str) -> tuple:
    """Calculate average goals scored and conceded in the season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Tuple of (avg_goals_scored, avg_goals_conceded) away
        Returns (0.0, 0.0) if no away matches played yet
    """
    target_season = get_season_from_date(reference_date)
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    total_goals_scored = 0
    total_goals_conceded = 0
    total_shots = 0
    total_shots_conceded = 0
    total_corners = 0
    total_corners_conceded = 0
    matches = 0

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
            matches += 1
            total_goals_scored += int(match['FTAG'])
            total_goals_conceded += int(match['FTHG'])
            total_shots += int(match['AS'])
            total_shots_conceded += int(match['HS'])
            total_corners += int(match['AC'])
            total_corners_conceded += int(match['HC'])
        elif match_season == target_season and match['HomeTeam'] == team:
            matches += 1
            total_goals_scored += int(match['FTHG'])
            total_goals_conceded += int(match['FTAG'])
            total_shots += int(match['HS'])
            total_shots_conceded += int(match['AS'])
            total_corners += int(match['HC'])
            total_corners_conceded += int(match['AC'])

    # Calculate averages
    if matches == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    avg_goals_scored = total_goals_scored / matches
    avg_goals_conceded = total_goals_conceded / matches
    avg_shots = total_shots / matches
    avg_shots_conceded = total_shots_conceded / matches
    avg_corners = total_corners / matches
    avg_corners_conceded = total_corners_conceded / matches

    return avg_goals_scored, avg_goals_conceded, avg_shots, avg_shots_conceded, avg_corners, avg_corners_conceded


def _process_single_match(args):
    """Helper function to process a single match. Used for parallel processing."""
    match, data = args

    # Skip matches with no date
    if not match.get('Date') or match['Date'].strip() == '':
        return match

    match_date = match['Date']
    home_team = match['HomeTeam']
    away_team = match['AwayTeam']

    # Get home team's record before this match
    h_wins, h_draws, h_losses = count_record_in_season(data, home_team, match_date)

    # Get away team's record before this match
    a_wins, a_draws, a_losses = count_record_in_season(data, away_team, match_date)

    # Get home team's goal averages at home
    h_goals_scored, h_goals_conceded, h_shots, h_shots_conceded, h_corners, h_corners_concealed = calculate_goal_averages(data, home_team, match_date)

    # Get away team's goal averages away
    a_goals_scored, a_goals_conceded, a_shots, a_shots_conceded, a_corners, a_corners_concealed = calculate_goal_averages(data, away_team, match_date)

    # Create enriched match record
    enriched_match = match.copy()
    enriched_match['HomeTeam_Wins'] = h_wins
    enriched_match['HomeTeam_Draws'] = h_draws
    enriched_match['HomeTeam_Losses'] = h_losses
    enriched_match['HomeTeam_AvgGoalsScored'] = round(h_goals_scored, 2)
    enriched_match['HomeTeam_AvgGoalsConceded'] = round(h_goals_conceded, 2)
    enriched_match['HomeTeam_AvgShots'] = round(h_shots, 2)
    enriched_match['HomeTeam_AvgShotsConceded'] = round(h_shots, 2)
    enriched_match['HomeTeam_AvgCorners'] = round(h_corners, 2)
    enriched_match['HomeTeam_AvgCornersConceded'] = round(h_corners_concealed, 2)

    enriched_match['AwayTeam_Wins'] = a_wins
    enriched_match['AwayTeam_Draws'] = a_draws
    enriched_match['AwayTeam_Losses'] = a_losses
    enriched_match['AwayTeam_AvgGoalsScored'] = round(a_goals_scored, 2)
    enriched_match['AwayTeam_AvgGoalsConceded'] = round(a_goals_conceded, 2)
    enriched_match['AwayTeam_AvgShots'] = round(a_shots, 2)
    enriched_match['AwayTeam_AvgShotsConceded'] = round(a_shots_conceded, 2)
    enriched_match['AwayTeam_AvgCorners'] = round(a_corners, 2)
    enriched_match['AwayTeam_AvgCornersConceded'] = round(a_corners_concealed, 2)

    return enriched_match


def add_team_records_to_data(data: List[dict], max_workers: int = 20) -> List[dict]:
    """Add home team and away team season records to each match.

    For each match, adds the following fields:
    - HomeTeam_Wins: Home team's total wins in season before this match
    - HomeTeam_Draws: Home team's total draws in season before this match
    - HomeTeam_Losses: Home team's total losses in season before this match
    - HomeTeam_AvgGoalsScored: Home team's average goals scored at home
    - HomeTeam_AvgGoalsConceded: Home team's average goals conceded at home
    - AwayTeam_Wins: Away team's total wins in season before this match
    - AwayTeam_Draws: Away team's total draws in season before this match
    - AwayTeam_Losses: Away team's total losses in season before this match
    - AwayTeam_AvgGoalsScored: Away team's average goals scored away
    - AwayTeam_AvgGoalsConceded: Away team's average goals conceded away

    Args:
        data: List of match dictionaries
        max_workers: Number of threads to use for parallel processing (default: 4)

    Returns:
        List of match dictionaries with added team record fields
    """
    print(f"Processing {len(data)} matches using {max_workers} threads...")

    # Prepare args for parallel processing
    args_list = [(match, data) for match in data]

    # Process in parallel
    enriched_data = [{}] * len(data)  # Pre-allocate list

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {executor.submit(_process_single_match, args): i
                           for i, args in enumerate(args_list)}

        # Collect results with progress bar
        for future in tqdm(as_completed(future_to_index), total=len(data), desc="Processing"):
            index = future_to_index[future]
            enriched_data[index] = future.result()

    return enriched_data
