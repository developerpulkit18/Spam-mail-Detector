"""
Phishing URL Detection — Random Forest Model Training
=======================================================
Trains a Random Forest classifier on the UCI Phishing Websites
dataset (11,055 samples, 30 features).

Features are pre-encoded as -1/0/1:
  -1 = phishing indicator,  0 = suspicious,  1 = legitimate

Label column 'Result':
   1 = phishing,  -1 = legitimate

Outputs:
  models/phishing_rf_model.pkl      — trained Random Forest
  models/phishing_model_metadata.pkl — performance metrics
  models/phishing_feature_names.pkl  — ordered feature list
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ─── Configuration ───────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')
DATASET_PATH = os.path.join(PROJECT_ROOT, 'dataset.csv')
RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_dataset():
    """Load and prepare the phishing dataset."""
    print("=" * 65)
    print("  PHISHING URL DETECTOR -- Random Forest Training Pipeline")
    print("=" * 65)

    print("\n[1/6] Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    # Drop the 'index' column (just row IDs)
    if 'index' in df.columns:
        df = df.drop(columns=['index'])

    # Separate features and label
    X = df.drop(columns=['Result'])
    y = df['Result']

    # Convert labels: 1 stays 1 (phishing), -1 becomes 0 (legitimate)
    y = y.map({1: 1, -1: 0})

    feature_names = list(X.columns)

    print(f"   Samples   : {len(df)}")
    print(f"   Features  : {len(feature_names)}")
    print(f"   Phishing  : {int(y.sum())} ({y.mean()*100:.1f}%)")
    print(f"   Legitimate: {int(len(y) - y.sum())} ({(1-y.mean())*100:.1f}%)")

    return X, y, feature_names


def train_model(X_train, y_train):
    """Train a Random Forest classifier."""
    print("\n[3/6] Training Random Forest...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight='balanced',
    )

    model.fit(X_train, y_train)
    print("   Training complete.")

    return model


def evaluate_model(model, X_train, X_test, y_train, y_test, feature_names):
    """Evaluate the model and print detailed results."""
    print("\n[4/6] Evaluating model...")

    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    acc      = accuracy_score(y_test, y_pred)
    prec     = precision_score(y_test, y_pred, zero_division=0)
    rec      = recall_score(y_test, y_pred, zero_division=0)
    f1       = f1_score(y_test, y_pred, zero_division=0)
    train_acc = accuracy_score(y_train, y_pred_train)

    print(f"\n   {'Metric':<20} {'Train':>10} {'Test':>10}")
    print(f"   {'-'*40}")
    print(f"   {'Accuracy':<20} {train_acc:>10.4f} {acc:>10.4f}")
    print(f"   {'Precision':<20} {'--':>10} {prec:>10.4f}")
    print(f"   {'Recall':<20} {'--':>10} {rec:>10.4f}")
    print(f"   {'F1-Score':<20} {'--':>10} {f1:>10.4f}")

    print("\n   Classification Report (Test Set):")
    target_names = ['Legitimate (0)', 'Phishing (1)']
    report = classification_report(y_test, y_pred, target_names=target_names)
    for line in report.split('\n'):
        print(f"   {line}")

    # Cross-validation
    print("\n[5/6] 5-Fold Cross-Validation...")
    cv_scores = cross_val_score(model, np.vstack([X_train, X_test]),
                                np.concatenate([y_train, y_test]),
                                cv=5, scoring='accuracy', n_jobs=-1)
    print(f"   CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

    # Feature importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("\n   Top 10 Features:")
    for rank, idx in enumerate(indices[:10], 1):
        print(f"   {rank:>3}. {feature_names[idx]:<35} {importances[idx]:.4f}")

    return {
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1,
        'train_accuracy': train_acc,
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'y_pred': y_pred,
    }


def plot_results(y_test, results, feature_names, model):
    """Generate confusion matrix and feature importance plots."""
    print("\n[6/6] Generating plots...")
    os.makedirs(MODEL_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ── Confusion Matrix ──
    cm = confusion_matrix(y_test, results['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn_r',
                xticklabels=['Legitimate', 'Phishing'],
                yticklabels=['Legitimate', 'Phishing'],
                ax=axes[0])
    axes[0].set_title(f"Confusion Matrix\nAccuracy: {results['accuracy']:.2%}", fontsize=12)
    axes[0].set_xlabel('Predicted')
    axes[0].set_ylabel('Actual')

    # ── Feature Importance ──
    importances = model.feature_importances_
    indices = np.argsort(importances)[-15:]  # Top 15
    axes[1].barh(range(len(indices)),
                 importances[indices],
                 color='#667eea', edgecolor='#764ba2', alpha=0.85)
    axes[1].set_yticks(range(len(indices)))
    axes[1].set_yticklabels([feature_names[i] for i in indices], fontsize=8)
    axes[1].set_title('Top 15 Feature Importances', fontsize=12)
    axes[1].set_xlabel('Importance')

    plt.tight_layout()
    plot_path = os.path.join(MODEL_DIR, 'phishing_model_report.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved report plot to: {plot_path}")


def save_model(model, feature_names, results):
    """Save the trained model, feature names, and metadata."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, 'phishing_rf_model.pkl')
    features_path = os.path.join(MODEL_DIR, 'phishing_feature_names.pkl')
    meta_path = os.path.join(MODEL_DIR, 'phishing_model_metadata.pkl')

    joblib.dump(model, model_path)
    joblib.dump(feature_names, features_path)

    metadata = {
        'model_name': 'Random Forest',
        'n_estimators': 200,
        'accuracy': results['accuracy'],
        'precision': results['precision'],
        'recall': results['recall'],
        'f1_score': results['f1_score'],
        'train_accuracy': results['train_accuracy'],
        'cv_mean': results['cv_mean'],
        'cv_std': results['cv_std'],
        'n_features': len(feature_names),
        'feature_names': feature_names,
    }
    joblib.dump(metadata, meta_path)

    print(f"\n   Model saved     : {model_path}")
    print(f"   Features saved  : {features_path}")
    print(f"   Metadata saved  : {meta_path}")


def main():
    # Step 1: Load
    X, y, feature_names = load_dataset()

    # Step 2: Split
    print("\n[2/6] Splitting dataset (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"   Train: {len(X_train)} | Test: {len(X_test)}")

    # Step 3: Train
    model = train_model(X_train.values, y_train.values)

    # Step 4-5: Evaluate
    results = evaluate_model(model, X_train.values, X_test.values,
                             y_train.values, y_test.values, feature_names)

    # Step 6: Plot
    plot_results(y_test.values, results, feature_names, model)

    # Save
    save_model(model, feature_names, results)

    print("\n" + "=" * 65)
    print("  TRAINING COMPLETE")
    print(f"  Accuracy: {results['accuracy']:.2%}  |  "
          f"F1: {results['f1_score']:.2%}  |  "
          f"CV: {results['cv_mean']:.2%}")
    print("=" * 65)


if __name__ == '__main__':
    main()
