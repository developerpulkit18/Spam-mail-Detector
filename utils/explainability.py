"""
Explainability Module for Spam Mail & Threat Intelligence System
=================================================================
Provides basic model explainability by extracting the top contributing
words from TF-IDF features that influenced the prediction.
"""

import numpy as np


def get_top_features(text: str, vectorizer, model, preprocessor, top_n: int = 10) -> list:
    """
    Get the top contributing TF-IDF features for a prediction.

    Parameters
    ----------
    text : str
        The raw input text.
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer.
    model : sklearn estimator
        The trained classification model.
    preprocessor : TextPreprocessor
        The text preprocessing pipeline.
    top_n : int
        Number of top features to return.

    Returns
    -------
    list of dict
        Each dict has 'word', 'tfidf_score', and 'contribution' keys.
    """
    # Preprocess and vectorize
    cleaned = preprocessor.clean_text(text)
    tfidf_vector = vectorizer.transform([cleaned])

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Get non-zero TF-IDF values for this document
    non_zero_indices = tfidf_vector.nonzero()[1]
    tfidf_scores = {}
    for idx in non_zero_indices:
        tfidf_scores[feature_names[idx]] = tfidf_vector[0, idx]

    if not tfidf_scores:
        return []

    # Try to get model coefficients for feature importance weighting
    contributions = {}
    if hasattr(model, 'coef_'):
        # Linear models (Logistic Regression, SVM)
        coefs = model.coef_[0] if model.coef_.ndim > 1 else model.coef_
        for word, score in tfidf_scores.items():
            idx = list(feature_names).index(word)
            contributions[word] = {
                'word': word,
                'tfidf_score': round(float(score), 4),
                'contribution': round(float(score * coefs[idx]), 4),
            }
    elif hasattr(model, 'feature_log_prob_'):
        # Naive Bayes — use log probability difference between spam and ham
        spam_log_prob = model.feature_log_prob_[1]  # spam class
        ham_log_prob = model.feature_log_prob_[0]   # ham class
        for word, score in tfidf_scores.items():
            idx = list(feature_names).index(word)
            diff = spam_log_prob[idx] - ham_log_prob[idx]
            contributions[word] = {
                'word': word,
                'tfidf_score': round(float(score), 4),
                'contribution': round(float(score * diff), 4),
            }
    else:
        # Fallback: just use TF-IDF scores
        for word, score in tfidf_scores.items():
            contributions[word] = {
                'word': word,
                'tfidf_score': round(float(score), 4),
                'contribution': round(float(score), 4),
            }

    # Sort by absolute contribution, descending
    sorted_features = sorted(
        contributions.values(),
        key=lambda x: abs(x['contribution']),
        reverse=True
    )

    return sorted_features[:top_n]


def explain_prediction(text: str, vectorizer, model, preprocessor, prediction_label: str) -> dict:
    """
    Generate a full explainability report for a prediction.

    Parameters
    ----------
    text : str
        Raw input text.
    vectorizer : TfidfVectorizer
        Fitted vectorizer.
    model : sklearn estimator
        Trained model.
    preprocessor : TextPreprocessor
        Text preprocessor.
    prediction_label : str
        The prediction result ('Spam' or 'Not Spam').

    Returns
    -------
    dict
        - prediction: the label
        - top_features: list of top contributing features
        - spam_indicators: features pushing toward spam
        - ham_indicators: features pushing toward ham
    """
    top_features = get_top_features(text, vectorizer, model, preprocessor)

    spam_indicators = [f for f in top_features if f['contribution'] > 0]
    ham_indicators = [f for f in top_features if f['contribution'] <= 0]

    return {
        'prediction': prediction_label,
        'top_features': top_features,
        'spam_indicators': spam_indicators,
        'ham_indicators': ham_indicators,
    }
