from feature_extractor import FeatureExtractor


def test_feature_extraction():
    """Test feature extraction functionality"""
    print("\n" + "="*60)
    print("FEATURE EXTRACTION - TEST SUITE")
    print("="*60 + "\n")

    extractor = FeatureExtractor()

    # Test URL feature extraction
    print("Testing URL Feature Extraction:\n")

    test_urls = [
        ("https://www.google.com", "Legitimate"),
        ("http://paypal-verify.com/login", "Phishing"),
        ("http://192.168.1.1/login", "IP Address"),
        ("https://bit.ly/3xYz123", "Shortened URL"),
    ]

    for url, description in test_urls:
        print(f"URL: {url}")
        print(f"Type: {description}")
        features = extractor.extract_url_features(url)

        print(f"  - URL Length: {features['url_length']}")
        print(f"  - Domain Length: {features['domain_length']}")
        print(f"  - Has IP: {features['has_ip']}")
        print(f"  - HTTPS: {features['https']}")
        print(f"  - Suspicious Keywords: {features['suspicious_keywords']}")
        print(f"  - Is Shortened: {features['is_shortened']}")
        print(f"  - Subdomain Count: {features['subdomain_count']}")
        print()

    # Test email feature extraction
    print("\nTesting Email Feature Extraction:\n")

    test_emails = [
        ("URGENT: Verify your account now!", "Phishing"),
        ("Your order has been shipped.", "Legitimate"),
        ("Click here http://test.com and here http://example.com", "Multiple URLs"),
    ]

    for content, description in test_emails:
        print(f"Email: {content}")
        print(f"Type: {description}")
        features = extractor.extract_email_features(content)

        print(f"  - Email Length: {features['email_length']}")
        print(f"  - Urgency Count: {features['urgency_count']}")
        print(f"  - URL Count: {features['url_count']}")
        print(f"  - Suspicious Phrases: {features['suspicious_phrases']}")
        print(f"  - Exclamation Count: {features['exclamation_count']}")
        print()

    print("="*60)
    print("All feature extraction tests completed ✓")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_feature_extraction()
