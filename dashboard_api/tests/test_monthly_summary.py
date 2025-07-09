#!/usr/bin/env python3
"""
Test script for the Monthly Summary API endpoint
Moved to tests/ directory as part of code decoupling
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_monthly_summary_api():
    """Test the monthly summary API endpoint"""
    
    print("Testing Monthly Summary API...")
    print("=" * 50)
    
    # Test 1: Get all monthly summaries
    print("\n1. Testing: Get all monthly summaries")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} months of data")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Filter by specific year
    print("\n2. Testing: Filter by year 2023")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/?year=2023")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} months for 2023")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Filter by specific month
    print("\n3. Testing: Filter by month 6 (June)")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/?month=6")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} June records")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 4: Filter by year and month
    print("\n4. Testing: Filter by year 2023 and month 6")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/?year=2023&month=6")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} records for June 2023")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 5: Test date range filter
    print("\n5. Testing: Date range filter (2023-01-01 to 2023-06-30)")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/?start_date=2023-01-01&end_date=2023-06-30")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} months in date range")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 6: Test default behavior (latest year)
    print("\n6. Testing: Default behavior (latest year)")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_months', 0)} months (default: latest year)")
            print(f"   Default behavior: {data.get('default_behavior', 'None')}")
            if data.get('data'):
                print(f"   Sample month: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 7: Test invalid date format
    print("\n7. Testing: Invalid date format")
    try:
        response = requests.get(f"{BASE_URL}/monthly-summary/?start_date=invalid-date")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Success! Properly handled invalid date format")
            print(f"   Error: {data.get('error', 'No error message')}")
        else:
            print(f"❌ Expected 400 error, got {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def print_api_documentation():
    """Print API documentation"""
    print("\n" + "=" * 50)
    print("MONTHLY SUMMARY API DOCUMENTATION")
    print("=" * 50)
    print("""
Endpoint: GET /api/monthly-summary/

Description:
This API provides monthly summarized environmental data with statistical aggregations,
similar to pandas df.describe() but grouped by month.

Query Parameters:
- year (optional): Filter by specific year (e.g., 2023)
- month (optional): Filter by specific month (1-12)
- start_date (optional): Start date in YYYY-MM-DD format (e.g., 2023-01-01)
- end_date (optional): End date in YYYY-MM-DD format (e.g., 2023-12-31)

Default Behavior:
- If no filters are provided, the API returns data for the latest year available

Response Format:
{
    "success": true,
    "data": [
        {
            "year": 2023,
            "month": 6,
            "month_name": "June",
            "record_count": 1440,
            "air_temperature_max": 25.5,
            "air_temperature_min": 10.2,
            "air_temperature_mean": 18.3,
            "air_temperature_std": 4.2,
            "relative_humidity_max": 95.0,
            "relative_humidity_min": 45.0,
            "relative_humidity_mean": 75.2,
            "relative_humidity_std": 12.1,
            "shortwave_radiation_max": 850.0,
            "shortwave_radiation_min": 0.0,
            "shortwave_radiation_mean": 425.3,
            "shortwave_radiation_std": 250.1,
            "rainfall_total": 125.5,
            "rainfall_max": 15.2,
            "rainfall_mean": 2.8,
            "rainfall_std": 3.1,
            "soil_temp_5cm_max": 22.1,
            "soil_temp_5cm_min": 8.5,
            "soil_temp_5cm_mean": 15.3,
            "soil_temp_5cm_std": 3.8,
            "wind_speed_max": 12.5,
            "wind_speed_min": 0.1,
            "wind_speed_mean": 3.2,
            "wind_speed_std": 2.1,
            "snow_depth_max": 0.0,
            "snow_depth_min": 0.0,
            "snow_depth_mean": 0.0,
            "snow_depth_std": 0.0,
            "atmospheric_pressure_max": 102.5,
            "atmospheric_pressure_min": 98.2,
            "atmospheric_pressure_mean": 100.8,
            "atmospheric_pressure_std": 1.2
        }
    ],
    "total_months": 1,
    "filters_applied": {
        "year": "2023",
        "month": "6",
        "start_date": null,
        "end_date": null
    },
    "default_behavior": null
}

Example Usage:
1. Get latest year data (default):
   GET /api/monthly-summary/

2. Get summaries for specific year:
   GET /api/monthly-summary/?year=2023

3. Get summaries for specific month across all years:
   GET /api/monthly-summary/?month=6

4. Get summary for specific year and month:
   GET /api/monthly-summary/?year=2023&month=6

5. Get data within date range:
   GET /api/monthly-summary/?start_date=2023-01-01&end_date=2023-06-30

6. Get data from specific start date:
   GET /api/monthly-summary/?start_date=2023-01-01

7. Get data until specific end date:
   GET /api/monthly-summary/?end_date=2023-12-31
""")

if __name__ == "__main__":
    print_api_documentation()
    test_monthly_summary_api() 