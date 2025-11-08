"""
Test the live API server with HTTP requests
Run this after starting the server with: python app.py
"""
import requests
import time
import sys

API_URL = "http://localhost:8000"


def test_live_api():
    """Test the live API server"""
    print("\n" + "="*60)
    print("LIVE API SERVER - TEST SUITE")
    print("="*60 + "\n")

    # Check if server is running
    print("Checking if API server is running...")
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        print("✓ API server is running\n")
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: API server is not running!")
        print("Please start the server first: python app.py\n")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}\n")
        return False

    passed = 0
    failed = 0

    # Test 1: Root endpoint
    print("Test 1: Root Endpoint")
    try:
        response = requests.get(f"{API_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✓ Root endpoint working")
        print(f"  Response: {data['message']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 2: Analyze phishing URL
    print("Test 2: Analyze Phishing URL")
    try:
        response = requests.post(
            f"{API_URL}/analyze/url",
            json={"url": "http://paypal-verify.com/login"}
        )
        assert response.status_code == 200
        data = response.json()
        print("✓ Phishing URL analyzed")
        print(f"  Classification: {data['classification']}")
        print(f"  Score: {data['score']:.1f}/100")
        print(f"  Message: {data['message']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 3: Analyze legitimate URL
    print("Test 3: Analyze Legitimate URL")
    try:
        response = requests.post(
            f"{API_URL}/analyze/url",
            json={"url": "https://www.google.com"}
        )
        assert response.status_code == 200
        data = response.json()
        print("✓ Legitimate URL analyzed")
        print(f"  Classification: {data['classification']}")
        print(f"  Score: {data['score']:.1f}/100")
        print(f"  Message: {data['message']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 4: Analyze phishing email
    print("Test 4: Analyze Phishing Email")
    try:
        response = requests.post(
            f"{API_URL}/analyze/email",
            json={
                "content": "URGENT: Your account will be suspended! Click here to verify immediately."}
        )
        assert response.status_code == 200
        data = response.json()
        print("✓ Phishing email analyzed")
        print(f"  Classification: {data['classification']}")
        print(f"  Score: {data['score']:.1f}/100")
        print(f"  Message: {data['message']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 5: Analyze legitimate email
    print("Test 5: Analyze Legitimate Email")
    try:
        response = requests.post(
            f"{API_URL}/analyze/email",
            json={
                "content": "Hello, your order #12345 has been shipped and will arrive tomorrow."}
        )
        assert response.status_code == 200
        data = response.json()
        print("✓ Legitimate email analyzed")
        print(f"  Classification: {data['classification']}")
        print(f"  Score: {data['score']:.1f}/100")
        print(f"  Message: {data['message']}")
        passed += 1
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    print()

    # Test 6: Performance test
    print("Test 6: Performance Test (10 requests)")
    try:
        start_time = time.time()
        for i in range(10):
            response = requests.post(
                f"{API_URL}/analyze/url",
                json={"url": f"http://test{i}.com"}
            )
            assert response.status_code == 200
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        print(f"✓ Performance test completed")
        print(f"  Average response time: {avg_time*1000:.1f}ms")
        print(f"  Total time: {end_time - start_time:.2f}s")
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
    success = test_live_api()
    sys.exit(0 if success else 1)
