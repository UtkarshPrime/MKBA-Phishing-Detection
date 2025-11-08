import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from feature_extractor import FeatureExtractor
import os


def create_sample_data():
    """Create sample training data if CSV files don't exist"""

    # Sample phishing URLs
    phishing_urls = [
        "http://paypal-verify.com/login",
        "https://secure-banking-update.net/account",
        "http://192.168.1.1/login",
        "http://amazon-security.tk/verify",
        "https://bit.ly/3xYz123",
        "http://apple-id-verify.com/update",
        "http://facebook-security.net/confirm",
        "https://netflix-billing.info/payment",
        "http://microsoft-account.xyz/verify",
        "https://google-security.tk/alert"
    ]

    # Sample legitimate URLs
    legitimate_urls = [
        "https://www.google.com",
        "https://www.amazon.com/products",
        "https://github.com/user/repo",
        "https://www.wikipedia.org/wiki/Article",
        "https://stackoverflow.com/questions",
        "https://www.paypal.com",
        "https://www.facebook.com",
        "https://www.netflix.com",
        "https://www.microsoft.com",
        "https://www.apple.com"
    ]

    # Create DataFrames
    phishing_df = pd.DataFrame({'url': phishing_urls, 'label': 1})
    legitimate_df = pd.DataFrame({'url': legitimate_urls, 'label': 0})

    return phishing_df, legitimate_df


def train_model():
    """Train the phishing detection model"""

    print("Starting model training...")

    # Check if data files exist
    phishing_path = "../data/phishing_urls.csv"
    legitimate_path = "../data/legitimate_urls.csv"

    if os.path.exists(phishing_path) and os.path.exists(legitimate_path):
        print("Loading data from CSV files...")
        phishing_df = pd.read_csv(phishing_path)
        legitimate_df = pd.read_csv(legitimate_path)
    else:
        print("CSV files not found. Creating sample data...")
        phishing_df, legitimate_df = create_sample_data()

    # Combine datasets
    df = pd.concat([phishing_df, legitimate_df], ignore_index=True)
    print(
        f"Total samples: {len(df)} (Phishing: {len(phishing_df)}, Legitimate: {len(legitimate_df)})")

    # Extract features
    print("Extracting features...")
    extractor = FeatureExtractor()

    features_list = []
    for url in df['url']:
        features = extractor.extract_url_features(url)
        features_list.append(features)

    # Convert to DataFrame
    features_df = pd.DataFrame(features_list)

    # Prepare training data
    X = features_df.values
    y = df['label'].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred,
          target_names=['Legitimate', 'Phishing']))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature importance
    feature_names = features_df.columns
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    print("\nTop 5 Most Important Features:")
    for i in range(min(5, len(feature_names))):
        print(
            f"{i+1}. {feature_names[indices[i]]}: {importances[indices[i]]:.4f}")

    # Save model
    print("\nSaving model...")
    joblib.dump(model, "model.pkl")
    print("Model saved as model.pkl")

    return model


if __name__ == "__main__":
    train_model()
