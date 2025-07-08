"""
Averaged chart views module for environmental data visualizations
Returns aggregated values over time periods (hourly, daily, monthly)
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q, Max, Avg, Min, Sum, Count
from django.db.models.functions import ExtractWeek
from django.db.models.functions import Substr

from .models import EnvironmentalData

# Set up logger
logger = logging.getLogger(__name__)


class AveragedSnowDepthView(APIView):
    """Averaged snow depth data for charts and dashboards"""
    permission_classes = [AllowAny]
    
    def get(self, request):
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
                aggregated_data = queryset.values('Month').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Month']:02d}",
                        'avg': round(record['avg_snow_depth'], 2),
                        'max': record['max_snow_depth'],
                        'min': record['min_snow_depth']
                    })
                    
            elif group_by == 'week':
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('week').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"W{record['week']:02d}",
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
    permission_classes = [AllowAny]
    
    def get(self, request):
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
                aggregated_data = queryset.values('Month').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Month']:02d}",
                        'avg': round(record['avg_rainfall'], 2),
                        'total': round(record['total_rainfall'], 2),
                        'max': record['max_rainfall']
                    })
                    
            elif group_by == 'week':
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('week').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Year', 'week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"W{record['week']:02d}",
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
    permission_classes = [AllowAny]
    
    def get(self, request):
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
                aggregated_data = queryset.values('Month').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Month']:02d}",
                        'avg': round(record['avg_temp'], 2),
                        'max': record['max_temp'],
                        'min': record['min_temp']
                    })
                    
            elif group_by == 'week':
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('week').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"W{record['week']:02d}",
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
    permission_classes = [AllowAny]
    
    def get(self, request):
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
                aggregated_data = queryset.values('Month').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Month']:02d}",
                        'avg': round(record['avg_humidity'], 2),
                        'max': record['max_humidity'],
                        'min': record['min_humidity']
                    })
                    
            elif group_by == 'week':
                # For weekly: return exactly 52 data points (1-52 weeks) with calculated averages
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('week').annotate(
                    avg_humidity=Avg('RelativeHumidity_Pct'),
                    max_humidity=Max('RelativeHumidity_Pct'),
                    min_humidity=Min('RelativeHumidity_Pct'),
                    data_points=Count('id')
                ).order_by('week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"W{record['week']:02d}",
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