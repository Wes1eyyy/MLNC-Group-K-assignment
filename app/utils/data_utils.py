from typing import List
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
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


def calculate_season_standings(data: List[dict], season: str) -> dict:
    """Calculate final standings for all teams in a given season.

    Points system: Win = 3 points, Draw = 1 point, Loss = 0 points

    Args:
        data: List of match dictionaries
        season: Season string (e.g., '2022-23')

    Returns:
        Dictionary mapping team name to their final ranking (1 = best, 2 = second best, etc.)
    """
    team_points = {}
    for match in data:

        match_season = get_season_from_date(match['Date'])

        if match_season != season:
            continue

        # Stop processing if we've moved past the target season
        if match_season > season:
            break

        home_team = match['HomeTeam']
        away_team = match['AwayTeam']
        result = match['FTR']

        # Initialize teams if not seen before
        if home_team not in team_points:
            team_points[home_team] = 0
        if away_team not in team_points:
            team_points[away_team] = 0

        # Award points based on result
        if result == 'H':  # Home win
            team_points[home_team] += 3
        elif result == 'A':  # Away win
            team_points[away_team] += 3
        elif result == 'D':  # Draw
            team_points[home_team] += 1
            team_points[away_team] += 1

    # Sort teams by points (descending) and assign rankings
    sorted_teams = sorted(team_points.items(), key=lambda x: x[1], reverse=True)

    team_rankings = {}
    for rank, (team, points) in enumerate(sorted_teams, 1):
        team_rankings[team] = rank

    return team_rankings


def get_previous_season_ranking(data: List[dict], team: str, current_season: str) -> int:
    """Get a team's ranking from the previous season.

    Args:
        data: List of match dictionaries
        team: Team name
        current_season: Current season string (e.g., '2023-24')

    Returns:
        Previous season ranking (1-20), or 0 if team didn't play in previous season
    """
    # Parse current season to get previous season
    season_parts = current_season.split('-')

    start_year = int(season_parts[0])
    prev_season = f"{start_year - 1}-{str(start_year)[-2:]}"

    # Calculate previous season standings
    prev_standings = calculate_season_standings(data, prev_season)

    # Return team's ranking, or 0 if not found (newly promoted team)
    return prev_standings.get(team, 0)


def calculate_goal_averages(data: List[dict], team: str, reference_date: str) -> tuple:
    """Calculate average goals scored and conceded in the season up to the reference date.

    Args:
        data: List of match dictionaries
        team: Team name to check
        reference_date: Date to determine which season and cutoff date (format: 'DD/MM/YYYY')

    Returns:
        Tuple of (avg_goals_scored, avg_goals_conceded, avg_shots, avg_shots_conceded, avg_corners, avg_corners_conceded, avg_fouls)
        Returns (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) if no away matches played yet
    """
    target_season = get_season_from_date(reference_date)
    ref_date = datetime.strptime(reference_date, '%d/%m/%Y')

    total_goals_scored = 0
    total_goals_conceded = 0
    total_shots = 0
    total_shots_conceded = 0
    total_corners = 0
    total_corners_conceded = 0
    total_fouls = 0
    matches = 0

    for match in data:
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
            total_fouls += int(match['AF'])
        elif match_season == target_season and match['HomeTeam'] == team:
            matches += 1
            total_goals_scored += int(match['FTHG'])
            total_goals_conceded += int(match['FTAG'])
            total_shots += int(match['HS'])
            total_shots_conceded += int(match['AS'])
            total_corners += int(match['HC'])
            total_corners_conceded += int(match['AC'])
            total_fouls += int(match['HF'])

    # Calculate averages
    if matches == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    avg_goals_scored = total_goals_scored / matches
    avg_goals_conceded = total_goals_conceded / matches
    avg_shots = total_shots / matches
    avg_shots_conceded = total_shots_conceded / matches
    avg_corners = total_corners / matches
    avg_corners_conceded = total_corners_conceded / matches
    avg_fouls = total_fouls / matches

    return avg_goals_scored, avg_goals_conceded, avg_shots, avg_shots_conceded, avg_corners, avg_corners_conceded, avg_fouls


def _process_single_match(args):
    """Helper function to process a single match. Used for parallel processing."""
    match, data = args

    match_date = match['Date']
    home_team = match['HomeTeam']
    away_team = match['AwayTeam']

    # Get current season
    current_season = get_season_from_date(match_date)

    # Get home team's record before this match
    h_wins, h_draws, h_losses = count_record_in_season(data, home_team, match_date)

    # Get away team's record before this match
    a_wins, a_draws, a_losses = count_record_in_season(data, away_team, match_date)

    # Get home team's goal averages at home
    h_goals_scored, h_goals_conceded, h_shots, h_shots_conceded, h_corners, h_corners_concealed, h_fouls = calculate_goal_averages(
        data, home_team, match_date)

    # Get away team's goal averages away
    a_goals_scored, a_goals_conceded, a_shots, a_shots_conceded, a_corners, a_corners_concealed, a_fouls = calculate_goal_averages(
        data, away_team, match_date)

    # NEW: Get previous season rankings
    h_prev_ranking = get_previous_season_ranking(data, home_team, current_season)
    a_prev_ranking = get_previous_season_ranking(data, away_team, current_season)

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
    enriched_match['HomeTeam_AvgFouls'] = round(h_fouls, 2)
    enriched_match['HomeTeam_PrevSeasonRank'] = h_prev_ranking

    enriched_match['AwayTeam_Wins'] = a_wins
    enriched_match['AwayTeam_Draws'] = a_draws
    enriched_match['AwayTeam_Losses'] = a_losses
    enriched_match['AwayTeam_AvgGoalsScored'] = round(a_goals_scored, 2)
    enriched_match['AwayTeam_AvgGoalsConceded'] = round(a_goals_conceded, 2)
    enriched_match['AwayTeam_AvgShots'] = round(a_shots, 2)
    enriched_match['AwayTeam_AvgShotsConceded'] = round(a_shots_conceded, 2)
    enriched_match['AwayTeam_AvgCorners'] = round(a_corners, 2)
    enriched_match['AwayTeam_AvgCornersConceded'] = round(a_corners_concealed, 2)
    enriched_match['AwayTeam_AvgFouls'] = round(a_fouls, 2)
    enriched_match['AwayTeam_PrevSeasonRank'] = a_prev_ranking

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


def temporal_train_test_split(data: List[dict], test_size: float = 0.1) -> tuple:
    """Split data into training and testing sets using temporal ordering.

    IMPORTANT: Uses temporal split (time-ordered) to prevent data leakage.
    The last test_size portion of matches chronologically becomes the test set.

    Args:
        data: List of match dictionaries (must contain 'Date' field)
        test_size: Proportion of data to use for testing (default: 0.2 = 20%)

    Returns:
        Tuple of (training_data, testing_data)

    Raises:
        ValueError: If test_size is not between 0 and 1
        ValueError: If data is empty or missing Date field
    """
    if not 0 < test_size < 1:
        raise ValueError(f"test_size must be between 0 and 1, got {test_size}")

    if not data:
        raise ValueError("Data is empty")

    if 'Date' not in data[0]:
        raise ValueError("Data must contain 'Date' field")

    # Calculate split index
    split_idx = int(len(data) * (1 - test_size))

    # Split data
    training_data = data[:split_idx]
    testing_data = data[split_idx:]

    # Print split information
    train_start = training_data[0]['Date']
    train_end = training_data[-1]['Date']
    test_start = testing_data[0]['Date']
    test_end = testing_data[-1]['Date']

    print(f"\n{'=' * 60}")
    print(f"Temporal Train-Test Split")
    print(f"{'=' * 60}")
    print(f"Total matches: {len(data)}")
    print(f"\nTraining set: {len(training_data)} matches ({len(training_data) / len(data) * 100:.1f}%)")
    print(f"  Date range: {train_start} to {train_end}")
    print(f"\nTesting set: {len(testing_data)} matches ({len(testing_data) / len(data) * 100:.1f}%)")
    print(f"  Date range: {test_start} to {test_end}")
    print(f"{'=' * 60}\n")

    return training_data, testing_data


def prepare_features(data):
    """
    Extract features and labels from data

    Args:
        data: List of match dictionaries

    Returns:
        X (numpy array): Feature matrix
        y (numpy array): Labels
        feature_cols (list): List of feature column names
    """
    # Define feature columns
    feature_cols = [
        'HomeTeam_Wins', 'HomeTeam_Draws', 'HomeTeam_Losses',
        'HomeTeam_AvgGoalsScored', 'HomeTeam_AvgGoalsConceded',
        'HomeTeam_AvgShots', 'HomeTeam_AvgShotsConceded',
        'HomeTeam_AvgCorners', 'HomeTeam_AvgCornersConceded',
        'HomeTeam_AvgFouls',
        'HomeTeam_PrevSeasonRank',
        'AwayTeam_Wins', 'AwayTeam_Draws', 'AwayTeam_Losses',
        'AwayTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsConceded',
        'AwayTeam_AvgShots', 'AwayTeam_AvgShotsConceded',
        'AwayTeam_AvgCorners', 'AwayTeam_AvgCornersConceded',
        'AwayTeam_AvgFouls',
        'AwayTeam_PrevSeasonRank'
    ]

    # Extract features
    X = []
    y = []

    count = 0
    for match in data:
        # Extract feature values
        features = []
        for col in feature_cols:
            value = match[col]
            # Convert to float
            features.append(float(value))

        X.append(features)
        y.append(match['FTR'])  # Target: H, D, A
        count += 1

    return np.array(X), np.array(y), feature_cols
