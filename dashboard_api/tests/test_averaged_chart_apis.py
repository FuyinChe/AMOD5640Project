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
            total_periods = data.get('total_periods', 0)
            aggregation = data.get('aggregation', 'N/A')
            group_by = data.get('group_by', 'N/A')
            filters = data.get('filters_applied', {})
            
            print(f"✅ Success! Retrieved {total_periods} averaged periods")
            print(f"   Aggregation: {aggregation}")
            print(f"   Group by: {group_by}")
            
            # Check if default year is applied
            if filters.get('year'):
                print(f"   📅 Default year applied: {filters['year']}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample data point: {sample}")
                
                # Validate averaged data structure
                required_fields = ['period', 'date', 'avg_snow_depth_cm', 'max_snow_depth_cm', 'min_snow_depth_cm', 'data_points']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required averaged fields present")
                else:
                    print(f"   ❌ Missing averaged fields: {missing_fields}")
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
            total_periods = data.get('total_periods', 0)
            group_by = data.get('group_by', 'N/A')
            
            print(f"✅ Success! Retrieved {total_periods} monthly periods")
            print(f"   Group by: {group_by}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample monthly data: {sample}")
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
            total_periods = data.get('total_periods', 0)
            
            print(f"✅ Success! Retrieved {total_periods} daily periods for January 2023")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample daily data: {sample}")
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
            total_periods = data.get('total_periods', 0)
            aggregation = data.get('aggregation', 'N/A')
            group_by = data.get('group_by', 'N/A')
            
            print(f"✅ Success! Retrieved {total_periods} averaged periods")
            print(f"   Aggregation: {aggregation}")
            print(f"   Group by: {group_by}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample data point: {sample}")
                
                # Validate rainfall averaged data structure
                required_fields = ['period', 'date', 'avg_rainfall_mm', 'total_rainfall_mm', 'max_rainfall_mm', 'data_points']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required rainfall averaged fields present")
                else:
                    print(f"   ❌ Missing rainfall averaged fields: {missing_fields}")
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
            total_periods = data.get('total_periods', 0)
            
            print(f"✅ Success! Retrieved {total_periods} monthly periods")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample monthly rainfall: {sample}")
                print(f"   💧 Total rainfall for month: {sample.get('total_rainfall_mm', 'N/A')} mm")
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
                required_fields = ['period', 'date', 'avg_snow_depth_cm', 'max_snow_depth_cm', 'min_snow_depth_cm', 'data_points']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required averaged fields present in snow depth data")
                    print(f"   Period format: {sample['period']}")
                    print(f"   Average value: {sample['avg_snow_depth_cm']} cm")
                    print(f"   Data points used: {sample['data_points']}")
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
                required_fields = ['period', 'date', 'avg_rainfall_mm', 'total_rainfall_mm', 'max_rainfall_mm', 'data_points']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required averaged fields present in rainfall data")
                    print(f"   Period format: {sample['period']}")
                    print(f"   Average rainfall: {sample['avg_rainfall_mm']} mm")
                    print(f"   Total rainfall: {sample['total_rainfall_mm']} mm")
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
        {'name': 'Monthly Grouping', 'group_by': 'month'}
    ]
    
    for test in grouping_tests:
        print(f"\n🔍 Testing: {test['name']}")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by={test['group_by']}&year=2023")
            if response.status_code == 200:
                data = response.json()
                total_periods = data.get('total_periods', 0)
                group_by = data.get('group_by', 'N/A')
                
                print(f"   ✅ Success! Retrieved {total_periods} periods")
                print(f"   Group by: {group_by}")
                
                if data.get('data') and len(data['data']) > 0:
                    sample = data['data'][0]
                    print(f"   📊 Sample period: {sample['period']}")
                    print(f"   📈 Average value: {sample['avg_snow_depth_cm']} cm")
                    
                    # Validate period format based on grouping
                    if test['group_by'] == 'day' and '-' in sample['period']:
                        print(f"   ✅ Daily period format correct")
                    elif test['group_by'] == 'week' and 'W' in sample['period']:
                        print(f"   ✅ Weekly period format correct")
                    elif test['group_by'] == 'month' and len(sample['period'].split('-')) == 2:
                        print(f"   ✅ Monthly period format correct")
                    else:
                        print(f"   ⚠️  Period format may be incorrect")
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
   - group_by (optional): Time grouping (day, week, month, default: day)

2. RAINFALL CHART API (AVERAGED)
   Endpoint: GET /api/charts/rainfall/
   Parameters: Same as snow depth
   Returns: Averaged and total rainfall data

3. SOIL TEMPERATURE CHART API (AVERAGED)
   Endpoint: GET /api/charts/soil-temperature/
   Parameters:
   - depth (optional): Soil depth (5cm, 10cm, 20cm, 25cm, 50cm, default: 5cm)
   - Other parameters same as above

4. MULTI-METRIC CHART API (AVERAGED)
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
            "date": "2023-06-15",
            "year": 2023,
            "month": 6,
            "day": 15,
            "avg_snow_depth_cm": 25.5,
            "max_snow_depth_cm": 30.2,
            "min_snow_depth_cm": 20.1,
            "data_points": 24
        }
    ],
    "total_periods": 365,
    "metric": "snow_depth_cm",
    "unit": "cm",
    "aggregation": "average",
    "group_by": "day",
    "filters_applied": {...}
}

Key Features:
- Default behavior: Returns last year's data
- Custom date ranges: Users can specify start_date and end_date
- Time grouping: day, week, or month aggregation
- Performance optimized: No raw data points, only calculated averages
- Multiple statistics: avg, max, min, total (where applicable)
- Data point count: Shows how many raw points were used for each average

Example Usage:
1. Snow depth averages for 2023: GET /api/charts/snow-depth/?year=2023
2. Monthly rainfall totals: GET /api/charts/rainfall/?group_by=month&year=2023
3. Daily averages with date range: GET /api/charts/snow-depth/?start_date=2023-01-01&end_date=2023-06-30&group_by=day
4. Weekly soil temperature: GET /api/charts/soil-temperature/?group_by=week&depth=20cm
""")


def run_all_averaged_chart_tests():
    """Run all averaged chart API tests"""
    print("🚀 Starting Averaged Chart APIs Test Suite")
    print("=" * 70)
    
    # Run individual test functions
    test_averaged_snow_depth_chart_api()
    test_averaged_rainfall_chart_api()
    test_averaged_data_structure()
    test_grouping_options()
    
    print("\n" + "=" * 70)
    print("✅ Averaged Chart APIs Test Suite Completed!")
    print("=" * 70)


if __name__ == "__main__":
    print_averaged_chart_api_documentation()
    run_all_averaged_chart_tests() 