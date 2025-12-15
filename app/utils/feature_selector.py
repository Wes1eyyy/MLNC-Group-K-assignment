"""
Feature selector for ablation study experiments
"""

# Define feature groups based on ablation study plan
FEATURE_GROUPS = {
    '2a': [
        'HomeTeam_Wins', 'HomeTeam_Draws', 'HomeTeam_Losses',
        'AwayTeam_Wins', 'AwayTeam_Draws', 'AwayTeam_Losses'
    ],
    '2b': [
        'HomeTeam_AvgGoalsScored', 'HomeTeam_AvgGoalsConceded',
        'AwayTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsConceded'
    ],
    '3': [
        'HomeTeam_AvgShots', 'HomeTeam_AvgShotsConceded',
        'AwayTeam_AvgShots', 'AwayTeam_AvgShotsConceded',
        'HomeTeam_AvgCorners', 'HomeTeam_AvgCornersConceded',
        'AwayTeam_AvgCorners', 'AwayTeam_AvgCornersConceded'
    ],
    '4': [
        'HomeTeam_AvgFouls', 'AwayTeam_AvgFouls'
    ],
    '5a': [
        'HomeTeam_PrevSeasonRank', 'AwayTeam_PrevSeasonRank'
    ],
    '5b': [
        'HomeTeam_AvgAge', 'HomeTeam_AvgValue',
        'AwayTeam_AvgAge', 'AwayTeam_AvgValue'
    ]
}

# Group names for reporting
GROUP_NAMES = {
    '2a': 'Win/Loss Record',
    '2b': 'Goal Statistics',
    '3': 'Match Dynamics',
    '4': 'Discipline',
    '5a': 'Previous Season Rank',
    '5b': 'Squad Quality (Age/Value)'
}


def get_all_feature_names():
    """Get all feature names across all groups"""
    all_features = []
    for features in FEATURE_GROUPS.values():
        all_features.extend(features)
    return all_features


def select_features_by_config(config):
    """
    Select features based on include/exclude groups

    Args:
        config: dict with either:
            - 'include_groups': list of group IDs to include
            - 'exclude_groups': list of group IDs to exclude from all

    Returns:
        list: Feature column names to use
    """
    if 'include_groups' in config:
        # Only include specified groups
        selected = []
        for group_id in config['include_groups']:
            if group_id in FEATURE_GROUPS:
                selected.extend(FEATURE_GROUPS[group_id])
            else:
                print(f"Warning: Unknown group ID '{group_id}'")
        return selected

    elif 'exclude_groups' in config:
        # Include all groups except specified ones
        all_features = get_all_feature_names()
        excluded = []
        for group_id in config['exclude_groups']:
            if group_id in FEATURE_GROUPS:
                excluded.extend(FEATURE_GROUPS[group_id])
            else:
                print(f"Warning: Unknown group ID '{group_id}'")

        return [f for f in all_features if f not in excluded]

    else:
        # If no config specified, return all features
        return get_all_feature_names()


def get_group_name(group_id):
    """Get human-readable name for a group ID"""
    return GROUP_NAMES.get(group_id, f"Group {group_id}")


def get_feature_count(config):
    """Get number of features for a given config"""
    return len(select_features_by_config(config))