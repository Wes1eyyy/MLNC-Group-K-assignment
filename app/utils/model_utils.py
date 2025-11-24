"""
Common utility functions for model training and evaluation
"""
import numpy as np
import os
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def evaluate_model(model, X_test, y_test, scaler=None, model_type=None):
    """
    Evaluate model on test set (works for sklearn models and Keras models)

    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        scaler: Optional scaler (for SVM, neural networks, etc.)
        model_type: Optional model type ('xgboost', 'svm', 'mlp', etc.)

    Returns:
        accuracy: Test accuracy
        y_pred: Predictions
    """
    print("\n" + "=" * 60)
    print("Model Evaluation")
    print("=" * 60)

    # Scale test features if scaler provided
    if scaler is not None:
        X_test_scaled = scaler.transform(X_test)
    else:
        X_test_scaled = X_test

    # Make predictions
    if model_type == 'mlp':
        # For Keras models, predict returns probabilities
        y_pred_proba = model.predict(X_test_scaled, verbose=0)
        y_pred_numeric = np.argmax(y_pred_proba, axis=1)
        # Convert numeric predictions back to labels
        reverse_label_map = {0: 'A', 1: 'D', 2: 'H'}
        y_pred = np.array([reverse_label_map[pred] for pred in y_pred_numeric])
    # Convert XGBoost numeric predictions back to labels
    elif model_type == 'xgboost':
        # XGBoost outputs numeric labels (0, 1, 2), convert to ('A', 'D', 'H')
        y_pred = model.predict(X_test_scaled)
        reverse_label_map = {0: 'A', 1: 'D', 2: 'H'}
        y_pred = np.array([reverse_label_map[pred] for pred in y_pred])
    else:
        y_pred = model.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

    # Detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred,
                                target_names=['Away Win (A)', 'Draw (D)', 'Home Win (H)']))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=['A', 'D', 'H'])
    print("\nConfusion Matrix:")
    print("                Predicted")
    print("              A    D    H")
    print(f"Actual  A   {cm[0][0]:3d}  {cm[0][1]:3d}  {cm[0][2]:3d}")
    print(f"        D   {cm[1][0]:3d}  {cm[1][1]:3d}  {cm[1][2]:3d}")
    print(f"        H   {cm[2][0]:3d}  {cm[2][1]:3d}  {cm[2][2]:3d}")

    return accuracy, y_pred


def save_model(model, model_path, scaler=None, scaler_path=None):
    """
    Save trained model (and optional scaler) to disk

    Args:
        model: Trained model
        model_path: Path to save model
        scaler: Optional scaler
        scaler_path: Path to save scaler
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save model
    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")

    # Save scaler if provided
    if scaler is not None and scaler_path is not None:
        joblib.dump(scaler, scaler_path)
        print(f"Scaler saved to: {scaler_path}")


def load_model(model_path, scaler_path=None):
    """
    Load trained model (and optional scaler) from disk

    Args:
        model_path: Path to model file
        scaler_path: Optional path to scaler file

    Returns:
        model: Loaded model
        scaler: Loaded scaler (or None if not provided)
    """
    model = joblib.load(model_path)
    print(f"Model loaded from: {model_path}")

    scaler = None
    if scaler_path is not None:
        scaler = joblib.load(scaler_path)
        print(f"Scaler loaded from: {scaler_path}")

    return model, scaler


def display_feature_importance(model, feature_names):
    """
    Display feature importance for tree-based models

    Args:
        model: Trained model with feature_importances_ attribute
        feature_names: List of feature names
    """
    if not hasattr(model, 'feature_importances_'):
        print("Model does not have feature importance")
        return

    print("\n" + "=" * 60)
    print("Feature Importance")
    print("=" * 60)

    # Get feature importance
    importances = model.feature_importances_

    # Sort by importance
    indices = np.argsort(importances)[::-1]

    print("\nTop 10 Most Important Features:")
    for i, idx in enumerate(indices[:10], 1):
        print(f"{i:2d}. {feature_names[idx]:30s} {importances[idx]:.4f}")