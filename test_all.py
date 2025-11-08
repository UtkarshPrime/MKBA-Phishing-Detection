"""
Master test script to run all tests
"""
import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print('='*70)

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {description}: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("  PHISHING DETECTION SYSTEM - COMPLETE TEST SUITE")
    print("="*70)

    # Change to backend directory
    os.chdir("backend")

    results = {}

    # Test 1: Feature Extraction
    results["Feature Extraction"] = run_command(
        f"{sys.executable} test_features.py",
        "TEST 1: Feature Extraction"
    )

    # Test 2: Model Testing
    results["Model Testing"] = run_command(
        f"{sys.executable} test_model.py",
        "TEST 2: ML Model Predictions"
    )

    # Test 3: API Testing
    results["API Testing"] = run_command(
        f"{sys.executable} test_api.py",
        "TEST 3: REST API Endpoints"
    )

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)

    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status:12} - {test_name}")

    total = len(results)
    passed = sum(results.values())

    print("="*70)
    print(f"  OVERALL: {passed}/{total} test suites passed")
    print("="*70 + "\n")

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
