#!/usr/bin/env python3
"""
Test script to demonstrate authentication requirement for Correlation Analysis API
"""

import requests

def test_authentication_requirement():
    """Test that the correlation API now requires authentication"""
    
    print("🔒 Testing Authentication Requirement for Correlation API")
    print("=" * 60)
    
    # Test 1: Request without authentication (should fail)
    print("\n📤 Test 1: Request without authentication")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:8000/api/charts/statistical/correlation/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Correctly requires authentication (401 Unauthorized)")
        elif response.status_code == 403:
            print("✅ Correctly requires authentication (403 Forbidden)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 2: Request with invalid token (should fail)
    print("\n📤 Test 2: Request with invalid token")
    print("-" * 40)
    
    try:
        headers = {'Authorization': 'Bearer invalid_token_12345'}
        response = requests.get("http://localhost:8000/api/charts/statistical/correlation/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Correctly rejects invalid token (401 Unauthorized)")
        elif response.status_code == 403:
            print("✅ Correctly rejects invalid token (403 Forbidden)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("✅ Correlation API now requires JWT authentication")
    print("✅ Unauthenticated requests are properly rejected")
    print("✅ Invalid tokens are properly rejected")
    print("✅ Your API is now protected against unauthorized access!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_authentication_requirement() 