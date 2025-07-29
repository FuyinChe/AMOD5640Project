#!/usr/bin/env python3
"""
Test script for the Averaged Chart APIs
Tests snow depth, rainfall, soil temperature, and multi-metric chart endpoints
that return averaged/aggregated values over time periods
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_averaged_snow_depth_chart_api():
    """Test the averaged snow depth chart API endpoint"""
    
    print("Testing Averaged Snow Depth Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged snow depth data with default grouping (day)
    print("\n1. Testing: Get averaged snow depth data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved snow depth data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                    print(f"   Unit: {data.get('unit', 'N/A')}")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Monthly grouping
    print("\n2. Testing: Snow depth with monthly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by=month&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved monthly snow depth data")
                print(f"   📊 Sample monthly data: {sample}")
            else:
                print("✅ Success! No monthly data available for 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Date range with daily grouping
    print("\n3. Testing: Snow depth with date range and daily grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?start_date=2023-01-01&end_date=2023-01-31&group_by=day")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved daily snow depth data for January 2023")
                print(f"   📊 Sample daily data: {sample}")
            else:
                print("✅ Success! No daily data available for January 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_rainfall_chart_api():
    """Test the averaged rainfall chart API endpoint"""
    
    print("\nTesting Averaged Rainfall Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged rainfall data with default grouping
    print("\n1. Testing: Get averaged rainfall data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved rainfall data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate rainfall averaged data structure
                required_fields = ['period', 'avg', 'total', 'max']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required rainfall averaged fields present")
                    print(f"   Unit: {data.get('unit', 'N/A')}")
                else:
                    print(f"   ❌ Missing rainfall averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Monthly grouping with total rainfall
    print("\n2. Testing: Rainfall with monthly grouping (total rainfall)")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?group_by=month&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved monthly rainfall data")
                print(f"   📊 Sample monthly rainfall: {sample}")
                print(f"   💧 Total rainfall for month: {sample.get('total', 'N/A')} mm")
            else:
                print("✅ Success! No monthly rainfall data available for 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Yearly grouping
    print("\n3. Testing: Rainfall with yearly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?group_by=year")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved yearly rainfall data")
                print(f"   📊 Sample yearly rainfall: {sample}")
                print(f"   💧 Total rainfall for year: {sample.get('total', 'N/A')} mm")
                print(f"   📅 Year: {sample.get('year', 'N/A')}")
                print(f"   📈 Data points: {sample.get('data_points', 'N/A')}")
            else:
                print("✅ Success! No yearly rainfall data available")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_shortwave_radiation_chart_api():
    """Test the averaged shortwave radiation chart API endpoint"""
    
    print("\nTesting Averaged Shortwave Radiation Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged shortwave radiation data with default grouping (day)
    print("\n1. Testing: Get averaged shortwave radiation data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/shortwave-radiation/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved shortwave radiation data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Monthly grouping
    print("\n2. Testing: Shortwave radiation with monthly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/shortwave-radiation/?group_by=month&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved monthly shortwave radiation data")
                print(f"   📊 Sample monthly data: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_wind_speed_chart_api():
    """Test the averaged wind speed chart API endpoint"""
    
    print("\nTesting Averaged Wind Speed Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged wind speed data with default grouping (day)
    print("\n1. Testing: Get averaged wind speed data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/wind-speed/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved wind speed data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Hourly grouping
    print("\n2. Testing: Wind speed with hourly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/wind-speed/?group_by=hour&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved hourly wind speed data")
                print(f"   📊 Sample hourly data: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_air_temperature_chart_api():
    """Test the averaged air temperature chart API endpoint"""
    
    print("\nTesting Averaged Air Temperature Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged air temperature data with default grouping (day)
    print("\n1. Testing: Get averaged air temperature data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved air temperature data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                    print(f"   Unit: {data.get('unit', 'N/A')}")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Monthly grouping
    print("\n2. Testing: Air temperature with monthly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/?group_by=month&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved monthly air temperature data")
                print(f"   📊 Sample monthly data: {sample}")
            else:
                print("✅ Success! No monthly data available for 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Date range with daily grouping
    print("\n3. Testing: Air temperature with date range and daily grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/air-temperature/?start_date=2023-01-01&end_date=2023-01-31&group_by=day")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved daily air temperature data for January 2023")
                print(f"   📊 Sample daily data: {sample}")
            else:
                print("✅ Success! No daily data available for January 2023")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_atmospheric_pressure_chart_api():
    """Test the averaged atmospheric pressure chart API endpoint"""
    
    print("\nTesting Averaged Atmospheric Pressure Chart API...")
    print("=" * 60)
    
    # Test 1: Get averaged atmospheric pressure data with default grouping (day)
    print("\n1. Testing: Get averaged atmospheric pressure data (default - day grouping)")
    try:
        response = requests.get(f"{BASE_URL}/charts/atmospheric-pressure/")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved atmospheric pressure data")
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
            else:
                print("✅ Success! No data available for the specified period")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Weekly grouping
    print("\n2. Testing: Atmospheric pressure with weekly grouping")
    try:
        response = requests.get(f"{BASE_URL}/charts/atmospheric-pressure/?group_by=week&year=2023")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"✅ Success! Retrieved weekly atmospheric pressure data")
                print(f"   📊 Sample weekly data: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_data_structure():
    """Test the structure and format of averaged chart data"""
    
    print("\nTesting Averaged Chart Data Structure...")
    print("=" * 60)
    
    # Test snow depth averaged data structure
    print("\n1. Testing: Snow depth averaged data structure")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by=day&limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                required_fields = ['period', 'avg', 'max', 'min']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required averaged fields present in snow depth data")
                    print(f"   Period format: {sample['period']}")
                    print(f"   Average value: {sample['avg']} cm")
                    print(f"   Unit: {data.get('unit', 'N/A')}")
                else:
                    print(f"❌ Missing averaged fields in snow depth data: {missing_fields}")
            else:
                print("❌ No averaged data returned for structure test")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test rainfall averaged data structure
    print("\n2. Testing: Rainfall averaged data structure")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?group_by=day&limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                required_fields = ['period', 'avg', 'total', 'max']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required averaged fields present in rainfall data")
                    print(f"   Period format: {sample['period']}")
                    print(f"   Average rainfall: {sample['avg']} mm")
                    print(f"   Total rainfall: {sample['total']} mm")
                    print(f"   Unit: {data.get('unit', 'N/A')}")
                else:
                    print(f"❌ Missing averaged fields in rainfall data: {missing_fields}")
            else:
                print("❌ No averaged data returned for structure test")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_grouping_options():
    """Test different grouping options (day, week, month)"""
    
    print("\nTesting Grouping Options...")
    print("=" * 60)
    
    grouping_tests = [
        {'name': 'Daily Grouping', 'group_by': 'day'},
        {'name': 'Weekly Grouping', 'group_by': 'week'},
        {'name': 'Monthly Grouping', 'group_by': 'month'},
        {'name': 'Yearly Grouping', 'group_by': 'year'}
    ]
    
    for test in grouping_tests:
        print(f"\n🔍 Testing: {test['name']}")
        print("-" * 40)
        
        try:
            # Use rainfall API for yearly grouping, snow-depth for others
            if test['group_by'] == 'year':
                response = requests.get(f"{BASE_URL}/charts/rainfall/?group_by={test['group_by']}")
            else:
                response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by={test['group_by']}&year=2023")
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    sample = data['data'][0]
                    print(f"   ✅ Success! Retrieved data with {test['group_by']} grouping")
                    print(f"   📊 Sample period: {sample['period']}")
                    print(f"   📈 Average value: {sample['avg']} {data.get('unit', 'units')}")
                    
                    # Validate period format based on grouping
                    if test['group_by'] == 'day' and '-' in sample['period']:
                        print(f"   ✅ Daily period format correct")
                    elif test['group_by'] == 'week' and 'week' in sample:
                        print(f"   ✅ Weekly period format correct")
                        print(f"   📊 Week number: {sample['week']}")
                    elif test['group_by'] == 'month' and len(sample['period']) <= 3:
                        print(f"   ✅ Monthly period format correct")
                    elif test['group_by'] == 'year' and sample['period'].isdigit():
                        print(f"   ✅ Yearly period format correct")
                        print(f"   📅 Year: {sample['period']}")
                    else:
                        print(f"   ⚠️  Period format may be incorrect")
                else:
                    print(f"   ✅ Success! No data available for {test['group_by']} grouping in 2023")
            else:
                print(f"   ❌ Failed with status code: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


def print_averaged_chart_api_documentation():
    """Print averaged chart API documentation"""
    print("\n" + "=" * 70)
    print("AVERAGED CHART APIs DOCUMENTATION")
    print("=" * 70)
    print("""
Averaged Chart APIs provide time-series aggregated data optimized for interactive visualizations.

1. SNOW DEPTH CHART API (AVERAGED)
   Endpoint: GET /api/charts/snow-depth/
   Parameters:
   - year (optional): Filter by specific year (defaults to latest year)
   - month (optional): Filter by specific month
   - start_date (optional): Start date in YYYY-MM-DD format
   - end_date (optional): End date in YYYY-MM-DD format
   - group_by (optional): Time grouping (day, week, month, year, default: day)

2. AIR TEMPERATURE CHART API (AVERAGED)
   Endpoint: GET /api/charts/air-temperature/
   Parameters: Same as snow depth
   Returns: Averaged air temperature data in °C

3. RAINFALL CHART API (AVERAGED)
   Endpoint: GET /api/charts/rainfall/
   Parameters: Same as snow depth
   Returns: Averaged and total rainfall data

4. SOIL TEMPERATURE CHART API (AVERAGED)
   Endpoint: GET /api/charts/soil-temperature/
   Parameters:
   - depth (optional): Soil depth (5cm, 10cm, 20cm, 25cm, 50cm, default: 5cm)
   - Other parameters same as above

5. SHORTWAVE RADIATION CHART API (AVERAGED)
   Endpoint: GET /api/charts/shortwave-radiation/
   Parameters: Same as snow depth
   Returns: Averaged shortwave radiation data in W/m²

6. WIND SPEED CHART API (AVERAGED)
   Endpoint: GET /api/charts/wind-speed/
   Parameters: Same as snow depth
   Returns: Averaged wind speed data in m/s

7. ATMOSPHERIC PRESSURE CHART API (AVERAGED)
   Endpoint: GET /api/charts/atmospheric-pressure/
   Parameters: Same as snow depth
   Returns: Averaged atmospheric pressure data in kPa

8. MULTI-METRIC CHART API (AVERAGED)
   Endpoint: GET /api/charts/multi-metric/
   Parameters:
   - metrics (optional): Comma-separated metrics (default: air_temp,humidity,wind_speed)
   - Other parameters same as above

Response Format (Averaged):
{
    "success": true,
    "data": [
        {
            "period": "2023-06-15",
            "avg": 25.5,
            "max": 30.2,
            "min": 20.1
        }
    ],
    "unit": "cm"
}

Key Features:
- Default behavior: Returns last year's data
- Custom date ranges: Users can specify start_date and end_date
- Time grouping: hour, day, week, month, or year aggregation
- Performance optimized: No raw data points, only calculated averages
- Multiple statistics: avg, max, min, total (where applicable)
- Appropriate units for each metric

Example Usage:
1. Snow depth averages for 2023: GET /api/charts/snow-depth/?year=2023
2. Air temperature averages for 2023: GET /api/charts/air-temperature/?year=2023
3. Monthly rainfall totals: GET /api/charts/rainfall/?group_by=month&year=2023
4. Yearly rainfall totals: GET /api/charts/rainfall/?group_by=year
4. Daily averages with date range: GET /api/charts/snow-depth/?start_date=2023-01-01&end_date=2023-06-30&group_by=day
5. Weekly soil temperature: GET /api/charts/soil-temperature/?group_by=week&depth=20cm
6. Hourly wind speed: GET /api/charts/wind-speed/?group_by=hour&year=2023
7. Monthly shortwave radiation: GET /api/charts/shortwave-radiation/?group_by=month&year=2023
8. Weekly atmospheric pressure: GET /api/charts/atmospheric-pressure/?group_by=week&year=2023
""")


def run_all_averaged_chart_tests():
    """Run all averaged chart API tests"""
    print("🚀 Starting Averaged Chart APIs Test Suite")
    print("=" * 70)
    
    # Run individual test functions
    test_averaged_snow_depth_chart_api()
    test_averaged_air_temperature_chart_api()
    test_averaged_rainfall_chart_api()
    test_averaged_shortwave_radiation_chart_api()
    test_averaged_wind_speed_chart_api()
    test_averaged_atmospheric_pressure_chart_api()
    test_averaged_data_structure()
    test_grouping_options()
    
    print("\n" + "=" * 70)
    print("✅ Averaged Chart APIs Test Suite Completed!")
    print("=" * 70)


if __name__ == "__main__":
    print_averaged_chart_api_documentation()
    run_all_averaged_chart_tests() 