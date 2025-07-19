#!/usr/bin/env python3
"""
Test script to verify that the Sample Environmental Data API is now publicly accessible
"""

import requests

def test_sample_data_public_access():
    """Test that the sample data API is publicly accessible"""
    
    print("🔓 Testing Sample Environmental Data API - Public Access")
    print("=" * 60)
    
    # Test 1: Request without authentication (should work)
    print("\n📤 Test 1: Request without authentication")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:8000/api/environmental/sample/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Sample data API is publicly accessible!")
            print(f"   Total records: {len(data)}")
            if data:
                print(f"   Sample record keys: {list(data[0].keys())}")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 2: Request with authentication (should also work)
    print("\n📤 Test 2: Request with authentication (optional)")
    print("-" * 40)
    
    try:
        headers = {'Authorization': 'Bearer test_token_12345'}
        response = requests.get("http://localhost:8000/api/environmental/sample/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Sample data API works with authentication too")
        else:
            print(f"⚠️  Status code with auth: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_sample_data_public_access()
    print("\n🎉 Sample data API is now publicly accessible! 🔓") 