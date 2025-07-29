#!/usr/bin/env python3
"""
Simple test script for the new Air Temperature API endpoint
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_air_temperature_api():
    """Test the new air temperature API endpoint"""
    
    print("Testing Air Temperature API Endpoint")
    print("=" * 50)
    
    # Test 1: Basic air temperature data retrieval
    print("\n1. Testing: Basic air temperature data retrieval")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! API endpoint is working")
            print(f"Response structure: {list(data.keys())}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"Sample data point: {sample}")
                print(f"Unit: {data.get('unit', 'N/A')}")
                
                # Validate required fields
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print("✅ All required fields present")
                else:
                    print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ API working but no data available for the period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Air temperature with monthly grouping
    print("\n2. Testing: Air temperature with monthly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/?group_by=month&year=2023")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                print(f"✅ Success! Retrieved monthly air temperature data")
                print(f"Number of data points: {len(data['data'])}")
                print(f"Sample monthly data: {data['data'][0]}")
            else:
                print("✅ API working but no monthly data available for 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Air temperature with date range
    print("\n3. Testing: Air temperature with date range")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/?start_date=2023-01-01&end_date=2023-01-31&group_by=day")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                print(f"✅ Success! Retrieved daily air temperature data for January 2023")
                print(f"Number of data points: {len(data['data'])}")
                print(f"Sample daily data: {data['data'][0]}")
            else:
                print("✅ API working but no daily data available for January 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Air Temperature API Test Completed!")

if __name__ == "__main__":
    test_air_temperature_api() 