import os
import re
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "messages.csv")
MODEL_PATH = os.path.join(BASE_DIR, "scam_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")

def clean_text(text: str) -> str:
    """Standardize text for NLP training and inference."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Replace URLs with token
    text = re.sub(r'https?://\S+|www\.\S+', ' url_token ', text)
    # Replace phone numbers
    text = re.sub(r'\+?\d[\d -]{8,}\d', ' phone_token ', text)
    # Replace currency amounts
    text = re.sub(r'[₹$€£]\s*\d+([,\.]\d+)?', ' currency_token ', text)
    # Remove excessive symbols but keep exclamation marks
    text = re.sub(r'[^a-zA-Z0-9\s!]', ' ', text)
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train():
    print(f"Loading dataset from: {DATASET_PATH}")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded {len(df)} samples across classes: {df['label'].value_counts().to_dict()}")

    df['cleaned_text'] = df['text'].apply(clean_text)

    X = df['cleaned_text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_features=2500,
        sublinear_tf=True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        C=2.0,
        class_weight='balanced',
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    y_prob = model.predict_proba(X_test_vec)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    cm = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "dataset_size": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "confusion_matrix": cm,
        "model_type": "TF-IDF + Calibrated Logistic Regression",
        "vocabulary_size": len(vectorizer.vocabulary_),
        "status": "TRAINED"
    }

    print("\n--- Training Evaluation Metrics ---")
    print(f"Accuracy:  {metrics['accuracy']}%")
    print(f"Precision: {metrics['precision']}%")
    print(f"Recall:    {metrics['recall']}%")
    print(f"F1-Score:  {metrics['f1_score']}%")
    print(f"Confusion Matrix: {cm}")

    # Save artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nModel artifacts saved to:\n - {MODEL_PATH}\n - {VECTORIZER_PATH}\n - {METRICS_PATH}")
    return metrics

if __name__ == "__main__":
    train()
