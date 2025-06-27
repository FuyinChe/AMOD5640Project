#!/usr/bin/env python3
"""
Debug script to test registration endpoint and identify issues
"""
import requests
import json

def test_registration_endpoint():
    """Test the registration endpoint directly"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Debugging Registration Endpoint")
    print("=" * 50)
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print(f"Testing registration with: {test_data}")
    print()
    
    try:
        # Test registration
        print("1. Testing registration endpoint...")
        response = requests.post(f"{base_url}/register/", json=test_data)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            
            # Test verification with a dummy code
            print("\n2. Testing verification endpoint...")
            verify_data = {
                "email": test_data["email"],
                "code": "123456"  # Dummy code
            }
            
            verify_response = requests.post(f"{base_url}/verify/", json=verify_data)
            print(f"   Status Code: {verify_response.status_code}")
            print(f"   Response: {verify_response.text}")
            
        else:
            print("   ❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error: Django server not running")
        print("   💡 Start Django server with: python manage.py runserver")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_email_config():
    """Test email configuration endpoint"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("\n📧 Testing Email Configuration")
    print("=" * 50)
    
    test_email = input("Enter email to test: ")
    
    try:
        response = requests.post(f"{base_url}/test-email/", json={"email": test_email})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email test successful!")
        else:
            print("❌ Email test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Django server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_server_status():
    """Check if Django server is running"""
    
    print("🔍 Checking Django Server Status")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/")
        print(f"Server Status: ✅ Running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("Server Status: ❌ Not running")
        print("💡 Start Django server with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"Server Status: ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Registration Debug Tool")
    print("=" * 60)
    
    # Check server status first
    server_running = check_server_status()
    
    if server_running:
        # Test registration
        test_registration_endpoint()
        
        # Test email configuration
        print("\n" + "="*60)
        test_email_config()
    else:
        print("\n❌ Cannot proceed without Django server running")
        print("💡 Please start the Django server and try again") 