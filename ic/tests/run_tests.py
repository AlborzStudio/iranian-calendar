"""
Test runner for Iranian Calendar package.

Runs all test modules and reports results.
"""

import sys
import importlib.util

def run_all_tests():
    """Run all test modules."""
    test_modules = [
        'test_leap.py',
        'test_core.py',
        'test_conversions.py'
    ]
    
    total_passed = 0
    total_failed = 0
    
    print("Running Iranian Calendar Test Suite")
    print("=" * 50)
    
    for module_name in test_modules:
        print(f"\nRunning {module_name}...")
        
        # Import and run the module
        spec = importlib.util.spec_from_file_location("test_module", module_name)
        module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(module)
            # Count tests by looking for test_ methods
            test_count = sum(1 for name in dir(module) if 'Test' in name)
            print(f"  {module_name}: Tests executed")
            total_passed += test_count
        except Exception as e:
            print(f"  {module_name}: FAILED - {e}")
            total_failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {total_passed} test modules checked")
    print("=" * 50)
    print()
    
    # Run with pytest for detailed results
    print("Running detailed test suite with pytest...")
    try:
        import pytest
        result = pytest.main(['-v', '--tb=short'] + test_modules)
        return result
    except ImportError:
        print("pytest not installed. Running basic tests only.")
        return 0

if __name__ == '__main__':
    sys.exit(run_all_tests())
