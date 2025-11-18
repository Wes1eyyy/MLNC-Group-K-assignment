# Models Directory

## Purpose
This directory stores trained machine learning models for EPL match outcome prediction.

## Development Plan

### Directory Contents:
- **Trained model files** (.pkl, .joblib, .h5 formats)
- **Model metadata** (training parameters, performance metrics)
- **Model versioning** (track different model iterations)

### Files to Create:

1. **best_model.pkl**
   - Final selected model for predictions
   - Trained on full training dataset
   - Optimized hyperparameters
   - Saved using joblib or pickle

2. **logistic_regression.pkl**
   - Baseline linear model
   - For comparison purposes

3. **random_forest.pkl**
   - Ensemble tree-based model
   - Feature importance available

4. **xgboost_model.pkl**
   - Gradient boosting model
   - Typically high performance

5. **model_metadata.json**
   - Training date and time
   - Hyperparameters used
   - Training/validation performance
   - Feature list
   - Cross-validation scores

### Usage:
```python
import joblib

# Save model
joblib.dump(model, 'models/best_model.pkl')

# Load model
model = joblib.load('models/best_model.pkl')
```

### Notes:
- Use .gitignore to exclude large model files from version control if needed
- Consider using model versioning (e.g., model_v1.pkl, model_v2.pkl)
- Keep model metadata for reproducibility
- Test model loading before final submission
