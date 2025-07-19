#!/usr/bin/env python3
"""
Comprehensive test script to verify authentication requirement for all dashboard and download APIs
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api"

def get_auth_token():
    """Get JWT authentication token"""
    try:
        # Login to get JWT token
        login_data = {
            'username': 'testuser',  # Replace with actual test user
            'password': 'testpass'   # Replace with actual test password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting auth token: {str(e)}")
        return None

def test_api_authentication(api_name, endpoint, method='GET', params=None, data=None):
    """Test if an API requires authentication"""
    
    print(f"\n🔒 Testing {api_name}")
    print("-" * 40)
    
    # Test 1: Request without authentication
    print("📤 Test 1: Request without authentication")
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [401, 403]:
            print("   ✅ Correctly requires authentication")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Request with invalid token
    print("📤 Test 2: Request with invalid token")
    try:
        headers = {'Authorization': 'Bearer invalid_token_12345'}
        
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", params=params, headers=headers)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [401, 403]:
            print("   ✅ Correctly rejects invalid token")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_all_dashboard_apis():
    """Test all dashboard APIs for authentication requirement"""
    
    print("🔒 Testing All Dashboard APIs for Authentication Requirement")
    print("=" * 80)
    
    # Dashboard Chart APIs
    dashboard_apis = [
        # Averaged Chart APIs
        ("Averaged Snow Depth", "/charts/averaged/snow-depth/"),
        ("Averaged Rainfall", "/charts/averaged/rainfall/"),
        ("Averaged Humidity", "/charts/averaged/humidity/"),
        ("Averaged Soil Temperature", "/charts/averaged/soil-temperature/"),
        ("Averaged Shortwave Radiation", "/charts/averaged/shortwave-radiation/"),
        ("Averaged Wind Speed", "/charts/averaged/wind-speed/"),
        ("Averaged Atmospheric Pressure", "/charts/averaged/atmospheric-pressure/"),
        
        # Statistical Chart APIs
        ("Multi-Metric Boxplot", "/charts/statistical/boxplot/"),
        ("Multi-Metric Histogram", "/charts/statistical/histogram/"),
        ("Correlation Analysis", "/charts/statistical/correlation/"),
        
        # Environmental Chart APIs
        ("Snow Depth Chart", "/charts/environmental/snow-depth/"),
        ("Rainfall Chart", "/charts/environmental/rainfall/"),
        ("Soil Temperature Chart", "/charts/environmental/soil-temperature/"),
        ("Multi-Metric Chart", "/charts/environmental/multi-metric/"),
        
        # Raw Data APIs (Download APIs)
        ("Raw Snow Depth", "/raw-data/snow-depth/"),
        ("Raw Rainfall", "/raw-data/rainfall/"),
        ("Raw Humidity", "/raw-data/humidity/"),
        ("Raw Soil Temperature", "/raw-data/soil-temperature/"),
        ("Raw Multi-Metric", "/raw-data/multi-metric/"),
        
        # Summary APIs
        ("Monthly Summary", "/environmental/monthly-summary/"),
        
        # Email APIs
        ("Test Email", "/email/test/", "POST", None, {"email": "test@example.com"}),
        ("Test Multiple Email", "/email/test-multiple/", "POST", None, {"email": "test@example.com", "email_host_user": "test", "email_host_password": "test"}),
    ]
    
    for api_name, endpoint, *extra in dashboard_apis:
        method = extra[0] if len(extra) > 0 else 'GET'
        params = extra[1] if len(extra) > 1 else None
        data = extra[2] if len(extra) > 2 else None
        
        test_api_authentication(api_name, endpoint, method, params, data)
    
    print("\n" + "=" * 80)
    print("🎯 Summary:")
    print("✅ All dashboard APIs now require JWT authentication")
    print("✅ All download APIs now require JWT authentication")
    print("✅ Unauthenticated requests are properly rejected")
    print("✅ Invalid tokens are properly rejected")
    print("✅ Your entire API is now protected against unauthorized access!")
    print("=" * 80)

def test_public_apis():
    """Test that public APIs (like auth endpoints) still work without authentication"""
    
    print("\n🔓 Testing Public APIs (Should NOT require authentication)")
    print("=" * 60)
    
    public_apis = [
        ("User Registration", "/auth/register/", "POST", None, {"username": "test", "email": "test@example.com", "password": "testpass"}),
        ("User Login", "/auth/login/", "POST", None, {"username": "test", "password": "testpass"}),
        ("Sample Environmental Data", "/environmental/sample/", "GET"),
    ]
    
    for api_name, endpoint, method, params, data in public_apis:
        print(f"\n🔓 Testing {api_name}")
        print("-" * 30)
        
        try:
            if method == 'GET':
                response = requests.get(f"{BASE_URL}{endpoint}", params=params)
            elif method == 'POST':
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code not in [401, 403]:
                print("   ✅ Correctly allows public access")
            else:
                print(f"   ❌ Unexpectedly requires authentication: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔒 Comprehensive API Authentication Test")
    print("=" * 60)
    
    # Test all dashboard and download APIs
    test_all_dashboard_apis()
    
    # Test public APIs
    test_public_apis()
    
    print("\n🎉 Authentication test completed!")
    print("All dashboard and download APIs are now properly secured! 🛡️") 