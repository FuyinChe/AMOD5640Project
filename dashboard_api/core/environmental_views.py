"""
Environmental data views module for handling environmental data APIs.
Includes endpoints for sample data, monthly summaries, and time series charts.
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Avg, Max, Min, StdDev, Sum, Count
import calendar
from datetime import datetime

# Swagger documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import EnvironmentalData
from .serializers import EnvironmentalDataSerializer, MonthlySummarySerializer

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


class EnvironmentalDataList(generics.ListAPIView):
    """List environmental data with pagination"""
    queryset = EnvironmentalData.objects.all().order_by('-Year', '-Month', '-Day')[:3000]  # return 3000
    serializer_class = EnvironmentalDataSerializer


class SampleEnvironmentalDataList(generics.ListAPIView):
    """Public API endpoint to provide a sample of environmental data for guest users (no authentication required)."""
    permission_classes = [AllowAny]  # No authentication required - public sample data
    serializer_class = EnvironmentalDataSerializer
    
    # return 40 random value with filtered data
    def get_queryset(self):

        return EnvironmentalData.objects.filter(
            Q(SnowDepth_cm__isnull=False) &
            Q(RelativeHumidity_Pct__isnull=False) &           
            Q(Rainfall_mm__isnull=False) &
            Q(SoilTemperature_5cm_degC__isnull=False) 
        ).order_by('-Year', '-Month', '-Day')[:40]


class MonthlySummaryView(APIView):
    """API endpoint to provide monthly summary aggregations of environmental data. Requires authentication."""
    
    @swagger_auto_schema(
        operation_description="Get monthly summarized environmental data with statistical aggregations",
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('month', openapi.IN_QUERY, description="Filter by month", type=openapi.TYPE_INTEGER),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description="Monthly summary data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                        'total_months': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'filters_applied': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        """
        Get monthly summarized environmental data with statistical aggregations.
        Similar to pandas df.describe() but grouped by month.
        """
        try:
            
            # Get query parameters for filtering
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')  # Format: YYYY-MM-DD
            end_date = request.query_params.get('end_date')      # Format: YYYY-MM-DD
            
            # Start with base queryset
            queryset = EnvironmentalData.objects.all()
            
            # Apply filters if provided
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            
            # Apply date range filters if provided
            if start_date:
                try:
                    start_date = start_date.strip().strip("'\"")
                    start_year, start_month, start_day = map(int, start_date.split('-'))
                    queryset = queryset.filter(
                        Q(Year__gt=start_year) |
                        (Q(Year=start_year) & Q(Month__gt=start_month)) |
                        (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                    )
                except (ValueError, TypeError):
                    return Response({
                        'success': False,
                        'error': 'Invalid start_date format. Use YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if end_date:
                try:
                    end_date = end_date.strip().strip("'\"")
                    end_year, end_month, end_day = map(int, end_date.split('-'))
                    queryset = queryset.filter(
                        Q(Year__lt=end_year) |
                        (Q(Year=end_year) & Q(Month__lt=end_month)) |
                        (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
                    )
                except (ValueError, TypeError):
                    return Response({
                        'success': False,
                        'error': 'Invalid end_date format. Use YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # If no filters are applied, default to the latest year
            if not any([year, month, start_date, end_date]):
                latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
                if latest_year:
                    queryset = queryset.filter(Year=latest_year)
                    year = str(latest_year)  # For response metadata
            
            # Group by year and month, then aggregate
            monthly_data = queryset.values('Year', 'Month').annotate(
                # Record count
                record_count=Count('id'),
                
                # Air Temperature statistics
                air_temperature_max=Max('AirTemperature_degC'),
                air_temperature_min=Min('AirTemperature_degC'),
                air_temperature_mean=Avg('AirTemperature_degC'),
                air_temperature_std=StdDev('AirTemperature_degC'),
                
                # Relative Humidity statistics
                relative_humidity_max=Max('RelativeHumidity_Pct'),
                relative_humidity_min=Min('RelativeHumidity_Pct'),
                relative_humidity_mean=Avg('RelativeHumidity_Pct'),
                relative_humidity_std=StdDev('RelativeHumidity_Pct'),
                
                # Shortwave Radiation statistics
                shortwave_radiation_max=Max('ShortwaveRadiation_Wm2'),
                shortwave_radiation_min=Min('ShortwaveRadiation_Wm2'),
                shortwave_radiation_mean=Avg('ShortwaveRadiation_Wm2'),
                shortwave_radiation_std=StdDev('ShortwaveRadiation_Wm2'),
                
                # Rainfall statistics
                rainfall_total=Sum('Rainfall_mm'),
                rainfall_max=Max('Rainfall_mm'),
                rainfall_mean=Avg('Rainfall_mm'),
                rainfall_std=StdDev('Rainfall_mm'),
                
                # Soil Temperature statistics (5cm)
                soil_temp_5cm_max=Max('SoilTemperature_5cm_degC'),
                soil_temp_5cm_min=Min('SoilTemperature_5cm_degC'),
                soil_temp_5cm_mean=Avg('SoilTemperature_5cm_degC'),
                soil_temp_5cm_std=StdDev('SoilTemperature_5cm_degC'),
                
                # Wind Speed statistics
                wind_speed_max=Max('WindSpeed_ms'),
                wind_speed_min=Min('WindSpeed_ms'),
                wind_speed_mean=Avg('WindSpeed_ms'),
                wind_speed_std=StdDev('WindSpeed_ms'),
                
                # Snow Depth statistics
                snow_depth_max=Max('SnowDepth_cm'),
                snow_depth_min=Min('SnowDepth_cm'),
                snow_depth_mean=Avg('SnowDepth_cm'),
                snow_depth_std=StdDev('SnowDepth_cm'),
                
                # Atmospheric Pressure statistics
                atmospheric_pressure_max=Max('AtmosphericPressure_kPa'),
                atmospheric_pressure_min=Min('AtmosphericPressure_kPa'),
                atmospheric_pressure_mean=Avg('AtmosphericPressure_kPa'),
                atmospheric_pressure_std=StdDev('AtmosphericPressure_kPa'),
                
            ).order_by('Year', 'Month')
            
            # Convert to list and add month names, and map keys for serializer
            result_data = []
            for item in monthly_data:
                item['year'] = item.pop('Year')
                item['month'] = item.pop('Month')
                item['month_name'] = calendar.month_name[item['month']]
                result_data.append(item)
            
            # Serialize the data
            serializer = MonthlySummarySerializer(result_data, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'total_months': len(result_data),
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date
                },
                'default_behavior': 'latest_year' if not any([year, month, start_date, end_date]) else None
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in MonthlySummaryView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve monthly summary: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class SnowDepthChartView(APIView):
    """Snow depth time series data for charts"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get snow depth data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                SnowDepth_cm__isnull=False
            )
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_date = start_date.strip().strip("'\"")
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_date = end_date.strip().strip("'\"")
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
            
            # Group by time period and calculate averages
            if group_by == 'month':
                # Group by year and month
                aggregated_data = queryset.values('Year', 'Month').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}",
                        'date': f"{record['Year']}-{record['Month']:02d}-01",
                        'year': record['Year'],
                        'month': record['Month'],
                        'avg_snow_depth_cm': round(record['avg_snow_depth'], 2),
                        'max_snow_depth_cm': record['max_snow_depth'],
                        'min_snow_depth_cm': record['min_snow_depth'],
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'week':
                # Group by year and week (simplified as week number)
                from django.db.models.functions import ExtractWeek
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('Year', 'week').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Year', 'week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-W{record['week']:02d}",
                        'date': f"{record['Year']}-01-01",  # Simplified
                        'year': record['Year'],
                        'week': record['week'],
                        'avg_snow_depth_cm': round(record['avg_snow_depth'], 2),
                        'max_snow_depth_cm': record['max_snow_depth'],
                        'min_snow_depth_cm': record['min_snow_depth'],
                        'data_points': record['data_points']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record.Day,
                        'avg_snow_depth_cm': round(record['avg_snow_depth'], 2),
                        'max_snow_depth_cm': record['max_snow_depth'],
                        'min_snow_depth_cm': record['min_snow_depth'],
                        'data_points': record['data_points']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'total_periods': len(chart_data),
                'metric': 'snow_depth_cm',
                'unit': 'cm',
                'aggregation': 'average',
                'group_by': group_by,
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'group_by': group_by
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in SnowDepthChartView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve snow depth data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RainfallChartView(APIView):
    """Rainfall time series data for charts"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get rainfall data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            group_by = request.query_params.get('group_by', 'day')  # day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                Rainfall_mm__isnull=False
            )
            
            # Apply filters
            if year:
                queryset = queryset.filter(Year=int(year))
            if month:
                queryset = queryset.filter(Month=int(month))
            if start_date:
                start_date = start_date.strip().strip("'\"")
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_date = end_date.strip().strip("'\"")
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
            
            # Group by time period and calculate averages
            if group_by == 'month':
                # Group by year and month
                aggregated_data = queryset.values('Year', 'Month').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}",
                        'date': f"{record['Year']}-{record['Month']:02d}-01",
                        'year': record['Year'],
                        'month': record['Month'],
                        'avg_rainfall_mm': round(record['avg_rainfall'], 2),
                        'total_rainfall_mm': round(record['total_rainfall'], 2),
                        'max_rainfall_mm': record['max_rainfall'],
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'week':
                # Group by year and week
                from django.db.models.functions import ExtractWeek
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('Year', 'week').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Year', 'week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-W{record['week']:02d}",
                        'date': f"{record['Year']}-01-01",  # Simplified
                        'year': record['Year'],
                        'week': record['week'],
                        'avg_rainfall_mm': round(record['avg_rainfall'], 2),
                        'total_rainfall_mm': round(record['total_rainfall'], 2),
                        'max_rainfall_mm': record['max_rainfall'],
                        'data_points': record['data_points']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record['Day'],
                        'avg_rainfall_mm': round(record['avg_rainfall'], 2),
                        'total_rainfall_mm': round(record['total_rainfall'], 2),
                        'max_rainfall_mm': record['max_rainfall'],
                        'data_points': record['data_points']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'total_periods': len(chart_data),
                'metric': 'rainfall',
                'unit': 'mm',
                'aggregation': 'average',
                'group_by': group_by,
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'group_by': group_by
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in RainfallChartView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve rainfall data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoilTemperatureChartView(APIView):
    """Soil temperature time series data for charts"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get soil temperature data over time for charting"""
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
                start_date = start_date.strip().strip("'\"")
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_date = end_date.strip().strip("'\"")
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
            
            # Format data for charts
            chart_data = []
            for record in queryset:
                chart_data.append({
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
                'data': chart_data,
                'total_points': len(chart_data),
                'metric': 'soil_temperature',
                'unit': '°C',
                'depth': depth,
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
            logger.error(f"Error in SoilTemperatureChartView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve soil temperature data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MultiMetricChartView(APIView):
    """Multi-metric time series data for comparison charts"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get multiple metrics over time for comparison charts"""
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
                start_date = start_date.strip().strip("'\"")
                start_year, start_month, start_day = map(int, start_date.split('-'))
                queryset = queryset.filter(
                    Q(Year__gt=start_year) |
                    (Q(Year=start_year) & Q(Month__gt=start_month)) |
                    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
                )
            if end_date:
                end_date = end_date.strip().strip("'\"")
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
            
            # Format data for charts
            chart_data = []
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
                
                chart_data.append(data_point)
            
            return Response({
                'success': True,
                'data': chart_data,
                'total_points': len(chart_data),
                'metrics': metrics,
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
            logger.error(f"Error in MultiMetricChartView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve multi-metric data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class DownloadEnvironmentalDataView(APIView):
    """
    API endpoint to download environmental data with advanced filtering.
    Supports filtering by date range (start_date, end_date) and selecting specific fields (fields).
    Requires authentication (JWT).
    Query params:
      - start_date: YYYY-MM-DD (optional)
      - end_date: YYYY-MM-DD (optional)
      - fields: comma-separated list of field names (optional, default: all fields)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Parse date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        fields = request.query_params.get('fields')

        # Set default date range if not provided
        if not start_date and not end_date:
            start_date = '2023-01-01'
            end_date = '2023-12-31'  # Default to full year 2023
            # Comment: Default date range is 2023-01-01 to 2023-12-31 if not specified

        queryset = EnvironmentalData.objects.all()
        # Filter by date range if provided
        if start_date:
            if isinstance(start_date, list):
                start_date = start_date[0]
            start_date = start_date.strip().strip("'\"")
            print(f"DEBUG: start_date received: {repr(start_date)}")
            print("DEBUG: start_date ords:", [ord(c) for c in start_date])
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                print(f"DEBUG: Parsed start: {start.year}-{start.month}-{start.day}")
            except Exception as e:
                return Response({'error': f'Invalid start_date value: {repr(start_date)}. Use YYYY-MM-DD.'}, status=400)
            try:
                queryset = queryset.filter(
                    Q(Year__gt=start.year) |
                    Q(Year=start.year, Month__gt=start.month) |
                    Q(Year=start.year, Month=start.month, Day__gte=start.day)
                )
            except Exception as e:
                return Response({'error': f'Error in start_date filtering: {str(e)}'}, status=400)
        if end_date:
            if isinstance(end_date, list):
                end_date = end_date[0]
            end_date = end_date.strip().strip("'\"")
            print(f"DEBUG: end_date received: {repr(end_date)}")
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                print(f"DEBUG: Parsed end: {end.year}-{end.month}-{end.day}")
            except Exception as e:
                return Response({'error': f'Invalid end_date value: {repr(end_date)}. Use YYYY-MM-DD.'}, status=400)
            try:
                queryset = queryset.filter(
                    Q(Year__lt=end.year) |
                    Q(Year=end.year, Month__lt=end.month) |
                    Q(Year=end.year, Month=end.month, Day__lte=end.day)
                )
            except Exception as e:
                return Response({'error': f'Error in end_date filtering: {str(e)}'}, status=400)

        # Limit to 10,000 records for performance
        queryset = queryset.order_by('-Year', '-Month', '-Day')[:10000]

        # Handle field selection with validation
        if fields:
            field_list = [f.strip() for f in fields.split(',') if f.strip()]
            # Always include id for uniqueness
            if 'id' not in field_list:
                field_list.append('id')
            # Validate fields
            valid_fields = set(f.name for f in EnvironmentalData._meta.get_fields())
            invalid_fields = [f for f in field_list if f not in valid_fields]
            if invalid_fields:
                return Response({'error': f'Invalid field(s): {", ".join(invalid_fields)}'}, status=400)
            data = list(queryset.values(*field_list))
        else:
            data = list(queryset.values())

        return Response(data) 