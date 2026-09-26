import os
import json
import joblib
import numpy as np
from ml_model.train import clean_text, MODEL_PATH, VECTORIZER_PATH, METRICS_PATH

_model = None
_vectorizer = None
_metrics = None

def load_ml_pipeline():
    global _model, _vectorizer, _metrics
    if _model is not None and _vectorizer is not None:
        return _model, _vectorizer, _metrics

    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            _model = joblib.load(MODEL_PATH)
            _vectorizer = joblib.load(VECTORIZER_PATH)
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, "r") as f:
                    _metrics = json.load(f)
            return _model, _vectorizer, _metrics
        except Exception as e:
            print(f"Warning: Failed to load ML model: {e}")
            return None, None, None
    return None, None, None

def predict_scam_probability(text: str):
    """
    Returns:
        prob (float 0.0 - 1.0 or None if model unavailable)
        top_features (list of tokens contributing to scam score)
    """
    model, vectorizer, _ = load_ml_pipeline()
    if model is None or vectorizer is None:
        return None, []

    cleaned = clean_text(text)
    if not cleaned:
        return 0.0, []

    vec = vectorizer.transform([cleaned])
    prob = float(model.predict_proba(vec)[0][1])

    # Find top contributing features for this specific text
    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]
    non_zero_indices = vec.nonzero()[1]

    scored_tokens = []
    for idx in non_zero_indices:
        token = feature_names[idx]
        tfidf_val = vec[0, idx]
        coef_val = coefficients[idx]
        impact = tfidf_val * coef_val
        if impact > 0:
            scored_tokens.append((token, float(impact)))

    scored_tokens.sort(key=lambda x: x[1], reverse=True)
    top_features = [item[0] for item in scored_tokens[:5]]

    return prob, top_features

def get_model_info():
    _, _, metrics = load_ml_pipeline()
    if metrics:
        return metrics
    return {
        "status": "NOT_TRAINED",
        "accuracy": None,
        "model_type": "TF-IDF + Logistic Regression",
        "description": "Rule-based fallback active"
    }
