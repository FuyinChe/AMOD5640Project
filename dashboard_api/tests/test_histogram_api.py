#!/usr/bin/env python3
"""
Test script for the Multi-Metric Histogram API
Tests the histogram functionality with default all metrics behavior
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

def test_histogram_api():
    """Test the histogram API with all metrics (default)"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Multi-Metric Histogram API")
    print("=" * 50)
    
    # Test parameters - just date range (defaults to all metrics)
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
        # No metrics specified - should use all
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
            params=params,
            timeout=60
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Histogram API test successful!")
            
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
                for metric_name, metric_data in metrics_data.items():
                    if 'bins' in metric_data and 'statistics' in metric_data:
                        stats = metric_data['statistics']
                        bins = metric_data['bins']
                        print(f"✅ {metric_name}: {len(bins)} bins, {stats.get('total_count', 'N/A')} data points")
                        print(f"   - Mean: {stats.get('mean', 'N/A')}")
                        print(f"   - Min: {stats.get('min', 'N/A')}")
                        print(f"   - Max: {stats.get('max', 'N/A')}")
                    else:
                        print(f"❌ {metric_name}: Missing bins or statistics")
            else:
                print("❌ Data field missing")
            
            # Check metadata
            if 'metadata' in data:
                metadata = data['metadata']
                print("✅ Metadata present")
                print(f"  - Bins: {metadata.get('bins', 'N/A')}")
                print(f"  - Metrics: {metadata.get('metrics', 'N/A')}")
                print(f"  - Date range: {metadata.get('start_date', 'N/A')} to {metadata.get('end_date', 'N/A')}")
            else:
                print("❌ Metadata missing")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

def test_specific_metrics():
    """Test with specific metrics"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Specific Metrics")
    print("=" * 50)
    
    # Test with specific metrics
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'metrics': ['temperature', 'humidity'],
        'bins': 15
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
            params=params,
            timeout=60
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Specific metrics test successful!")
            
            # Check data structure
            if 'data' in data:
                metrics_data = data['data']
                print(f"Metrics returned: {list(metrics_data.keys())}")
                
                # Check each metric
                for metric_name, metric_data in metrics_data.items():
                    if 'bins' in metric_data and 'statistics' in metric_data:
                        stats = metric_data['statistics']
                        bins = metric_data['bins']
                        print(f"✅ {metric_name}: {len(bins)} bins, {stats.get('total_count', 'N/A')} data points")
                        
                        # Show first few bins
                        if bins:
                            print(f"   - First bin: {bins[0]['bin_start']} to {bins[0]['bin_end']} ({bins[0]['count']} points, {bins[0]['percentage']}%)")
                            print(f"   - Last bin: {bins[-1]['bin_start']} to {bins[-1]['bin_end']} ({bins[-1]['count']} points, {bins[-1]['percentage']}%)")
                    else:
                        print(f"❌ {metric_name}: Missing bins or statistics")
            else:
                print("❌ Data field missing")
                
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_custom_bins():
    """Test with custom number of bins"""
    
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 50)
    print("Testing Custom Bins")
    print("=" * 50)
    
    # Test with custom bins
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'metrics': ['temperature'],
        'bins': 10
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
            params=params,
            timeout=30
        )
        
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Custom bins test successful!")
            
            # Check data structure
            if 'data' in data and 'temperature' in data['data']:
                temp_data = data['data']['temperature']
                if 'bins' in temp_data:
                    bins = temp_data['bins']
                    print(f"✅ Temperature: {len(bins)} bins (requested: 10)")
                    
                    # Show all bins
                    print("   Bins:")
                    for i, bin_data in enumerate(bins):
                        print(f"     {i+1:2d}. {bin_data['bin_start']:6.1f} to {bin_data['bin_end']:6.1f}: {bin_data['count']:4d} points ({bin_data['percentage']:5.1f}%)")
                else:
                    print("❌ Missing bins data")
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
        'depth': '10cm',
        'bins': 12
    }
    
    start_time = time.time()
    
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
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
                if 'bins' in soil_data and 'statistics' in soil_data:
                    stats = soil_data['statistics']
                    bins = soil_data['bins']
                    print(f"✅ Soil temperature: {len(bins)} bins, {stats.get('total_count', 'N/A')} data points")
                    print(f"   - Mean: {stats.get('mean', 'N/A')}")
                    print(f"   - Min: {stats.get('min', 'N/A')}")
                    print(f"   - Max: {stats.get('max', 'N/A')}")
                else:
                    print("❌ Missing bins or statistics")
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
            f"{base_url}/api/charts/statistical/histogram/",
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
    
    # Test invalid bins
    print("\n2. Testing invalid bins...")
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
            params={
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'bins': 'invalid'
            },
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly rejected invalid bins")
        else:
            print("❌ Should have rejected invalid bins")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test bins out of range
    print("\n3. Testing bins out of range...")
    try:
        response = requests.get(
            f"{base_url}/api/charts/statistical/histogram/",
            params={
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'bins': '150'
            },
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly rejected bins out of range")
        else:
            print("❌ Should have rejected bins out of range")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Run all tests"""
    print("Multi-Metric Histogram API Tests")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test all metrics (default)
    test_histogram_api()
    
    # Test specific metrics
    test_specific_metrics()
    
    # Test custom bins
    test_custom_bins()
    
    # Test soil temperature
    test_soil_temperature()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print(f"Test finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 