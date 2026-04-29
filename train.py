"""
Spam Mail Detector — Model Training Script
============================================
Agent 2: Data Processing & Model Development

This script:
1. Downloads/loads the SMS Spam Collection dataset
2. Preprocesses all text data
3. Extracts features using TF-IDF
4. Trains multiple ML models (Naive Bayes, Logistic Regression, SVM)
5. Evaluates and compares all models
6. Saves the best model and vectorizer to disk
7. Generates confusion matrix visualizations
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.preprocessor import TextPreprocessor

# ─── Configuration ───────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')
# Local dataset file: tab-separated SMS Spam Collection
LOCAL_DATASET_FILE = os.path.join(PROJECT_ROOT, 'SMSSpamCollection (1)')
DATASET_FILE = os.path.join(DATA_DIR, 'spam.csv')
RANDOM_STATE = 42
TEST_SIZE = 0.2


def prepare_dataset():
    """Load the local SMSSpamCollection text file and convert to CSV."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(DATASET_FILE):
        print(f"📂 Dataset CSV already exists at: {DATASET_FILE}")
        return

    if not os.path.exists(LOCAL_DATASET_FILE):
        print(f"❌ Local dataset not found at: {LOCAL_DATASET_FILE}")
        print("   Please place the 'SMSSpamCollection (1)' file in the project root.")
        sys.exit(1)

    print(f"📂 Loading local dataset: {LOCAL_DATASET_FILE}")

    # Read the tab-separated text file
    rows = []
    with open(LOCAL_DATASET_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t', 1)
            if len(parts) == 2:
                rows.append(parts)

    df = pd.DataFrame(rows, columns=['label', 'message'])
    df.to_csv(DATASET_FILE, index=False)
    print(f"✅ Dataset converted and saved to: {DATASET_FILE}")
    print(f"   Total samples: {len(df)}")


def load_data():
    """Load dataset from CSV file."""
    print("\n📊 Loading dataset...")
    df = pd.read_csv(DATASET_FILE)

    # Standardize label column
    df['label'] = df['label'].str.lower().str.strip()

    # Convert labels to binary (spam=1, ham=0)
    df['label_num'] = df['label'].map({'spam': 1, 'ham': 0})

    # Drop any rows with NaN
    df = df.dropna(subset=['message', 'label_num'])

    print(f"   Total messages: {len(df)}")
    print(f"   Spam messages:  {int(df['label_num'].sum())} ({df['label_num'].mean()*100:.1f}%)")
    print(f"   Ham messages:   {int(len(df) - df['label_num'].sum())} ({(1-df['label_num'].mean())*100:.1f}%)")

    return df


def preprocess_data(df):
    """Apply text preprocessing to the dataset."""
    print("\n🔧 Preprocessing text data...")
    preprocessor = TextPreprocessor()
    df['cleaned_message'] = preprocessor.transform_series(df['message'])
    
    # Remove empty messages after cleaning
    df = df[df['cleaned_message'].str.len() > 0]
    
    print(f"   Preprocessing complete. {len(df)} messages retained.")
    return df


def extract_features(X_train, X_test):
    """Extract TF-IDF features from preprocessed text."""
    print("\n🔢 Extracting TF-IDF features...")
    
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=2,
        max_df=0.95,
        ngram_range=(1, 2),  # Unigrams and bigrams
        sublinear_tf=True
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"   Feature matrix shape: {X_train_tfidf.shape}")
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    return X_train_tfidf, X_test_tfidf, vectorizer


def train_models(X_train, y_train):
    """Train multiple ML models and return them."""
    print("\n🤖 Training models...")
    
    models = {}
    
    # 1. Multinomial Naive Bayes
    print("   Training Multinomial Naive Bayes...")
    nb_model = MultinomialNB(alpha=0.1)
    nb_model.fit(X_train, y_train)
    models['Multinomial Naive Bayes'] = nb_model
    
    # 2. Logistic Regression
    print("   Training Logistic Regression...")
    lr_model = LogisticRegression(
        max_iter=1000,
        C=1.0,
        solver='lbfgs',
        random_state=RANDOM_STATE
    )
    lr_model.fit(X_train, y_train)
    models['Logistic Regression'] = lr_model
    
    # 3. SVM (Linear) with calibration for probability estimates
    print("   Training SVM (Linear)...")
    svm_base = LinearSVC(max_iter=2000, C=1.0, random_state=RANDOM_STATE)
    svm_model = CalibratedClassifierCV(svm_base, cv=3)
    svm_model.fit(X_train, y_train)
    models['SVM (Linear)'] = svm_model
    
    # 4. Random Forest (Bonus)
    print("   Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    models['Random Forest'] = rf_model
    
    print(f"   ✅ {len(models)} models trained successfully!")
    return models


def evaluate_models(models, X_test, y_test):
    """Evaluate all models and return results."""
    print("\n📈 Evaluating models...")
    print("=" * 70)
    
    results = {}
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'y_pred': y_pred
        }
        
        print(f"\n🔹 {name}")
        print(f"   Accuracy:  {acc:.4f}")
        print(f"   Precision: {prec:.4f}")
        print(f"   Recall:    {rec:.4f}")
        print(f"   F1-Score:  {f1:.4f}")
    
    print("\n" + "=" * 70)
    return results


def plot_confusion_matrices(models, results, y_test):
    """Generate and save confusion matrix visualizations."""
    print("\n📊 Generating confusion matrix visualizations...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    n_models = len(models)
    fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4))
    
    if n_models == 1:
        axes = [axes]
    
    for ax, (name, result) in zip(axes, results.items()):
        cm = confusion_matrix(y_test, result['y_pred'])
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Ham', 'Spam'],
            yticklabels=['Ham', 'Spam'],
            ax=ax
        )
        ax.set_title(f'{name}\nAccuracy: {result["accuracy"]:.2%}', fontsize=10)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
    
    plt.tight_layout()
    plot_path = os.path.join(MODEL_DIR, 'confusion_matrices.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved to: {plot_path}")


def plot_model_comparison(results):
    """Generate a bar chart comparing model performances."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    model_names = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    metric_labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    x = np.arange(len(model_names))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#4A90D9', '#50C878', '#FF6B6B', '#FFD93D']
    
    for i, (metric, label, color) in enumerate(zip(metrics, metric_labels, colors)):
        values = [results[name][metric] for name in model_names]
        bars = ax.bar(x + i * width, values, width, label=label, color=color, alpha=0.85)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(model_names, fontsize=9)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_ylim(0, 1.12)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(MODEL_DIR, 'model_comparison.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Saved comparison chart to: {plot_path}")


def save_best_model(models, results, vectorizer):
    """Identify and save the best performing model."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Select best model based on F1-Score
    best_name = max(results, key=lambda k: results[k]['f1_score'])
    best_model = models[best_name]
    best_f1 = results[best_name]['f1_score']
    
    model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
    vectorizer_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    # Also save model metadata
    metadata = {
        'model_name': best_name,
        'accuracy': results[best_name]['accuracy'],
        'precision': results[best_name]['precision'],
        'recall': results[best_name]['recall'],
        'f1_score': results[best_name]['f1_score'],
    }
    metadata_path = os.path.join(MODEL_DIR, 'model_metadata.pkl')
    joblib.dump(metadata, metadata_path)
    
    print(f"\n🏆 Best Model: {best_name}")
    print(f"   F1-Score: {best_f1:.4f}")
    print(f"   💾 Model saved to: {model_path}")
    print(f"   💾 Vectorizer saved to: {vectorizer_path}")
    
    return best_name


def main():
    """Run the complete training pipeline."""
    print("=" * 70)
    print("  📧 SPAM MAIL DETECTOR — Model Training Pipeline")
    print("=" * 70)
    
    # Step 1: Prepare dataset from local file
    prepare_dataset()
    
    # Step 2: Load data
    df = load_data()
    
    # Step 3: Preprocess
    df = preprocess_data(df)
    
    # Step 4: Split dataset
    print("\n✂️  Splitting dataset (80% train / 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['cleaned_message'], df['label_num'],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df['label_num']
    )
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Test set:     {len(X_test)} samples")
    
    # Step 5: Feature extraction
    X_train_tfidf, X_test_tfidf, vectorizer = extract_features(X_train, X_test)
    
    # Step 6: Train models
    models = train_models(X_train_tfidf, y_train)
    
    # Step 7: Evaluate
    results = evaluate_models(models, X_test_tfidf, y_test)
    
    # Step 8: Visualizations
    plot_confusion_matrices(models, results, y_test)
    plot_model_comparison(results)
    
    # Step 9: Save best model
    best_name = save_best_model(models, results, vectorizer)
    
    # Step 10: Test with sample messages
    print("\n" + "=" * 70)
    print("  🧪 Testing with sample messages")
    print("=" * 70)
    
    from utils.model_utils import ModelManager
    
    manager = ModelManager(
        model_path=os.path.join(MODEL_DIR, 'best_model.pkl'),
        vectorizer_path=os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    )
    
    test_messages = [
        "Congratulations! You've won a $1000 gift card. Click here now!",
        "Hey, are we still meeting for lunch tomorrow?",
        "URGENT: Your account has been compromised. Verify NOW",
        "Can you send me the meeting notes from today?",
        "FREE entry to win a brand new iPhone! Text WIN to 80085",
        "Don't forget to pick up milk on your way home",
    ]
    
    for msg in test_messages:
        result = manager.predict(msg)
        emoji = "🔴" if result['label'] == 1 else "🟢"
        print(f"\n{emoji} [{result['prediction']}] (confidence: {result['confidence']:.1%})")
        print(f"   \"{msg[:60]}{'...' if len(msg) > 60 else ''}\"")
    
    print("\n" + "=" * 70)
    print("  ✅ Training pipeline complete!")
    print(f"  Best model: {best_name}")
    print(f"  Run the app:  streamlit run app/app.py")
    print("=" * 70)


if __name__ == '__main__':
    main()
