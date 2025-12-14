# Ablation Study Plan - EPL Match Outcome Prediction

## Objective
Systematically analyze the contribution of different feature groups to model performance by removing or adding features, identify critical features, and optimize the model architecture.

---

## Feature Grouping

Based on the current `epl-features-training.csv`, features are divided into the following groups:

### Group 1: Match Statistics (Real-time) - 12 features
**Available only during/after the match - NOT used for pre-match prediction**
- `HS, AS` - Home/Away Shots
- `HST, AST` - Home/Away Shots on Target
- `HC, AC` - Home/Away Corners
- `HF, AF` - Home/Away Fouls
- `HY, AY` - Home/Away Yellow Cards
- `HR, AR` - Home/Away Red Cards

**Note**: These features should be excluded for future match prediction.

---

### Group 2: Team Form & Performance - 10 features
**Rolling statistics based on historical data**

#### 2a. Win/Loss Record (6 features)
- `HomeTeam_Wins, HomeTeam_Draws, HomeTeam_Losses`
- `AwayTeam_Wins, AwayTeam_Draws, AwayTeam_Losses`

#### 2b. Goal Statistics (4 features)
- `HomeTeam_AvgGoalsScored, HomeTeam_AvgGoalsConceded`
- `AwayTeam_AvgGoalsScored, AwayTeam_AvgGoalsConceded`

---

### Group 3: Match Dynamics - 8 features
**Offensive/Defensive capability indicators**
- `HomeTeam_AvgShots, HomeTeam_AvgShotsConceded`
- `AwayTeam_AvgShots, AwayTeam_AvgShotsConceded`
- `HomeTeam_AvgCorners, HomeTeam_AvgCornersConceded`
- `AwayTeam_AvgCorners, AwayTeam_AvgCornersConceded`

---

### Group 4: Discipline - 2 features
**Team discipline indicators**
- `HomeTeam_AvgFouls`
- `AwayTeam_AvgFouls`

---

### Group 5: Squad Quality Indicators - 6 features
**External metrics of team strength**

#### 5a. Previous Season Ranking (2 features)
- `HomeTeam_PrevSeasonRank`
- `AwayTeam_PrevSeasonRank`

#### 5b. Squad Age & Market Value (4 features)
- `HomeTeam_AvgAge, HomeTeam_AvgValue`
- `AwayTeam_AvgAge, AwayTeam_AvgValue`

---

## Experimental Design

### Phase 1: Baseline Establishment
| Exp ID | Description | Features Used | Purpose |
|--------|-------------|---------------|---------|
| **EXP-0** | **Full Model** | All features (Groups 2-5) | **Baseline performance** |
| **EXP-0a** | **Minimal Baseline** | Team names + Referee only | Lower bound performance |

---

### Phase 2: Individual Group Ablation
**Remove one feature group at a time from the full model**

| Exp ID | Removed Group | Features Removed (Count) | Hypothesis |
|--------|---------------|--------------------------|------------|
| **EXP-1** | Group 2 (Team Form) | Win/Loss + Goals (10) | Significant drop expected - core features |
| **EXP-2** | Group 3 (Match Dynamics) | Shots/Corners stats (8) | Moderate impact - reflects attack/defense quality |
| **EXP-3** | Group 4 (Discipline) | Fouls stats (2) | Minor impact - secondary factor |
| **EXP-4** | Group 5a (Prev Rank) | Previous season rank (2) | Moderate impact - historical strength |
| **EXP-5** | Group 5b (Squad Quality) | Age + Market Value (4) | Test value of newly added features |

---

### Phase 3: Cumulative Addition
**Start from minimal baseline and progressively add feature groups**

| Exp ID | Added Groups | Total Feature Groups | Purpose |
|--------|--------------|----------------------|---------|
| **EXP-6** | Baseline + Group 2 | Win/Loss + Goals | Test if core features are sufficient |
| **EXP-7** | EXP-6 + Group 3 | + Match Dynamics | Measure incremental value of dynamics |
| **EXP-8** | EXP-7 + Group 5a | + Previous Rank | Check if historical rank is redundant |
| **EXP-9** | EXP-8 + Group 5b | + Squad Quality | Full feature set benefit |
| **EXP-10** | EXP-6 + Group 5b | Form + Squad Quality (skip dynamics) | Test if middle layer can be omitted |

---

### Phase 4: Feature Subgroup Analysis
**Fine-grained testing of important feature groups**

| Exp ID | Description | Features Tested | Purpose |
|--------|-------------|-----------------|---------|
| **EXP-11** | Win/Loss Only | Wins, Draws, Losses only | Is record sufficient? |
| **EXP-12** | Goals Only | AvgGoalsScored/Conceded only | Are goals sufficient? |
| **EXP-13** | Win/Loss + Goals | Complete Group 2 | Validate combination effect |
| **EXP-14** | Goals + Squad Value | Cross-group interaction | Test feature synergy |
| **EXP-15** | Shots vs Corners | Shots only vs Corners only | Compare attack indicators |

---

### Phase 5: Cross-Model Validation
**Repeat key experiments across different algorithms**

| Exp ID | Model | Configuration | Purpose |
|--------|-------|---------------|---------|
| **EXP-16** | Logistic Regression | EXP-0 vs EXP-1 vs EXP-6 | Linear model feature sensitivity |
| **EXP-17** | XGBoost | Same as above | Tree model feature importance |
| **EXP-18** | Random Forest | Same as above | Ensemble model stability |
| **EXP-19** | MLP | Same as above | Neural network feature learning |

---

## Evaluation Metrics

### Primary Metrics
1. **Accuracy** - Overall classification accuracy
2. **F1-Score (Macro)** - Account for class imbalance
3. **Per-Class F1** - Performance on H/D/A separately

### Secondary Metrics
4. **Confusion Matrix** - Analyze misclassification patterns
5. **Training Time** - Impact of feature count on efficiency
6. **Feature Importance** - (For tree models) Validate ablation conclusions

---

## Automation Script Architecture

### File Structure
```
app/
├── ablation_study.py           # Main ablation script
├── configs/
│   └── ablation_configs.yaml   # Experiment configurations
├── results/
│   ├── ablation_results.csv    # Numeric results
│   └── ablation_plots/         # Visualizations
└── utils/
    └── feature_selector.py     # Feature group selection
```

### Core Implementation
```python
# ablation_study.py

ABLATION_CONFIGS = {
    'EXP-0': {
        'name': 'Full Model',
        'exclude_groups': [],
        'include_groups': ['2a', '2b', '3', '4', '5a', '5b']
    },
    'EXP-1': {
        'name': 'Ablate Team Form',
        'exclude_groups': ['2a', '2b'],
        'include_groups': ['3', '4', '5a', '5b']
    },
    # ... more configurations
}

def run_ablation_experiment(exp_id, model_type='random_forest'):
    """
    Run a single ablation experiment

    Args:
        exp_id: Experiment identifier (e.g., 'EXP-0')
        model_type: Model to train

    Returns:
        dict: Evaluation metrics
    """
    config = ABLATION_CONFIGS[exp_id]

    # 1. Select features based on config
    features = select_features_by_config(config)

    # 2. Load data and prepare features
    X_train, y_train, X_test, y_test = load_and_prepare_data(features)

    # 3. Train model
    model = train_model(X_train, y_train, model_type)

    # 4. Evaluate
    results = evaluate_model(model, X_test, y_test)

    # 5. Log results
    log_results(exp_id, config['name'], features, results)

    return results


def run_all_experiments(model_type='random_forest'):
    """Run all ablation experiments and generate report"""
    results_all = {}

    for exp_id in ABLATION_CONFIGS.keys():
        print(f"\n{'='*60}")
        print(f"Running {exp_id}: {ABLATION_CONFIGS[exp_id]['name']}")
        print(f"{'='*60}")

        results = run_ablation_experiment(exp_id, model_type)
        results_all[exp_id] = results

    # Generate comparison report
    generate_report(results_all)
    generate_visualizations(results_all)

    return results_all
```

### Feature Selection Function
```python
# utils/feature_selector.py

FEATURE_GROUPS = {
    '2a': ['HomeTeam_Wins', 'HomeTeam_Draws', 'HomeTeam_Losses',
           'AwayTeam_Wins', 'AwayTeam_Draws', 'AwayTeam_Losses'],
    '2b': ['HomeTeam_AvgGoalsScored', 'HomeTeam_AvgGoalsConceded',
           'AwayTeam_AvgGoalsScored', 'AwayTeam_AvgGoalsConceded'],
    '3': ['HomeTeam_AvgShots', 'HomeTeam_AvgShotsConceded',
          'AwayTeam_AvgShots', 'AwayTeam_AvgShotsConceded',
          'HomeTeam_AvgCorners', 'HomeTeam_AvgCornersConceded',
          'AwayTeam_AvgCorners', 'AwayTeam_AvgCornersConceded'],
    '4': ['HomeTeam_AvgFouls', 'AwayTeam_AvgFouls'],
    '5a': ['HomeTeam_PrevSeasonRank', 'AwayTeam_PrevSeasonRank'],
    '5b': ['HomeTeam_AvgAge', 'HomeTeam_AvgValue',
           'AwayTeam_AvgAge', 'AwayTeam_AvgValue']
}

def select_features_by_config(config):
    """
    Select features based on include/exclude groups

    Args:
        config: dict with 'include_groups' or 'exclude_groups'

    Returns:
        list: Feature column names to use
    """
    if 'include_groups' in config:
        selected = []
        for group_id in config['include_groups']:
            selected.extend(FEATURE_GROUPS[group_id])
        return selected

    elif 'exclude_groups' in config:
        all_features = []
        for features in FEATURE_GROUPS.values():
            all_features.extend(features)

        excluded = []
        for group_id in config['exclude_groups']:
            excluded.extend(FEATURE_GROUPS[group_id])

        return [f for f in all_features if f not in excluded]
```

---

## Expected Outputs

### 1. Performance Comparison Table
```
| Exp ID | Name              | #Features | Accuracy | F1-Macro | F1-H  | F1-D  | F1-A  | Time(s) |
|--------|-------------------|-----------|----------|----------|-------|-------|-------|---------|
| EXP-0  | Full Model        | 26        | 0.XXX    | 0.XXX    | 0.XXX | 0.XXX | 0.XXX | XX.X    |
| EXP-1  | w/o Team Form     | 16        | 0.XXX ↓  | 0.XXX ↓  | ...   | ...   | ...   | XX.X    |
| EXP-2  | w/o Match Dyn     | 18        | 0.XXX ↓  | 0.XXX ↓  | ...   | ...   | ...   | XX.X    |
| EXP-3  | w/o Discipline    | 24        | 0.XXX    | 0.XXX    | ...   | ...   | ...   | XX.X    |
| EXP-4  | w/o Prev Rank     | 24        | 0.XXX ↓  | 0.XXX ↓  | ...   | ...   | ...   | XX.X    |
| EXP-5  | w/o Squad Quality | 22        | 0.XXX ↓  | 0.XXX ↓  | ...   | ...   | ...   | XX.X    |
| ...    | ...               | ...       | ...      | ...      | ...   | ...   | ...   | ...     |
```

### 2. Feature Group Importance Ranking
```
Feature Group Contribution Analysis:
=====================================
1. Group 2 (Team Form): ΔAccuracy = -8.5%, ΔF1 = -9.2%
   → CRITICAL: Core predictor of match outcomes

2. Group 3 (Match Dynamics): ΔAccuracy = -3.2%, ΔF1 = -3.8%
   → IMPORTANT: Reflects offensive/defensive quality

3. Group 5b (Squad Quality): ΔAccuracy = -1.8%, ΔF1 = -2.1%
   → MODERATE: Valuable external indicators

4. Group 5a (Previous Rank): ΔAccuracy = -1.2%, ΔF1 = -1.5%
   → MODERATE: Captures historical strength

5. Group 4 (Discipline): ΔAccuracy = -0.3%, ΔF1 = -0.4%
   → MINIMAL: Negligible impact
```

### 3. Visualizations

#### A. Performance Comparison Bar Chart
```
Accuracy across experiments
     EXP-0  ████████████████████ 0.XXX
     EXP-1  ████████████░░░░░░░░ 0.XXX (-X.X%)
     EXP-2  ██████████████████░░ 0.XXX (-X.X%)
     EXP-3  ███████████████████░ 0.XXX (-X.X%)
     ...
```

#### B. Feature Addition Curve (Phase 3)
```
      Accuracy
        ^
        |                    EXP-9 (Full)
   0.XX |                  ●
        |                ／
   0.XX |              ●  EXP-8
        |            ／
   0.XX |          ●  EXP-7
        |        ／
   0.XX |      ●  EXP-6 (Form only)
        |    ／
   0.XX |  ●  EXP-0a (Baseline)
        +─────────────────────────────>
           0   10   20   30  (# Features)
```

#### C. Cross-Model Heatmap (Phase 5)
```
                    Logistic    XGBoost    RandomForest    MLP
EXP-0 (Full)         0.XXX       0.XXX        0.XXX       0.XXX
EXP-1 (w/o Form)     0.XXX       0.XXX        0.XXX       0.XXX
EXP-6 (Form only)    0.XXX       0.XXX        0.XXX       0.XXX
```

---

## Execution Timeline

### Week 1: Infrastructure & Baseline (Phase 1)
**Tasks:**
- [ ] Implement `ablation_study.py` script
- [ ] Create `feature_selector.py` module
- [ ] Set up automated logging system
- [ ] Run EXP-0 and EXP-0a

**Deliverables:**
- Working ablation framework
- Baseline performance metrics

---

### Week 2: Core Ablation Experiments (Phase 2)
**Tasks:**
- [ ] Run EXP-1 through EXP-5 (single group ablation)
- [ ] Analyze performance drops
- [ ] Rank feature groups by importance

**Deliverables:**
- Phase 2 results table
- Initial feature importance ranking

---

### Week 3: Progressive & Fine-grained Analysis (Phase 3-4)
**Tasks:**
- [ ] Run EXP-6 through EXP-10 (cumulative addition)
- [ ] Run EXP-11 through EXP-15 (subgroup analysis)
- [ ] Identify optimal feature subset
- [ ] Generate visualizations

**Deliverables:**
- Complete ablation results
- Feature addition curve
- Optimal feature configuration

---

### Week 4: Cross-Model Validation & Reporting (Phase 5)
**Tasks:**
- [ ] Run EXP-16 through EXP-19 (multi-model tests)
- [ ] Generate cross-model comparison
- [ ] Write ablation study section for report
- [ ] Create presentation slides

**Deliverables:**
- Final ablation study report
- Model comparison analysis
- Recommendations for deployment

---

## Key Research Questions

### RQ1: Which feature groups contribute most to prediction accuracy?
**Relevant Experiments**: EXP-1 through EXP-5
**Method**: Measure ΔAccuracy when removing each group
**Expected Outcome**: Team Form (Group 2) has largest impact

---

### RQ2: Is there feature redundancy across groups?
**Relevant Experiments**: EXP-10, EXP-14, EXP-15
**Method**: Test if certain groups can substitute for others
**Expected Outcome**: Squad Quality may partially substitute for Form

---

### RQ3: Do newly added features (Age/Value) justify data collection costs?
**Relevant Experiments**: EXP-5, EXP-9 vs EXP-8
**Method**: Compare models with/without Squad Quality features
**Expected Outcome**: Moderate improvement (1-2% accuracy gain)

---

### RQ4: What is the minimal feature set for near-optimal performance?
**Relevant Experiments**: EXP-6 through EXP-10
**Method**: Progressive addition from baseline
**Expected Outcome**: Form + Match Dynamics achieves 95% of full model performance

---

### RQ5: Are feature importance patterns consistent across model types?
**Relevant Experiments**: EXP-16 through EXP-19
**Method**: Replicate key experiments on 4 different models
**Expected Outcome**: Tree models may handle raw features better than linear models

---

## Experimental Controls

### ✅ Controlled Variables
- **Data Split**: Same temporal train/test split across all experiments
- **Random Seed**: `random_state=42` for reproducibility
- **Model Hyperparameters**: Same initial config (Phase 1-4)
- **Evaluation Metrics**: Consistent metric calculation
- **Preprocessing**: Same scaling/encoding procedures

### ⚠️ Data Leakage Prevention
- **Exclude Group 1**: Match statistics are real-time data (not predictive)
- **Temporal Validation**: Features use only pre-match historical data
- **No Future Information**: Rolling stats computed chronologically

### 📊 Result Validation
- **Significance Testing**: Use paired t-test for accuracy differences
- **Confidence Intervals**: Report 95% CI for key metrics
- **Stability Check**: Run critical experiments 5 times with different seeds

---

## Report Integration

### Ablation Study Section Structure

#### 1. Introduction
```
To understand the relative importance of different feature categories,
we conducted a comprehensive ablation study. We systematically removed
or added feature groups while measuring the impact on model performance.
```

#### 2. Methodology
```
We divided features into five groups: Team Form (win/loss records and
goals), Match Dynamics (shots and corners), Discipline (fouls), Previous
Season Rank, and Squad Quality (age and market value). We performed
three types of experiments: (1) removing one group at a time from the
full model, (2) progressively adding groups to a minimal baseline, and
(3) testing fine-grained feature subsets.
```

#### 3. Results
```
Table X shows the ablation study results. Removing Team Form features
(Group 2) caused the largest performance drop (ΔAccuracy = -8.5%,
ΔF1 = -9.2%), confirming these are the core predictors. Match Dynamics
features contributed moderately (ΔAccuracy = -3.2%), while Discipline
features had minimal impact (ΔAccuracy = -0.3%).

[Insert Performance Comparison Table]

Progressive addition experiments (Figure Y) revealed that Team Form
features alone achieve 85% of the full model's performance, with Match
Dynamics adding another 10%.

[Insert Feature Addition Curve]
```

#### 4. Discussion
```
The ablation study reveals that a minimal feature set of Team Form +
Match Dynamics achieves 95% of the full model's performance while using
only 18/26 features. Newly added Squad Quality features provide a modest
but significant improvement (ΔAccuracy = +1.8%), suggesting they are
worth collecting despite additional data acquisition costs.

Cross-model validation (EXP-16-19) shows that Random Forest and XGBoost
are less sensitive to feature selection than linear models, maintaining
higher performance even with reduced feature sets.
```

---

## Statistical Analysis

### Significance Testing
```python
from scipy.stats import ttest_rel

def test_significance(results_exp0, results_exp1, n_runs=5):
    """
    Test if performance difference is statistically significant

    Args:
        results_exp0: Array of accuracies from experiment 0 (full model)
        results_exp1: Array of accuracies from experiment 1 (ablated)
        n_runs: Number of repeated runs with different seeds

    Returns:
        p_value: Statistical significance
    """
    t_stat, p_value = ttest_rel(results_exp0, results_exp1)

    if p_value < 0.05:
        print(f"Performance difference is statistically significant (p={p_value:.4f})")
    else:
        print(f"Performance difference is NOT significant (p={p_value:.4f})")

    return p_value
```

---

## Appendix: Complete Feature List

### Baseline (Always Included)
- `Date` (temporal ordering)
- `HomeTeam` (encoded)
- `AwayTeam` (encoded)
- `Referee` (optional encoding)

### Group 2a: Win/Loss Record (6 features)
1. `HomeTeam_Wins`
2. `HomeTeam_Draws`
3. `HomeTeam_Losses`
4. `AwayTeam_Wins`
5. `AwayTeam_Draws`
6. `AwayTeam_Losses`

### Group 2b: Goal Statistics (4 features)
7. `HomeTeam_AvgGoalsScored`
8. `HomeTeam_AvgGoalsConceded`
9. `AwayTeam_AvgGoalsScored`
10. `AwayTeam_AvgGoalsConceded`

### Group 3: Match Dynamics (8 features)
11. `HomeTeam_AvgShots`
12. `HomeTeam_AvgShotsConceded`
13. `AwayTeam_AvgShots`
14. `AwayTeam_AvgShotsConceded`
15. `HomeTeam_AvgCorners`
16. `HomeTeam_AvgCornersConceded`
17. `AwayTeam_AvgCorners`
18. `AwayTeam_AvgCornersConceded`

### Group 4: Discipline (2 features)
19. `HomeTeam_AvgFouls`
20. `AwayTeam_AvgFouls`

### Group 5a: Previous Season Rank (2 features)
21. `HomeTeam_PrevSeasonRank`
22. `AwayTeam_PrevSeasonRank`

### Group 5b: Squad Quality (4 features)
23. `HomeTeam_AvgAge`
24. `HomeTeam_AvgValue`
25. `AwayTeam_AvgAge`
26. `AwayTeam_AvgValue`

**Total Features in Full Model**: 26

---

**Document Version**: 1.0
**Last Updated**: 2025-12-14
**Project**: EPL Match Outcome Prediction (COMP0036)
**Team**: MLNC Group K