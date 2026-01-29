#!/usr/bin/env python3
"""
Anomaly Detection Integration Verification Script
Verifies all components are properly configured and working.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from emissions.models import EmissionLog
from dashboard.views import detect_anomaly, detect_user_anomalies, get_anomaly_summary
import numpy as np

def verify_imports():
    """Verify all imports work correctly"""
    print("✓ All imports successful")
    return True

def verify_numpy():
    """Verify numpy is working"""
    test_array = np.array([1, 2, 3, 4, 5])
    mean = np.mean(test_array)
    assert mean == 3.0, "Numpy mean calculation failed"
    print("✓ Numpy working correctly")
    return True

def verify_detect_anomaly():
    """Test the detect_anomaly function"""
    history = [2.0, 2.1, 2.2, 2.3, 2.4]
    
    # Normal value
    is_anom, z_score, desc = detect_anomaly(2.5, history)
    assert not is_anom, "Normal value incorrectly flagged as anomaly"
    
    # Anomalous value
    is_anom, z_score, desc = detect_anomaly(5.0, history)
    assert is_anom, "Anomalous value not detected"
    assert z_score > 2.5, f"Z-score should be > 2.5, got {z_score}"
    
    print("✓ detect_anomaly() working correctly")
    return True

def verify_database():
    """Verify database is accessible"""
    try:
        user_count = User.objects.count()
        emission_count = EmissionLog.objects.count()
        print(f"✓ Database accessible ({user_count} users, {emission_count} emissions)")
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def verify_user_anomalies():
    """Test detect_user_anomalies with actual data if available"""
    users = User.objects.all()
    
    if not users.exists():
        print("⚠ No users found in database (skip user anomaly test)")
        return True
    
    user = users.first()
    try:
        result = detect_user_anomalies(user)
        assert isinstance(result, dict), "Result should be a dict"
        assert 'has_anomalies' in result, "Missing 'has_anomalies' key"
        assert 'anomalies' in result, "Missing 'anomalies' key"
        print(f"✓ detect_user_anomalies() working for {user.username}")
        return True
    except Exception as e:
        print(f"✗ detect_user_anomalies error: {e}")
        return False

def verify_anomaly_summary():
    """Test get_anomaly_summary with actual data if available"""
    users = User.objects.all()
    
    if not users.exists():
        print("⚠ No users found in database (skip summary test)")
        return True
    
    user = users.first()
    try:
        summary = get_anomaly_summary(user)
        assert isinstance(summary, dict), "Result should be a dict"
        assert 'status' in summary, "Missing 'status' key"
        assert 'severity' in summary, "Missing 'severity' key"
        assert 'count' in summary, "Missing 'count' key"
        print(f"✓ get_anomaly_summary() working for {user.username}")
        return True
    except Exception as e:
        print(f"✗ get_anomaly_summary error: {e}")
        return False

def verify_views():
    """Verify views are properly configured"""
    try:
        from dashboard.views import dashboard
        from emissions.views import anomaly_check
        print("✓ All views imported successfully")
        return True
    except ImportError as e:
        print(f"✗ View import error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("\n" + "="*60)
    print("ANOMALY DETECTION - INTEGRATION VERIFICATION")
    print("="*60 + "\n")
    
    tests = [
        ("Imports", verify_imports),
        ("Numpy", verify_numpy),
        ("detect_anomaly()", verify_detect_anomaly),
        ("Database", verify_database),
        ("Views", verify_views),
        ("User Anomalies", verify_user_anomalies),
        ("Anomaly Summary", verify_anomaly_summary),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - SYSTEM READY!")
        print("\nYour anomaly detection system is fully operational.")
        print("Start the server and access: http://localhost:8000/dashboard/")
    else:
        print(f"\n⚠ {total - passed} test(s) failed - review above for details")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
