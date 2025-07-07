from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdmin

class AdminDocsView(APIView):
    """
    Serve API documentation for admin users only.
    Simple and reliable approach.
    """
    permission_classes = [IsAdmin]
    authentication_classes = [SessionAuthentication]

    def get(self, request, path=''):
        # Serve different documentation based on path
        if path == '' or path == 'index.html':
            return self._serve_main_docs()
        elif path == 'separated-chart-apis':
            return self._serve_separated_chart_docs()
        elif path == 'monthly-summary':
            return self._serve_monthly_summary_docs()
        else:
            return Response({
                'error': 'Documentation not found',
                'available_docs': [
                    'index.html - Main documentation',
                    'separated-chart-apis - Separated Chart APIs',
                    'monthly-summary - Monthly Summary API'
                ]
            }, status=status.HTTP_404_NOT_FOUND)

    def _serve_main_docs(self):
        """Serve main API documentation"""
        docs_content = {
            'title': 'Dashboard API Documentation',
            'description': 'Environmental data API documentation for admin users',
            'endpoints': {
                'authentication': {
                    'login': 'POST /api/token',
                    'refresh': 'POST /api/token/refresh',
                    'register': 'POST /api/register',
                    'verify_email': 'POST /api/verify'
                },
                'environmental_data': {
                    'list': 'GET /api/environmental-data/',
                    'sample': 'GET /api/sample/environmental-data/',
                    'monthly_summary': 'GET /api/monthly-summary/'
                },
                'raw_data_apis': {
                    'snow_depth': 'GET /api/raw/snow-depth/',
                    'rainfall': 'GET /api/raw/rainfall/',
                    'soil_temperature': 'GET /api/raw/soil-temperature/',
                    'multi_metric': 'GET /api/raw/multi-metric/'
                },
                'chart_apis': {
                    'snow_depth': 'GET /api/charts/snow-depth/',
                    'rainfall': 'GET /api/charts/rainfall/',
                    'soil_temperature': 'GET /api/charts/soil-temperature/'
                },
                'admin': {
                    'dashboard': 'GET /api/admin-dashboard/',
                    'user_info': 'GET /api/userinfo/',
                    'docs': 'GET /api/docs/'
                }
            },
            'authentication': {
                'jwt': 'Use JWT tokens for API access',
                'session': 'Use Django session for admin access'
            },
            'permissions': {
                'public': 'Some endpoints are public',
                'authenticated': 'Some endpoints require authentication',
                'admin': 'Some endpoints require admin group membership'
            }
        }
        return Response(docs_content)

    def _serve_separated_chart_docs(self):
        """Serve separated chart APIs documentation"""
        docs_content = {
            'title': 'Separated Chart APIs Documentation',
            'description': 'Documentation for raw data and averaged chart APIs',
            'raw_data_apis': {
                'description': 'For detailed analysis with performance limits',
                'base_path': '/api/raw/',
                'endpoints': {
                    'snow_depth': {
                        'url': 'GET /api/raw/snow-depth/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'limit'],
                        'limit': 'default: 1000, max: 10,000'
                    },
                    'rainfall': {
                        'url': 'GET /api/raw/rainfall/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'limit']
                    },
                    'soil_temperature': {
                        'url': 'GET /api/raw/soil-temperature/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'depth', 'limit'],
                        'depth_options': ['5cm', '10cm', '20cm', '25cm', '50cm']
                    },
                    'multi_metric': {
                        'url': 'GET /api/raw/multi-metric/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'metrics', 'limit'],
                        'metrics': ['air_temp', 'humidity', 'wind_speed', 'snow_depth', 'rainfall', 'soil_temp_5cm', 'atmospheric_pressure', 'solar_radiation']
                    }
                }
            },
            'averaged_chart_apis': {
                'description': 'For visualizations and dashboards',
                'base_path': '/api/charts/',
                'endpoints': {
                    'snow_depth': {
                        'url': 'GET /api/charts/snow-depth/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'group_by'],
                        'group_by_options': ['hour', 'day', 'week', 'month']
                    },
                    'rainfall': {
                        'url': 'GET /api/charts/rainfall/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'group_by']
                    },
                    'soil_temperature': {
                        'url': 'GET /api/charts/soil-temperature/',
                        'params': ['year', 'month', 'start_date', 'end_date', 'depth', 'group_by']
                    }
                }
            },
            'key_differences': {
                'raw_apis': 'Individual data points, include limits, for detailed analysis',
                'chart_apis': 'Aggregated values, no limits, optimized for visualizations'
            }
        }
        return Response(docs_content)

    def _serve_monthly_summary_docs(self):
        """Serve monthly summary API documentation"""
        docs_content = {
            'title': 'Monthly Summary API Documentation',
            'description': 'Statistical summary of environmental data grouped by month',
            'endpoint': 'GET /api/monthly-summary/',
            'parameters': {
                'year': 'Filter by specific year (optional)',
                'month': 'Filter by specific month (optional)',
                'start_date': 'Start date in YYYY-MM-DD format (optional)',
                'end_date': 'End date in YYYY-MM-DD format (optional)'
            },
            'response_format': {
                'success': 'Boolean indicating success',
                'data': 'Array of monthly summary objects',
                'metadata': 'Information about the request and data'
            },
            'example_response': {
                'success': True,
                'data': [
                    {
                        'year': 2023,
                        'month': 1,
                        'avg_air_temp': 12.5,
                        'max_air_temp': 25.0,
                        'min_air_temp': -5.0,
                        'avg_snow_depth': 15.2,
                        'total_rainfall': 45.6
                    }
                ],
                'total_months': 12,
                'filters_applied': {
                    'year': '2023'
                }
            }
        }
        return Response(docs_content) 