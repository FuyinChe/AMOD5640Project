#!/usr/bin/env python3
"""
Test script for the Chart APIs
Tests snow depth, rainfall, soil temperature, and multi-metric chart endpoints
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_snow_depth_chart_api():
    """Test the snow depth chart API endpoint"""
    
    print("Testing Snow Depth Chart API...")
    print("=" * 50)
    
    # Test 1: Get snow depth data with default parameters (should default to last year)
    print("\n1. Testing: Get snow depth data (default - last year)")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            filters = data.get('filters_applied', {})
            print(f"✅ Success! Retrieved {total_points} snow depth data points")
            print(f"   Metric: {data.get('metric', 'N/A')}")
            print(f"   Unit: {data.get('unit', 'N/A')}")
            
            # Check if default year is applied
            if filters.get('year'):
                print(f"   📅 Default year applied: {filters['year']}")
            else:
                print(f"   ⚠️  No default year in filters")
                
            # Validate data is from the expected year
            if data.get('data') and len(data['data']) > 0:
                sample_year = data['data'][0]['year']
                print(f"   📊 Data year: {sample_year}")
                
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Filter by year
    print("\n2. Testing: Snow depth filtered by year 2023")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?year=2023&limit=100")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} snow depth points for 2023")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Date range filter
    print("\n3. Testing: Snow depth with date range")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?start_date=2023-01-01&end_date=2023-03-31&limit=50")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} snow depth points in date range")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_rainfall_chart_api():
    """Test the rainfall chart API endpoint"""
    
    print("\nTesting Rainfall Chart API...")
    print("=" * 50)
    
    # Test 1: Get rainfall data with default parameters (should default to last year)
    print("\n1. Testing: Get rainfall data (default - last year)")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            filters = data.get('filters_applied', {})
            print(f"✅ Success! Retrieved {total_points} rainfall data points")
            print(f"   Metric: {data.get('metric', 'N/A')}")
            print(f"   Unit: {data.get('unit', 'N/A')}")
            
            # Check if default year is applied
            if filters.get('year'):
                print(f"   📅 Default year applied: {filters['year']}")
            else:
                print(f"   ⚠️  No default year in filters")
                
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Filter by month
    print("\n2. Testing: Rainfall filtered by month 6 (June)")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?month=6&limit=100")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} rainfall points for June")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Limited data points
    print("\n3. Testing: Rainfall with limited data points")
    try:
        response = requests.get(f"{BASE_URL}/charts/rainfall/?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} rainfall points (limited)")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_soil_temperature_chart_api():
    """Test the soil temperature chart API endpoint"""
    
    print("\nTesting Soil Temperature Chart API...")
    print("=" * 50)
    
    # Test 1: Get soil temperature data with default depth (5cm) and default year
    print("\n1. Testing: Get soil temperature data (default 5cm, last year)")
    try:
        response = requests.get(f"{BASE_URL}/charts/soil-temperature/")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            filters = data.get('filters_applied', {})
            print(f"✅ Success! Retrieved {total_points} soil temperature data points")
            print(f"   Metric: {data.get('metric', 'N/A')}")
            print(f"   Unit: {data.get('unit', 'N/A')}")
            print(f"   Depth: {data.get('depth', 'N/A')}")
            
            # Check if default year is applied
            if filters.get('year'):
                print(f"   📅 Default year applied: {filters['year']}")
            else:
                print(f"   ⚠️  No default year in filters")
                
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Different depth (20cm)
    print("\n2. Testing: Soil temperature at 20cm depth")
    try:
        response = requests.get(f"{BASE_URL}/charts/soil-temperature/?depth=20cm&limit=100")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} soil temperature points at 20cm")
            print(f"   Depth: {data.get('depth', 'N/A')}")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Invalid depth parameter
    print("\n3. Testing: Soil temperature with invalid depth")
    try:
        response = requests.get(f"{BASE_URL}/charts/soil-temperature/?depth=invalid")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved data with invalid depth (should default to 5cm)")
            print(f"   Depth: {data.get('depth', 'N/A')}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_multi_metric_chart_api():
    """Test the multi-metric chart API endpoint"""
    
    print("\nTesting Multi-Metric Chart API...")
    print("=" * 50)
    
    # Test 1: Get multi-metric data with default parameters (should default to last year)
    print("\n1. Testing: Get multi-metric data (default - last year)")
    try:
        response = requests.get(f"{BASE_URL}/charts/multi-metric/")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            filters = data.get('filters_applied', {})
            print(f"✅ Success! Retrieved {total_points} multi-metric data points")
            print(f"   Metrics: {data.get('metrics', 'N/A')}")
            
            # Check if default year is applied
            if filters.get('year'):
                print(f"   📅 Default year applied: {filters['year']}")
            else:
                print(f"   ⚠️  No default year in filters")
                
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Custom metrics
    print("\n2. Testing: Multi-metric with custom metrics")
    try:
        response = requests.get(f"{BASE_URL}/charts/multi-metric/?metrics=snow_depth,rainfall,air_temp&limit=100")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} multi-metric points")
            print(f"   Metrics: {data.get('metrics', 'N/A')}")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Single metric
    print("\n3. Testing: Multi-metric with single metric")
    try:
        response = requests.get(f"{BASE_URL}/charts/multi-metric/?metrics=humidity&year=2023&limit=50")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Retrieved {data.get('total_points', 0)} humidity points")
            print(f"   Metrics: {data.get('metrics', 'N/A')}")
            if data.get('data'):
                print(f"   Sample data point: {data['data'][0]}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_date_range_chart_apis():
    """Test date range functionality across all chart APIs"""
    
    print("\nTesting Date Range Functionality (Main Requests)...")
    print("=" * 60)
    
    # Test scenarios for date ranges
    test_scenarios = [
        {
            'name': 'Winter Season (Dec-Feb)',
            'start_date': '2023-12-01',
            'end_date': '2023-02-28',
            'description': 'Cross-year winter period'
        },
        {
            'name': 'Summer Season (Jun-Aug)',
            'start_date': '2023-06-01',
            'end_date': '2023-08-31',
            'description': 'Summer months'
        },
        {
            'name': 'Spring Season (Mar-May)',
            'start_date': '2023-03-01',
            'end_date': '2023-05-31',
            'description': 'Spring months'
        },
        {
            'name': 'Full Year',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'description': 'Complete year data'
        },
        {
            'name': 'Short Period (1 week)',
            'start_date': '2023-06-01',
            'end_date': '2023-06-07',
            'description': 'One week of data'
        },
        {
            'name': 'Month Range',
            'start_date': '2023-07-01',
            'end_date': '2023-08-31',
            'description': 'Two consecutive months'
        }
    ]
    
    # Test each chart API with date ranges
    chart_apis = [
        {
            'name': 'Snow Depth',
            'endpoint': '/charts/snow-depth/',
            'expected_metric': 'snow_depth_cm'
        },
        {
            'name': 'Rainfall',
            'endpoint': '/charts/rainfall/',
            'expected_metric': 'rainfall'
        },
        {
            'name': 'Soil Temperature (5cm)',
            'endpoint': '/charts/soil-temperature/?depth=5cm',
            'expected_metric': 'soil_temperature'
        },
        {
            'name': 'Multi-Metric',
            'endpoint': '/charts/multi-metric/?metrics=air_temp,humidity,wind_speed',
            'expected_metric': 'multiple'
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📅 Testing Scenario: {scenario['name']}")
        print(f"   Period: {scenario['start_date']} to {scenario['end_date']}")
        print(f"   Description: {scenario['description']}")
        print("-" * 50)
        
        for api in chart_apis:
            print(f"\n   Testing {api['name']} API...")
            try:
                url = f"{BASE_URL}{api['endpoint']}"
                params = {
                    'start_date': scenario['start_date'],
                    'end_date': scenario['end_date'],
                    'limit': 500  # Reasonable limit for testing
                }
                
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    total_points = data.get('total_points', 0)
                    
                    print(f"   ✅ Success! Retrieved {total_points} data points")
                    
                    # Validate date range in response
                    if data.get('data') and len(data['data']) > 0:
                        first_date = data['data'][0]['date']
                        last_date = data['data'][-1]['date']
                        print(f"   📊 Date range in data: {first_date} to {last_date}")
                        
                        # Check if data is within requested range
                        if first_date >= scenario['start_date'] and last_date <= scenario['end_date']:
                            print(f"   ✅ Date range validation: PASSED")
                        else:
                            print(f"   ⚠️  Date range validation: Data outside requested range")
                    
                    # Check filters applied
                    filters = data.get('filters_applied', {})
                    if filters.get('start_date') == scenario['start_date'] and filters.get('end_date') == scenario['end_date']:
                        print(f"   ✅ Filters validation: PASSED")
                    else:
                        print(f"   ⚠️  Filters validation: Mismatch in applied filters")
                        
                else:
                    print(f"   ❌ Failed with status code: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
    
    # Test edge cases for date ranges
    print(f"\n🔍 Testing Date Range Edge Cases...")
    print("-" * 50)
    
    edge_cases = [
        {
            'name': 'Invalid Date Format',
            'start_date': '2023-13-01',  # Invalid month
            'end_date': '2023-12-31',
            'expected_status': 400
        },
        {
            'name': 'Start Date After End Date',
            'start_date': '2023-12-31',
            'end_date': '2023-01-01',
            'expected_status': 200  # Should return empty data
        },
        {
            'name': 'Same Start and End Date',
            'start_date': '2023-06-15',
            'end_date': '2023-06-15',
            'expected_status': 200
        },
        {
            'name': 'Future Date Range',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'expected_status': 200  # Should return empty data
        }
    ]
    
    for edge_case in edge_cases:
        print(f"\n   Testing Edge Case: {edge_case['name']}")
        try:
            url = f"{BASE_URL}/charts/snow-depth/"
            params = {
                'start_date': edge_case['start_date'],
                'end_date': edge_case['end_date'],
                'limit': 10
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == edge_case['expected_status']:
                print(f"   ✅ Expected status {edge_case['expected_status']}: PASSED")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   📊 Retrieved {data.get('total_points', 0)} data points")
            else:
                print(f"   ❌ Expected status {edge_case['expected_status']}, got {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


def test_default_last_year_behavior():
    """Test that all chart APIs default to the last year when no date parameters are provided"""
    
    print("\nTesting Default Last Year Behavior...")
    print("=" * 60)
    
    # Test all chart APIs without any date parameters
    chart_apis = [
        {
            'name': 'Snow Depth',
            'endpoint': '/charts/snow-depth/',
            'description': 'Snow depth data should default to last year'
        },
        {
            'name': 'Rainfall',
            'endpoint': '/charts/rainfall/',
            'description': 'Rainfall data should default to last year'
        },
        {
            'name': 'Soil Temperature',
            'endpoint': '/charts/soil-temperature/',
            'description': 'Soil temperature data should default to last year'
        },
        {
            'name': 'Multi-Metric',
            'endpoint': '/charts/multi-metric/',
            'description': 'Multi-metric data should default to last year'
        }
    ]
    
    for api in chart_apis:
        print(f"\n🔍 Testing: {api['name']} API")
        print(f"   Description: {api['description']}")
        print("-" * 50)
        
        try:
            # Make request without any date parameters
            response = requests.get(f"{BASE_URL}{api['endpoint']}")
            
            if response.status_code == 200:
                data = response.json()
                filters = data.get('filters_applied', {})
                total_points = data.get('total_points', 0)
                
                print(f"   ✅ Success! Retrieved {total_points} data points")
                
                # Check if year filter is applied
                if filters.get('year'):
                    print(f"   📅 Year filter applied: {filters['year']}")
                    
                    # Validate that data is from the specified year
                    if data.get('data') and len(data['data']) > 0:
                        data_years = set(point['year'] for point in data['data'])
                        if len(data_years) == 1 and list(data_years)[0] == int(filters['year']):
                            print(f"   ✅ Data validation: All points are from year {filters['year']}")
                        else:
                            print(f"   ⚠️  Data validation: Mixed years found {data_years}")
                else:
                    print(f"   ❌ No year filter applied - default behavior not working")
                
                # Check for other filters that shouldn't be applied by default
                unexpected_filters = ['month', 'start_date', 'end_date']
                applied_unexpected = [f for f in unexpected_filters if filters.get(f)]
                if applied_unexpected:
                    print(f"   ⚠️  Unexpected filters applied: {applied_unexpected}")
                else:
                    print(f"   ✅ No unexpected filters applied")
                    
            else:
                print(f"   ❌ Failed with status code: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Test that explicit date parameters override the default
    print(f"\n🔍 Testing: Explicit date parameters override default")
    print("-" * 50)
    
    try:
        # Test with explicit year parameter
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?year=2022")
        if response.status_code == 200:
            data = response.json()
            filters = data.get('filters_applied', {})
            
            if filters.get('year') == '2022':
                print(f"   ✅ Explicit year parameter works: {filters['year']}")
            else:
                print(f"   ❌ Explicit year parameter not applied correctly")
        else:
            print(f"   ❌ Failed with explicit year parameter")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def test_performance_limits():
    """Test performance limit enforcement and optimization"""
    
    print("\nTesting Performance Limits and Optimization...")
    print("=" * 60)
    
    # Test performance limit enforcement
    print("\n1. Testing: Performance limit enforcement")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?limit=50000")
        if response.status_code == 400:
            data = response.json()
            if 'max_limit' in data and data['max_limit'] == 10000:
                print("✅ Success! Properly enforced performance limit")
                print(f"   Max limit: {data['max_limit']:,}")
                print(f"   Suggestion: {data.get('suggestion', 'N/A')}")
            else:
                print("❌ Missing max_limit in error response")
        else:
            print(f"❌ Expected 400 for excessive limit, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test invalid limit parameter
    print("\n2. Testing: Invalid limit parameter")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?limit=invalid")
        if response.status_code == 400:
            data = response.json()
            if 'Invalid limit parameter' in data.get('error', ''):
                print("✅ Success! Properly handled invalid limit parameter")
            else:
                print("❌ Unexpected error message")
        else:
            print(f"❌ Expected 400 for invalid limit, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test reasonable limit works
    print("\n3. Testing: Reasonable limit works")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?limit=5000")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            print(f"✅ Success! Reasonable limit works: {total_points} points")
        else:
            print(f"❌ Failed with reasonable limit: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test default limit behavior
    print("\n4. Testing: Default limit behavior")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/")
        if response.status_code == 200:
            data = response.json()
            total_points = data.get('total_points', 0)
            filters = data.get('filters_applied', {})
            default_limit = filters.get('limit', 0)
            
            print(f"✅ Success! Default limit applied: {default_limit}")
            print(f"   Actual points returned: {total_points}")
            
            if total_points <= default_limit:
                print("   ✅ Data size within limit")
            else:
                print("   ⚠️  Data size exceeds limit")
        else:
            print(f"❌ Failed with default limit: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test performance across all chart APIs
    print("\n5. Testing: Performance limits across all chart APIs")
    chart_apis = [
        '/charts/snow-depth/',
        '/charts/rainfall/',
        '/charts/soil-temperature/',
        '/charts/multi-metric/'
    ]
    
    for endpoint in chart_apis:
        print(f"\n   Testing: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}?limit=15000")
            if response.status_code == 400:
                print(f"   ✅ Performance limit enforced")
            else:
                print(f"   ❌ Performance limit not enforced (status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


def test_chart_data_structure():
    """Test the structure and format of chart data"""
    
    print("\nTesting Chart Data Structure...")
    print("=" * 50)
    
    # Test snow depth data structure
    print("\n1. Testing: Snow depth data structure")
    try:
        response = requests.get(f"{BASE_URL}/charts/snow-depth/?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                required_fields = ['timestamp', 'date', 'time', 'snow_depth_cm', 'year', 'month', 'day']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required fields present in snow depth data")
                    print(f"   Timestamp format: {sample['timestamp']}")
                    print(f"   Data types: timestamp={type(sample['timestamp'])}, snow_depth_cm={type(sample['snow_depth_cm'])}")
                else:
                    print(f"❌ Missing fields in snow depth data: {missing_fields}")
            else:
                print("❌ No data returned for structure test")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test multi-metric data structure
    print("\n2. Testing: Multi-metric data structure")
    try:
        response = requests.get(f"{BASE_URL}/charts/multi-metric/?metrics=air_temp,humidity&limit=1")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                sample = data['data'][0]
                required_fields = ['timestamp', 'date', 'time', 'year', 'month', 'day']
                missing_fields = [field for field in required_fields if field not in sample]
                
                if not missing_fields:
                    print("✅ Success! All required fields present in multi-metric data")
                    print(f"   Available metrics: {list(sample.keys())}")
                    print(f"   Timestamp format: {sample['timestamp']}")
                else:
                    print(f"❌ Missing fields in multi-metric data: {missing_fields}")
            else:
                print("❌ No data returned for structure test")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def print_chart_api_documentation():
    """Print chart API documentation"""
    print("\n" + "=" * 60)
    print("CHART APIs DOCUMENTATION")
    print("=" * 60)
    print("""
Chart APIs provide time-series data optimized for interactive visualizations.

1. SNOW DEPTH CHART API
   Endpoint: GET /api/charts/snow-depth/
   Parameters:
   - year (optional): Filter by specific year
   - month (optional): Filter by specific month
   - start_date (optional): Start date in YYYY-MM-DD format
   - end_date (optional): End date in YYYY-MM-DD format
   - limit (optional): Maximum number of data points (default: 1000, max: 10,000)

2. RAINFALL CHART API
   Endpoint: GET /api/charts/rainfall/
   Parameters: Same as snow depth
   Returns: Rainfall and precipitation data

3. SOIL TEMPERATURE CHART API
   Endpoint: GET /api/charts/soil-temperature/
   Parameters:
   - depth (optional): Soil depth (5cm, 10cm, 20cm, 25cm, 50cm, default: 5cm)
   - Other parameters same as above (limit max: 10,000)

4. MULTI-METRIC CHART API
   Endpoint: GET /api/charts/multi-metric/
   Parameters:
   - metrics (optional): Comma-separated metrics (default: air_temp,humidity,wind_speed)
   - Available metrics: air_temp, humidity, wind_speed, snow_depth, rainfall, 
     soil_temp_5cm, soil_temp_10cm, soil_temp_20cm, atmospheric_pressure, solar_radiation
   - Other parameters same as above

Response Format:
{
    "success": true,
    "data": [
        {
            "timestamp": "2023-06-15 14:30:00",
            "date": "2023-06-15",
            "time": "14:30:00",
            "metric_value": 25.5,
            "year": 2023,
            "month": 6,
            "day": 15
        }
    ],
    "total_points": 1000,
    "metric": "metric_name",
    "unit": "unit_of_measurement",
    "filters_applied": {...}
}

Example Usage:
1. Snow depth for 2023: GET /api/charts/snow-depth/?year=2023&limit=500
2. Rainfall with date range: GET /api/charts/rainfall/?start_date=2023-01-01&end_date=2023-06-30
3. Soil temperature at 20cm: GET /api/charts/soil-temperature/?depth=20cm&year=2023
4. Multi-metric comparison: GET /api/charts/multi-metric/?metrics=air_temp,humidity,wind_speed&year=2023
""")


def run_all_chart_tests():
    """Run all chart API tests"""
    print("🚀 Starting Chart APIs Test Suite")
    print("=" * 60)
    
    # Run individual test functions
    test_snow_depth_chart_api()
    test_rainfall_chart_api()
    test_soil_temperature_chart_api()
    test_multi_metric_chart_api()
    test_default_last_year_behavior()  # Test default behavior
    test_date_range_chart_apis()  # Main date range testing
    test_performance_limits()  # Test performance optimization
    test_chart_data_structure()
    
    print("\n" + "=" * 60)
    print("✅ Chart APIs Test Suite Completed!")
    print("=" * 60)


if __name__ == "__main__":
    print_chart_api_documentation()
    run_all_chart_tests() 