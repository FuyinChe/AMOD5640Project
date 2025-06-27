#!/usr/bin/env python3
"""
Complete Registration Script
Helps you complete the registration process by using the verification code
"""
import requests
import json

def complete_registration():
    """Complete registration with verification code"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔐 Complete Registration Process")
    print("=" * 50)
    
    # Get user input
    email = input("Enter your registered email: ")
    verification_code = input("Enter the verification code from your email: ")
    
    print(f"\nVerifying email: {email}")
    print(f"Using code: {verification_code}")
    
    # Verify email
    verify_data = {
        "email": email,
        "code": verification_code
    }
    
    try:
        response = requests.post(f"{base_url}/verify/", json=verify_data)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Email verified successfully!")
            print("🎉 Your account is now active!")
            
            # Test login
            print("\n🔑 Testing login...")
            login_data = {
                "email": email,
                "password": input("Enter your password to test login: ")
            }
            
            login_response = requests.post(f"{base_url}/token", json=login_data)
            print(f"Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Login successful!")
                token_data = login_response.json()
                print(f"Access Token: {token_data.get('access', 'N/A')[:20]}...")
            else:
                print("❌ Login failed!")
                print(f"Login Response: {login_response.text}")
                
        else:
            print("\n❌ Email verification failed!")
            
            # Check if code expired
            if "expired" in response.text.lower():
                print("💡 The verification code has expired.")
                print("💡 You can request a new code using the resend endpoint.")
                
                resend = input("\nWould you like to resend the verification code? (y/n): ")
                if resend.lower() == 'y':
                    resend_code(email, base_url)
                    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Django server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

def resend_code(email, base_url):
    """Resend verification code"""
    
    print(f"\n📧 Resending verification code to {email}...")
    
    try:
        response = requests.post(f"{base_url}/resend-code/", json={"email": email})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ New verification code sent!")
            print("📧 Please check your email for the new code.")
        else:
            print("❌ Failed to resend verification code!")
            
    except Exception as e:
        print(f"❌ Error resending code: {e}")

def test_registration_flow():
    """Test the complete registration flow"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("🧪 Test Complete Registration Flow")
    print("=" * 50)
    
    # Step 1: Register
    test_email = input("Enter test email: ")
    test_password = input("Enter test password: ")
    
    register_data = {
        "email": test_email,
        "password": test_password
    }
    
    print(f"\n1️⃣ Registering user: {test_email}")
    
    try:
        response = requests.post(f"{base_url}/register/", json=register_data)
        
        if response.status_code == 201:
            print(f"✅ Registration successful!")
            print(f"📧 Please check your email for the verification code.")
            # Step 2: Prompt user for code
            verification_code = input("Enter the verification code from your email: ").strip()
            print(f"\n2️⃣ Verifying email with code: {verification_code}")
            
            verify_data = {
                "email": test_email,
                "code": verification_code
            }
            
            verify_response = requests.post(f"{base_url}/verify/", json=verify_data)
            
            if verify_response.status_code == 200:
                print("✅ Email verification successful!")
                
                # Step 3: Login
                print(f"\n3️⃣ Testing login...")
                
                login_data = {
                    "email": test_email,
                    "password": test_password
                }
                
                login_response = requests.post(f"{base_url}/token", json=login_data)
                
                if login_response.status_code == 200:
                    print("✅ Login successful!")
                    print("🎉 Complete registration flow test passed!")
                else:
                    print("❌ Login failed!")
                    print(f"Login Response: {login_response.text}")
            else:
                print("❌ Email verification failed!")
                print(f"Verify Response: {verify_response.text}")
        else:
            print("❌ Registration failed!")
            print(f"Register Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Registration Completion Tool")
    print("=" * 60)
    
    print("Choose an option:")
    print("1. Complete existing registration (with verification code)")
    print("2. Test complete registration flow")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        complete_registration()
    elif choice == "2":
        test_registration_flow()
    else:
        print("Invalid choice!") 