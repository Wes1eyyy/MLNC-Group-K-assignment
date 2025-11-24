"""
通用模型训练脚本 - 支持多种算法
使用方法: python train_model.py --model svm
         python train_model.py --model random_forest
         python train_model.py --model knn
         python train_model.py --model xgboost
         python train_model.py --model bayes
         python train_model.py --model decision_tree
         python train_model.py --model mlp
"""
import sys
import os
import numpy as np
import argparse
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

# Keras/TensorFlow imports for MLP
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

# Add utils directory to path
sys.path.append(os.path.dirname(__file__))
from utils.data_utils import load_data, temporal_train_test_split, prepare_features
from utils.model_utils import evaluate_model, save_model, display_feature_importance

# Configuration
DATA_PATH = "../data/epl-features-training.csv"
MODELS_DIR = "../models"
TEST_SIZE = 0.1  # 10% for testing


def train_svm(X_train, y_train):
    """
    Train SVM model with StandardScaler

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained SVM model
        scaler: Fitted StandardScaler
    """
    print("\nTraining SVM model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Scale features (important for SVM!)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train SVM with RBF kernel
    model = SVC(
        kernel='rbf',  # Radial Basis Function kernel
        C=1.0,  # Regularization parameter
        gamma='scale',  # Kernel coefficient
        class_weight='balanced',  # Handle class imbalance
        random_state=42,
        verbose=True
    )

    model.fit(X_train_scaled, y_train)
    print("Training completed!")

    return model, scaler


def train_random_forest(X_train, y_train):
    """
    Train Random Forest model

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained Random Forest model
        scaler: None (Random Forest doesn't need scaling)
    """
    print("\nTraining Random Forest model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,  # Number of trees
        max_depth=10,  # Maximum depth of trees
        min_samples_split=5,  # Minimum samples to split
        min_samples_leaf=2,  # Minimum samples at leaf
        max_features='sqrt',  # Number of features for best split
        class_weight='balanced',  # Handle class imbalance
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
        verbose=1
    )

    model.fit(X_train, y_train)
    print("Training completed!")

    return model, None  # Random Forest doesn't need scaler


def train_knn(X_train, y_train):
    """
    Train K-Nearest Neighbors model

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained KNN model
        scaler: Fitted StandardScaler (KNN benefits from scaling)
    """
    print("\nTraining KNN model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Scale features (important for KNN - distance-based algorithm)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train KNN
    model = KNeighborsClassifier(
        n_neighbors=5,  # Number of neighbors to consider
        weights='distance',  # Weight by inverse distance
        algorithm='auto',  # Use best algorithm automatically
        metric='minkowski',  # Distance metric
        p=2,  # p=2 means Euclidean distance
        n_jobs=-1  # Use all CPU cores
    )

    model.fit(X_train_scaled, y_train)
    print("Training completed!")

    return model, scaler


def train_xgboost(X_train, y_train):
    """
    Train XGBoost model

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained XGBoost model
        scaler: None (XGBoost doesn't need scaling)
    """
    print("\nTraining XGBoost model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Convert labels to numeric (A=0, D=1, H=2)
    label_map = {'A': 0, 'D': 1, 'H': 2}
    y_train_numeric = np.array([label_map[label] for label in y_train])

    # Calculate class weights for imbalance
    unique_classes, class_counts = np.unique(y_train_numeric, return_counts=True)
    total_samples = len(y_train_numeric)
    class_weights = {cls: total_samples / (len(unique_classes) * count)
                     for cls, count in zip(unique_classes, class_counts)}

    # Assign sample weights
    sample_weights = np.array([class_weights[label] for label in y_train_numeric])

    # Train XGBoost
    model = xgb.XGBClassifier(
        n_estimators=100,        # Number of boosting rounds
        max_depth=6,             # Maximum tree depth
        learning_rate=0.1,       # Step size shrinkage
        subsample=0.8,           # Fraction of samples for each tree
        colsample_bytree=0.8,    # Fraction of features for each tree
        objective='multi:softmax',  # Multiclass classification
        num_class=3,             # Number of classes (A, D, H)
        random_state=42,
        n_jobs=-1,               # Use all CPU cores
        verbosity=1
    )

    model.fit(X_train, y_train_numeric, sample_weight=sample_weights)

    # Store label mapping for predictions
    model.label_map = label_map
    model.reverse_label_map = {v: k for k, v in label_map.items()}

    print("Training completed!")

    return model, None  # XGBoost doesn't need scaler


def train_bayes(X_train, y_train):
    """
    Train Gaussian Naive Bayes model

    Gaussian Naive Bayes assumes features follow a Gaussian (normal) distribution
    and are conditionally independent given the class. It's particularly efficient
    for high-dimensional data and works well with continuous features.

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained Gaussian Naive Bayes model
        scaler: None (Naive Bayes is probability-based, doesn't require scaling)
    """
    print("\nTraining Gaussian Naive Bayes model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Train Gaussian Naive Bayes
    # Note: GaussianNB doesn't have as many hyperparameters as other models
    model = GaussianNB(
        var_smoothing=1e-9  # Portion of largest variance added to variances for stability
    )

    model.fit(X_train, y_train)

    # Display class priors learned by the model
    print("\nClass priors learned by the model:")
    class_labels = model.classes_
    class_priors = model.class_prior_
    for label, prior in zip(class_labels, class_priors):
        print(f"  {label}: {prior:.4f} ({prior * 100:.2f}%)")

    print("Training completed!")

    return model, None  # Naive Bayes doesn't need scaler


def train_decision_tree(X_train, y_train):
    """
    Train Decision Tree model (CART algorithm with entropy criterion)

    Decision trees create a tree-like model of decisions based on feature values.
    This implementation uses:
    - Entropy (information gain) as splitting criterion (similar to C4.5/C5.0)
    - Pruning parameters to prevent overfitting
    - Class weights to handle imbalanced data

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained Decision Tree model
        scaler: None (Decision Tree doesn't need scaling)
    """
    print("\nTraining Decision Tree model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # Train Decision Tree with entropy criterion (information gain)
    model = DecisionTreeClassifier(
        criterion='entropy',         # Use entropy for information gain (like C4.5/C5.0)
        max_depth=10,               # Maximum depth to prevent overfitting
        min_samples_split=20,       # Minimum samples required to split
        min_samples_leaf=10,        # Minimum samples required at leaf node
        max_features='sqrt',        # Number of features for best split
        class_weight='balanced',    # Handle class imbalance
        random_state=42
    )

    model.fit(X_train, y_train)

    # Display tree statistics
    print(f"\nDecision Tree statistics:")
    print(f"  Tree depth: {model.get_depth()}")
    print(f"  Number of leaves: {model.get_n_leaves()}")
    print(f"  Number of features used: {model.n_features_in_}")

    print("Training completed!")

    return model, None  # Decision Tree doesn't need scaler


def train_mlp(X_train, y_train):
    """
    Train Multi-Layer Perceptron (MLP) Neural Network

    MLP is a feedforward neural network that can learn complex non-linear
    relationships between features. This implementation uses:
    - Multiple hidden layers with ReLU activation
    - Dropout for regularization (prevent overfitting)
    - Batch Normalization for training stability
    - Early stopping to prevent overfitting
    - Class weights to handle imbalanced data

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        model: Trained MLP model (Keras Sequential)
        scaler: Fitted StandardScaler
    """

    print("\nTraining Multi-Layer Perceptron (MLP) model...")
    print(f"Training samples: {len(X_train)}")
    print(f"Feature dimensions: {X_train.shape[1]}")

    # 1. Scale features (critical for neural networks!)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # 2. Convert labels to numeric and one-hot encoding
    label_map = {'A': 0, 'D': 1, 'H': 2}
    y_train_numeric = np.array([label_map[label] for label in y_train])
    y_train_onehot = to_categorical(y_train_numeric, num_classes=3)

    # 3. Calculate class weights for imbalanced data
    unique_classes, class_counts = np.unique(y_train_numeric, return_counts=True)
    total_samples = len(y_train_numeric)
    class_weights = {cls: total_samples / (len(unique_classes) * count)
                     for cls, count in zip(unique_classes, class_counts)}

    print(f"\nClass weights for imbalanced data:")
    for cls, weight in class_weights.items():
        print(f"  Class {cls} ({list(label_map.keys())[cls]}): {weight:.3f}")

    # 4. Build MLP architecture
    print("\nBuilding MLP architecture...")
    model = Sequential([
        # Input layer + First hidden layer
        Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        BatchNormalization(),
        Dropout(0.3),

        # Second hidden layer
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),

        # Third hidden layer
        Dense(32, activation='relu'),
        Dropout(0.2),

        # Output layer (3 classes: A, D, H)
        Dense(3, activation='softmax')
    ])

    # 5. Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\nModel Architecture:")
    model.summary()

    # 6. Setup callbacks
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=1
    )

    # 7. Train model
    print("\nTraining MLP...")
    history = model.fit(
        X_train_scaled, y_train_onehot,
        validation_split=0.15,  # Use 15% of training data for validation
        epochs=100,
        batch_size=32,
        class_weight=class_weights,
        callbacks=[early_stop],
        verbose=1
    )

    # 8. Display training results
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print(f"\nTraining completed!")
    print(f"  Final training accuracy: {final_train_acc:.4f}")
    print(f"  Final validation accuracy: {final_val_acc:.4f}")
    print(f"  Total epochs trained: {len(history.history['accuracy'])}")

    # Store label mapping for predictions
    model.label_map = label_map
    model.reverse_label_map = {v: k for k, v in label_map.items()}

    return model, scaler


def main():
    """Main training pipeline"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train EPL match outcome prediction model')
    parser.add_argument('--model', type=str, default='svm',
                        choices=['svm', 'random_forest', 'knn', 'xgboost', 'bayes', 'decision_tree', 'mlp'],
                        help='Model type to train (default: svm)')
    args = parser.parse_args()

    model_type = args.model

    print("=" * 60)
    print(f"EPL Match Outcome Prediction - {model_type.upper()} Training")
    print("=" * 60)

    # 1. Load data
    print("\nStep 1: Loading data...")
    data = load_data(DATA_PATH)
    print(f"Loaded {len(data)} matches")

    # 2. Split data temporally
    print("\nStep 2: Splitting data...")
    training_data, testing_data = temporal_train_test_split(data, test_size=TEST_SIZE)

    # 3. Prepare features
    print("\nStep 3: Preparing features...")
    X_train, y_train, feature_names = prepare_features(training_data)
    X_test, y_test, _ = prepare_features(testing_data)

    print(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"Testing set: {X_test.shape[0]} samples, {X_test.shape[1]} features")

    # Check class distribution
    unique, counts = np.unique(y_train, return_counts=True)
    print(f"\nTraining set class distribution:")
    for label, count in zip(unique, counts):
        print(f"  {label}: {count} ({count / len(y_train) * 100:.1f}%)")

    # 4. Train model
    print(f"\nStep 4: Training {model_type} model...")
    if model_type == 'svm':
        model, scaler = train_svm(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'svm_model.pkl')
        scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    elif model_type == 'random_forest':
        model, scaler = train_random_forest(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'random_forest_model.pkl')
        scaler_path = None

        # Display feature importance for Random Forest
        display_feature_importance(model, feature_names)
    elif model_type == 'knn':
        model, scaler = train_knn(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'knn_model.pkl')
        scaler_path = os.path.join(MODELS_DIR, 'knn_scaler.pkl')
    elif model_type == 'xgboost':
        model, scaler = train_xgboost(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'xgboost_model.pkl')
        scaler_path = None

        # Display feature importance for XGBoost
        display_feature_importance(model, feature_names)
    elif model_type == 'bayes':
        model, scaler = train_bayes(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'bayes_model.pkl')
        scaler_path = None
    elif model_type == 'decision_tree':
        model, scaler = train_decision_tree(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'decision_tree_model.pkl')
        scaler_path = None

        # Display feature importance for Decision Tree
        display_feature_importance(model, feature_names)
    elif model_type == 'mlp':
        model, scaler = train_mlp(X_train, y_train)
        model_path = os.path.join(MODELS_DIR, 'mlp_model.pkl')
        scaler_path = os.path.join(MODELS_DIR, 'mlp_scaler.pkl')
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    # 5. Evaluate model
    print("\nStep 5: Evaluating model...")
    accuracy, y_pred = evaluate_model(model, X_test, y_test, scaler, model_type)

    # 6. Save model
    print("\nStep 6: Saving model...")
    save_model(model, model_path, scaler, scaler_path)

    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Final Test Accuracy: {accuracy:.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()