import joblib
import numpy as np
from feature_extractor import FeatureExtractor
import os


def test_model():
    """Test the trained model"""
    print("\n" + "="*60)
    print("ML MODEL - TEST SUITE")
    print("="*60 + "\n")

    # Check if model exists
    if not os.path.exists("model.pkl"):
        print("❌ ERROR: model.pkl not found!")
        print("Please run 'python train_model.py' first.\n")
        return False

    # Load model
    print("Loading model...")
    model = joblib.load("model.pkl")
    print("✓ Model loaded successfully\n")

    # Initialize feature extractor
    extractor = FeatureExtractor()

    # Test cases
    test_cases = [
        ("http://paypal-verify.com/login", "Phishing", 1),
        ("https://www.google.com", "Legitimate", 0),
        ("http://192.168.1.1/login", "Phishing (IP)", 1),
        ("https://www.amazon.com", "Legitimate", 0),
        ("http://secure-banking-update.net/account", "Phishing", 1),
    ]

    print("Testing model predictions:\n")

    correct = 0
    total = len(test_cases)

    for url, expected_type, expected_label in test_cases:
        # Extract features
        features = extractor.extract_url_features(url)

        # Prepare feature vector
        feature_names = ['url_length', 'domain_length', 'path_length', 'subdomain_count',
                         'has_ip', 'dot_count', 'dash_count', 'at_symbol',
                         'double_slash_redirect', 'https', 'suspicious_keywords',
                         'is_shortened', 'special_char_count', 'digit_ratio']

        feature_vector = np.array(
            [[features.get(name, 0) for name in feature_names]])

        # Predict
        prediction = model.predict(feature_vector)[0]
        probability = model.predict_proba(feature_vector)[0]

        # Calculate score
        phishing_prob = probability[1] if len(
            probability) > 1 else probability[0]
        score = phishing_prob * 100

        # Determine classification
        if score > 70:
            classification = "phishing"
        elif score > 40:
            classification = "suspicious"
        else:
            classification = "legitimate"

        # Check if correct
        is_correct = (prediction == expected_label)
        if is_correct:
            correct += 1

        status = "✓" if is_correct else "✗"
        print(f"{status} URL: {url}")
        print(f"  Expected: {expected_type} ({expected_label})")
        print(f"  Predicted: {classification} ({prediction})")
        print(f"  Score: {score:.1f}/100")
        print(f"  Confidence: {max(probability)*100:.1f}%")
        print()

    accuracy = (correct / total) * 100
    print("="*60)
    print(f"MODEL ACCURACY: {accuracy:.1f}% ({correct}/{total} correct)")
    print("="*60 + "\n")

    return accuracy >= 60  # At least 60% accuracy expected


if __name__ == "__main__":
    success = test_model()
    exit(0 if success else 1)
