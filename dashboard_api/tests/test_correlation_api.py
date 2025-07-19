#!/usr/bin/env python3
"""
Test script for Correlation Analysis API
Tests the correlation analysis functionality with sample data
"""

import requests
import json
from datetime import datetime, timedelta

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

def test_correlation_api():
    """Test the correlation analysis API"""
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return False
    
    # Test parameters
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'metrics': ['humidity', 'temperature', 'wind_speed'],
        'correlation_method': 'pearson',
        'include_p_values': 'true',
        'sample_size': '5000'
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print("Testing Correlation Analysis API...")
    print(f"Parameters: {params}")
    print("-" * 50)
    
    try:
        # Make API request with authentication
        response = requests.get(f"{BASE_URL}/charts/statistical/correlation/", params=params, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ API call successful!")
                
                # Display results
                result_data = data['data']
                metadata = data['metadata']
                
                print(f"\n📊 Analysis Results:")
                print(f"   Metrics: {result_data['metric_names']}")
                print(f"   Total Records: {result_data['statistics']['total_records']}")
                print(f"   Valid Pairs: {result_data['statistics']['valid_pairs']}")
                print(f"   Strong Correlations: {result_data['statistics']['strong_correlations']}")
                print(f"   Moderate Correlations: {result_data['statistics']['moderate_correlations']}")
                print(f"   Weak Correlations: {result_data['statistics']['weak_correlations']}")
                
                print(f"\n🔗 Pairwise Correlations:")
                for pair in result_data['pairwise_correlations'][:5]:  # Show first 5
                    significance = "***" if pair['p_value'] < 0.001 else "**" if pair['p_value'] < 0.01 else "*" if pair['p_value'] < 0.05 else ""
                    print(f"   {pair['metric1']} vs {pair['metric2']}: {pair['correlation']:.4f} (p={pair['p_value']:.6f}) {significance}")
                
                print(f"\n📋 Metadata:")
                print(f"   Method: {metadata['correlation_method']}")
                print(f"   Date Range: {metadata['start_date']} to {metadata['end_date']}")
                print(f"   Sample Size: {metadata['sample_size']}")
                
                # Test correlation matrix format
                if result_data['correlation_matrix']:
                    print(f"\n📈 Correlation Matrix Shape: {len(result_data['correlation_matrix'])}x{len(result_data['correlation_matrix'][0])}")
                    
                return True
                
            else:
                print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                return False
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def test_default_2023_date_range():
    """Test the default 2023 date range functionality"""
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return False
    
    print("\n" + "="*60)
    print("Testing Default 2023 Date Range")
    print("="*60)
    
    # Test without providing any dates (should default to 2023)
    print("\n📅 Testing API call without date parameters...")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        # Make API request without date parameters
        response = requests.get(f"{BASE_URL}/charts/statistical/correlation/", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ Default date range API call successful!")
                
                metadata = data['metadata']
                print(f"   Default Start Date: {metadata['start_date']}")
                print(f"   Default End Date: {metadata['end_date']}")
                
                # Verify it defaults to 2023
                if metadata['start_date'] == '2023-01-01' and metadata['end_date'] == '2023-12-31':
                    print("   ✅ Correctly defaulted to 2023 date range")
                else:
                    print(f"   ❌ Expected 2023-01-01 to 2023-12-31, got {metadata['start_date']} to {metadata['end_date']}")
                
                return True
                
            else:
                print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
                return False
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def test_correlation_methods():
    """Test different correlation methods"""
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return False
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    methods = ['pearson', 'spearman', 'kendall']
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print("\n" + "="*60)
    print("Testing Different Correlation Methods")
    print("="*60)
    
    for method in methods:
        print(f"\n🔬 Testing {method.upper()} correlation...")
        
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'metrics': ['humidity', 'temperature'],
            'correlation_method': method,
            'include_p_values': 'true',
            'sample_size': '1000'
        }
        
        try:
            response = requests.get(f"{BASE_URL}/charts/statistical/correlation/", params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data['data']['pairwise_correlations']:
                    correlation = data['data']['pairwise_correlations'][0]['correlation']
                    p_value = data['data']['pairwise_correlations'][0]['p_value']
                    print(f"   ✅ {method}: r = {correlation:.4f}, p = {p_value:.6f}")
                else:
                    print(f"   ❌ {method}: No data returned")
            else:
                print(f"   ❌ {method}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {method}: Error - {str(e)}")


def test_parameter_validation():
    """Test parameter validation"""
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return False
    
    print("\n" + "="*60)
    print("Testing Parameter Validation")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test invalid date format
    print("\n📅 Testing invalid date format...")
    params = {
        'start_date': 'invalid-date',
        'end_date': '2023-12-31'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/charts/statistical/correlation/", params=params, headers=headers)
        if response.status_code == 400:
            print("   ✅ Correctly rejected invalid date format")
        else:
            print(f"   ❌ Should have rejected invalid date, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test invalid correlation method
    print("\n🔬 Testing invalid correlation method...")
    params = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'correlation_method': 'invalid_method'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/charts/statistical/correlation/", params=params)
        if response.status_code == 400:
            print("   ✅ Correctly rejected invalid correlation method")
        else:
            print(f"   ❌ Should have rejected invalid method, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Correlation Analysis API Tests")
    print("="*60)
    
    # Run tests
    success = test_correlation_api()
    test_default_2023_date_range()
    test_correlation_methods()
    test_parameter_validation()
    
    print("\n" + "="*60)
    if success:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    print("="*60) 