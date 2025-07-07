#!/usr/bin/env python3
"""
Test script for the Separated Chart APIs
Tests both raw data APIs (with limits) and averaged chart APIs (hourly, daily, monthly)
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_raw_data_apis():
    """Test raw data APIs that return individual data points with limits"""
    
    print("Testing Raw Data APIs (with limits)...")
    print("=" * 60)
    
    # Test raw snow depth API
    print("\n1. Testing: Raw snow depth data API")
    try:
        response = requests.get(f"{BASE_URL}/raw/snow-depth/?limit=100")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            data_type = data.get('data_type', 'N/A')
            filters = data.get('filters_applied', {})
            
            print(f"✅ Success! Retrieved {total_points} raw data points")
            print(f"   Data type: {data_type}")
            print(f"   Limit applied: {filters.get('limit', 'N/A')}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample data point: {sample}")
                
                # Validate raw data structure
                required_fields = ['timestamp', 'date', 'time', 'snow_depth_cm', 'year', 'month', 'day']
                missing_fields = [field for field in required_fields if field not in sample]
                if not missing_fields:
                    print(f"   ✅ All required raw data fields present")
                else:
                    print(f"   ❌ Missing raw data fields: {missing_fields}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test raw rainfall API
    print("\n2. Testing: Raw rainfall data API")
    try:
        response = requests.get(f"{BASE_URL}/raw/rainfall/?limit=50")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            data_type = data.get('data_type', 'N/A')
            
            print(f"✅ Success! Retrieved {total_points} raw rainfall points")
            print(f"   Data type: {data_type}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample rainfall point: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test raw soil temperature API
    print("\n3. Testing: Raw soil temperature data API")
    try:
        response = requests.get(f"{BASE_URL}/raw/soil-temperature/?depth=20cm&limit=75")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            depth = data.get('depth', 'N/A')
            
            print(f"✅ Success! Retrieved {total_points} raw soil temperature points")
            print(f"   Depth: {depth}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample soil temp point: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test raw multi-metric API
    print("\n4. Testing: Raw multi-metric data API")
    try:
        response = requests.get(f"{BASE_URL}/raw/multi-metric/?metrics=air_temp,humidity&limit=25")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            metrics = data.get('metrics', [])
            
            print(f"✅ Success! Retrieved {total_points} raw multi-metric points")
            print(f"   Metrics: {metrics}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample multi-metric point: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_averaged_chart_apis():
    """Test averaged chart APIs that return aggregated values over time periods"""
    
    print("\nTesting Averaged Chart APIs (hourly, daily, monthly)...")
    print("=" * 60)
    
    # Test averaged snow depth API with different groupings
    print("\n1. Testing: Averaged snow depth chart API")
    
    grouping_tests = [
        {'name': 'Daily Grouping', 'group_by': 'day'},
        {'name': 'Weekly Grouping', 'group_by': 'week'},
        {'name': 'Monthly Grouping', 'group_by': 'month'}
    ]
    
    for test in grouping_tests:
        print(f"\n   Testing: {test['name']}")
        try:
            response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by={test['group_by']}&year=2023")
            if response.status_code == 200:
                data = response.json()
                total_periods = data.get('total_periods', 0)
                group_by = data.get('group_by', 'N/A')
                aggregation = data.get('aggregation', 'N/A')
                
                print(f"   ✅ Success! Retrieved {total_periods} {group_by} periods")
                print(f"   Aggregation: {aggregation}")
                
                if data.get('data') and len(data['data']) > 0:
                    sample = data['data'][0]
                    print(f"   📊 Sample period: {sample['period']}")
                    print(f"   📈 Average value: {sample['avg_snow_depth_cm']} cm")
            else:
                print(f"   ❌ Failed with status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test averaged rainfall API
    print("\n2. Testing: Averaged rainfall chart API")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?group_by=month&year=2023")
        if response.status_code == 200:
            data = response.json()
            total_periods = data.get('total_periods', 0)
            group_by = data.get('group_by', 'N/A')
            
            print(f"✅ Success! Retrieved {total_periods} {group_by} periods")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample monthly rainfall: {sample}")
                print(f"   💧 Total rainfall: {sample.get('total_rainfall_mm', 'N/A')} mm")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test averaged soil temperature API
    print("\n3. Testing: Averaged soil temperature chart API")
    try:
        response = requests.get(f"{BASE_URL}/charts/soil-temperature/?depth=10cm&group_by=day&year=2023")
        if response.status_code == 200:
            data = response.json()
            total_periods = data.get('total_periods', 0)
            depth = data.get('depth', 'N/A')
            group_by = data.get('group_by', 'N/A')
            
            print(f"✅ Success! Retrieved {total_periods} {group_by} periods")
            print(f"   Depth: {depth}")
            
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                print(f"   📊 Sample daily soil temp: {sample}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_performance_comparison():
    """Compare performance between raw data and averaged APIs"""
    
    print("\nTesting Performance Comparison...")
    print("=" * 60)
    
    # Test raw data API performance
    print("\n1. Testing: Raw data API performance (limited)")
    try:
        import time
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/raw/snow-depth/?limit=1000")
        raw_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            print(f"✅ Raw data API: {total_points} points in {raw_time:.2f} seconds")
        else:
            print(f"❌ Raw data API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Raw data API error: {str(e)}")
    
    # Test averaged API performance
    print("\n2. Testing: Averaged chart API performance")
    try:
        import time
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?group_by=day&year=2023")
        avg_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            total_periods = data.get('total_periods', 0)
            print(f"✅ Averaged API: {total_periods} periods in {avg_time:.2f} seconds")
        else:
            print(f"❌ Averaged API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Averaged API error: {str(e)}")


def test_api_documentation():
    """Print API documentation for the separated endpoints"""
    
    print("\n" + "=" * 70)
    print("SEPARATED CHART APIs DOCUMENTATION")
    print("=" * 70)
    print("""
The chart APIs have been separated into two categories:

1. RAW DATA APIs (for detailed analysis)
   Base path: /api/raw/
   
   Endpoints:
   - GET /api/raw/snow-depth/ - Raw snow depth data points
   - GET /api/raw/rainfall/ - Raw rainfall data points  
   - GET /api/raw/soil-temperature/ - Raw soil temperature data points
   - GET /api/raw/multi-metric/ - Raw multi-metric data points
   
   Parameters:
   - year, month, start_date, end_date (optional): Date filtering
   - limit (optional): Maximum data points (default: 1000, max: 10,000)
   - depth (soil temp only): 5cm, 10cm, 20cm, 25cm, 50cm
   - metrics (multi-metric only): Comma-separated metric names
   
   Response: Individual data points with timestamps

2. AVERAGED CHART APIs (for visualizations)
   Base path: /api/charts/
   
   Endpoints:
   - GET /api/charts/snow-depth/ - Averaged snow depth data
   - GET /api/charts/rainfall/ - Averaged rainfall data
   - GET /api/charts/soil-temperature/ - Averaged soil temperature data
   
   Parameters:
   - year, month, start_date, end_date (optional): Date filtering
   - group_by (optional): Time grouping (hour, day, week, month, default: day)
   - depth (soil temp only): 5cm, 10cm, 20cm, 25cm, 50cm
   
   Response: Aggregated values (avg, max, min, total) per time period

Key Differences:
- Raw APIs: Individual data points, include limits, for detailed analysis
- Chart APIs: Aggregated values, no limits, optimized for visualizations
- Default behavior: Both default to last year if no date parameters provided
- Performance: Chart APIs are much faster for large datasets

Example Usage:
1. Raw data for analysis: GET /api/raw/snow-depth/?limit=500&year=2023
2. Daily averages for charts: GET /api/charts/snow-depth/?group_by=day&year=2023
3. Monthly totals for dashboards: GET /api/charts/rainfall/?group_by=month&year=2023
""")


def run_all_separated_api_tests():
    """Run all separated API tests"""
    print("🚀 Starting Separated Chart APIs Test Suite")
    print("=" * 70)
    
    # Run individual test functions
    test_raw_data_apis()
    test_averaged_chart_apis()
    test_performance_comparison()
    
    print("\n" + "=" * 70)
    print("✅ Separated Chart APIs Test Suite Completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_api_documentation()
    run_all_separated_api_tests() 