#!/usr/bin/env python3
"""
API-only test script for user registration and verification flow
Tests the Django API endpoints without integrated email sending
"""
import requests
import json

def test_api_registration_flow():
    """Test the API registration and verification flow using actual Django emails"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("🧪 Testing API Registration Flow (Django Email System)")
    print("=" * 60)
    print("💡 This test uses the actual Django email system")
    print("   Check your email for verification codes!")
    print()
    
    # Step 1: Register a new user
    print("1️⃣ Testing User Registration...")
    
    # Get user input for email
    test_email = input("Enter email to register: ").strip()
    test_password = input("Enter password: ").strip()
    
    register_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{base_url}/register/", json=register_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            print("   📧 Check your email for verification code")
        else:
            print("   ❌ Registration failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 2: Get verification code from user
    print("\n2️⃣ Email Verification...")
    print(f"   📧 Email sent to: {test_email}")
    print("   📬 Please check your email (including spam folder)")
    print("   🔐 Enter the 6-digit verification code you received")
    
    verification_code = input("\n   Enter verification code: ").strip()
    
    # Step 3: Verify the email
    print("\n3️⃣ Testing Email Verification...")
    verify_data = {
        "email": test_email,
        "code": verification_code
    }
    
    try:
        response = requests.post(f"{base_url}/verify/", json=verify_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Email verification successful!")
        else:
            print("   ❌ Email verification failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False
    
    # Step 4: Test resend verification code
    print("\n4️⃣ Testing Resend Verification Code...")
    resend_data = {
        "email": test_email
    }
    
    try:
        response = requests.post(f"{base_url}/resend-code/", json=resend_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Resend verification code successful!")
            print("   📧 New verification code sent to your email")
            print("   📬 Check your email for the new code")
        else:
            print("   ⚠️ Resend verification code failed (might be already verified)")
            
    except Exception as e:
        print(f"   ❌ Resend error: {e}")
    
    print("\n🎉 API flow test finished!")
    return True

def test_email_configuration():
    """Test email configuration via API"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("\n📧 Testing Email Configuration via API...")
    print("=" * 60)
    
    test_email = input("Enter email to receive test: ")
    
    try:
        response = requests.post(f"{base_url}/test-email/", json={"email": test_email})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email configuration test successful!")
            print("📧 Check your email for the test message")
            return True
        else:
            print("❌ Email configuration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Trent Farm Data - API-Only Registration Test")
    print("=" * 60)
    print("✅ All valid email addresses are now accepted")
    print("💡 This test uses the actual Django email system")
    print("   No integrated email sending - check your real emails!")
    print()
    
    # Test email configuration first
    email_success = test_email_configuration()
    
    if email_success:
        # Test complete registration flow
        registration_success = test_api_registration_flow()
        
        if registration_success:
            print("\n🎉 All API tests passed! Your registration system is working correctly.")
        else:
            print("\n❌ API registration flow test failed.")
    else:
        print("\n❌ Email configuration test failed. Please fix email settings first.") 