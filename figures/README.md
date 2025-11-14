# Figures Directory

## Purpose
This directory stores all visualization outputs from data analysis, feature engineering, and model evaluation.

## Development Plan

### Directory Structure:

#### 1. **eda/** - Exploratory Data Analysis Figures
Files to create:
- `match_outcomes_distribution.png` - Bar chart of H/D/A distribution
- `goals_distribution.png` - Histogram of goals scored
- `home_vs_away_performance.png` - Home advantage analysis
- `correlation_heatmap.png` - Feature correlation matrix
- `shots_distribution.png` - Distribution of shots and shots on target
- `cards_over_time.png` - Yellow/red cards trends over seasons
- `team_performance_comparison.png` - Win rates by team
- `temporal_trends.png` - Goals and other metrics over time

#### 2. **feature_analysis/** - Feature Engineering Analysis
Files to create:
- `feature_correlations.png` - Correlation with target variable
- `top_features_importance.png` - Initial feature importance ranking
- `feature_distributions.png` - Distribution of engineered features
- `rolling_averages_example.png` - Example of rolling window features
- `head_to_head_analysis.png` - H2H matchup statistics
- `form_vs_outcome.png` - Recent form correlation with results

#### 3. **model_performance/** - Model Evaluation Figures
Files to create:
- `confusion_matrix_best_model.png` - Main confusion matrix
- `confusion_matrix_comparison.png` - All models' confusion matrices
- `model_accuracy_comparison.png` - Bar chart comparing model accuracies
- `roc_curves.png` - ROC curves for all models (if applicable)
- `feature_importance_final.png` - Final model feature importance
- `shap_summary.png` - SHAP summary plot
- `shap_dependence.png` - SHAP dependence plots for top features
- `calibration_curve.png` - Prediction probability calibration
- `learning_curves.png` - Training vs validation performance
- `prediction_confidence.png` - Distribution of prediction probabilities
- `error_analysis.png` - Analysis of misclassifications

### File Format Guidelines:
- Use PNG format for web/report inclusion (300 DPI for publication)
- Use consistent color schemes (e.g., seaborn default or custom palette)
- Include clear titles, axis labels, and legends
- Add grid lines for readability where appropriate
- Use appropriate figure sizes (typically 10x6 or 12x8 inches)

### Usage Example:
```python
import matplotlib.pyplot as plt

# Create plot
plt.figure(figsize=(10, 6))
# ... plotting code ...
plt.savefig('figures/eda/match_outcomes_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Notes:
- Keep original high-resolution versions for report
- May create lower-resolution copies for presentations
- Use consistent styling across all figures
- Ensure all figures are referenced in notebooks and report
