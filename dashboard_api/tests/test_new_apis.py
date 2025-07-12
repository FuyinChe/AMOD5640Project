#!/usr/bin/env python3
"""
Simple test script for the three new API endpoints:
- Shortwave Radiation
- Wind Speed  
- Atmospheric Pressure
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_new_apis():
    """Test the three new API endpoints"""
    
    print("Testing New API Endpoints...")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        {
            'name': 'Shortwave Radiation',
            'url': '/charts/shortwave-radiation/',
            'unit': 'W/m²'
        },
        {
            'name': 'Wind Speed',
            'url': '/charts/wind-speed/',
            'unit': 'm/s'
        },
        {
            'name': 'Atmospheric Pressure',
            'url': '/charts/atmospheric-pressure/',
            'unit': 'kPa'
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing: {endpoint['name']}")
        print("-" * 30)
        
        try:
            # Test basic endpoint
            response = requests.get(f"{BASE_URL}{endpoint['url']}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Status: {response.status_code}")
                print(f"   📊 Unit: {data.get('unit', 'N/A')}")
                
                if data.get('data') and len(data['data']) > 0:
                    sample = data['data'][0]
                    print(f"   📈 Sample data: {sample}")
                    
                    # Check required fields
                    required_fields = ['period', 'avg', 'max', 'min']
                    missing_fields = [field for field in required_fields if field not in sample]
                    if not missing_fields:
                        print(f"   ✅ All required fields present")
                    else:
                        print(f"   ❌ Missing fields: {missing_fields}")
                else:
                    print(f"   ℹ️  No data available (this is normal if no data exists)")
            else:
                print(f"   ❌ Failed! Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ New API Endpoints Test Completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_new_apis() 