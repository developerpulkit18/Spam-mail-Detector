"""
Model Utilities Module for Spam Mail Detector
==============================================
Handles model loading, saving, and prediction operations.
"""

import os
import joblib
import numpy as np
from utils.preprocessor import TextPreprocessor


class ModelManager:
    """
    Manages ML model loading, saving, and real-time prediction.
    
    Attributes
    ----------
    model : sklearn estimator
        The trained classification model.
    vectorizer : sklearn transformer
        The fitted TF-IDF vectorizer.
    preprocessor : TextPreprocessor
        Text preprocessing pipeline.
    """
    
    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        """
        Initialize ModelManager with optional pre-trained model paths.
        
        Parameters
        ----------
        model_path : str, optional
            Path to the saved model file (.pkl).
        vectorizer_path : str, optional
            Path to the saved vectorizer file (.pkl).
        """
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        
        if model_path and vectorizer_path:
            self.load(model_path, vectorizer_path)
    
    def load(self, model_path: str, vectorizer_path: str):
        """
        Load a trained model and vectorizer from disk.
        
        Parameters
        ----------
        model_path : str
            Path to the model pickle file.
        vectorizer_path : str
            Path to the vectorizer pickle file.
            
        Raises
        ------
        FileNotFoundError
            If model or vectorizer files don't exist.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        # Use ASCII-safe output to avoid UnicodeEncodeError on Windows
        print(f"[OK] Model loaded from: {model_path}")
        print(f"[OK] Vectorizer loaded from: {vectorizer_path}")
    
    def save(self, model, vectorizer, model_path: str, vectorizer_path: str):
        """
        Save a trained model and vectorizer to disk.
        
        Parameters
        ----------
        model : sklearn estimator
            Trained model to save.
        vectorizer : sklearn transformer
            Fitted vectorizer to save.
        model_path : str
            Destination path for model file.
        vectorizer_path : str
            Destination path for vectorizer file.
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        joblib.dump(model, model_path)
        joblib.dump(vectorizer, vectorizer_path)
        
        self.model = model
        self.vectorizer = vectorizer
        
        print(f"[SAVED] Model saved to: {model_path}")
        print(f"[SAVED] Vectorizer saved to: {vectorizer_path}")
    
    def predict(self, text: str) -> dict:
        """
        Predict whether a message is spam or ham.
        
        Parameters
        ----------
        text : str
            Raw input message/email text.
            
        Returns
        -------
        dict
            Dictionary with keys:
            - 'prediction': str ('Spam' or 'Not Spam')
            - 'label': int (1 for spam, 0 for ham)
            - 'confidence': float (prediction confidence 0-1)
            - 'spam_probability': float (probability of being spam)
            - 'ham_probability': float (probability of being ham)
            
        Raises
        ------
        RuntimeError
            If model or vectorizer is not loaded.
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Model and vectorizer must be loaded before prediction.")
        
        # Preprocess the input text
        cleaned_text = self.preprocessor.clean_text(text)
        
        # Vectorize
        text_vector = self.vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = self.model.predict(text_vector)[0]
        
        # Get prediction probabilities
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(text_vector)[0]
            ham_prob = probabilities[0]
            spam_prob = probabilities[1]
            confidence = max(ham_prob, spam_prob)
        elif hasattr(self.model, 'decision_function'):
            decision = self.model.decision_function(text_vector)[0]
            # Convert decision function to pseudo-probability using sigmoid
            spam_prob = 1 / (1 + np.exp(-decision))
            ham_prob = 1 - spam_prob
            confidence = max(ham_prob, spam_prob)
        else:
            spam_prob = float(prediction)
            ham_prob = 1 - spam_prob
            confidence = 1.0
        
        return {
            'prediction': 'Spam' if prediction == 1 else 'Not Spam',
            'label': int(prediction),
            'confidence': round(float(confidence), 4),
            'spam_probability': round(float(spam_prob), 4),
            'ham_probability': round(float(ham_prob), 4),
        }
    
    def predict_batch(self, texts: list) -> list:
        """
        Predict spam/ham for a batch of messages.
        
        Parameters
        ----------
        texts : list of str
            List of raw message texts.
            
        Returns
        -------
        list of dict
            List of prediction result dictionaries.
        """
        return [self.predict(text) for text in texts]
