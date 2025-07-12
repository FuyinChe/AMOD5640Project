#!/usr/bin/env python3
"""
Test script for the simplified Multi-Metric Boxplot API
Tests the overall-only boxplot functionality with default all metrics behavior
"""

import os
import sys
import time
import requests
import json
from datetime import datetime

# Add Django project to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_api.settings')

import django
django.setup()

def test_overall_boxplot():
    """Test the simplified boxplot API with overall grouping"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Simplified Boxplot API (Overall Only)")
    print("=" * 50)
    
    # Test parameters - simplified API (no group_by needed)
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',  # Full year, processed as one dataset
        'metrics': ['temperature', 'humidity', 'wind_speed']
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params=params,
            timeout=60
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Overall boxplot test successful!")
            
            # Check response structure
            if 'success' in data and data['success']:
                print("✅ Success flag is true")
            else:
                print("❌ Success flag is false")
                return
            
            # Check data structure
            if 'data' in data:
                print("✅ Data field present")
                metrics_data = data['data']
                print(f"Metrics returned: {list(metrics_data.keys())}")
                
                # Check each metric
                for metric in params['metrics']:
                    if metric in metrics_data:
                        metric_data = metrics_data[metric]
                        if isinstance(metric_data, list) and len(metric_data) > 0:
                            period_data = metric_data[0]
                            if 'period' in period_data and 'statistics' in period_data:
                                stats = period_data['statistics']
                                print(f"✅ {metric}: {period_data['period']} - Count: {stats.get('count', 'N/A')}")
                            else:
                                print(f"❌ {metric}: Missing period or statistics")
                        else:
                            print(f"❌ {metric}: Invalid data structure")
                    else:
                        print(f"❌ {metric}: Not found in response")
            else:
                print("❌ Data field missing")
            
            # Check metadata
            if 'metadata' in data:
                metadata = data['metadata']
                print("✅ Metadata present")
                print(f"  - Group by: {metadata.get('group_by', 'N/A')}")
                print(f"  - Metrics: {metadata.get('metrics', 'N/A')}")
                print(f"  - Date range: {metadata.get('start_date', 'N/A')} to {metadata.get('end_date', 'N/A')}")
            else:
                print("❌ Metadata missing")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

def test_all_metrics():
    """Test with all metrics (default behavior)"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing All Metrics (Default)")
    print("=" * 50)
    
    # Test with no metrics specified (should use all)
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
        # No metrics specified - should use all
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params=params,
            timeout=60
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ All metrics test successful!")
            print(f"Metrics returned: {list(data.get('data', {}).keys())}")
            
            # Check if all expected metrics are present
            expected_metrics = ['humidity', 'temperature', 'wind_speed', 'rainfall', 'snow_depth', 'shortwave_radiation', 'atmospheric_pressure', 'soil_temperature']
            returned_metrics = list(data.get('data', {}).keys())
            
            print(f"Expected metrics: {expected_metrics}")
            print(f"Returned metrics: {returned_metrics}")
            
            missing_metrics = [m for m in expected_metrics if m not in returned_metrics]
            if missing_metrics:
                print(f"⚠️  Missing metrics: {missing_metrics}")
            else:
                print("✅ All expected metrics returned!")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_single_metric_overall():
    """Test single metric with overall grouping"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Single Metric")
    print("=" * 50)
    
    # Test single metric
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'metrics': ['temperature']
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params=params,
            timeout=30
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Single metric test successful!")
            
            # Check data structure
            if 'data' in data and 'temperature' in data['data']:
                temp_data = data['data']['temperature']
                if isinstance(temp_data, list) and len(temp_data) > 0:
                    period_data = temp_data[0]
                    stats = period_data.get('statistics', {})
                    print(f"✅ Temperature statistics:")
                    print(f"  - Period: {period_data.get('period', 'N/A')}")
                    print(f"  - Count: {stats.get('count', 'N/A')}")
                    print(f"  - Min: {stats.get('min', 'N/A')}")
                    print(f"  - Q1: {stats.get('q1', 'N/A')}")
                    print(f"  - Median: {stats.get('median', 'N/A')}")
                    print(f"  - Q3: {stats.get('q3', 'N/A')}")
                    print(f"  - Max: {stats.get('max', 'N/A')}")
                    print(f"  - Outliers: {len(stats.get('outliers', []))} points")
                else:
                    print("❌ Invalid temperature data structure")
            else:
                print("❌ Temperature data not found")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_soil_temperature():
    """Test soil temperature with depth parameter"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Soil Temperature with Depth")
    print("=" * 50)
    
    # Test soil temperature with custom depth
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'metrics': ['soil_temperature'],
        'depth': '10cm'
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params=params,
            timeout=30
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Soil temperature test successful!")
            
            # Check metadata for depth
            if 'metadata' in data:
                metadata = data['metadata']
                depth = metadata.get('depth')
                print(f"✅ Depth parameter: {depth}")
            
            # Check data structure
            if 'data' in data and 'soil_temperature' in data['data']:
                soil_data = data['data']['soil_temperature']
                if isinstance(soil_data, list) and len(soil_data) > 0:
                    period_data = soil_data[0]
                    stats = period_data.get('statistics', {})
                    print(f"✅ Soil temperature statistics:")
                    print(f"  - Period: {period_data.get('period', 'N/A')}")
                    print(f"  - Count: {stats.get('count', 'N/A')}")
                    print(f"  - Min: {stats.get('min', 'N/A')}")
                    print(f"  - Max: {stats.get('max', 'N/A')}")
                else:
                    print("❌ Invalid soil temperature data structure")
            else:
                print("❌ Soil temperature data not found")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_error_handling():
    """Test error handling for invalid parameters"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)
    
    # Test missing required parameters
    print("\n1. Testing missing start_date...")
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params={'end_date': '2023-12-31'},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly rejected missing start_date")
        else:
            print("❌ Should have rejected missing start_date")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test missing end_date
    print("\n2. Testing missing end_date...")
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params={'start_date': '2023-01-01'},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly rejected missing end_date")
        else:
            print("❌ Should have rejected missing end_date")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test invalid date format
    print("\n3. Testing invalid date format...")
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/boxplot/",
            params={
                'start_date': 'invalid-date',
                'end_date': '2023-12-31'
            },
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly rejected invalid date format")
        else:
            print("❌ Should have rejected invalid date format")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Run all tests"""
    print("Multi-Metric Boxplot API Tests")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test overall grouping
    test_overall_boxplot()
    
    # Test all metrics (default)
    test_all_metrics()
    
    # Test single metric
    test_single_metric_overall()
    
    # Test soil temperature
    test_soil_temperature()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print(f"Test finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 