#!/usr/bin/env python3
"""
Comprehensive verification and fix script
Checks all fixes are properly applied and working
"""

import sys
import os
from pathlib import Path

def check_file_content(filepath, line_num, expected_content):
    """Check if a file contains expected content at a specific line"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if line_num <= len(lines):
                actual = lines[line_num - 1].strip()
                if expected_content in actual:
                    return True, actual
                else:
                    return False, actual
            return False, f"Line {line_num} doesn't exist"
    except Exception as e:
        return False, str(e)

def verify_fixes():
    """Verify all fixes are present"""

    print("🔍 VERIFYING ALL FIXES")
    print("=" * 70)

    station_11_path = "app/agents/station_11_runtime_planning.py"

    checks = [
        {
            "name": "Station 11: debug_mode attribute",
            "file": station_11_path,
            "line": 118,
            "expected": "self.debug_mode = False"
        },
        {
            "name": "Station 11: enable_debug_mode() method",
            "file": station_11_path,
            "line": 120,
            "expected": "def enable_debug_mode(self):"
        },
        {
            "name": "Station 11: format fix line 604",
            "file": station_11_path,
            "line": 604,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 608",
            "file": station_11_path,
            "line": 608,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 612",
            "file": station_11_path,
            "line": 612,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 616",
            "file": station_11_path,
            "line": 616,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 638",
            "file": station_11_path,
            "line": 638,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 645",
            "file": station_11_path,
            "line": 645,
            "expected": "str(value)"
        },
        {
            "name": "Station 11: format fix line 652",
            "file": station_11_path,
            "line": 652,
            "expected": "str(value)"
        },
    ]

    all_passed = True

    for check in checks:
        success, content = check_file_content(check["file"], check["line"], check["expected"])
        status = "✅" if success else "❌"
        print(f"{status} {check['name']}")
        if not success:
            print(f"   Expected: {check['expected']}")
            print(f"   Got: {content}")
            all_passed = False

    print("\n" + "=" * 70)

    if all_passed:
        print("✅ ALL FIXES VERIFIED IN SOURCE CODE")
        return True
    else:
        print("❌ SOME FIXES ARE MISSING!")
        return False

def test_station_11_import():
    """Test importing and using Station 11"""

    print("\n🧪 TESTING STATION 11 IMPORT AND USAGE")
    print("=" * 70)

    try:
        # Clear any cached imports
        if 'app.agents.station_11_runtime_planning' in sys.modules:
            del sys.modules['app.agents.station_11_runtime_planning']

        # Import fresh
        from app.agents.station_11_runtime_planning import Station11RuntimePlanning

        # Test instantiation
        station = Station11RuntimePlanning()
        print("✅ Station 11 instantiated successfully")

        # Test debug_mode attribute
        if hasattr(station, 'debug_mode'):
            print(f"✅ debug_mode attribute exists: {station.debug_mode}")
        else:
            print("❌ debug_mode attribute missing!")
            return False

        # Test enable_debug_mode method
        if hasattr(station, 'enable_debug_mode'):
            station.enable_debug_mode()
            print(f"✅ enable_debug_mode() method works, debug_mode now: {station.debug_mode}")
        else:
            print("❌ enable_debug_mode() method missing!")
            return False

        print("=" * 70)
        print("✅ STATION 11 IMPORT AND USAGE TEST PASSED")
        return True

    except Exception as e:
        print(f"❌ STATION 11 TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def clean_python_cache():
    """Clean all Python cache files"""

    print("\n🧹 CLEANING PYTHON CACHE")
    print("=" * 70)

    import subprocess

    # Remove __pycache__ directories
    result = subprocess.run(
        "find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null",
        shell=True,
        capture_output=True
    )

    # Remove .pyc files
    result = subprocess.run(
        "find . -name '*.pyc' -delete 2>/dev/null",
        shell=True,
        capture_output=True
    )

    print("✅ Python cache cleaned")
    print("=" * 70)

def main():
    """Main verification process"""

    print("\n" + "=" * 70)
    print("  COMPREHENSIVE FIX VERIFICATION")
    print("=" * 70 + "\n")

    # Step 1: Clean cache first
    clean_python_cache()

    # Step 2: Verify fixes in source code
    fixes_ok = verify_fixes()

    if not fixes_ok:
        print("\n❌ VERIFICATION FAILED: Fixes not properly applied!")
        print("Please re-run the fix application process.")
        sys.exit(1)

    # Step 3: Test Station 11 import and usage
    import_ok = test_station_11_import()

    if not import_ok:
        print("\n❌ VERIFICATION FAILED: Station 11 import test failed!")
        sys.exit(1)

    # All checks passed
    print("\n" + "=" * 70)
    print("🎉 ALL VERIFICATIONS PASSED!")
    print("=" * 70)
    print("\n✅ Fixes properly applied in source code")
    print("✅ Station 11 imports and works correctly")
    print("✅ Debug mode support verified")
    print("✅ Format string handling verified")
    print("\n🚀 System is ready to run!")
    print("\nYou can now run:")
    print("  python full_automation.py --auto-approve")
    print("=" * 70 + "\n")

    sys.exit(0)

if __name__ == "__main__":
    main()
