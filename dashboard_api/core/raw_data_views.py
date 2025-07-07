"""
Raw data views module for detailed environmental data analysis
Returns individual data points with performance limits
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q, Max

# Swagger documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import EnvironmentalData

# Set up logger
logger = logging.getLogger(__name__)


def validate_and_get_limit(request, default_limit=1000, max_limit=10000):
    """Validate and get limit parameter with performance constraints"""
    requested_limit = request.query_params.get('limit')
    if requested_limit:
        try:
            limit = int(requested_limit)
            # Enforce maximum limit for performance
            if limit > max_limit:
                return None, {
                    'success': False,
                    'error': f'Limit cannot exceed {max_limit:,} points for performance reasons. Use date filters to reduce data size.',
                    'max_limit': max_limit,
                    'suggestion': 'Use start_date and end_date parameters to filter data'
                }
            return limit, None
        except ValueError:
            return None, {
                'success': False,
                'error': 'Invalid limit parameter. Must be a number.'
            }
    else:
        return default_limit, None


class RawSnowDepthView(APIView):
    """Raw snow depth data for detailed analysis"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get raw snow depth data points for detailed analysis"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # Performance optimization: validate limit
            limit, error_response = validate_and_get_limit(request)
            if error_response:
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = EnvironmentalData.objects.filter(
                SnowDepth_cm__isnull=False
            ).order_by('Year', 'Month', 'Day', 'Time')
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_year, end_month, end_day = map(int, end_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__lt=end_year) |
                    (Q(Year=end_year) & Q(Month__lt=end_month)) |
                    (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
                )
            
            # If no date filters are applied, default to the latest year
            if not any([year, month, start_date, end_date]):
                latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
                if latest_year:
                    queryset = queryset.filter(Year=latest_year)
                    year = str(latest_year)  # For response metadata
            
            # Limit results for performance
            queryset = queryset[:limit]
            
            # Format data for detailed analysis
            raw_data = []
            for record in queryset:
                raw_data.append({
                    'timestamp': f"{record.Year}-{record.Month:02d}-{record.Day:02d} {record.Time}",
                    'date': f"{record.Year}-{record.Month:02d}-{record.Day:02d}",
                    'time': record.Time,
                    'snow_depth_cm': record.SnowDepth_cm,
                    'year': record.Year,
                    'month': record.Month,
                    'day': record.Day
                })
            
            return Response({
                'success': True,
                'data': raw_data,
                'total_points': len(raw_data),
                'metric': 'snow_depth_cm',
                'unit': 'cm',
                'data_type': 'raw_points',
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'limit': limit
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in RawSnowDepthView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve raw snow depth data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RawRainfallView(APIView):
    """Raw rainfall data for detailed analysis"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get raw rainfall data points for detailed analysis"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # Performance optimization: validate limit
            limit, error_response = validate_and_get_limit(request)
            if error_response:
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = EnvironmentalData.objects.filter(
                Rainfall_mm__isnull=False
            ).order_by('Year', 'Month', 'Day', 'Time')
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_year, end_month, end_day = map(int, end_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__lt=end_year) |
                    (Q(Year=end_year) & Q(Month__lt=end_month)) |
                    (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
                )
            
            # If no date filters are applied, default to the latest year
            if not any([year, month, start_date, end_date]):
                latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
                if latest_year:
                    queryset = queryset.filter(Year=latest_year)
                    year = str(latest_year)  # For response metadata
            
            queryset = queryset[:limit]
            
            # Format data for detailed analysis
            raw_data = []
            for record in queryset:
                raw_data.append({
                    'timestamp': f"{record.Year}-{record.Month:02d}-{record.Day:02d} {record.Time}",
                    'date': f"{record.Year}-{record.Month:02d}-{record.Day:02d}",
                    'time': record.Time,
                    'rainfall_mm': record.Rainfall_mm,
                    'total_precipitation_mm': record.TotalPrecipitation_mm,
                    'year': record.Year,
                    'month': record.Month,
                    'day': record.Day
                })
            
            return Response({
                'success': True,
                'data': raw_data,
                'total_points': len(raw_data),
                'metric': 'rainfall',
                'unit': 'mm',
                'data_type': 'raw_points',
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'limit': limit
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in RawRainfallView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve raw rainfall data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RawSoilTemperatureView(APIView):
    """Raw soil temperature data for detailed analysis"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get raw soil temperature data points for detailed analysis"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            depth = request.query_params.get('depth', '5cm')  # 5cm, 10cm, 20cm, 25cm, 50cm
            
            # Performance optimization: validate limit
            limit, error_response = validate_and_get_limit(request)
            if error_response:
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
            # Map depth to field name
            depth_fields = {
                '5cm': 'SoilTemperature_5cm_degC',
                '10cm': 'SoilTemperature_10cm_degC',
                '20cm': 'SoilTemperature_20cm_degC',
                '25cm': 'SoilTemperature_25cm_degC',
                '50cm': 'SoilTemperature_50cm_degC'
            }
            
            field_name = depth_fields.get(depth, 'SoilTemperature_5cm_degC')
            
            queryset = EnvironmentalData.objects.filter(
                **{f"{field_name}__isnull": False}
            ).order_by('Year', 'Month', 'Day', 'Time')
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_year, end_month, end_day = map(int, end_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__lt=end_year) |
                    (Q(Year=end_year) & Q(Month__lt=end_month)) |
                    (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
                )
            
            # If no date filters are applied, default to the latest year
            if not any([year, month, start_date, end_date]):
                latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
                if latest_year:
                    queryset = queryset.filter(Year=latest_year)
                    year = str(latest_year)  # For response metadata
            
            queryset = queryset[:limit]
            
            # Format data for detailed analysis
            raw_data = []
            for record in queryset:
                raw_data.append({
                    'timestamp': f"{record.Year}-{record.Month:02d}-{record.Day:02d} {record.Time}",
                    'date': f"{record.Year}-{record.Month:02d}-{record.Day:02d}",
                    'time': record.Time,
                    'soil_temp_degc': getattr(record, field_name),
                    'depth': depth,
                    'year': record.Year,
                    'month': record.Month,
                    'day': record.Day
                })
            
            return Response({
                'success': True,
                'data': raw_data,
                'total_points': len(raw_data),
                'metric': 'soil_temperature',
                'unit': '°C',
                'depth': depth,
                'data_type': 'raw_points',
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'depth': depth,
                    'limit': limit
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in RawSoilTemperatureView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve raw soil temperature data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RawMultiMetricView(APIView):
    """Raw multi-metric data for detailed analysis"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get raw multi-metric data points for detailed analysis"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            metrics = request.query_params.get('metrics', 'air_temp,humidity,wind_speed').split(',')
            
            # Performance optimization: validate limit
            limit, error_response = validate_and_get_limit(request)
            if error_response:
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            
            # Map metrics to field names
            metric_fields = {
                'air_temp': 'AirTemperature_degC',
                'humidity': 'RelativeHumidity_Pct',
                'wind_speed': 'WindSpeed_ms',
                'snow_depth': 'SnowDepth_cm',
                'rainfall': 'Rainfall_mm',
                'soil_temp_5cm': 'SoilTemperature_5cm_degC',
                'soil_temp_10cm': 'SoilTemperature_10cm_degC',
                'soil_temp_20cm': 'SoilTemperature_20cm_degC',
                'atmospheric_pressure': 'AtmosphericPressure_kPa',
                'solar_radiation': 'ShortwaveRadiation_Wm2'
            }
            
            # Build filter conditions
            filter_conditions = Q()
            for metric in metrics:
                if metric in metric_fields:
                    field_name = metric_fields[metric]
                    filter_conditions |= Q(**{f"{field_name}__isnull": False})
            
            queryset = EnvironmentalData.objects.filter(filter_conditions).order_by('Year', 'Month', 'Day', 'Time')
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_year, end_month, end_day = map(int, end_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__lt=end_year) |
                    (Q(Year=end_year) & Q(Month__lt=end_month)) |
                    (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
                )
            
            # If no date filters are applied, default to the latest year
            if not any([year, month, start_date, end_date]):
                latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
                if latest_year:
                    queryset = queryset.filter(Year=latest_year)
                    year = str(latest_year)  # For response metadata
            
            queryset = queryset[:limit]
            
            # Format data for detailed analysis
            raw_data = []
            for record in queryset:
                data_point = {
                    'timestamp': f"{record.Year}-{record.Month:02d}-{record.Day:02d} {record.Time}",
                    'date': f"{record.Year}-{record.Month:02d}-{record.Day:02d}",
                    'time': record.Time,
                    'year': record.Year,
                    'month': record.Month,
                    'day': record.Day
                }
                
                # Add requested metrics
                for metric in metrics:
                    if metric in metric_fields:
                        field_name = metric_fields[metric]
                        data_point[metric] = getattr(record, field_name)
                
                raw_data.append(data_point)
            
            return Response({
                'success': True,
                'data': raw_data,
                'total_points': len(raw_data),
                'metrics': metrics,
                'data_type': 'raw_points',
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'metrics': metrics,
                    'limit': limit
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in RawMultiMetricView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve raw multi-metric data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 