"""
Simple API tests using direct function calls
"""
from app import app, feature_extractor, model
import os


def test_api():
    """Test the Phishing Detection API"""
    print("\n" + "="*60)
    print("PHISHING DETECTION API - TEST SUITE")
    print("="*60 + "\n")

    # Check if model exists
    if not os.path.exists("model.pkl"):
        print("❌ ERROR: model.pkl not found!")
        print("Please run 'python train_model.py' first.\n")
        return False

    print("Model found ✓\n")
    print("Running tests...\n")

    passed = 0
    failed = 0

    # Test 1: Feature extraction for phishing URL
    print("Test 1: Phishing URL Detection")
    try:
        features = feature_extractor.extract_url_features(
            "http://paypal-verify.com/login")
        assert features['suspicious_keywords'] > 0
        assert features['https'] == 0
        print("✓ Phishing URL features extracted correctly")
        print(f"  - Suspicious keywords: {features['suspicious_keywords']}")
        print(f"  - HTTPS: {features['https']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 2: Feature extraction for legitimate URL
    print("Test 2: Legitimate URL Detection")
    try:
        features = feature_extractor.extract_url_features(
            "https://www.google.com")
        assert features['https'] == 1
        assert features['suspicious_keywords'] == 0
        print("✓ Legitimate URL features extracted correctly")
        print(f"  - HTTPS: {features['https']}")
        print(f"  - Suspicious keywords: {features['suspicious_keywords']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 3: IP address detection
    print("Test 3: IP Address Detection")
    try:
        features = feature_extractor.extract_url_features(
            "http://192.168.1.1/login")
        assert features['has_ip'] == 1
        print("✓ IP address detected correctly")
        print(f"  - Has IP: {features['has_ip']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 4: URL shortener detection
    print("Test 4: URL Shortener Detection")
    try:
        features = feature_extractor.extract_url_features(
            "https://bit.ly/3xYz123")
        assert features['is_shortened'] == 1
        print("✓ URL shortener detected correctly")
        print(f"  - Is shortened: {features['is_shortened']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 5: Email urgency detection
    print("Test 5: Email Urgency Detection")
    try:
        features = feature_extractor.extract_email_features(
            "URGENT: Verify your account now!")
        assert features['urgency_count'] > 0
        print("✓ Email urgency detected correctly")
        print(f"  - Urgency count: {features['urgency_count']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 6: Email URL extraction
    print("Test 6: Email URL Extraction")
    try:
        features = feature_extractor.extract_email_features(
            "Click here: http://test.com and http://example.com")
        assert features['url_count'] >= 2
        print("✓ Email URLs extracted correctly")
        print(f"  - URL count: {features['url_count']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 7: Model prediction for phishing
    print("Test 7: Model Prediction - Phishing URL")
    try:
        import numpy as np
        features = feature_extractor.extract_url_features(
            "http://paypal-verify.com/login")
        feature_names = ['url_length', 'domain_length', 'path_length', 'subdomain_count',
                         'has_ip', 'dot_count', 'dash_count', 'at_symbol',
                         'double_slash_redirect', 'https', 'suspicious_keywords',
                         'is_shortened', 'special_char_count', 'digit_ratio']
        feature_vector = np.array(
            [[features.get(name, 0) for name in feature_names]])
        prediction = model.predict(feature_vector)[0]
        probability = model.predict_proba(feature_vector)[0]
        score = probability[1] * 100

        assert score > 40  # Should be at least suspicious
        print("✓ Model correctly identified phishing URL")
        print(f"  - Prediction: {prediction}")
        print(f"  - Score: {score:.1f}/100")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 8: Model prediction for legitimate
    print("Test 8: Model Prediction - Legitimate URL")
    try:
        import numpy as np
        features = feature_extractor.extract_url_features(
            "https://www.google.com")
        feature_names = ['url_length', 'domain_length', 'path_length', 'subdomain_count',
                         'has_ip', 'dot_count', 'dash_count', 'at_symbol',
                         'double_slash_redirect', 'https', 'suspicious_keywords',
                         'is_shortened', 'special_char_count', 'digit_ratio']
        feature_vector = np.array(
            [[features.get(name, 0) for name in feature_names]])
        prediction = model.predict(feature_vector)[0]
        probability = model.predict_proba(feature_vector)[0]
        score = probability[1] * 100

        assert score < 70  # Should be legitimate or suspicious at most
        print("✓ Model correctly identified legitimate URL")
        print(f"  - Prediction: {prediction}")
        print(f"  - Score: {score:.1f}/100")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Summary
    print("="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)
