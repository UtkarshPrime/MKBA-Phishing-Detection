from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
from feature_extractor import FeatureExtractor
from gemma_client import GemmaClient
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

# Initialize Gemma Client
gemma_client = GemmaClient()


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

# Load Email Model
EMAIL_MODEL_PATH = "email_model.pkl"
TFIDF_PATH = "tfidf_vectorizer.pkl"
email_model = None
tfidf_vectorizer = None

try:
    if os.path.exists(EMAIL_MODEL_PATH) and os.path.exists(TFIDF_PATH):
        email_model = joblib.load(EMAIL_MODEL_PATH)
        tfidf_vectorizer = joblib.load(TFIDF_PATH)
        print("Email Model loaded successfully")
    else:
        print("Warning: Email model not found. Please train it first.")
except Exception as e:
    print(f"Error loading email model: {e}")


class URLRequest(BaseModel):
    url: str


class EmailRequest(BaseModel):
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list = []
    context: dict = {}


@app.post("/chat")
def chat(request: ChatRequest):
    """Chat with the security assistant"""
    if not gemma_client.is_available():
        raise HTTPException(status_code=503, detail="AI Assistant is currently unavailable (Ollama not running).")
    
    response = gemma_client.chat(request.message, request.history, request.context)
    return {"response": response}



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
            "POST /analyze/email": "Analyze email content for phishing",
            "POST /chat": "Chat with the security assistant"
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
    """Analyze email content for phishing indicators using ML Model (TF-IDF + Random Forest)"""
    try:
        # Check if ML model is available
        if not email_model or not tfidf_vectorizer:
             # Fallback to Gemma if ML model is missing (or return error)
             if not gemma_client.is_available():
                 return AnalysisResponse(
                    classification="unknown",
                    score=0,
                    features={},
                    message="⚠️ Analysis Unavailable. Please train the email model or ensure Ollama is running."
                )
             # ... (Gemma fallback logic could go here, but let's stick to ML as primary)
             raise HTTPException(status_code=503, detail="Email ML model not loaded.")

        print("Using ML Model for email analysis...")
        
        # Vectorize content
        features_vector = tfidf_vectorizer.transform([request.content])
        
        # Predict
        prediction = email_model.predict(features_vector)[0]
        probability = email_model.predict_proba(features_vector)[0]
        
        # Calculate score
        phishing_prob = probability[1] if len(probability) > 1 else probability[0]
        score = float(phishing_prob * 100)
        
        # Determine classification
        if score > 70:
            classification = "phishing"
            message = "⚠️ This email contains patterns consistent with phishing attempts."
        elif score > 40:
            classification = "suspicious"
            message = "⚡ This email looks suspicious. Proceed with caution."
        else:
            classification = "legitimate"
            message = "✓ This email appears to be safe."

        # Optional: Use Gemma for explanation only (if available)
        if gemma_client.is_available():
            try:
                # Ask Gemma for a brief explanation based on the ML verdict
                prompt = f"I have classified this email as '{classification}'. Explain why briefly.\n\nEmail: {request.content[:500]}..."
                explanation = gemma_client._generate(prompt)
                if explanation:
                    message += f" AI Note: {explanation}"
            except:
                pass

        return AnalysisResponse(
            classification=classification,
            score=score,
            features={}, 
            message=message
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing email: {str(e)}")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
