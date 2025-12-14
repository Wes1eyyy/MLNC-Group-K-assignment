"""
Ablation Study for EPL Match Outcome Prediction
Systematically test different feature combinations to understand their contribution
"""
import sys
import os
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path
sys.path.append(os.path.dirname(__file__))
from utils.data_utils import load_data, temporal_train_test_split
from utils.feature_selector import select_features_by_config, get_all_feature_names, get_group_name

# Configuration
DATA_PATH = "../data/epl-features-training.csv"
RESULTS_DIR = "../results/ablation"
TEST_SIZE = 0.1
RANDOM_STATE = 42

# Ablation experiment configurations
ABLATION_CONFIGS = {
    # Phase 1: Baseline
    'EXP-0': {
        'name': 'Full Model (Baseline)',
        'include_groups': ['2a', '2b', '3', '4', '5a', '5b']
    },
    'EXP-0a': {
        'name': 'Minimal Baseline',
        'include_groups': []  # No features (will use baseline predictor)
    },

    # Phase 2: Individual Group Ablation
    'EXP-1': {
        'name': 'Ablate Team Form (Group 2)',
        'exclude_groups': ['2a', '2b']
    },
    'EXP-2': {
        'name': 'Ablate Match Dynamics (Group 3)',
        'exclude_groups': ['3']
    },
    'EXP-3': {
        'name': 'Ablate Discipline (Group 4)',
        'exclude_groups': ['4']
    },
    'EXP-4': {
        'name': 'Ablate Previous Rank (Group 5a)',
        'exclude_groups': ['5a']
    },
    'EXP-5': {
        'name': 'Ablate Squad Quality (Group 5b)',
        'exclude_groups': ['5b']
    },

    # Phase 3: Progressive Addition
    'EXP-6': {
        'name': 'Only Team Form (Group 2)',
        'include_groups': ['2a', '2b']
    },
    'EXP-7': {
        'name': 'Team Form + Match Dynamics',
        'include_groups': ['2a', '2b', '3']
    },
    'EXP-8': {
        'name': 'Form + Dynamics + Prev Rank',
        'include_groups': ['2a', '2b', '3', '5a']
    },
    'EXP-9': {
        'name': 'Form + Dynamics + Prev Rank + Squad Quality (Full)',
        'include_groups': ['2a', '2b', '3', '5a', '5b']
    },
    'EXP-10': {
        'name': 'Team Form + Squad Quality (Skip Dynamics)',
        'include_groups': ['2a', '2b', '5a', '5b']
    },

    # Phase 4: Fine-grained Analysis
    'EXP-11': {
        'name': 'Win/Loss Record Only (Group 2a)',
        'include_groups': ['2a']
    },
    'EXP-12': {
        'name': 'Goal Statistics Only (Group 2b)',
        'include_groups': ['2b']
    },
    'EXP-13': {
        'name': 'Win/Loss + Goals (Complete Group 2)',
        'include_groups': ['2a', '2b']
    },
    'EXP-14': {
        'name': 'Goals + Squad Value',
        'include_groups': ['2b', '5b']
    },
    'EXP-15': {
        'name': 'Only Squad Quality (Group 5b)',
        'include_groups': ['5b']
    },
}


def prepare_features_custom(data, feature_cols):
    """
    Extract features and labels from data with custom feature columns

    Args:
        data: List of match dictionaries
        feature_cols: List of feature column names to use

    Returns:
        X (numpy array): Feature matrix
        y (numpy array): Labels
    """
    if not feature_cols:
        # No features - return empty array
        return np.array([]).reshape(len(data), 0), np.array([match['FTR'] for match in data])

    X = []
    y = []

    for match in data:
        features = []
        for col in feature_cols:
            value = match[col]
            features.append(float(value))

        X.append(features)
        y.append(match['FTR'])

    return np.array(X), np.array(y)


def train_and_evaluate(X_train, y_train, X_test, y_test, config_name):
    """
    Train Random Forest and evaluate

    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels
        config_name: Name of configuration

    Returns:
        dict: Evaluation metrics
    """
    start_time = time.time()

    # Handle case with no features (baseline predictor)
    if X_train.shape[1] == 0:
        # Simple baseline: always predict most common class
        unique, counts = np.unique(y_train, return_counts=True)
        most_common = unique[np.argmax(counts)]
        y_pred = np.array([most_common] * len(y_test))
    else:
        # Train Random Forest
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=0
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    train_time = time.time() - start_time

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro', labels=['H', 'D', 'A'])
    f1_per_class = f1_score(y_test, y_pred, average=None, labels=['H', 'D', 'A'])

    # Get classification report as dict
    report = classification_report(y_test, y_pred, labels=['H', 'D', 'A'],
                                   target_names=['H', 'D', 'A'], output_dict=True)

    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_H': f1_per_class[0],
        'f1_D': f1_per_class[1],
        'f1_A': f1_per_class[2],
        'train_time': train_time,
        'report': report
    }


def run_ablation_experiment(exp_id, training_data, testing_data):
    """
    Run a single ablation experiment

    Args:
        exp_id: Experiment ID (e.g., 'EXP-0')
        training_data: Training dataset
        testing_data: Testing dataset

    Returns:
        dict: Results including metrics and configuration info
    """
    config = ABLATION_CONFIGS[exp_id]

    print(f"\n{'='*70}")
    print(f"{exp_id}: {config['name']}")
    print(f"{'='*70}")

    # Select features based on config
    feature_cols = select_features_by_config(config)

    print(f"Number of features: {len(feature_cols)}")
    if feature_cols:
        print(f"Features: {', '.join(feature_cols[:5])}{'...' if len(feature_cols) > 5 else ''}")
    else:
        print("Features: None (baseline predictor)")

    # Prepare features
    X_train, y_train = prepare_features_custom(training_data, feature_cols)
    X_test, y_test = prepare_features_custom(testing_data, feature_cols)

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Train and evaluate
    metrics = train_and_evaluate(X_train, y_train, X_test, y_test, config['name'])

    # Print results
    print(f"\nResults:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  F1-Macro:  {metrics['f1_macro']:.4f}")
    print(f"  F1-H:      {metrics['f1_H']:.4f}")
    print(f"  F1-D:      {metrics['f1_D']:.4f}")
    print(f"  F1-A:      {metrics['f1_A']:.4f}")
    print(f"  Train Time: {metrics['train_time']:.2f}s")

    # Store configuration info
    results = {
        'exp_id': exp_id,
        'name': config['name'],
        'n_features': len(feature_cols),
        'features': feature_cols,
        **metrics
    }

    return results


def run_all_experiments():
    """Run all ablation experiments and save results"""

    print("="*70)
    print("EPL ABLATION STUDY")
    print("="*70)

    # Load data
    print(f"\nLoading data from {DATA_PATH}...")
    data = load_data(DATA_PATH)
    print(f"Loaded {len(data)} matches")

    # Split data temporally
    print(f"\nSplitting data (test_size={TEST_SIZE})...")
    training_data, testing_data = temporal_train_test_split(data, test_size=TEST_SIZE)

    # Run all experiments
    all_results = []

    for exp_id in ABLATION_CONFIGS.keys():
        results = run_ablation_experiment(exp_id, training_data, testing_data)
        all_results.append(results)

    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)

    # Save detailed results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results_csv_path = os.path.join(RESULTS_DIR, 'ablation_results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"\n\nDetailed results saved to: {results_csv_path}")

    # Print summary table
    print("\n" + "="*70)
    print("ABLATION STUDY SUMMARY")
    print("="*70)
    print(f"\n{'Exp ID':<10} {'Name':<45} {'#Feat':<7} {'Acc':<7} {'F1':<7}")
    print("-"*80)

    for _, row in results_df.iterrows():
        print(f"{row['exp_id']:<10} {row['name']:<45} {row['n_features']:<7} "
              f"{row['accuracy']:.4f}  {row['f1_macro']:.4f}")

    # Find baseline (EXP-0)
    baseline = results_df[results_df['exp_id'] == 'EXP-0'].iloc[0]

    # Calculate performance drops for Phase 2 experiments
    print("\n" + "="*70)
    print("FEATURE GROUP IMPORTANCE (Performance Drop When Removed)")
    print("="*70)

    ablation_exps = ['EXP-1', 'EXP-2', 'EXP-3', 'EXP-4', 'EXP-5']
    ablation_names = {
        'EXP-1': 'Team Form (Groups 2a+2b)',
        'EXP-2': 'Match Dynamics (Group 3)',
        'EXP-3': 'Discipline (Group 4)',
        'EXP-4': 'Previous Rank (Group 5a)',
        'EXP-5': 'Squad Quality (Group 5b)'
    }

    importance_data = []
    for exp_id in ablation_exps:
        exp_row = results_df[results_df['exp_id'] == exp_id].iloc[0]
        delta_acc = baseline['accuracy'] - exp_row['accuracy']
        delta_f1 = baseline['f1_macro'] - exp_row['f1_macro']
        importance_data.append({
            'group': ablation_names[exp_id],
            'delta_acc': delta_acc,
            'delta_f1': delta_f1
        })

    # Sort by delta_acc
    importance_data.sort(key=lambda x: x['delta_acc'], reverse=True)

    print(f"\n{'Rank':<6} {'Feature Group':<40} {'ΔAcc':<10} {'ΔF1':<10}")
    print("-"*70)
    for i, item in enumerate(importance_data, 1):
        print(f"{i:<6} {item['group']:<40} {item['delta_acc']:>+.4f}    {item['delta_f1']:>+.4f}")

    return results_df


if __name__ == "__main__":
    results = run_all_experiments()

    print("\n" + "="*70)
    print("ABLATION STUDY COMPLETED")
    print("="*70)
    print("\nResults saved to ../results/ablation/ablation_results.csv")
    print("Next step: Generate visualizations and write report")