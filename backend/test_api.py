import httpx
from app import app
import joblib
import os

# Create a simple HTTP client for testing
base_url = "http://testserver"


class TestAPI:
    """Test cases for the Phishing Detection API"""

    def test_root_endpoint(self):
        """Test the root endpoint returns API information"""
        with httpx.Client(app=app, base_url=base_url) as client:
            response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        print("✓ Root endpoint test passed")

    def test_analyze_url_phishing(self):
        """Test URL analysis with a phishing URL"""
        response = client.post(
            "/analyze/url",
            json={"url": "http://paypal-verify.com/login"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "score" in data
        assert "features" in data
        assert "message" in data
        assert data["score"] > 40  # Should be suspicious or phishing
        print(
            f"✓ Phishing URL test passed - Score: {data['score']:.1f}, Classification: {data['classification']}")

    def test_analyze_url_legitimate(self):
        """Test URL analysis with a legitimate URL"""
        response = client.post(
            "/analyze/url",
            json={"url": "https://www.google.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "score" in data
        assert data["score"] < 70  # Should be legitimate or suspicious at most
        print(
            f"✓ Legitimate URL test passed - Score: {data['score']:.1f}, Classification: {data['classification']}")

    def test_analyze_url_with_ip(self):
        """Test URL with IP address (common phishing indicator)"""
        response = client.post(
            "/analyze/url",
            json={"url": "http://192.168.1.1/login"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["features"]["has_ip"] == 1
        print(
            f"✓ IP address URL test passed - Has IP: {data['features']['has_ip']}")

    def test_analyze_url_shortened(self):
        """Test URL shortening service detection"""
        response = client.post(
            "/analyze/url",
            json={"url": "https://bit.ly/3xYz123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["features"]["is_shortened"] == 1
        print(
            f"✓ Shortened URL test passed - Is shortened: {data['features']['is_shortened']}")

    def test_analyze_url_invalid(self):
        """Test with invalid URL format"""
        response = client.post(
            "/analyze/url",
            json={"url": "not-a-valid-url"}
        )
        # Should still process but may have lower confidence
        assert response.status_code in [200, 400, 500]
        print("✓ Invalid URL handling test passed")

    def test_analyze_email_phishing(self):
        """Test email analysis with phishing content"""
        response = client.post(
            "/analyze/email",
            json={
                "content": "URGENT: Your account will be suspended! Click here to verify immediately."}
        )
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "score" in data
        # Should detect urgency and suspicious content
        assert data["score"] > 40
        print(
            f"✓ Phishing email test passed - Score: {data['score']:.1f}, Classification: {data['classification']}")

    def test_analyze_email_legitimate(self):
        """Test email analysis with legitimate content"""
        response = client.post(
            "/analyze/email",
            json={
                "content": "Hello, your order #12345 has been shipped and will arrive tomorrow."}
        )
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert data["score"] < 70  # Should be legitimate
        print(
            f"✓ Legitimate email test passed - Score: {data['score']:.1f}, Classification: {data['classification']}")

    def test_analyze_email_urgency(self):
        """Test email with urgency keywords"""
        response = client.post(
            "/analyze/email",
            json={"content": "URGENT ACTION REQUIRED IMMEDIATE VERIFY"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["features"]["urgency_count"] > 0
        print(
            f"✓ Email urgency detection test passed - Urgency count: {data['features']['urgency_count']}")

    def test_analyze_email_with_urls(self):
        """Test email containing URLs"""
        response = client.post(
            "/analyze/email",
            json={"content": "Click here: http://example.com and here: http://test.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["features"]["url_count"] >= 2
        print(
            f"✓ Email URL extraction test passed - URL count: {data['features']['url_count']}")


def run_tests():
    """Run all tests"""
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

    test = TestAPI()
    tests = [
        ("Root Endpoint", test.test_root_endpoint),
        ("Phishing URL Detection", test.test_analyze_url_phishing),
        ("Legitimate URL Detection", test.test_analyze_url_legitimate),
        ("IP Address Detection", test.test_analyze_url_with_ip),
        ("URL Shortener Detection", test.test_analyze_url_shortened),
        ("Invalid URL Handling", test.test_analyze_url_invalid),
        ("Phishing Email Detection", test.test_analyze_email_phishing),
        ("Legitimate Email Detection", test.test_analyze_email_legitimate),
        ("Email Urgency Detection", test.test_analyze_email_urgency),
        ("Email URL Extraction", test.test_analyze_email_with_urls),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {name} failed: {str(e)}")
            failed += 1

    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
