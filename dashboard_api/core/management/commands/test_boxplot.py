from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
import json


class Command(BaseCommand):
    help = 'Test the Multi-Metric Boxplot API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='Start date (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2023-12-31',
            help='End date (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--metrics',
            nargs='+',
            default=['temperature', 'humidity'],
            help='List of metrics to test'
        )
        parser.add_argument(
            '--group-by',
            type=str,
            default='month',
            help='Grouping period (month, season, year, day)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Testing Multi-Metric Boxplot API...')
        )
        
        client = Client()
        
        # Test parameters
        params = {
            'start_date': options['start_date'],
            'end_date': options['end_date'],
            'metrics': options['metrics'],
            'group_by': options['group_by']
        }
        
        self.stdout.write(f"Parameters: {params}")
        self.stdout.write("-" * 50)
        
        try:
            # Make the request
            response = client.get(reverse('multi-metric-boxplot'), params)
            
            self.stdout.write(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.stdout.write(
                    self.style.SUCCESS('✅ API call successful!')
                )
                self.stdout.write(f"Success: {data.get('success')}")
                self.stdout.write(f"Metrics returned: {list(data.get('data', {}).keys())}")
                self.stdout.write(f"Metadata: {data.get('metadata')}")
                
                # Show sample data for first metric
                if data.get('data'):
                    first_metric = list(data['data'].keys())[0]
                    first_period = data['data'][first_metric][0] if data['data'][first_metric] else None
                    if first_period:
                        self.stdout.write(f"\nSample data for {first_metric}:")
                        self.stdout.write(f"  Period: {first_period['period']}")
                        self.stdout.write(f"  Statistics: {first_period['statistics']}")
                
            else:
                self.stdout.write(
                    self.style.ERROR('❌ API call failed!')
                )
                self.stdout.write(f"Error: {response.content.decode()}")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Unexpected Error: {str(e)}')
            )
        
        # Test validation
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Testing API Validation...")
        self.stdout.write("=" * 50)
        
        # Test cases for validation
        test_cases = [
            {
                'name': 'Missing start_date',
                'params': {'end_date': '2023-12-31', 'metrics': ['temperature']},
                'expected_status': 400
            },
            {
                'name': 'Missing end_date',
                'params': {'start_date': '2023-01-01', 'metrics': ['temperature']},
                'expected_status': 400
            },
            {
                'name': 'Missing metrics',
                'params': {'start_date': '2023-01-01', 'end_date': '2023-12-31'},
                'expected_status': 400
            },
            {
                'name': 'Invalid date format',
                'params': {'start_date': '2023/01/01', 'end_date': '2023-12-31', 'metrics': ['temperature']},
                'expected_status': 400
            },
            {
                'name': 'Invalid metric',
                'params': {'start_date': '2023-01-01', 'end_date': '2023-12-31', 'metrics': ['invalid_metric']},
                'expected_status': 400
            }
        ]
        
        for test_case in test_cases:
            self.stdout.write(f"\nTesting: {test_case['name']}")
            try:
                response = client.get(reverse('multi-metric-boxplot'), test_case['params'])
                
                if response.status_code == test_case['expected_status']:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Passed: Got expected status {response.status_code}")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Failed: Expected {test_case['expected_status']}, got {response.status_code}")
                    )
                    self.stdout.write(f"   Response: {response.content.decode()[:200]}...")
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error: {str(e)}")
                )
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS("Test completed!")
        )
        self.stdout.write("=" * 50) 