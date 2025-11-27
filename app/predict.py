"""
Prediction script - Use trained Random Forest model to predict EPL test data
Usage: python predict.py
"""
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime

# Add utils directory to path
sys.path.append(os.path.dirname(__file__))
from utils.data_utils import load_data, prepare_features, process_single_match
from utils.model_utils import load_model

# Configuration
TRAINING_DATA_PATH = "../data/epl-training.csv"
TEST_DATA_PATH = "../data/epl-test.csv"
MODEL_PATH = "../models/random_forest_model.pkl"
OUTPUT_PATH = "../data/predictions.csv"


def convert_date_format(date_str):
    """
    Convert date from '31 Jan 26' format to 'DD/MM/YYYY' format

    Args:
        date_str: Date string in format 'DD Mon YY'

    Returns:
        Date string in format 'DD/MM/YYYY'
    """
    # Parse the date (e.g., '31 Jan 26')
    date = datetime.strptime(date_str, '%d %b %y')

    # Convert to DD/MM/YYYY format
    return date.strftime('%d/%m/%Y')


def prepare_test_data(test_data, training_data):
    """
    Prepare features for test data

    Args:
        test_data: Test data (only Date, HomeTeam, AwayTeam)
        training_data: Historical training data (used to calculate features)

    Returns:
        test_enriched: Test data with calculated features
    """
    print("\nPreparing test data features...")

    # Add placeholder values for required fields
    # These are needed for feature calculation but won't affect the predictions
    test_data_with_placeholder = []
    for match in test_data:
        match_copy = match.copy()
        # Add all required fields (set to 0 or placeholder values)
        match_copy['FTHG'] = 0
        match_copy['FTAG'] = 0
        match_copy['FTR'] = 'H'  # Temporary value, doesn't affect feature calculation
        match_copy['HTHG'] = 0
        match_copy['HTAG'] = 0
        match_copy['HTR'] = 'H'
        match_copy['Referee'] = 'Unknown'
        match_copy['HS'] = 0
        match_copy['AS'] = 0
        match_copy['HST'] = 0
        match_copy['AST'] = 0
        match_copy['HC'] = 0
        match_copy['AC'] = 0
        match_copy['HF'] = 0
        match_copy['AF'] = 0
        match_copy['HY'] = 0
        match_copy['AY'] = 0
        match_copy['HR'] = 0
        match_copy['AR'] = 0
        test_data_with_placeholder.append(match_copy)

    # Combine training and test data for feature calculation
    combined_data = training_data + test_data_with_placeholder

    print(f"Combined data: {len(combined_data)} matches")
    print(f"Training data: {len(training_data)} matches")
    print(f"Test data: {len(test_data)} matches")

    # Calculate features for test data (based on historical data)
    test_enriched = []
    for i, test_match in enumerate(test_data_with_placeholder):
        enriched_match = process_single_match((test_match, combined_data))
        test_enriched.append(enriched_match)

    print(f"Test data features calculated!")

    return test_enriched


def main():
    """Main prediction pipeline"""
    print("=" * 60)
    print("EPL Match Outcome Prediction - Random Forest Model")
    print("=" * 60)

    # 1. Load training data (for calculating test features)
    print("\nStep 1: Loading historical training data...")
    training_data = load_data(TRAINING_DATA_PATH)
    print(f"Loaded {len(training_data)} historical matches")

    # 2. Load test data
    print("\nStep 2: Loading test data...")
    test_data = load_data(TEST_DATA_PATH)
    print(f"Loaded {len(test_data)} test matches")

    # Convert date format from '31 Jan 26' to 'DD/MM/YYYY'
    print("Converting date format...")
    original_dates = []  # Store original dates for submission file
    for match in test_data:
        original_dates.append(match['Date'])
        match['Date'] = convert_date_format(match['Date'])

    # Display test matches
    print("\nTest matches:")
    for i, match in enumerate(test_data, 1):
        print(f"  {i}. {match['Date']:12s} {match['HomeTeam']:20s} vs {match['AwayTeam']:20s}")

    # 3. Prepare test data features
    print("\nStep 3: Calculating features for test data...")
    test_enriched = prepare_test_data(test_data, training_data)

    # 4. Extract feature matrix
    print("\nStep 4: Extracting feature matrix...")
    X_test, _, feature_names = prepare_features(test_enriched)
    print(f"Feature matrix shape: {X_test.shape}")
    print(f"Number of features: {len(feature_names)}")

    # 5. Load Random Forest model
    print("\nStep 5: Loading Random Forest model...")
    model, scaler = load_model(MODEL_PATH)
    print("Model loaded successfully!")

    # 6. Make predictions
    print("\nStep 6: Predicting match outcomes...")
    predictions = model.predict(X_test)

    # Get prediction probabilities
    prediction_probabilities = model.predict_proba(X_test)

    # 7. Display prediction results
    print("\n" + "=" * 80)
    print("Prediction Results")
    print("=" * 80)
    print(f"{'No.':<4} {'Date':<12} {'Home Team':<20} {'Away Team':<20} {'Prediction':<12} {'Confidence':<10}")
    print("-" * 80)

    for i, (match, pred, prob) in enumerate(zip(test_data, predictions, prediction_probabilities), 1):
        # Get probability of predicted class
        pred_idx = list(model.classes_).index(pred)
        confidence = prob[pred_idx] * 100

        # Map prediction to description
        result_map = {
            'H': 'Home Win',
            'D': 'Draw',
            'A': 'Away Win'
        }

        print(f"{i:<4} {match['Date']:<12} {match['HomeTeam']:<20} {match['AwayTeam']:<20} "
              f"{result_map[pred]:<12} {confidence:>6.2f}%")

    # 8. Save predictions to submission file
    print("\nStep 7: Saving predictions...")

    # Create submission data (use original date format)
    submission_data = []
    for orig_date, match, pred in zip(original_dates, test_data, predictions):
        submission_data.append({
            'Date': orig_date,  # Use original date format for submission
            'HomeTeam': match['HomeTeam'],
            'AwayTeam': match['AwayTeam'],
            'FTR': pred
        })

    # Save as CSV
    df = pd.DataFrame(submission_data)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Predictions saved to: {OUTPUT_PATH}")

    # 9. Display prediction statistics
    print("\n" + "=" * 60)
    print("Prediction Statistics")
    print("=" * 60)
    unique, counts = np.unique(predictions, return_counts=True)
    result_map = {'H': 'Home Win', 'D': 'Draw', 'A': 'Away Win'}
    for label, count in zip(unique, counts):
        print(f"{result_map[label]}: {count} matches ({count/len(predictions)*100:.1f}%)")

    print("\n" + "=" * 60)
    print("Prediction completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()