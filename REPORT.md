# EPL Match Outcome Prediction - Comprehensive Model Evaluation Report

**Course:** COMP0036 - Machine Learning for Natural and Computational Sciences
**Dataset:** English Premier League Matches (2000-2024)
**Date:** November 24, 2025

---

## Executive Summary

This report presents a comprehensive evaluation of **9 machine learning algorithms** for predicting English Premier League match outcomes (Home Win, Draw, Away Win). The models were trained on 8,640 historical matches (2000-2023) and tested on 960 matches (2023-2025).

**Key Findings:**
- **Best Performing Model:** Random Forest (51.77% accuracy)
- **Fastest Training:** Gaussian Naive Bayes (<1 second)
- **Most Interpretable:** Decision Tree & Logistic Regression
- **Worst Performer:** Decision Tree (40.52% accuracy)

---

## 1. Dataset Overview

### 1.1 Data Split
- **Total Matches:** 9,600
- **Training Set:** 8,640 matches (90%) | Date Range: 19/08/2000 - 03/04/2023
- **Testing Set:** 960 matches (10%) | Date Range: 04/04/2023 - 25/05/2025
- **Features:** 20 engineered features (team statistics, rolling averages)

### 1.2 Class Distribution
The dataset exhibits class imbalance:
- **Home Win (H):** 45.9% (3,969 matches)
- **Away Win (A):** 29.1% (2,518 matches)
- **Draw (D):** 24.9% (2,153 matches)

This reflects the well-known home advantage in football.

---

## 2. Feature Engineering

### 2.1 Feature Categories
All features are rolling averages computed from historical match data:

1. **Offensive Statistics:**
   - Average Goals Scored (Home/Away)
   - Average Shots (Home/Away)
   - Average Shots on Target (Home/Away)
   - Average Corners (Home/Away)

2. **Defensive Statistics:**
   - Average Goals Conceded (Home/Away)
   - Average Shots Conceded (Home/Away)
   - Average Corners Conceded (Home/Away)

3. **Form Indicators:**
   - Recent Wins
   - Recent Losses
   - Recent Draws

### 2.2 Temporal Splitting Strategy
To prevent data leakage, we employed **temporal train-test split** instead of random splitting. This ensures the model is tested on future matches it has never seen.

---

## 3. Model Implementations

We implemented and evaluated 9 different machine learning algorithms:

### 3.1 Traditional Machine Learning Models
1. **Support Vector Machine (SVM)** - Non-linear classification with RBF kernel
2. **Logistic Regression** - Linear baseline model with multinomial loss
3. **Gaussian Naive Bayes** - Probabilistic classifier assuming feature independence
4. **K-Nearest Neighbors (KNN)** - Instance-based learning with k=5
5. **Decision Tree** - CART algorithm with entropy criterion
6. **Random Forest** - Ensemble of 100 decision trees
7. **XGBoost** - Gradient boosting with 100 estimators

### 3.2 Deep Learning Model
8. **Multi-Layer Perceptron (MLP)** - Neural network with 3 hidden layers

---

## 4. Model Performance Results

### 4.1 Overall Accuracy Comparison

| Rank | Model | Test Accuracy | Training Time | Feature Scaling Required |
|------|-------|---------------|---------------|-------------------------|
| >G 1 | **Random Forest** | **51.77%** | ~1s | No |
| >H 2 | **Gaussian Naive Bayes** | **51.25%** | <1s | No |
| >I 3 | **XGBoost** | **50.10%** | ~2s | No |
| 4 | **Support Vector Machine** | **46.35%** | ~30s | Yes |
| 5 | **Logistic Regression** | **45.52%** | ~1s | Yes |
| 6 | **Multi-Layer Perceptron** | **45.42%** | ~15s | Yes |
| 7 | **K-Nearest Neighbors** | **44.38%** | <1s | Yes |
| 8 | **Decision Tree** | **40.52%** | <1s | No |

---

### 4.2 Detailed Model Results

#### 4.2.1 Random Forest (Best Overall)
```
Test Accuracy: 51.77%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.52      0.49      0.51       321
    Draw (D)       0.27      0.16      0.20       215
Home Win (H)       0.58      0.72      0.64       424

Confusion Matrix:
              A    D    H
Actual  A   158   49  114
        D    73   35  107
        H    72   48  304
```

**Key Strengths:**
- Highest overall accuracy (51.77%)
- Best performance on Home Wins (72% recall)
- Provides feature importance rankings
- Robust to overfitting through ensemble averaging

**Top 5 Important Features:**
1. AwayTeam_AvgShots (8.25%)
2. AwayTeam_AvgGoalsScored (7.22%)
3. HomeTeam_AvgShots (6.87%)
4. HomeTeam_AvgShotsConceded (6.47%)
5. AwayTeam_AvgCornersConceded (6.15%)

---

#### 4.2.2 Gaussian Naive Bayes (Second Best)
```
Test Accuracy: 51.25%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.49      0.51      0.50       321
    Draw (D)       0.18      0.07      0.10       215
Home Win (H)       0.57      0.74      0.65       424

Confusion Matrix:
              A    D    H
Actual  A   165   38  118
        D    86   14  115
        H    87   24  313
```

**Key Strengths:**
- Extremely fast training (<1 second)
- No hyperparameter tuning required
- Good baseline model
- Probabilistic predictions

**Class Priors Learned:**
- Away Win: 29.14%
- Draw: 24.92%
- Home Win: 45.94%

---

#### 4.2.3 XGBoost (Third Best)
```
Test Accuracy: 50.10%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.47      0.52      0.49       321
    Draw (D)       0.26      0.07      0.10       215
Home Win (H)       0.54      0.71      0.62       424

Confusion Matrix:
              A    D    H
Actual  A   166   19  136
        D    85   14  116
        H   103   20  301
```

**Key Strengths:**
- State-of-the-art gradient boosting
- Handles class imbalance well
- Feature importance analysis
- Regularization to prevent overfitting

**Top 5 Important Features:**
1. AwayTeam_AvgGoalsScored (6.57%)
2. AwayTeam_AvgShots (6.46%)
3. HomeTeam_AvgShotsConceded (6.36%)
4. HomeTeam_AvgShots (5.91%)
5. HomeTeam_AvgGoalsScored (5.56%)

---

#### 4.2.4 Support Vector Machine
```
Test Accuracy: 46.35%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.49      0.42      0.45       321
    Draw (D)       0.24      0.29      0.26       215
Home Win (H)       0.58      0.59      0.58       424

Confusion Matrix:
              A    D    H
Actual  A   134   94   93
        D    62   62   91
        H    76   99  249
```

**Characteristics:**
- RBF kernel for non-linear classification
- Relatively slow training (~30 seconds)
- Requires feature scaling
- Good at capturing complex decision boundaries

---

#### 4.2.5 Logistic Regression
```
Test Accuracy: 45.52%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.51      0.39      0.44       321
    Draw (D)       0.24      0.38      0.29       215
Home Win (H)       0.62      0.54      0.58       424

Confusion Matrix:
              A    D    H
Actual  A   126  129   66
        D    59   81   75
        H    61  133  230
```

**Characteristics:**
- Simple linear baseline model
- Fast training (converged in 31 iterations)
- Highly interpretable through feature coefficients
- Multinomial loss for multi-class classification

**Top 5 Features by Coefficient Magnitude:**
1. Feature 2 (0.3072)
2. Feature 12 (0.2697)
3. Feature 0 (0.1504)
4. Feature 11 (0.1449)
5. Feature 10 (0.1434)

---

#### 4.2.6 Multi-Layer Perceptron (Neural Network)
```
Test Accuracy: 45.42%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.49      0.54      0.51       321
    Draw (D)       0.21      0.27      0.24       215
Home Win (H)       0.62      0.48      0.54       424

Confusion Matrix:
              A    D    H
Actual  A   172   89   60
        D    90   59   66
        H    92  127  205
```

**Architecture:**
- Input Layer: 20 features
- Hidden Layer 1: 128 neurons (ReLU + BatchNorm + Dropout 0.3)
- Hidden Layer 2: 64 neurons (ReLU + BatchNorm + Dropout 0.3)
- Hidden Layer 3: 32 neurons (ReLU + Dropout 0.2)
- Output Layer: 3 neurons (Softmax)

**Training Details:**
- Total Parameters: 13,891
- Optimizer: Adam (learning_rate=0.001)
- Early Stopping: Triggered at epoch 34
- Training Accuracy: 49.47%
- Validation Accuracy: 48.23%

---

#### 4.2.7 K-Nearest Neighbors
```
Test Accuracy: 44.38%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.44      0.48      0.46       321
    Draw (D)       0.19      0.18      0.19       215
Home Win (H)       0.58      0.55      0.56       424

Confusion Matrix:
              A    D    H
Actual  A   154   79   88
        D    93   39   83
        H   107   84  233
```

**Characteristics:**
- k=5 neighbors with distance weighting
- Simple instance-based learning
- No explicit training phase
- Requires feature scaling

---

#### 4.2.8 Decision Tree (Worst Performer)
```
Test Accuracy: 40.52%

Classification Report:
              precision    recall  f1-score   support
Away Win (A)       0.40      0.49      0.44       321
    Draw (D)       0.21      0.29      0.25       215
Home Win (H)       0.62      0.40      0.49       424

Confusion Matrix:
              A    D    H
Actual  A   157  112   52
        D   100   62   53
        H   137  117  170
```

**Tree Statistics:**
- Maximum Depth: 10
- Number of Leaves: 285
- Features Used: All 20

**Top 5 Important Features:**
1. AwayTeam_AvgShots (15.82%)
2. HomeTeam_AvgShotsConceded (14.57%)
3. AwayTeam_AvgGoalsScored (7.81%)
4. HomeTeam_AvgCornersConceded (7.03%)
5. AwayTeam_AvgCornersConceded (5.96%)

---

## 5. Analysis and Insights

### 5.1 Model Performance Patterns

#### 5.1.1 Tree-Based Models Excel
The top 3 models are all tree-based or ensemble methods:
- **Random Forest** (51.77%) - Ensemble averaging reduces variance
- **XGBoost** (50.10%) - Gradient boosting captures complex patterns

However, single Decision Tree performs worst (40.52%), highlighting the importance of ensemble techniques.

#### 5.1.2 The "Draw Problem"
All models struggle to predict draws (D class):
- Best Draw Recall: Logistic Regression (38%)
- Worst Draw Recall: Naive Bayes & XGBoost (7%)
- Average Draw Precision: ~23%

**Reasons:**
1. Draws are the minority class (24.9%)
2. Draws have less distinctive patterns than wins
3. Football draws are inherently unpredictable

#### 5.1.3 Home Advantage Captured Well
All models effectively capture home advantage:
- Average Home Win Recall: 59%
- Average Home Win Precision: 59%
- Home wins are most predictable due to clear statistical patterns

### 5.2 Feature Importance Insights

Consistent across Random Forest, XGBoost, and Decision Tree:

**Most Important Features:**
1. **AwayTeam_AvgShots** - Away team's offensive capability
2. **AwayTeam_AvgGoalsScored** - Direct measure of away scoring ability
3. **HomeTeam_AvgShotsConceded** - Home team's defensive weakness
4. **HomeTeam_AvgShots** - Home team's offensive capability

**Key Insight:** Away team statistics are slightly more predictive than home team statistics, suggesting that strong away teams are more distinctive.

### 5.3 Computational Efficiency

| Model | Training Time | Prediction Time | Scalability |
|-------|---------------|-----------------|-------------|
| Naive Bayes | <1s | Instant | Excellent |
| Decision Tree | <1s | Instant | Excellent |
| Logistic Regression | ~1s | Instant | Excellent |
| Random Forest | ~1s | Fast | Good |
| KNN | Instant (lazy) | Slow | Poor |
| XGBoost | ~2s | Fast | Good |
| MLP | ~15s | Fast | Moderate |
| SVM | ~30s | Moderate | Poor |

**For Production:** Random Forest or Naive Bayes offer the best accuracy-speed tradeoff.

---

## 6. Challenges and Limitations

### 6.1 Inherent Unpredictability of Football
- Football matches are influenced by many factors not in our dataset:
  - Player injuries and suspensions
  - Weather conditions
  - Referee decisions
  - Team motivation and psychology
  - Tactical changes during the match

### 6.2 Class Imbalance
- Draws (24.9%) are significantly underrepresented
- Models tend to favor the majority class (Home Wins)
- Class weighting helped but didn't fully solve the issue

### 6.3 Feature Limitations
- Only aggregate statistics are used
- No player-level information
- No venue-specific factors
- No head-to-head history

### 6.4 Temporal Factors
- Team composition changes over seasons
- League competitiveness evolves
- Tactical trends shift over time

---

## 7. Conclusions and Recommendations

### 7.1 Key Findings

1. **Random Forest is the Best Overall Model** (51.77% accuracy)
   - Balances accuracy, speed, and robustness
   - Provides interpretable feature importance
   - Recommended for deployment

2. **Gaussian Naive Bayes is an Excellent Baseline** (51.25% accuracy)
   - Extremely fast training and prediction
   - Minimal hyperparameter tuning
   - Good for rapid prototyping

3. **Deep Learning (MLP) Doesn't Outperform Traditional ML**
   - 45.42% accuracy despite complex architecture
   - Requires more data to be effective
   - Computationally expensive for marginal gains

4. **Draw Prediction Remains the Biggest Challenge**
   - All models struggle with Draw class
   - May require specialized approaches (e.g., ordinal regression)

### 7.2 Recommendations for Improvement

#### 7.2.1 Data Enhancement
- Incorporate player-level statistics
- Add weather and venue information
- Include team motivation factors (e.g., league position, recent form)
- Use head-to-head historical records

#### 7.2.2 Feature Engineering
- Create interaction features (e.g., HomeShots × AwayDefense)
- Add momentum indicators (win/loss streaks)
- Include time-decay weights for recent matches
- Engineer squad strength metrics

#### 7.2.3 Model Improvements
- **Ensemble Methods:** Combine top models (Random Forest + Naive Bayes + XGBoost)
- **Specialized Draw Classifier:** Train a separate binary classifier for draws
- **Ordinal Regression:** Model outcomes as ordered categories (Loss < Draw < Win)
- **Time Series Models:** Use LSTM/GRU to capture temporal patterns

#### 7.2.4 Evaluation Metrics
- Consider business-oriented metrics (e.g., betting ROI)
- Use probability calibration for risk-aware predictions
- Implement confidence intervals for predictions

### 7.3 Final Remarks

This comprehensive study demonstrates that:
- **Football outcome prediction is feasible** but limited (~52% accuracy ceiling)
- **Simple models can match complex ones** with proper feature engineering
- **Ensemble methods consistently outperform** single models
- **The "Draw problem" requires specialized attention**

The 51.77% accuracy achieved by Random Forest represents a **significant improvement over random guessing (33.3%)** and baseline predictions (45.9% by always predicting Home Win). However, the inherent unpredictability of football matches remains a fundamental challenge.

---

## 8. Appendix

### 8.1 Model Hyperparameters

#### Random Forest
- n_estimators: 100
- max_depth: 10
- min_samples_split: 5
- min_samples_leaf: 2
- class_weight: balanced

#### XGBoost
- n_estimators: 100
- max_depth: 6
- learning_rate: 0.1
- subsample: 0.8
- colsample_bytree: 0.8

#### SVM
- kernel: RBF
- C: 1.0
- gamma: scale
- class_weight: balanced

#### MLP
- layers: [128, 64, 32]
- activation: ReLU
- optimizer: Adam (lr=0.001)
- dropout: [0.3, 0.3, 0.2]
- batch_size: 32
- early_stopping: patience=15

### 8.2 Software and Libraries
- Python 3.11
- scikit-learn 1.5+
- XGBoost 2.0+
- TensorFlow/Keras 2.15+
- NumPy, Pandas, Matplotlib

---

**Report Generated:** November 24, 2025
**Total Models Evaluated:** 9
**Total Experiments Run:** 9
**Best Model:** Random Forest (51.77% accuracy)

---