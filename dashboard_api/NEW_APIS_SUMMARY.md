# New Environmental Data API Endpoints

## Overview
Four new API endpoints have been added to provide averaged environmental data for dashboard visualizations:

1. **Shortwave Radiation API**
2. **Wind Speed API** 
3. **Atmospheric Pressure API**
4. **Multi-Metric Boxplot API**

## API Endpoints

### 1. Shortwave Radiation API
- **Endpoint**: `GET /api/charts/shortwave-radiation/`
- **Field**: `ShortwaveRadiation_Wm2`
- **Unit**: `W/m²`
- **Returns**: `avg`, `max`, `min` values

### 2. Wind Speed API
- **Endpoint**: `GET /api/charts/wind-speed/`
- **Field**: `WindSpeed_ms`
- **Unit**: `m/s`
- **Returns**: `avg`, `max`, `min` values

### 3. Atmospheric Pressure API
- **Endpoint**: `GET /api/charts/atmospheric-pressure/`
- **Field**: `AtmosphericPressure_kPa`
- **Unit**: `kPa`
- **Returns**: `avg`, `max`, `min` values

### 4. Multi-Metric Boxplot API
- **Endpoint**: `GET /api/charts/statistical/boxplot/`
- **Purpose**: Generate boxplot data for multiple environmental metrics across different time periods
- **Returns**: Statistical measures (min, q1, median, q3, max, outliers, count) for each metric and time period

## Query Parameters

### Standard Chart APIs (1-3)
All standard chart endpoints support the following query parameters:

- `year` (optional): Filter by specific year (defaults to latest year)
- `month` (optional): Filter by specific month
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `group_by` (optional): Time grouping (`hour`, `day`, `week`, `month`, default: `day`)

### Multi-Metric Boxplot API (4)
The boxplot API supports the following query parameters:

- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `metrics` (required): List of metric names to analyze
- `group_by` (optional): Time period grouping (`month`, `season`, `year`, `day`, default: `month`)
- `include_outliers` (optional): Include outlier data (default: `true`)
- `depth` (optional): Soil temperature depth for soil_temperature metric (default: `5cm`)

## Response Format

### Standard Chart APIs (1-3)
```json
{
    "success": true,
    "data": [
        {
            "period": "2023-06-15",
            "avg": 25.5,
            "max": 30.2,
            "min": 20.1
        }
    ],
    "unit": "W/m²"
}
```

### Multi-Metric Boxplot API (4)
```json
{
    "success": true,
    "data": {
        "temperature": [
            {
                "period": "January",
                "period_code": 1,
                "statistics": {
                    "min": 8.0,
                    "q1": 9.0,
                    "median": 10.0,
                    "q3": 11.0,
                    "max": 12.0,
                    "outliers": [7.5, 13.2],
                    "count": 31
                }
            }
        ]
    },
    "metadata": {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "metrics": ["temperature"],
        "group_by": "month",
        "include_outliers": true,
        "depth": null
    }
}
```

## Example Usage

### Standard Chart APIs (1-3)
```bash
# Get shortwave radiation data for latest year
GET /api/charts/shortwave-radiation/

# Get wind speed data for 2023
GET /api/charts/wind-speed/?year=2023

# Get atmospheric pressure data for specific month
GET /api/charts/atmospheric-pressure/?year=2023&month=6
```

### Multi-Metric Boxplot API (4)
```bash
# Basic monthly boxplot for temperature and humidity
GET /api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=temperature&metrics=humidity&group_by=month

# Seasonal analysis with outliers excluded
GET /api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=temperature&metrics=wind_speed&group_by=season&include_outliers=false

# Soil temperature at different depths
GET /api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=soil_temperature&depth=20cm&group_by=month
```

### Time Grouping
```bash
# Hourly grouping
GET /api/charts/wind-speed/?group_by=hour&year=2023

# Weekly grouping
GET /api/charts/atmospheric-pressure/?group_by=week&year=2023

# Monthly grouping
GET /api/charts/shortwave-radiation/?group_by=month&year=2023
```

### Date Range
```bash
# Custom date range with daily grouping
GET /api/charts/shortwave-radiation/?start_date=2023-01-01&end_date=2023-06-30&group_by=day
```

## Files Modified

1. **`core/averaged_chart_views.py`**: Added four new view classes (including MultiMetricBoxplotView)
2. **`core/views.py`**: Updated imports and exports
3. **`core/urls.py`**: Added URL patterns
4. **`core/serializers.py`**: Added boxplot serializers
5. **`tests/test_averaged_chart_apis.py`**: Added comprehensive tests
6. **`tests/test_new_apis.py`**: Created simple test script
7. **`tests/test_boxplot_api.py`**: Added comprehensive boxplot API tests
8. **`docs/BOXPLOT_API.md`**: Created detailed documentation

## Testing

Run the test script to verify the APIs are working:

```bash
cd tests
python test_new_apis.py
```

Or run the comprehensive test suite:

```bash
cd tests
python test_averaged_chart_apis.py
```

## Features

### Standard Chart APIs (1-3)
- ✅ Same structure as existing chart APIs
- ✅ Time grouping (hour, day, week, month)
- ✅ Date filtering and ranges
- ✅ Default to latest year if no filters
- ✅ Error handling and logging
- ✅ Consistent response format
- ✅ Appropriate units for each metric
- ✅ Comprehensive test coverage

### Multi-Metric Boxplot API (4)
- ✅ Statistical analysis with quartiles, median, and outliers
- ✅ Multiple time period groupings (month, season, year, day)
- ✅ Support for all environmental metrics
- ✅ Configurable outlier inclusion/exclusion
- ✅ Soil temperature depth selection
- ✅ Comprehensive error handling and validation
- ✅ Swagger documentation
- ✅ Detailed test coverage
- ✅ Professional documentation

## Notes

### Standard Chart APIs (1-3)
- The APIs follow the same pattern as existing snow depth, rainfall, and soil temperature APIs
- All endpoints use `AllowAny` permissions for public access
- Data is aggregated using Django ORM functions (Avg, Max, Min)
- Weekly grouping returns a `week` field instead of `period` for week numbers
- Rainfall API also includes a `total` field for cumulative values

### Multi-Metric Boxplot API (4)
- Uses standard 1.5 × IQR method for outlier detection
- Supports all environmental metrics: humidity, temperature, wind_speed, rainfall, snow_depth, shortwave_radiation, atmospheric_pressure, soil_temperature
- Soil temperature supports multiple depths: 5cm, 10cm, 20cm, 25cm, 50cm
- All numerical values are rounded to 2 decimal places
- Includes data point counts for quality assessment
- Comprehensive validation for all input parameters 