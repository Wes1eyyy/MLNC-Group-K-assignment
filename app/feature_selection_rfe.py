"""
Feature Selection using RFE (Recursive Feature Elimination)

This script uses RFE to select the top 10 most important features
and generates a new dataset with only these features.

Usage: python feature_selection_rfe.py
"""
import sys
import os
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Add utils directory to path
sys.path.append(os.path.dirname(__file__))
from utils.data_utils import load_data, prepare_features

# Configuration
INPUT_DATA_PATH = "../data/epl-features-training.csv"
N_FEATURES_TO_SELECT = 15


def perform_rfe(X, y, feature_names, n_features=10, estimator_type='random_forest'):
    """
    Perform Recursive Feature Elimination to select top features

    Args:
        X: Feature matrix
        y: Target labels
        feature_names: List of feature names
        n_features: Number of features to select (default: 10)
        estimator_type: Type of estimator to use ('random_forest' or 'logistic')

    Returns:
        selected_features: List of selected feature names
        rfe: Fitted RFE object
        feature_ranking: Dictionary of feature rankings
    """
    print(f"\n{'=' * 60}")
    print("Recursive Feature Elimination (RFE)")
    print(f"{'=' * 60}")
    print(f"Total features: {len(feature_names)}")
    print(f"Features to select: {n_features}")
    print(f"Estimator: {estimator_type}")

    # Choose base estimator
    if estimator_type == 'random_forest':
        estimator = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        print("Using Random Forest as base estimator")
    elif estimator_type == 'logistic':
        estimator = LogisticRegression(
            multi_class='multinomial',
            solver='lbfgs',
            max_iter=1000,
            random_state=42
        )
        print("Using Logistic Regression as base estimator")
    else:
        raise ValueError(f"Unknown estimator type: {estimator_type}")

    # Create RFE selector
    print(f"\nRunning RFE to select {n_features} features...")
    rfe = RFE(
        estimator=estimator,
        n_features_to_select=n_features,
        step=1,  # Remove 1 feature at each iteration
        verbose=1
    )

    # Fit RFE
    rfe.fit(X, y)

    # Get selected features
    selected_mask = rfe.support_
    selected_features = [feature_names[i] for i in range(len(feature_names)) if selected_mask[i]]

    # Get feature rankings (1 = selected, >1 = eliminated)
    feature_ranking = {feature_names[i]: rfe.ranking_[i] for i in range(len(feature_names))}

    # Sort by ranking
    sorted_features = sorted(feature_ranking.items(), key=lambda x: x[1])

    print(f"\n{'=' * 60}")
    print("RFE Results")
    print(f"{'=' * 60}")
    print(f"\nTop {n_features} Selected Features (Ranking = 1):")
    for i, (feature, rank) in enumerate(sorted_features[:n_features], 1):
        print(f"  {i:2d}. {feature:<35s} (Rank: {rank})")

    print(f"\nEliminated Features:")
    for i, (feature, rank) in enumerate(sorted_features[n_features:], 1):
        print(f"  {i:2d}. {feature:<35s} (Rank: {rank})")

    return selected_features, rfe, feature_ranking


def create_reduced_dataset(input_path, output_path, selected_features):
    """
    Create a new dataset with only selected features

    Args:
        input_path: Path to original dataset
        output_path: Path to save reduced dataset
        selected_features: List of feature names to keep
    """
    print(f"\n{'=' * 60}")
    print("Creating Reduced Dataset")
    print(f"{'=' * 60}")

    # Load original data
    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Original dataset shape: {df.shape}")

    # Identify feature columns (exclude Date, HomeTeam, AwayTeam, FTR, etc.)
    non_feature_cols = ['Date', 'HomeTeam', 'AwayTeam', 'Referee', 'FTR']
    metadata_cols = [col for col in df.columns if col in non_feature_cols]

    print(f"\nMetadata columns to preserve: {metadata_cols}")
    print(f"Selected feature columns: {len(selected_features)}")

    # Create new dataframe with metadata + selected features
    columns_to_keep = metadata_cols + selected_features
    df_reduced = df[columns_to_keep]

    print(f"Reduced dataset shape: {df_reduced.shape}")
    print(f"Columns: {list(df_reduced.columns)}")

    # Save reduced dataset
    print(f"\nSaving reduced dataset to: {output_path}")
    df_reduced.to_csv(output_path, index=False)
    print("✓ Dataset saved successfully!")

    return df_reduced


def analyze_feature_importance(rfe, feature_names, selected_features):
    """
    Analyze and display feature importance from the base estimator

    Args:
        rfe: Fitted RFE object
        feature_names: List of all feature names
        selected_features: List of selected feature names
    """
    estimator = rfe.estimator_

    # Check if estimator has feature_importances_
    if hasattr(estimator, 'feature_importances_'):
        print(f"\n{'=' * 60}")
        print("Feature Importance (from base estimator)")
        print(f"{'=' * 60}")

        # After RFE, the estimator's feature_importances_ corresponds to selected features
        importances = estimator.feature_importances_

        # Create importance dictionary for selected features
        # The importances array has the same length as selected_features
        feature_importance = {selected_features[i]: importances[i]
                             for i in range(len(selected_features))}

        # Sort by importance
        sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

        print(f"\nSelected Features Ranked by Importance:")
        for i, (feature, importance) in enumerate(sorted_importance, 1):
            print(f"  {i:2d}. {feature:<35s} {importance:.4f}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("Feature Selection using RFE")
    print("=" * 60)

    # 1. Load data
    print("\nStep 1: Loading data...")
    data = load_data(INPUT_DATA_PATH)
    print(f"Loaded {len(data)} matches")

    # 2. Prepare features
    print("\nStep 2: Preparing features...")
    X, y, feature_names = prepare_features(data)
    print(f"Feature matrix shape: {X.shape}")
    print(f"Total features: {len(feature_names)}")

    # Display class distribution
    unique, counts = np.unique(y, return_counts=True)
    print(f"\nClass distribution:")
    for label, count in zip(unique, counts):
        print(f"  {label}: {count} ({count / len(y) * 100:.1f}%)")

    # 3. Perform RFE with Random Forest
    print("\n" + "=" * 60)
    print("Running RFE with Random Forest estimator...")
    print("=" * 60)
    selected_features, rfe, feature_ranking = perform_rfe(
        X, y, feature_names,
        n_features=N_FEATURES_TO_SELECT,
        estimator_type='random_forest'
    )

    # 4. Analyze feature importance
    analyze_feature_importance(rfe, feature_names, selected_features)

    # 5. Summary
    print(f"\n{'=' * 60}")
    print("Summary")
    print(f"{'=' * 60}")
    print(f"✓ Original features: {len(feature_names)}")
    print(f"✓ Selected features: {N_FEATURES_TO_SELECT}")
    print(f"✓ Reduction: {(1 - N_FEATURES_TO_SELECT / len(feature_names)) * 100:.1f}%")
    print(f"✓ Original dataset: {INPUT_DATA_PATH}")
    print(f"\nSelected Features:")
    for i, feature in enumerate(selected_features, 1):
        print(f"  {i:2d}. {feature}")

    print("\n" + "=" * 60)
    print("Feature selection completed successfully!")
    print("=" * 60)

    # Optional: Compare with Logistic Regression
    print("\n" + "=" * 60)
    print("Optional: Running RFE with Logistic Regression for comparison...")
    print("=" * 60)
    selected_features_lr, rfe_lr, _ = perform_rfe(
        X, y, feature_names,
        n_features=N_FEATURES_TO_SELECT,
        estimator_type='logistic'
    )

    # Compare feature selections
    common_features = set(selected_features) & set(selected_features_lr)
    print(f"\n{'=' * 60}")
    print("Comparison: Random Forest vs Logistic Regression")
    print(f"{'=' * 60}")
    print(f"Common features selected by both methods: {len(common_features)}/{N_FEATURES_TO_SELECT}")
    if common_features:
        print("Common features:")
        for i, feature in enumerate(sorted(common_features), 1):
            print(f"  {i:2d}. {feature}")

    print("\nFeatures selected only by Random Forest:")
    rf_only = set(selected_features) - set(selected_features_lr)
    for feature in sorted(rf_only):
        print(f"  - {feature}")

    print("\nFeatures selected only by Logistic Regression:")
    lr_only = set(selected_features_lr) - set(selected_features)
    for feature in sorted(lr_only):
        print(f"  - {feature}")


if __name__ == "__main__":
    main()