"""
Text Preprocessing Module for Spam Mail Detector
=================================================
Handles all text cleaning and transformation operations:
- Lowercasing
- Punctuation removal
- Stopword removal
- Stemming (Porter Stemmer)
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class TextPreprocessor:
    """
    A comprehensive text preprocessing pipeline for spam detection.
    
    Applies the following transformations in order:
    1. Convert to lowercase
    2. Remove HTML tags
    3. Remove URLs
    4. Remove email addresses
    5. Remove numbers
    6. Remove punctuation
    7. Tokenize
    8. Remove stopwords
    9. Apply stemming
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        # Keep some negation words as they can be important for spam detection
        self.stop_words -= {'not', 'no', 'nor', 'don', "don't", 'won', "won't"}
    
    def clean_text(self, text: str) -> str:
        """
        Apply the full preprocessing pipeline to a single text string.
        
        Parameters
        ----------
        text : str
            Raw input text (email or message).
            
        Returns
        -------
        str
            Cleaned and preprocessed text.
        """
        if not isinstance(text, str):
            return ""
        
        # Step 1: Lowercase
        text = text.lower()
        
        # Step 2: Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Step 3: Remove URLs
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
        
        # Step 4: Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Step 5: Remove numbers
        text = re.sub(r'\d+', ' ', text)
        
        # Step 6: Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Step 7: Tokenize
        tokens = word_tokenize(text)
        
        # Step 8: Remove stopwords
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 1]
        
        # Step 9: Stemming
        tokens = [self.stemmer.stem(t) for t in tokens]
        
        return ' '.join(tokens)
    
    def transform_series(self, series):
        """
        Apply preprocessing to a pandas Series of texts.
        
        Parameters
        ----------
        series : pd.Series
            Series containing raw text data.
            
        Returns
        -------
        pd.Series
            Series with cleaned text.
        """
        return series.apply(self.clean_text)


def preprocess_text(text: str) -> str:
    """
    Convenience function for single text preprocessing.
    
    Parameters
    ----------
    text : str
        Raw text input.
        
    Returns
    -------
    str
        Preprocessed text.
    """
    preprocessor = TextPreprocessor()
    return preprocessor.clean_text(text)
