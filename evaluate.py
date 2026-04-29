"""
Spam Mail Detector — Model Evaluation Script
==============================================
Standalone evaluation script for testing the trained model
with custom inputs and generating detailed reports.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.model_utils import ModelManager

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')


def evaluate_on_test_data():
    """Evaluate the saved model on the test dataset."""
    print("=" * 60)
    print("  📧 SPAM MAIL DETECTOR — Model Evaluation")
    print("=" * 60)
    
    # Load model
    model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
    vectorizer_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    
    if not os.path.exists(model_path):
        print("❌ Model not found. Please run train.py first.")
        return
    
    manager = ModelManager(model_path, vectorizer_path)
    
    # Test with comprehensive examples
    test_cases = [
        # Spam messages
        ("Congratulations! You've won a $5000 prize! Click here to claim!", "Spam"),
        ("URGENT: Your bank account has been compromised. Verify NOW!", "Spam"),
        ("FREE entry to win iPhone 15! Text WIN to 80085", "Spam"),
        ("You've been selected for our exclusive $1M lottery!", "Spam"),
        ("Hot singles in your area! Meet them tonight", "Spam"),
        ("Make $5000/week working from home! Sign up FREE", "Spam"),
        ("Your account will be suspended! Click to verify", "Spam"),
        ("Buy cheap medications online! No prescription needed", "Spam"),
        ("Lose 20 pounds in 2 weeks! Order miracle pill now", "Spam"),
        ("ALERT: Suspicious activity on your credit card", "Spam"),
        
        # Ham messages
        ("Hey, are we still meeting for lunch tomorrow?", "Not Spam"),
        ("Can you send me the meeting notes from today?", "Not Spam"),
        ("Don't forget to pick up milk on your way home", "Not Spam"),
        ("The project deadline has been extended to Friday", "Not Spam"),
        ("Happy birthday! Hope you have an amazing day!", "Not Spam"),
        ("Can you review my pull request when you get a chance?", "Not Spam"),
        ("I'll be home late tonight, don't wait up", "Not Spam"),
        ("The weather looks nice tomorrow. Want to go hiking?", "Not Spam"),
        ("I've attached the quarterly report for your review", "Not Spam"),
        ("Running 10 minutes late for our 3pm meeting", "Not Spam"),
    ]
    
    print("\n🧪 Running evaluation on test cases...\n")
    
    correct = 0
    total = len(test_cases)
    results = []
    
    for message, expected in test_cases:
        result = manager.predict(message)
        is_correct = result['prediction'] == expected
        correct += int(is_correct)
        
        emoji = "✅" if is_correct else "❌"
        status = "🔴" if result['prediction'] == "Spam" else "🟢"
        
        results.append({
            'message': message[:55],
            'expected': expected,
            'predicted': result['prediction'],
            'confidence': result['confidence'],
            'correct': is_correct
        })
        
        print(f"  {emoji} {status} [{result['prediction']:>8}] "
              f"(conf: {result['confidence']:.1%}) | "
              f"\"{message[:50]}{'...' if len(message) > 50 else ''}\"")
    
    accuracy = correct / total
    print(f"\n{'=' * 60}")
    print(f"  📊 Results: {correct}/{total} correct ({accuracy:.1%} accuracy)")
    print(f"{'=' * 60}")
    
    return results


def interactive_evaluation():
    """Interactive mode for testing custom messages."""
    model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
    vectorizer_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    
    if not os.path.exists(model_path):
        print("❌ Model not found. Please run train.py first.")
        return
    
    manager = ModelManager(model_path, vectorizer_path)
    
    print("\n" + "=" * 60)
    print("  📧 INTERACTIVE SPAM DETECTOR")
    print("  Type a message and press Enter to classify.")
    print("  Type 'quit' to exit.")
    print("=" * 60)
    
    while True:
        print()
        message = input("📝 Enter message: ").strip()
        
        if message.lower() in ('quit', 'exit', 'q'):
            print("\n👋 Goodbye!")
            break
        
        if not message:
            print("⚠️  Please enter a message.")
            continue
        
        result = manager.predict(message)
        
        if result['label'] == 1:
            print(f"\n  🔴 SPAM DETECTED")
            print(f"     Confidence: {result['confidence']:.1%}")
            print(f"     Spam probability: {result['spam_probability']:.1%}")
        else:
            print(f"\n  🟢 NOT SPAM (Legitimate)")
            print(f"     Confidence: {result['confidence']:.1%}")
            print(f"     Ham probability: {result['ham_probability']:.1%}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Spam Mail Detector — Evaluation')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run in interactive mode')
    args = parser.parse_args()
    
    if args.interactive:
        interactive_evaluation()
    else:
        evaluate_on_test_data()
