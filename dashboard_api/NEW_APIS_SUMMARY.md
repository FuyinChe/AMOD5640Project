# New Environmental Data API Endpoints

## Overview
Three new API endpoints have been added to provide averaged environmental data for dashboard visualizations:

1. **Shortwave Radiation API**
2. **Wind Speed API** 
3. **Atmospheric Pressure API**

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

## Query Parameters

All endpoints support the following query parameters:

- `year` (optional): Filter by specific year (defaults to latest year)
- `month` (optional): Filter by specific month
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `group_by` (optional): Time grouping (`hour`, `day`, `week`, `month`, default: `day`)

## Response Format

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

## Example Usage

### Basic Usage
```bash
# Get shortwave radiation data for latest year
GET /api/charts/shortwave-radiation/

# Get wind speed data for 2023
GET /api/charts/wind-speed/?year=2023

# Get atmospheric pressure data for specific month
GET /api/charts/atmospheric-pressure/?year=2023&month=6
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

1. **`core/averaged_chart_views.py`**: Added three new view classes
2. **`core/views.py`**: Updated imports and exports
3. **`core/urls.py`**: Added URL patterns
4. **`tests/test_averaged_chart_apis.py`**: Added comprehensive tests
5. **`tests/test_new_apis.py`**: Created simple test script

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

- ✅ Same structure as existing chart APIs
- ✅ Time grouping (hour, day, week, month)
- ✅ Date filtering and ranges
- ✅ Default to latest year if no filters
- ✅ Error handling and logging
- ✅ Consistent response format
- ✅ Appropriate units for each metric
- ✅ Comprehensive test coverage

## Notes

- The APIs follow the same pattern as existing snow depth, rainfall, and soil temperature APIs
- All endpoints use `AllowAny` permissions for public access
- Data is aggregated using Django ORM functions (Avg, Max, Min)
- Weekly grouping returns a `week` field instead of `period` for week numbers
- Rainfall API also includes a `total` field for cumulative values 