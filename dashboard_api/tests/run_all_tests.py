#!/usr/bin/env python3
"""
Test runner for Trent Farm Data test suite
Run all tests or specific tests from the tests folder
"""
import os
import sys
import subprocess
import time

def print_header():
    """Print a header for the test suite runner, including project and folder info."""
    print("🚀 Trent Farm Data - Test Suite Runner")
    print("=" * 60)
    print("📁 All test files are organized in the tests/ folder")
    print()

def list_test_files():
    """List all available test files and their descriptions for the user to choose from."""
    test_files = [
        ("test_email.py", "Comprehensive email system testing"),
        ("test_email_quick.py", "Quick email troubleshooting"),
        ("test_registration.py", "Registration and verification flow"),
        ("test_complete_flow.py", "Complete end-to-end testing"),
        ("test_api_only.py", "Pure API testing with Django emails")
    ]
    
    print("📋 Available Test Files:")
    print("-" * 40)
    for i, (filename, description) in enumerate(test_files, 1):
        print(f"{i}. {filename}")
        print(f"   {description}")
        print()
    
    return test_files

def run_test(test_file):
    """Run a specific test file"""
    print(f"🧪 Running: {test_file}")
    print("=" * 50)
    
    try:
        # Run the test file
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"\n✅ {test_file} completed successfully!")
        else:
            print(f"\n❌ {test_file} failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ Error running {test_file}: {e}")
        return False

def run_all_tests():
    """Run all test files in sequence, stopping if any test fails, and print a summary."""
    test_files = [
        "test_email.py",
        "test_email_quick.py", 
        "test_registration.py",
        "test_complete_flow.py",
        "test_api_only.py"
    ]
    
    print("🔄 Running all tests in sequence...")
    print("=" * 50)
    
    results = []
    for test_file in test_files:
        success = run_test(test_file)
        results.append((test_file, success))
        
        if not success:
            print(f"\n⚠️ Stopping at failed test: {test_file}")
            print("💡 Fix the issue and run again, or run individual tests")
            break
            
        print("\n" + "="*50 + "\n")
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("📊 Test Results Summary:")
    print("-" * 30)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_file, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_file}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

def main():
    """Main entry point for the test runner. Handles user interaction and test selection."""
    print_header()
    
    # Check if Django server is running (for API tests)
    print("💡 Note: For API tests, ensure Django server is running:")
    print("   python manage.py runserver")
    print()
    
    while True:
        print("Choose an option:")
        print("1. Run all tests")
        print("2. Run specific test")
        print("3. List test files")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_all_tests()
            break
        elif choice == "2":
            test_files = list_test_files()
            try:
                test_num = int(input("\nEnter test number (1-5): ").strip())
                if 1 <= test_num <= len(test_files):
                    test_file = test_files[test_num - 1][0]
                    run_test(test_file)
                else:
                    print("❌ Invalid test number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        elif choice == "3":
            list_test_files()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main() 