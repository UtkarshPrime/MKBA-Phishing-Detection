import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def train_email_model():
    """Train the email phishing detection model using TF-IDF and Random Forest"""
    
    print("Starting email model training...")
    
    data_path = "../data/emails.csv"
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        print("Please run generate_data.py first.")
        return

    # Load data
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Handle missing values if any
    df.dropna(subset=['content'], inplace=True)
    
    print(f"Total samples: {len(df)}")
    print(df['label'].value_counts())

    # Split data
    X = df['content']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # TF-IDF Vectorization
    print("Vectorizing text...")
    tfidf = TfidfVectorizer(max_features=3000, stop_words='english')
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    # Train Model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    # Save artifacts
    print("\nSaving model and vectorizer...")
    joblib.dump(model, "email_model.pkl")
    joblib.dump(tfidf, "tfidf_vectorizer.pkl")
    print("Model saved as email_model.pkl")
    print("Vectorizer saved as tfidf_vectorizer.pkl")

if __name__ == "__main__":
    train_email_model()
