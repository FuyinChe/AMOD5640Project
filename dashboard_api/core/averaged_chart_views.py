"""
Averaged chart views module for environmental data visualizations
Returns aggregated values over time periods (hourly, daily, monthly)
"""
import logging
from typing import Any, Dict, List, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from django.db.models import Q, Max, Avg, Min, Sum, Count, Value, CharField
from django.db.models.functions import ExtractWeek, Substr, Concat, Cast
from django.db.models import DateField
from django.db.models.query import QuerySet
from datetime import datetime

# Swagger documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import EnvironmentalData

# Set up logger
logger = logging.getLogger(__name__)


class AveragedSnowDepthView(APIView):
    """Averaged snow depth data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged snow depth data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                SnowDepth_cm__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_snow_depth'], 2),
                            'max': record['max_snow_depth'],
                            'min': record['min_snow_depth']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                    
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_snow_depth'], 2),
                        'max': record['max_snow_depth'],
                        'min': record['min_snow_depth']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_snow_depth'], 2),
                        'max': record['max_snow_depth'],
                        'min': record['min_snow_depth']
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
                        'avg': round(record['avg_snow_depth'], 2),
                        'max': record['max_snow_depth'],
                        'min': record['min_snow_depth']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': 'cm'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedSnowDepthView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged snow depth data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AveragedRainfallView(APIView):
    """Averaged rainfall data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged rainfall data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                Rainfall_mm__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_rainfall'], 2),
                            'total': round(record['total_rainfall'], 2),
                            'max': record['max_rainfall']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                    
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_rainfall'], 2),
                        'total': round(record['total_rainfall'], 2),
                        'max': record['max_rainfall']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_rainfall'], 2),
                        'total': round(record['total_rainfall'], 2),
                        'max': record['max_rainfall']
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
                        'avg': round(record['avg_rainfall'], 2),
                        'total': round(record['total_rainfall'], 2),
                        'max': record['max_rainfall']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': 'mm'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedRainfallView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged rainfall data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AveragedSoilTemperatureView(APIView):
    """Averaged soil temperature data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged soil temperature data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            depth = request.query_params.get('depth', '5cm')  # 5cm, 10cm, 20cm, 25cm, 50cm
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
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
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_temp'], 2),
                            'max': record['max_temp'],
                            'min': record['min_temp']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                        
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_temp'], 2),
                        'max': record['max_temp'],
                        'min': record['min_temp']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_temp'], 2),
                        'max': record['max_temp'],
                        'min': record['min_temp']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'avg': round(record['avg_temp'], 2),
                        'max': record['max_temp'],
                        'min': record['min_temp']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': '°C'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedSoilTemperatureView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged soil temperature data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AveragedHumidityView(APIView):
    """Averaged humidity data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged humidity data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                RelativeHumidity_Pct__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_humidity'], 2),
                            'max': record['max_humidity'],
                            'min': record['min_humidity']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                        
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_humidity'], 2),
                        'max': record['max_humidity'],
                        'min': record['min_humidity']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_humidity'], 2),
                        'max': record['max_humidity'],
                        'min': record['min_humidity']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'avg': round(record['avg_humidity'], 2),
                        'max': record['max_humidity'],
                        'min': record['min_humidity']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': '%'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedHumidityView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged humidity data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class AveragedShortwaveRadiationView(APIView):
    """Averaged shortwave radiation data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged shortwave radiation data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                ShortwaveRadiation_Wm2__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_radiation=Avg('ShortwaveRadiation_Wm2'),
                    max_radiation=Max('ShortwaveRadiation_Wm2'),
                    min_radiation=Min('ShortwaveRadiation_Wm2'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_radiation'], 2),
                            'max': record['max_radiation'],
                            'min': record['min_radiation']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                        
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_radiation=Avg('ShortwaveRadiation_Wm2'),
                    max_radiation=Max('ShortwaveRadiation_Wm2'),
                    min_radiation=Min('ShortwaveRadiation_Wm2'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_radiation'], 2),
                        'max': record['max_radiation'],
                        'min': record['min_radiation']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_radiation=Avg('ShortwaveRadiation_Wm2'),
                    max_radiation=Max('ShortwaveRadiation_Wm2'),
                    min_radiation=Min('ShortwaveRadiation_Wm2'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_radiation'], 2),
                        'max': record['max_radiation'],
                        'min': record['min_radiation']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_radiation=Avg('ShortwaveRadiation_Wm2'),
                    max_radiation=Max('ShortwaveRadiation_Wm2'),
                    min_radiation=Min('ShortwaveRadiation_Wm2'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'avg': round(record['avg_radiation'], 2),
                        'max': record['max_radiation'],
                        'min': record['min_radiation']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': 'W/m²'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedShortwaveRadiationView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged shortwave radiation data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AveragedWindSpeedView(APIView):
    """Averaged wind speed data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged wind speed data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                WindSpeed_ms__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_wind_speed=Avg('WindSpeed_ms'),
                    max_wind_speed=Max('WindSpeed_ms'),
                    min_wind_speed=Min('WindSpeed_ms'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_wind_speed'], 2),
                            'max': record['max_wind_speed'],
                            'min': record['min_wind_speed']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                        
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_wind_speed=Avg('WindSpeed_ms'),
                    max_wind_speed=Max('WindSpeed_ms'),
                    min_wind_speed=Min('WindSpeed_ms'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_wind_speed'], 2),
                        'max': record['max_wind_speed'],
                        'min': record['min_wind_speed']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_wind_speed=Avg('WindSpeed_ms'),
                    max_wind_speed=Max('WindSpeed_ms'),
                    min_wind_speed=Min('WindSpeed_ms'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_wind_speed'], 2),
                        'max': record['max_wind_speed'],
                        'min': record['min_wind_speed']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_wind_speed=Avg('WindSpeed_ms'),
                    max_wind_speed=Max('WindSpeed_ms'),
                    min_wind_speed=Min('WindSpeed_ms'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'avg': round(record['avg_wind_speed'], 2),
                        'max': record['max_wind_speed'],
                        'min': record['min_wind_speed']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': 'm/s'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedWindSpeedView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged wind speed data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AveragedAtmosphericPressureView(APIView):
    """Averaged atmospheric pressure data for charts and dashboards"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Get averaged atmospheric pressure data over time for charting"""
        try:
            # Get query parameters
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            group_by = request.query_params.get('group_by', 'day')  # hour, day, week, month
            
            queryset = EnvironmentalData.objects.filter(
                AtmosphericPressure_kPa__isnull=False
            )
            
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
            
            # Group by time period and calculate averages
            if group_by == 'hour':
                # For hourly: return exactly 24 data points (0-23 hours) with calculated averages
                aggregated_data = queryset.annotate(
                    hour=Substr('Time', 1, 2)  # Extract first 2 characters as hour
                ).values('hour').annotate(
                    avg_pressure=Avg('AtmosphericPressure_kPa'),
                    max_pressure=Max('AtmosphericPressure_kPa'),
                    min_pressure=Min('AtmosphericPressure_kPa'),
                    data_points=Count('id')
                ).order_by('hour')
                
                chart_data = []
                for record in aggregated_data:
                    try:
                        hour_int = int(record['hour']) if record['hour'] else 0
                        chart_data.append({
                            'period': f"{hour_int:02d}:00",
                            'avg': round(record['avg_pressure'], 2),
                            'max': record['max_pressure'],
                            'min': record['min_pressure']
                        })
                    except (ValueError, TypeError):
                        # Skip records with invalid hour format
                        continue
                        
            elif group_by == 'month':
                # For monthly: return exactly 12 data points (1-12 months) with calculated averages
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                aggregated_data = queryset.values('Month').annotate(
                    avg_pressure=Avg('AtmosphericPressure_kPa'),
                    max_pressure=Max('AtmosphericPressure_kPa'),
                    min_pressure=Min('AtmosphericPressure_kPa'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': month_names.get(record['Month'], f"{record['Month']:02d}"),
                        'avg': round(record['avg_pressure'], 2),
                        'max': record['max_pressure'],
                        'min': record['min_pressure']
                    })
                    
            elif group_by in ['week', 'weekly']:
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    date_field=Cast(
                        Concat(
                            Cast('Year', output_field=CharField()),
                            Value('-'),
                            Cast('Month', output_field=CharField()),
                            Value('-'),
                            Cast('Day', output_field=CharField())
                        ),
                        output_field=DateField()
                    )
                ).annotate(
                    week=ExtractWeek('date_field')
                ).values('week').annotate(
                    avg_pressure=Avg('AtmosphericPressure_kPa'),
                    max_pressure=Max('AtmosphericPressure_kPa'),
                    min_pressure=Min('AtmosphericPressure_kPa'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'week': record['week'],
                        'avg': round(record['avg_pressure'], 2),
                        'max': record['max_pressure'],
                        'min': record['min_pressure']
                    })
                    
            else:  # Default: group by day
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    avg_pressure=Avg('AtmosphericPressure_kPa'),
                    max_pressure=Max('AtmosphericPressure_kPa'),
                    min_pressure=Min('AtmosphericPressure_kPa'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'avg': round(record['avg_pressure'], 2),
                        'max': record['max_pressure'],
                        'min': record['min_pressure']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'unit': 'kPa'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedAtmosphericPressureView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged atmospheric pressure data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class MultiMetricBoxplotView(APIView):
    """Multi-metric boxplot data for statistical analysis across different time periods"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Generate boxplot data for multiple environmental metrics across different time periods",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('metrics', openapi.IN_QUERY, description="List of metric names (optional, defaults to all metrics)", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), required=False),
            openapi.Parameter('include_outliers', openapi.IN_QUERY, description="Include outlier data", type=openapi.TYPE_BOOLEAN, default=True),
            openapi.Parameter('depth', openapi.IN_QUERY, description="Soil temperature depth (5cm, 10cm, 20cm, 25cm, 50cm)", type=openapi.TYPE_STRING, default="5cm"),
        ],
        responses={
            200: openapi.Response(
                description="Boxplot data for multiple metrics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'period': openapi.Schema(type=openapi.TYPE_STRING),
                                        'period_code': openapi.Schema(type=openapi.TYPE_STRING),
                                        'statistics': openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'min': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'q1': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'median': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'q3': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'max': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'outliers': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER)),
                                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            }
                                        )
                                    }
                                )
                            )
                        ),
                        'metadata': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            400: 'Bad Request - Invalid parameters',
            500: 'Internal Server Error'
        }
    )
    def get(self, request: Request) -> Response:
        """Get boxplot data for multiple environmental metrics across different time periods"""
        try:
            # Get query parameters
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            metrics = request.query_params.getlist('metrics')  # List of metric names (optional, defaults to all)
            include_outliers = request.query_params.get('include_outliers', 'true').lower() == 'true'
            depth = request.query_params.get('depth', '5cm')  # For soil temperature
            
            # Validate required parameters
            if not start_date or not end_date:
                return Response({
                    'success': False,
                    'error': 'start_date and end_date are required parameters'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # If no metrics specified, use all available metrics
            if not metrics:
                metrics = ['humidity', 'temperature', 'wind_speed', 'rainfall', 'snow_depth', 'shortwave_radiation', 'atmospheric_pressure', 'soil_temperature']
            
            # Validate date format
            try:
                start_year, start_month, start_day = map(int, str(start_date).split('-'))
                end_year, end_month, end_day = map(int, str(end_date).split('-'))
            except (ValueError, TypeError):
                return Response({
                    'success': False,
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Define metric field mappings
            metric_fields = {
                'humidity': 'RelativeHumidity_Pct',
                'temperature': 'AirTemperature_degC',
                'wind_speed': 'WindSpeed_ms',
                'rainfall': 'Rainfall_mm',
                'snow_depth': 'SnowDepth_cm',
                'shortwave_radiation': 'ShortwaveRadiation_Wm2',
                'atmospheric_pressure': 'AtmosphericPressure_kPa',
                'soil_temperature': self._get_soil_temperature_field(depth)
            }
            
            # Validate metrics
            invalid_metrics = [m for m in metrics if m not in metric_fields]
            if invalid_metrics:
                return Response({
                    'success': False,
                    'error': f'Invalid metrics: {invalid_metrics}. Valid metrics: {list(metric_fields.keys())}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Start with base queryset
            queryset = EnvironmentalData.objects.all()
            
            # Apply date filters
            queryset = queryset.filter(
                Q(Year__gt=start_year) |
                (Q(Year=start_year) & Q(Month__gt=start_month)) |
                (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
            ).filter(
                Q(Year__lt=end_year) |
                (Q(Year=end_year) & Q(Month__lt=end_month)) |
                (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
            )
            
            # Generate boxplot data for each metric (overall only)
            boxplot_data = {}
            
            for metric in metrics:
                field_name = metric_fields[metric]
                
                # Filter out null values for this metric
                metric_queryset = queryset.filter(**{f'{field_name}__isnull': False})
                
                # Add performance optimization: limit data points if too many
                total_count = metric_queryset.count()
                if total_count > 10000:  # If more than 10k data points
                    logger.warning(f"Large dataset detected for {metric}: {total_count} records. Consider using smaller date ranges.")
                
                # Always use overall grouping for maximum performance
                boxplot_data[metric] = self._get_overall_boxplot_data(metric_queryset, field_name, include_outliers)
            
            return Response({
                'success': True,
                'data': boxplot_data,
                'metadata': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'metrics': metrics,
                    'group_by': 'overall',
                    'include_outliers': include_outliers,
                    'depth': depth if 'soil_temperature' in metrics else None
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in MultiMetricBoxplotView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve boxplot data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_soil_temperature_field(self, depth: str) -> str:
        """Get the appropriate soil temperature field based on depth"""
        depth_mapping = {
            '5cm': 'SoilTemperature_5cm_degC',
            '10cm': 'SoilTemperature_10cm_degC',
            '20cm': 'SoilTemperature_20cm_degC',
            '25cm': 'SoilTemperature_25cm_degC',
            '50cm': 'SoilTemperature_50cm_degC'
        }
        return depth_mapping.get(depth, 'SoilTemperature_5cm_degC')
    
    def _calculate_boxplot_statistics(self, values: list, include_outliers: bool = True) -> dict:
        """Calculate boxplot statistics (min, q1, median, q3, max, outliers)"""
        if not values:
            return {
                'min': None, 'q1': None, 'median': None, 'q3': None, 'max': None,
                'outliers': [] if include_outliers else None, 'count': 0
            }
        
        # Filter out None values and convert to float for better performance
        values = [float(v) for v in values if v is not None]
        if not values:
            return {
                'min': None, 'q1': None, 'median': None, 'q3': None, 'max': None,
                'outliers': [] if include_outliers else None, 'count': 0
            }
        
        n = len(values)
        
        # Use numpy for faster statistical calculations if available
        try:
            import numpy as np
            values_array = np.array(values)
            q1 = float(np.percentile(values_array, 25))
            median = float(np.median(values_array))
            q3 = float(np.percentile(values_array, 75))
        except ImportError:
            # Fallback to manual calculation
            values = sorted(values)
            q1_idx = int(0.25 * n)
            median_idx = int(0.5 * n)
            q3_idx = int(0.75 * n)
            
            q1 = values[q1_idx] if q1_idx < n else values[-1]
            median = values[median_idx] if median_idx < n else values[-1]
            q3 = values[q3_idx] if q3_idx < n else values[-1]
        
        # Calculate IQR and outlier bounds
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Find outliers more efficiently
        outliers = []
        if include_outliers:
            outliers = [v for v in values if v < lower_bound or v > upper_bound]
        
        # Get min and max (excluding outliers if requested)
        if include_outliers:
            min_val = min(values)
            max_val = max(values)
        else:
            non_outliers = [v for v in values if lower_bound <= v <= upper_bound]
            min_val = min(non_outliers) if non_outliers else None
            max_val = max(non_outliers) if non_outliers else None
        
        return {
            'min': round(min_val, 2) if min_val is not None else None,
            'q1': round(q1, 2),
            'median': round(median, 2),
            'q3': round(q3, 2),
            'max': round(max_val, 2) if max_val is not None else None,
            'outliers': [round(v, 2) for v in outliers] if include_outliers else None,
            'count': len(values)
        }
    

    
    def _get_overall_boxplot_data(self, queryset, field_name: str, include_outliers: bool) -> list:
        """Get overall boxplot data for the entire date range (much faster)"""
        
        # Fetch all values at once for maximum performance
        all_values = list(queryset.values_list(field_name, flat=True))
        
        # Calculate statistics for the entire dataset
        stats = self._calculate_boxplot_statistics(all_values, include_outliers)
        
        # Return single period with overall statistics
        return [{
            'period': 'Overall',
            'period_code': 'overall',
            'statistics': stats
        }] 


class MultiMetricHistogramView(APIView):
    """
    Multi-Metric Histogram API (Overall Only)
    
    Generates histogram data for multiple environmental metrics across a date range.
    Processes the entire date range as one dataset for maximum performance.
    Returns bin counts and percentages for data distribution analysis.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Generate histogram data for multiple environmental metrics (overall processing)",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('metrics', openapi.IN_QUERY, description="List of metric names (optional, defaults to all metrics)", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), required=False),
            openapi.Parameter('bins', openapi.IN_QUERY, description="Number of histogram bins", type=openapi.TYPE_INTEGER, default=20),
            openapi.Parameter('depth', openapi.IN_QUERY, description="Soil temperature depth (5cm, 10cm, 20cm, 25cm, 50cm)", type=openapi.TYPE_STRING, default="5cm"),
        ],
        responses={
            200: openapi.Response('Histogram data generated successfully'),
            400: openapi.Response('Bad request - invalid parameters'),
            500: openapi.Response('Internal server error')
        }
    )
    def get(self, request):
        try:
            # Get query parameters
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            metrics = request.query_params.getlist('metrics')  # List of metric names (optional, defaults to all)
            bins = request.query_params.get('bins', '20')  # Number of bins
            depth = request.query_params.get('depth', '5cm')  # For soil temperature
            
            # Validate required parameters
            if not start_date or not end_date:
                return Response({
                    'success': False,
                    'error': 'start_date and end_date are required parameters'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # If no metrics specified, use all available metrics
            if not metrics:
                metrics = ['humidity', 'temperature', 'wind_speed', 'rainfall', 'snow_depth', 'shortwave_radiation', 'atmospheric_pressure', 'soil_temperature']
            
            # Validate date format
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Invalid date format. Use YYYY-MM-DD format.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate bins parameter
            try:
                bins = int(bins)
                if bins < 1 or bins > 100:
                    return Response({
                        'success': False,
                        'error': 'bins must be between 1 and 100'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'bins must be a valid integer'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate metrics
            valid_metrics = ['humidity', 'temperature', 'wind_speed', 'rainfall', 'snow_depth', 'shortwave_radiation', 'atmospheric_pressure', 'soil_temperature']
            invalid_metrics = [m for m in metrics if m not in valid_metrics]
            if invalid_metrics:
                return Response({
                    'success': False,
                    'error': f'Invalid metrics: {", ".join(invalid_metrics)}. Valid metrics: {", ".join(valid_metrics)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate depth for soil temperature
            if 'soil_temperature' in metrics:
                valid_depths = ['5cm', '10cm', '20cm', '25cm', '50cm']
                if depth not in valid_depths:
                    return Response({
                        'success': False,
                        'error': f'Invalid depth for soil_temperature: {depth}. Valid depths: {", ".join(valid_depths)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Map metric names to database fields
            metric_fields = {
                'humidity': 'RelativeHumidity_Pct',
                'temperature': 'AirTemperature_degC',
                'wind_speed': 'WindSpeed_ms',
                'rainfall': 'Rainfall_mm',
                'snow_depth': 'SnowDepth_cm',
                'shortwave_radiation': 'ShortwaveRadiation_Wm2',
                'atmospheric_pressure': 'AtmosphericPressure_kPa',
                'soil_temperature': f'SoilTemperature_{depth}_degC'
            }
            
            # Build base queryset using Year, Month, Day fields
            start_year, start_month, start_day = start_date_obj.year, start_date_obj.month, start_date_obj.day
            end_year, end_month, end_day = end_date_obj.year, end_date_obj.month, end_date_obj.day
            
            queryset = EnvironmentalData.objects.filter(
                Q(Year__gt=start_year) |
                (Q(Year=start_year) & Q(Month__gt=start_month)) |
                (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
            ).filter(
                Q(Year__lt=end_year) |
                (Q(Year=end_year) & Q(Month__lt=end_month)) |
                (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
            )
            
            # Generate histogram data for each metric with performance optimization
            histogram_data = {}
            
            for metric in metrics:
                field_name = metric_fields[metric]
                
                # Filter out null values for this metric
                metric_queryset = queryset.filter(**{f'{field_name}__isnull': False})
                
                # Performance optimization: limit data points if too many
                total_count = metric_queryset.count()
                if total_count > 50000:  # If more than 50k data points
                    logger.warning(f"Large dataset detected for {metric}: {total_count} records. Sampling data for performance.")
                    # Sample data for better performance
                    sample_size = min(50000, total_count)
                    metric_queryset = metric_queryset.order_by('?')[:sample_size]
                elif total_count > 10000:
                    logger.warning(f"Large dataset detected for {metric}: {total_count} records. Consider using smaller date ranges.")
                
                # Generate histogram data
                histogram_data[metric] = self._get_histogram_data(metric_queryset, field_name, bins)
            
            return Response({
                'success': True,
                'data': histogram_data,
                'metadata': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'metrics': metrics,
                    'bins': bins,
                    'depth': depth if 'soil_temperature' in metrics else None
                }
            })
            
        except Exception as e:
            logger.error(f"Error in histogram API: {str(e)}")
            return Response({
                'success': False,
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_histogram_data(self, queryset, field_name: str, bins: int) -> dict:
        """Generate histogram data for a metric with performance optimization"""
        try:
            # Get all values for this metric (optimized)
            values = list(queryset.values_list(field_name, flat=True))
            
            if not values:
                return {
                    'bins': [],
                    'statistics': {
                        'mean': 0,
                        'median': 0,
                        'std_dev': 0,
                        'min': 0,
                        'max': 0,
                        'total_count': 0
                    }
                }
            
            # Performance optimization: limit data for very large datasets
            if len(values) > 100000:
                import random
                values = random.sample(values, 100000)
                logger.info(f"Sampled {len(values)} values from {field_name} for histogram calculation")
            
            # Calculate statistics using numpy (optimized)
            import numpy as np
            values_array = np.array(values, dtype=np.float64)
            
            # Use numpy's optimized functions
            stats = {
                'mean': float(np.mean(values_array)),
                'median': float(np.median(values_array)),
                'std_dev': float(np.std(values_array)),
                'min': float(np.min(values_array)),
                'max': float(np.max(values_array)),
                'total_count': len(values)
            }
            
            # Create histogram bins (optimized)
            hist, bin_edges = np.histogram(values_array, bins=bins, density=False)
            
            # Format bins data (optimized)
            bins_data = []
            total_count = stats['total_count']
            
            for i in range(len(hist)):
                bin_start = float(bin_edges[i])
                bin_end = float(bin_edges[i + 1])
                count = int(hist[i])
                percentage = (count / total_count) * 100 if total_count > 0 else 0
                
                bins_data.append({
                    'bin_start': round(bin_start, 2),
                    'bin_end': round(bin_end, 2),
                    'count': count,
                    'percentage': round(percentage, 2)
                })
            
            return {
                'bins': bins_data,
                'statistics': {
                    'mean': round(stats['mean'], 2),
                    'median': round(stats['median'], 2),
                    'std_dev': round(stats['std_dev'], 2),
                    'min': round(stats['min'], 2),
                    'max': round(stats['max'], 2),
                    'total_count': stats['total_count']
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating histogram for {field_name}: {str(e)}")
            return {
                'bins': [],
                'statistics': {
                    'mean': 0,
                    'median': 0,
                    'std_dev': 0,
                    'min': 0,
                    'max': 0,
                    'total_count': 0
                }
            } 


class CorrelationAnalysisView(APIView):
    """
    Correlation Analysis API for environmental data metrics
    
    Generates correlation matrices and pairwise correlation data for multiple environmental metrics.
    Optimized for frontend visualization with Plotly.js heatmaps and scatter plots.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Generate correlation analysis for multiple environmental metrics",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD) - defaults to 2023-01-01", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD) - defaults to 2023-12-31", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('metrics', openapi.IN_QUERY, description="List of metric names (optional, defaults to all metrics)", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), required=False),
            openapi.Parameter('correlation_method', openapi.IN_QUERY, description="Correlation method: pearson, spearman, kendall", type=openapi.TYPE_STRING, default="pearson"),
            openapi.Parameter('depth', openapi.IN_QUERY, description="Soil temperature depth (5cm, 10cm, 20cm, 25cm, 50cm)", type=openapi.TYPE_STRING, default="5cm"),
            openapi.Parameter('include_p_values', openapi.IN_QUERY, description="Include p-values in response", type=openapi.TYPE_BOOLEAN, default=True),
            openapi.Parameter('sample_size', openapi.IN_QUERY, description="Maximum sample size for analysis (default: 10000)", type=openapi.TYPE_INTEGER, default=10000),
        ],
        responses={
            200: openapi.Response(
                description="Correlation analysis data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'correlation_matrix': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER))),
                                'p_value_matrix': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER))),
                                'metric_names': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'pairwise_correlations': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'metric1': openapi.Schema(type=openapi.TYPE_STRING),
                                            'metric2': openapi.Schema(type=openapi.TYPE_STRING),
                                            'correlation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                            'p_value': openapi.Schema(type=openapi.TYPE_NUMBER),
                                            'sample_size': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        }
                                    )
                                ),
                                'statistics': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'total_records': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'valid_pairs': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'strong_correlations': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'moderate_correlations': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'weak_correlations': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                )
                            }
                        ),
                        'metadata': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            400: 'Bad Request - Invalid parameters',
            500: 'Internal Server Error'
        }
    )
    def get(self, request: Request) -> Response:
        """Get correlation analysis for multiple environmental metrics"""
        try:
            # Get query parameters
            start_date = request.query_params.get('start_date', '2023-01-01')  # Default to 2023-01-01
            end_date = request.query_params.get('end_date', '2023-12-31')      # Default to 2023-12-31
            metrics = request.query_params.getlist('metrics')  # List of metric names (optional, defaults to all)
            correlation_method = request.query_params.get('correlation_method', 'pearson').lower()
            depth = request.query_params.get('depth', '5cm')  # For soil temperature
            include_p_values = request.query_params.get('include_p_values', 'true').lower() == 'true'
            sample_size = int(request.query_params.get('sample_size', '10000'))
            
            # Validate correlation method
            valid_methods = ['pearson', 'spearman', 'kendall']
            if correlation_method not in valid_methods:
                return Response({
                    'success': False,
                    'error': f'Invalid correlation_method: {correlation_method}. Valid methods: {valid_methods}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # If no metrics specified, use all available metrics
            if not metrics:
                metrics = ['humidity', 'temperature', 'wind_speed', 'rainfall', 'snow_depth', 'shortwave_radiation', 'atmospheric_pressure', 'soil_temperature']
            
            # Validate date format
            try:
                start_year, start_month, start_day = map(int, str(start_date).split('-'))
                end_year, end_month, end_day = map(int, str(end_date).split('-'))
            except (ValueError, TypeError):
                return Response({
                    'success': False,
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Define metric field mappings
            metric_fields = {
                'humidity': 'RelativeHumidity_Pct',
                'temperature': 'AirTemperature_degC',
                'wind_speed': 'WindSpeed_ms',
                'rainfall': 'Rainfall_mm',
                'snow_depth': 'SnowDepth_cm',
                'shortwave_radiation': 'ShortwaveRadiation_Wm2',
                'atmospheric_pressure': 'AtmosphericPressure_kPa',
                'soil_temperature': self._get_soil_temperature_field(depth)
            }
            
            # Validate metrics
            invalid_metrics = [m for m in metrics if m not in metric_fields]
            if invalid_metrics:
                return Response({
                    'success': False,
                    'error': f'Invalid metrics: {invalid_metrics}. Valid metrics: {list(metric_fields.keys())}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Start with base queryset
            queryset = EnvironmentalData.objects.all()
            
            # Apply date filters
            queryset = queryset.filter(
                Q(Year__gt=start_year) |
                (Q(Year=start_year) & Q(Month__gt=start_month)) |
                (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
            ).filter(
                Q(Year__lt=end_year) |
                (Q(Year=end_year) & Q(Month__lt=end_month)) |
                (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
            )
            
            # Generate correlation analysis
            correlation_data = self._generate_correlation_analysis(
                queryset, metrics, metric_fields, correlation_method, include_p_values, sample_size
            )
            
            return Response({
                'success': True,
                'data': correlation_data,
                'metadata': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'metrics': metrics,
                    'correlation_method': correlation_method,
                    'include_p_values': include_p_values,
                    'sample_size': sample_size,
                    'depth': depth if 'soil_temperature' in metrics else None
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in CorrelationAnalysisView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve correlation analysis: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_soil_temperature_field(self, depth: str) -> str:
        """Get the appropriate soil temperature field based on depth"""
        depth_mapping = {
            '5cm': 'SoilTemperature_5cm_degC',
            '10cm': 'SoilTemperature_10cm_degC',
            '20cm': 'SoilTemperature_20cm_degC',
            '25cm': 'SoilTemperature_25cm_degC',
            '50cm': 'SoilTemperature_50cm_degC'
        }
        return depth_mapping.get(depth, 'SoilTemperature_5cm_degC')
    
    def _generate_correlation_analysis(self, queryset, metrics, metric_fields, correlation_method, include_p_values, sample_size):
        """Generate correlation analysis for the given metrics"""
        try:
            import numpy as np
            import pandas as pd
            from scipy import stats
        except ImportError:
            return {
                'correlation_matrix': [],
                'p_value_matrix': [],
                'metric_names': [],
                'pairwise_correlations': [],
                'statistics': {
                    'total_records': 0,
                    'valid_pairs': 0,
                    'strong_correlations': 0,
                    'moderate_correlations': 0,
                    'weak_correlations': 0
                }
            }
        
        try:
            # Create a dictionary to store data for each metric
            metric_data = {}
            valid_metrics = []
            
            # Collect data for each metric
            for metric in metrics:
                field_name = metric_fields[metric]
                
                # Filter out null values for this metric
                metric_queryset = queryset.filter(**{f'{field_name}__isnull': False})
                
                # Sample data if too large
                total_count = metric_queryset.count()
                if total_count > sample_size:
                    logger.info(f"Sampling {sample_size} records from {total_count} for {metric}")
                    # Use random sampling for better performance
                    metric_queryset = metric_queryset.order_by('?')[:sample_size]
                
                # Get values
                values = list(metric_queryset.values_list(field_name, flat=True))
                
                if len(values) > 0:
                    metric_data[metric] = values
                    valid_metrics.append(metric)
            
            if len(valid_metrics) < 2:
                return {
                    'correlation_matrix': [],
                    'p_value_matrix': [],
                    'metric_names': valid_metrics,
                    'pairwise_correlations': [],
                    'statistics': {
                        'total_records': 0,
                        'valid_pairs': 0,
                        'strong_correlations': 0,
                        'moderate_correlations': 0,
                        'weak_correlations': 0
                    }
                }
            
            # Create DataFrame for correlation analysis
            df_data = {}
            min_length = float('inf')
            
            # Find the minimum length to align all metrics
            for metric in valid_metrics:
                min_length = min(min_length, len(metric_data[metric]))
            
            # Align all metrics to the same length (take first min_length values)
            for metric in valid_metrics:
                df_data[metric] = metric_data[metric][:min_length]
            
            df = pd.DataFrame(df_data)
            
            # Calculate correlation matrix
            if correlation_method == 'pearson':
                corr_matrix = df.corr(method='pearson')
            elif correlation_method == 'spearman':
                corr_matrix = df.corr(method='spearman')
            else:  # kendall
                corr_matrix = df.corr(method='kendall')
            
            # Calculate p-values if requested
            p_value_matrix = None
            if include_p_values:
                p_value_matrix = np.zeros_like(corr_matrix.values)
                for i, metric1 in enumerate(valid_metrics):
                    for j, metric2 in enumerate(valid_metrics):
                        if i == j:
                            p_value_matrix[i, j] = 0.0  # Perfect correlation with self
                        else:
                            # Calculate p-value for correlation
                            if correlation_method == 'pearson':
                                corr, p_val = stats.pearsonr(df[metric1], df[metric2])
                            elif correlation_method == 'spearman':
                                corr, p_val = stats.spearmanr(df[metric1], df[metric2])
                            else:  # kendall
                                corr, p_val = stats.kendalltau(df[metric1], df[metric2])
                            p_value_matrix[i, j] = p_val
            
            # Generate pairwise correlations
            pairwise_correlations = []
            strong_correlations = 0
            moderate_correlations = 0
            weak_correlations = 0
            
            for i, metric1 in enumerate(valid_metrics):
                for j, metric2 in enumerate(valid_metrics):
                    if i < j:  # Only include each pair once
                        correlation = corr_matrix.iloc[i, j]
                        p_value = p_value_matrix[i, j] if p_value_matrix is not None else None
                        
                        # Categorize correlation strength
                        abs_corr = abs(correlation)
                        if abs_corr >= 0.7:
                            strong_correlations += 1
                        elif abs_corr >= 0.3:
                            moderate_correlations += 1
                        else:
                            weak_correlations += 1
                        
                        pairwise_correlations.append({
                            'metric1': metric1,
                            'metric2': metric2,
                            'correlation': round(correlation, 4),
                            'p_value': round(p_value, 6) if p_value is not None else None,
                            'sample_size': min_length
                        })
            
            # Sort pairwise correlations by absolute correlation value
            pairwise_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            return {
                'correlation_matrix': corr_matrix.values.tolist(),
                'p_value_matrix': p_value_matrix.tolist() if p_value_matrix is not None else None,
                'metric_names': valid_metrics,
                'pairwise_correlations': pairwise_correlations,
                'statistics': {
                    'total_records': min_length,
                    'valid_pairs': len(pairwise_correlations),
                    'strong_correlations': strong_correlations,
                    'moderate_correlations': moderate_correlations,
                    'weak_correlations': weak_correlations
                }
            }
            
        except Exception as e:
            logger.error(f"Error in correlation analysis: {str(e)}")
            return {
                'correlation_matrix': [],
                'p_value_matrix': [],
                'metric_names': [],
                'pairwise_correlations': [],
                'statistics': {
                    'total_records': 0,
                    'valid_pairs': 0,
                    'strong_correlations': 0,
                    'moderate_correlations': 0,
                    'weak_correlations': 0
                }
            } 