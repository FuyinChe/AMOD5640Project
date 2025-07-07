# Monthly Summary API Documentation

## Overview

The Monthly Summary API provides statistical aggregations of environmental data grouped by month, similar to pandas `df.describe()` functionality. This API is designed to give users quick insights into environmental trends and patterns over time.

## Endpoint

```
GET /api/monthly-summary/
```

## Features

- **Monthly Aggregation**: Groups environmental data by year and month
- **Statistical Summaries**: Provides max, min, mean, and standard deviation for key metrics
- **Flexible Filtering**: Supports filtering by year and/or month
- **Comprehensive Metrics**: Covers all major environmental parameters

## Query Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `year` | integer | No | Filter by specific year | `2023` |
| `month` | integer | No | Filter by specific month (1-12) | `6` |
| `start_date` | string | No | Start date in YYYY-MM-DD format | `2023-01-01` |
| `end_date` | string | No | End date in YYYY-MM-DD format | `2023-12-31` |

## Default Behavior

If no query parameters are provided, the API automatically returns data for the **latest year** available in the database. This provides users with the most recent data by default.

## Response Format

### Success Response (200 OK)

```json
{
    "success": true,
    "data": [
        {
            "year": 2023,
            "month": 6,
            "month_name": "June",
            "record_count": 1440,
            
            "air_temperature_max": 25.5,
            "air_temperature_min": 10.2,
            "air_temperature_mean": 18.3,
            "air_temperature_std": 4.2,
            
            "relative_humidity_max": 95.0,
            "relative_humidity_min": 45.0,
            "relative_humidity_mean": 75.2,
            "relative_humidity_std": 12.1,
            
            "shortwave_radiation_max": 850.0,
            "shortwave_radiation_min": 0.0,
            "shortwave_radiation_mean": 425.3,
            "shortwave_radiation_std": 250.1,
            
            "rainfall_total": 125.5,
            "rainfall_max": 15.2,
            "rainfall_mean": 2.8,
            "rainfall_std": 3.1,
            
            "soil_temp_5cm_max": 22.1,
            "soil_temp_5cm_min": 8.5,
            "soil_temp_5cm_mean": 15.3,
            "soil_temp_5cm_std": 3.8,
            
            "wind_speed_max": 12.5,
            "wind_speed_min": 0.1,
            "wind_speed_mean": 3.2,
            "wind_speed_std": 2.1,
            
            "snow_depth_max": 0.0,
            "snow_depth_min": 0.0,
            "snow_depth_mean": 0.0,
            "snow_depth_std": 0.0,
            
            "atmospheric_pressure_max": 102.5,
            "atmospheric_pressure_min": 98.2,
            "atmospheric_pressure_mean": 100.8,
            "atmospheric_pressure_std": 1.2
        }
    ],
    "total_months": 1,
    "filters_applied": {
        "year": "2023",
        "month": "6",
        "start_date": null,
        "end_date": null
    },
    "default_behavior": null
}
```

### Error Response (500 Internal Server Error)

```json
{
    "success": false,
    "error": "Failed to retrieve monthly summary: [error details]"
}
```

## Metrics Included

### 1. Air Temperature (°C)
- **Max**: Highest recorded temperature
- **Min**: Lowest recorded temperature  
- **Mean**: Average temperature
- **Std**: Standard deviation

### 2. Relative Humidity (%)
- **Max**: Highest humidity level
- **Min**: Lowest humidity level
- **Mean**: Average humidity
- **Std**: Standard deviation

### 3. Shortwave Radiation (W/m²)
- **Max**: Peak solar radiation
- **Min**: Minimum solar radiation
- **Mean**: Average solar radiation
- **Std**: Standard deviation

### 4. Rainfall (mm)
- **Total**: Sum of all rainfall for the month
- **Max**: Highest single rainfall event
- **Mean**: Average rainfall per measurement
- **Std**: Standard deviation

### 5. Soil Temperature at 5cm (°C)
- **Max**: Highest soil temperature
- **Min**: Lowest soil temperature
- **Mean**: Average soil temperature
- **Std**: Standard deviation

### 6. Wind Speed (m/s)
- **Max**: Peak wind speed
- **Min**: Minimum wind speed
- **Mean**: Average wind speed
- **Std**: Standard deviation

### 7. Snow Depth (cm)
- **Max**: Maximum snow depth
- **Min**: Minimum snow depth
- **Mean**: Average snow depth
- **Std**: Standard deviation

### 8. Atmospheric Pressure (kPa)
- **Max**: Highest atmospheric pressure
- **Min**: Lowest atmospheric pressure
- **Mean**: Average atmospheric pressure
- **Std**: Standard deviation

## Usage Examples

### 1. Get Latest Year Data (Default)
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/"
```

### 2. Filter by Specific Year
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?year=2023"
```

### 3. Filter by Specific Month (Across All Years)
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?month=6"
```

### 4. Filter by Year and Month
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?year=2023&month=6"
```

### 5. Filter by Date Range
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?start_date=2023-01-01&end_date=2023-06-30"
```

### 6. Filter from Start Date
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?start_date=2023-01-01"
```

### 7. Filter until End Date
```bash
curl -X GET "http://localhost:8000/api/monthly-summary/?end_date=2023-12-31"
```

### 5. Python Example
```python
import requests

# Get latest year data (default)
response = requests.get("http://localhost:8000/api/monthly-summary/")
data = response.json()

# Get June 2023 data
response = requests.get("http://localhost:8000/api/monthly-summary/?year=2023&month=6")
june_data = response.json()

# Get data within date range
response = requests.get("http://localhost:8000/api/monthly-summary/?start_date=2023-01-01&end_date=2023-06-30")
range_data = response.json()

# Access specific metrics
if june_data['data']:
    june_summary = june_data['data'][0]
    print(f"June 2023 Average Temperature: {june_summary['air_temperature_mean']}°C")
    print(f"June 2023 Total Rainfall: {june_summary['rainfall_total']}mm")

# Check default behavior
if data.get('default_behavior'):
    print(f"Default behavior: {data['default_behavior']}")
```

## Data Processing Notes

- **Null Values**: Fields with no data will return `null`
- **Aggregation**: All statistics are calculated using Django's ORM aggregation functions
- **Ordering**: Results are ordered by year and month (ascending)
- **Performance**: The API uses database-level aggregations for optimal performance
- **Date Range Filtering**: Uses efficient database queries with proper date comparison logic
- **Default Behavior**: Automatically detects and returns the latest year's data when no filters are applied

## Testing

A test script is provided at `test_monthly_summary.py` to verify the API functionality:

```bash
cd AMOD5640Project/dashboard_api
python test_monthly_summary.py
```

## Implementation Details

### Database Queries
The API uses Django's `values()` and `annotate()` methods to perform efficient database-level aggregations:

```python
monthly_data = queryset.values('Year', 'Month').annotate(
    record_count=Count('id'),
    air_temperature_max=Max('AirTemperature_degC'),
    air_temperature_min=Min('AirTemperature_degC'),
    air_temperature_mean=Avg('AirTemperature_degC'),
    air_temperature_std=StdDev('AirTemperature_degC'),
    # ... other aggregations
).order_by('Year', 'Month')
```

### Date Range Filtering
The API implements sophisticated date range filtering using Django's Q objects for complex queries:

```python
# Start date filtering
queryset = queryset.filter(
    Q(Year__gt=start_year) |
    (Q(Year=start_year) & Q(Month__gt=start_month)) |
    (Q(Year=start_year) & Q(Month=start_month) & Q(Day__gte=start_day))
)

# End date filtering
queryset = queryset.filter(
    Q(Year__lt=end_year) |
    (Q(Year=end_year) & Q(Month__lt=end_month)) |
    (Q(Year=end_year) & Q(Month=end_month) & Q(Day__lte=end_day))
)
```

### Default Behavior
When no filters are provided, the API automatically detects the latest year:

```python
if not any([year, month, start_date, end_date]):
    latest_year = EnvironmentalData.objects.aggregate(Max('Year'))['Year__max']
    if latest_year:
        queryset = queryset.filter(Year=latest_year)
```

### Serialization
The response is serialized using a custom `MonthlySummarySerializer` that handles:
- Data type validation
- Null value handling
- Month name conversion
- Response formatting

## Future Enhancements

Potential improvements for future versions:
- Additional statistical measures (median, percentiles)
- Seasonal aggregations
- Custom date range filtering
- Export functionality (CSV, Excel)
- Caching for improved performance
- Additional environmental metrics 