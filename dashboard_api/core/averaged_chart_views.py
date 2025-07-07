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
from django.db.models.functions import ExtractHour, ExtractWeek

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
                # Group by year, month, day, and hour
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    hour=ExtractHour('Time')
                ).values('Year', 'Month', 'Day', 'hour').annotate(
                    avg_snow_depth=Avg('SnowDepth_cm'),
                    max_snow_depth=Max('SnowDepth_cm'),
                    min_snow_depth=Min('SnowDepth_cm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day', 'hour')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d} {record['hour']:02d}:00",
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'hour': record['hour'],
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record['Day'],
                        'avg_snow_depth_cm': round(record['avg_snow_depth'], 2),
                        'max_snow_depth_cm': record['max_snow_depth'],
                        'min_snow_depth_cm': record['min_snow_depth'],
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'month':
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
                # Group by year and week
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
                        'day': record['Day'],
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
                # Group by year, month, day, and hour
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    hour=ExtractHour('Time')
                ).values('Year', 'Month', 'Day', 'hour').annotate(
                    avg_rainfall=Avg('Rainfall_mm'),
                    total_rainfall=Sum('Rainfall_mm'),
                    max_rainfall=Max('Rainfall_mm'),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day', 'hour')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d} {record['hour']:02d}:00",
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'hour': record['hour'],
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record['Day'],
                        'avg_rainfall_mm': round(record['avg_rainfall'], 2),
                        'total_rainfall_mm': round(record['total_rainfall'], 2),
                        'max_rainfall_mm': record['max_rainfall'],
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'month':
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
                # Group by year, month, day, and hour
                aggregated_data = queryset.values('Year', 'Month', 'Day').annotate(
                    hour=ExtractHour('Time')
                ).values('Year', 'Month', 'Day', 'hour').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Year', 'Month', 'Day', 'hour')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d} {record['hour']:02d}:00",
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'hour': record['hour'],
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record['Day'],
                        'avg_soil_temp_degc': round(record['avg_temp'], 2),
                        'max_soil_temp_degc': record['max_temp'],
                        'min_soil_temp_degc': record['min_temp'],
                        'depth': depth,
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'month':
                # Group by year and month
                aggregated_data = queryset.values('Year', 'Month').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Year', 'Month')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-{record['Month']:02d}",
                        'date': f"{record['Year']}-{record['Month']:02d}-01",
                        'year': record['Year'],
                        'month': record['Month'],
                        'avg_soil_temp_degc': round(record['avg_temp'], 2),
                        'max_soil_temp_degc': record['max_temp'],
                        'min_soil_temp_degc': record['min_temp'],
                        'depth': depth,
                        'data_points': record['data_points']
                    })
                    
            elif group_by == 'week':
                # Group by year and week
                aggregated_data = queryset.annotate(
                    week=ExtractWeek('Year', 'Month', 'Day')
                ).values('Year', 'week').annotate(
                    avg_temp=Avg(field_name),
                    max_temp=Max(field_name),
                    min_temp=Min(field_name),
                    data_points=Count('id')
                ).order_by('Year', 'week')
                
                chart_data = []
                for record in aggregated_data:
                    chart_data.append({
                        'period': f"{record['Year']}-W{record['week']:02d}",
                        'date': f"{record['Year']}-01-01",  # Simplified
                        'year': record['Year'],
                        'week': record['week'],
                        'avg_soil_temp_degc': round(record['avg_temp'], 2),
                        'max_soil_temp_degc': record['max_temp'],
                        'min_soil_temp_degc': record['min_temp'],
                        'depth': depth,
                        'data_points': record['data_points']
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
                        'date': f"{record['Year']}-{record['Month']:02d}-{record['Day']:02d}",
                        'year': record['Year'],
                        'month': record['Month'],
                        'day': record['Day'],
                        'avg_soil_temp_degc': round(record['avg_temp'], 2),
                        'max_soil_temp_degc': record['max_temp'],
                        'min_soil_temp_degc': record['min_temp'],
                        'depth': depth,
                        'data_points': record['data_points']
                    })
            
            return Response({
                'success': True,
                'data': chart_data,
                'total_periods': len(chart_data),
                'metric': 'soil_temperature',
                'unit': '°C',
                'depth': depth,
                'aggregation': 'average',
                'group_by': group_by,
                'filters_applied': {
                    'year': year,
                    'month': month,
                    'start_date': start_date,
                    'end_date': end_date,
                    'depth': depth,
                    'group_by': group_by
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in AveragedSoilTemperatureView: {str(e)}")
            return Response({
                'success': False,
                'error': f'Failed to retrieve averaged soil temperature data: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 