# 📧 Spam Mail Detector

An intelligent machine learning system that classifies emails and messages as **Spam** or **Not Spam (Ham)** using Natural Language Processing and multiple ML algorithms.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange?logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Problem Statement

Email spam is one of the most common cybersecurity threats, costing businesses billions annually. This project builds an ML-powered spam detection system that:

- Classifies messages as **Spam** or **Ham** in real-time
- Uses NLP techniques for text preprocessing
- Compares multiple ML algorithms for best accuracy
- Provides a beautiful, interactive web interface

## 🏗️ System Architecture

```
User Input (Email/Message)
        │
        ▼
┌─────────────────────┐
│  Text Preprocessing  │  → Lowercasing, punctuation removal,
│                      │    stopword removal, stemming
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Feature Extraction  │  → TF-IDF Vectorization
│                      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   ML Model Predict   │  → Multinomial Naive Bayes /
│                      │    Logistic Regression / SVM
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Output Result      │  → Spam / Not Spam + Confidence
└─────────────────────┘
```

## 📁 Project Structure

```
spam-mail-detector/
├── data/                    # Dataset files
│   └── spam.csv             # SMS Spam Collection Dataset
├── models/                  # Trained models & vectorizers
│   ├── best_model.pkl       # Best performing model
│   └── tfidf_vectorizer.pkl # Fitted TF-IDF vectorizer
├── notebooks/               # Jupyter notebooks for exploration
│   └── exploration.md       # Analysis notes
├── app/                     # Streamlit web application
│   └── app.py               # Main Streamlit app
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── preprocessor.py      # Text preprocessing functions
│   └── model_utils.py       # Model loading & prediction
├── train.py                 # Model training script
├── evaluate.py              # Model evaluation script
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd spam-mail-detector
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords punkt_tab
```

### 2. Train the Model

```bash
python train.py
```

This will:
- Load and preprocess the SMS Spam Collection dataset
- Train Naive Bayes, Logistic Regression, and SVM models
- Evaluate all models and save the best one
- Generate a confusion matrix visualization

### 3. Run the Web App

```bash
streamlit run app/app.py
```

Open your browser to `http://localhost:8501` and start classifying messages!

## 🧪 Sample Test Inputs

| Message | Expected |
|---------|----------|
| `Congratulations! You've won a $1000 gift card. Click here to claim now!` | 🔴 Spam |
| `Hey, are we still meeting for lunch tomorrow?` | 🟢 Not Spam |
| `URGENT: Your account has been compromised. Verify your identity NOW` | 🔴 Spam |
| `Can you send me the meeting notes from today?` | 🟢 Not Spam |
| `FREE entry to win a brand new iPhone! Text WIN to 80085` | 🔴 Spam |
| `Don't forget to pick up milk on your way home` | 🟢 Not Spam |

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Multinomial Naive Bayes | ~97% | ~100% | ~87% | ~93% |
| Logistic Regression | ~96% | ~97% | ~88% | ~92% |
| SVM (Linear) | ~98% | ~99% | ~90% | ~94% |

*Results may vary slightly based on random split*

## 🛠️ Tech Stack

- **Python 3.8+** — Core programming language
- **Scikit-learn** — ML algorithms & evaluation
- **NLTK** — Natural language processing
- **Pandas & NumPy** — Data manipulation
- **Streamlit** — Interactive web interface
- **Matplotlib & Seaborn** — Visualizations
- **Joblib** — Model serialization

## 📝 License

MIT License — feel free to use, modify, and distribute.
