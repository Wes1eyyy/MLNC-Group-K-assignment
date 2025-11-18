# Results Directory

## Purpose
This directory stores model predictions, performance metrics, and analysis results.

## Development Plan

### Directory Contents:
- **Prediction files** (submission.csv)
- **Performance metrics** (CSV tables, JSON files)
- **Comparison results** (model performance comparison)
- **Feature analysis** (feature importance, SHAP values)

### Files to Create:

1. **submission.csv**
   - Final predictions for test dataset
   - Format: Date, HomeTeam, AwayTeam, FTR
   - Must match sample-submission.csv format
   - Ready for competition submission

2. **model_comparison.csv**
   - Performance metrics for all models
   - Columns: model_name, accuracy, precision, recall, f1_score, log_loss
   - Used for model selection justification

3. **feature_importance.csv**
   - Feature names and importance scores
   - Sorted by importance (descending)
   - Used for model interpretation

4. **confusion_matrices.json**
   - Confusion matrices for all models
   - Saved as dictionary/JSON format
   - For detailed error analysis

5. **cross_validation_results.csv**
   - CV scores for each model and fold
   - Mean and standard deviation
   - Assess model stability

6. **best_hyperparameters.json**
   - Optimal hyperparameters for each model
   - From grid search or random search
   - For reproducibility

7. **evaluation_metrics.json**
   - Comprehensive metrics dictionary
   - All models and metrics
   - Classification reports

### Usage:
```python
# Save predictions
predictions_df.to_csv('results/submission.csv', index=False)

# Save metrics
metrics_df.to_csv('results/model_comparison.csv', index=False)
```

### Validation:
- Verify submission.csv has correct format
- Check for missing values
- Ensure all test matches have predictions
- Validate FTR values are only H, D, or A
