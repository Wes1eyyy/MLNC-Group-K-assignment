# Data Directory

## Purpose
This directory contains all dataset files for the EPL match prediction project.

## Development Plan

### Directory Structure:

#### raw/
Contains original, unmodified data files:
- **epl-training.csv** - Historical EPL match data (2000-2024)
  - ~9,600 matches
  - Features: Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR, HTHG, HTAG, HTR, Referee, HS, AS, HST, AST, HC, AC, HF, AF, HY, AY, HR, AR
  - Target: FTR (Full Time Result: H/D/A)
  
- **epl-test.csv** - Test matches for prediction
  - 10 matches from January 31, 2026
  - Same feature structure as training (without FTR)
  - Need to predict FTR for submission
  
- **sample-submission.csv** - Format template for predictions
  - Shows required output format
  - Columns: Date, HomeTeam, AwayTeam, FTR

#### processed/
Contains transformed and feature-engineered datasets:

**Files to Create:**

1. **cleaned_training.csv**
   - Cleaned version of raw training data
   - Missing values handled
   - Data types corrected
   - Duplicates removed
   - Date parsed properly
   - Quality validated

2. **features_training.csv**
   - Training data with engineered features
   - Team statistics (win rates, averages)
   - Form features (rolling windows)
   - Head-to-head features
   - Time-based features
   - Ready for model training

3. **features_test.csv**
   - Test data with same features as training
   - Consistent feature engineering pipeline
   - Ready for predictions

4. **feature_descriptions.txt**
   - Documentation of all features
   - Feature name, type, description
   - How each feature was calculated
   - For reproducibility and report

## Data Dictionary

### Original Features:
- **Date**: Match date (DD/MM/YYYY)
- **HomeTeam**: Home team name
- **AwayTeam**: Away team name
- **FTHG**: Full Time Home Goals
- **FTAG**: Full Time Away Goals
- **FTR**: Full Time Result (H=Home Win, D=Draw, A=Away Win) - TARGET
- **HTHG**: Half Time Home Goals
- **HTAG**: Half Time Away Goals
- **HTR**: Half Time Result
- **Referee**: Match referee name
- **HS**: Home Shots
- **AS**: Away Shots
- **HST**: Home Shots on Target
- **AST**: Away Shots on Target
- **HC**: Home Corners
- **AC**: Away Corners
- **HF**: Home Fouls
- **AF**: Away Fouls
- **HY**: Home Yellow Cards
- **AY**: Away Yellow Cards
- **HR**: Home Red Cards
- **AR**: Away Red Cards

### Engineered Features (to be created):
See feature_engineering.py and notebooks for complete list.

## Data Usage Guidelines

1. **Never modify raw data files** - Keep originals intact
2. **Use temporal splits** - Don't shuffle when splitting train/test
3. **Avoid data leakage** - Only use past data for features
4. **Document transformations** - Keep track of all preprocessing
5. **Validate outputs** - Check processed data for errors

## Data Quality Notes

### Known Issues:
- Check for missing values in some matches
- Some early seasons may have less complete data
- Team names should be consistent across years
- Handle promoted/relegated teams appropriately

### Validation Checks:
- [ ] No negative values for counts (goals, shots, etc.)
- [ ] FTR matches FTHG vs FTAG relationship
- [ ] Dates are chronological
- [ ] No duplicate matches
- [ ] All teams in test set exist in training data

## Processing Pipeline

1. **Load raw data** → `data/raw/epl-training.csv`
2. **Clean data** → `data/processed/cleaned_training.csv`
3. **Engineer features** → `data/processed/features_training.csv`
4. **Apply to test** → `data/processed/features_test.csv`
5. **Train models** → Use features_training.csv
6. **Make predictions** → Use features_test.csv
7. **Create submission** → Format as sample-submission.csv
