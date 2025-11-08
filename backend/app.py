from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
from feature_extractor import FeatureExtractor
import numpy as np

app = FastAPI(title="Phishing Detection API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize feature extractor
feature_extractor = FeatureExtractor()

# Load model (will be created by training script)
MODEL_PATH = "model.pkl"
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
    else:
        print("Warning: Model not found. Please train the model first.")
except Exception as e:
    print(f"Error loading model: {e}")


class URLRequest(BaseModel):
    url: str


class EmailRequest(BaseModel):
    content: str


class AnalysisResponse(BaseModel):
    classification: str
    score: float
    features: dict
    message: str


@app.get("/")
def read_root():
    return {
        "message": "Phishing Detection API",
        "endpoints": {
            "POST /analyze/url": "Analyze a URL for phishing",
            "POST /analyze/email": "Analyze email content for phishing"
        }
    }


@app.post("/analyze/url", response_model=AnalysisResponse)
def analyze_url(request: URLRequest):
    """Analyze a URL for phishing indicators"""
    if not model:
        raise HTTPException(
            status_code=503, detail="Model not loaded. Please train the model first.")

    try:
        # Extract features
        features = feature_extractor.extract_url_features(request.url)

        # Prepare features for model (ensure correct order)
        feature_names = ['url_length', 'domain_length', 'path_length', 'subdomain_count',
                         'has_ip', 'dot_count', 'dash_count', 'at_symbol',
                         'double_slash_redirect', 'https', 'suspicious_keywords',
                         'is_shortened', 'special_char_count', 'digit_ratio']

        feature_vector = np.array(
            [[features.get(name, 0) for name in feature_names]])

        # Predict
        prediction = model.predict(feature_vector)[0]
        probability = model.predict_proba(feature_vector)[0]

        # Calculate score (0-100)
        phishing_prob = probability[1] if len(
            probability) > 1 else probability[0]
        score = float(phishing_prob * 100)

        # Determine classification
        if score > 70:
            classification = "phishing"
            message = "⚠️ This URL appears to be a phishing attempt. Do not proceed."
        elif score > 40:
            classification = "suspicious"
            message = "⚡ This URL shows suspicious characteristics. Proceed with caution."
        else:
            classification = "legitimate"
            message = "✓ This URL appears to be safe."

        return AnalysisResponse(
            classification=classification,
            score=score,
            features=features,
            message=message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing URL: {str(e)}")


@app.post("/analyze/email", response_model=AnalysisResponse)
def analyze_email(request: EmailRequest):
    """Analyze email content for phishing indicators"""
    try:
        # Extract features
        features = feature_extractor.extract_email_features(request.content)

        # Simple rule-based classification for emails (can be enhanced with ML)
        score = 0

        if features['urgency_count'] > 2:
            score += 30
        if features['url_count'] > 3:
            score += 25
        if features['suspicious_phrases'] > 1:
            score += 30
        if features['exclamation_count'] > 3:
            score += 15

        score = min(score, 100)

        # Determine classification
        if score > 70:
            classification = "phishing"
            message = "⚠️ This email appears to be a phishing attempt."
        elif score > 40:
            classification = "suspicious"
            message = "⚡ This email shows suspicious characteristics."
        else:
            classification = "legitimate"
            message = "✓ This email appears to be safe."

        return AnalysisResponse(
            classification=classification,
            score=float(score),
            features=features,
            message=message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing email: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
