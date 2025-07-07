# Separated Chart APIs Documentation

## Overview

The environmental data chart APIs have been separated into two distinct categories to optimize for different use cases:

1. **Raw Data APIs** - For detailed analysis and data exploration
2. **Averaged Chart APIs** - For visualizations and dashboards

## 1. Raw Data APIs

### Purpose
- Return individual data points for detailed analysis
- Include performance limits to prevent overwhelming responses
- Suitable for data exploration, debugging, and detailed investigations

### Base Path
```
/api/raw/
```

### Available Endpoints

#### 1.1 Raw Snow Depth Data
```
GET /api/raw/snow-depth/
```

**Parameters:**
- `year` (optional): Filter by specific year
- `month` (optional): Filter by specific month
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `limit` (optional): Maximum data points (default: 1000, max: 10,000)

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2023-01-15 14:30:00",
      "date": "2023-01-15",
      "time": "14:30:00",
      "snow_depth_cm": 25.5,
      "year": 2023,
      "month": 1,
      "day": 15
    }
  ],
  "total_points": 1000,
  "metric": "snow_depth_cm",
  "unit": "cm",
  "data_type": "raw_points",
  "filters_applied": {
    "year": "2023",
    "limit": 1000
  }
}
```

#### 1.2 Raw Rainfall Data
```
GET /api/raw/rainfall/
```

**Parameters:**
- Same as snow depth, plus:
- `limit` (optional): Maximum data points (default: 1000, max: 10,000)

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2023-01-15 14:30:00",
      "date": "2023-01-15",
      "time": "14:30:00",
      "rainfall_mm": 2.5,
      "total_precipitation_mm": 15.2,
      "year": 2023,
      "month": 1,
      "day": 15
    }
  ],
  "total_points": 500,
  "metric": "rainfall",
  "unit": "mm",
  "data_type": "raw_points"
}
```

#### 1.3 Raw Soil Temperature Data
```
GET /api/raw/soil-temperature/
```

**Parameters:**
- Same as above, plus:
- `depth` (optional): Soil depth (5cm, 10cm, 20cm, 25cm, 50cm, default: 5cm)

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2023-01-15 14:30:00",
      "date": "2023-01-15",
      "time": "14:30:00",
      "soil_temp_degc": 8.5,
      "depth": "20cm",
      "year": 2023,
      "month": 1,
      "day": 15
    }
  ],
  "total_points": 750,
  "metric": "soil_temperature",
  "unit": "°C",
  "depth": "20cm",
  "data_type": "raw_points"
}
```

#### 1.4 Raw Multi-Metric Data
```
GET /api/raw/multi-metric/
```

**Parameters:**
- Same as above, plus:
- `metrics` (optional): Comma-separated metric names (default: air_temp,humidity,wind_speed)

**Available Metrics:**
- `air_temp` - Air temperature
- `humidity` - Relative humidity
- `wind_speed` - Wind speed
- `snow_depth` - Snow depth
- `rainfall` - Rainfall
- `soil_temp_5cm`, `soil_temp_10cm`, etc. - Soil temperature at different depths
- `atmospheric_pressure` - Atmospheric pressure
- `solar_radiation` - Solar radiation

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2023-01-15 14:30:00",
      "date": "2023-01-15",
      "time": "14:30:00",
      "air_temp": 12.5,
      "humidity": 65.2,
      "year": 2023,
      "month": 1,
      "day": 15
    }
  ],
  "total_points": 250,
  "metrics": ["air_temp", "humidity"],
  "data_type": "raw_points"
}
```

## 2. Averaged Chart APIs

### Purpose
- Return aggregated values over time periods for charting
- Optimized for frontend visualizations
- No performance limits (data is pre-aggregated)
- Suitable for dashboards and trend analysis

### Base Path
```
/api/charts/
```

### Available Endpoints

#### 2.1 Averaged Snow Depth Chart
```
GET /api/charts/snow-depth/
```

**Parameters:**
- `year` (optional): Filter by specific year
- `month` (optional): Filter by specific month
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `group_by` (optional): Time grouping (hour, day, week, month, default: day)

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "period": "2023-01-15",
      "date": "2023-01-15",
      "year": 2023,
      "month": 1,
      "day": 15,
      "avg_snow_depth_cm": 24.8,
      "max_snow_depth_cm": 28.5,
      "min_snow_depth_cm": 21.2,
      "data_points": 24
    }
  ],
  "total_periods": 365,
  "metric": "snow_depth_cm",
  "unit": "cm",
  "aggregation": "average",
  "group_by": "day"
}
```

#### 2.2 Averaged Rainfall Chart
```
GET /api/charts/rainfall/
```

**Parameters:**
- Same as snow depth

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "period": "2023-01-15",
      "date": "2023-01-15",
      "year": 2023,
      "month": 1,
      "day": 15,
      "avg_rainfall_mm": 1.8,
      "total_rainfall_mm": 43.2,
      "max_rainfall_mm": 5.5,
      "data_points": 24
    }
  ],
  "total_periods": 365,
  "metric": "rainfall",
  "unit": "mm",
  "aggregation": "average",
  "group_by": "day"
}
```

#### 2.3 Averaged Soil Temperature Chart
```
GET /api/charts/soil-temperature/
```

**Parameters:**
- Same as above, plus:
- `depth` (optional): Soil depth (5cm, 10cm, 20cm, 25cm, 50cm, default: 5cm)

**Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "period": "2023-01-15",
      "date": "2023-01-15",
      "year": 2023,
      "month": 1,
      "day": 15,
      "avg_soil_temp_degc": 8.2,
      "max_soil_temp_degc": 12.5,
      "min_soil_temp_degc": 4.8,
      "depth": "20cm",
      "data_points": 24
    }
  ],
  "total_periods": 365,
  "metric": "soil_temperature",
  "unit": "°C",
  "depth": "20cm",
  "aggregation": "average",
  "group_by": "day"
}
```

## 3. Key Differences

| Feature | Raw Data APIs | Averaged Chart APIs |
|---------|---------------|-------------------|
| **Data Type** | Individual data points | Aggregated values |
| **Performance** | Limited by `limit` parameter | No limits, optimized |
| **Use Case** | Detailed analysis, debugging | Charts, dashboards |
| **Response Size** | Can be large (up to 10K points) | Compact, aggregated |
| **Time Grouping** | None (raw timestamps) | Hour, day, week, month |
| **Calculations** | None (raw values) | Average, max, min, total |
| **Default Behavior** | Latest year if no filters | Latest year if no filters |

## 4. Performance Considerations

### Raw Data APIs
- **Limit Enforcement**: Maximum 10,000 data points per request
- **Use Cases**: Data exploration, debugging, detailed analysis
- **Recommendation**: Use date filters to reduce data size

### Averaged Chart APIs
- **No Limits**: Data is pre-aggregated at the database level
- **Use Cases**: Frontend charts, dashboards, trend analysis
- **Performance**: Much faster for large datasets

## 5. Example Usage Scenarios

### Scenario 1: Data Exploration
```bash
# Get raw data for detailed analysis
GET /api/raw/snow-depth/?limit=1000&year=2023&month=1
```

### Scenario 2: Daily Chart
```bash
# Get daily averages for line chart
GET /api/charts/snow-depth/?group_by=day&year=2023
```

### Scenario 3: Monthly Dashboard
```bash
# Get monthly totals for dashboard
GET /api/charts/rainfall/?group_by=month&year=2023
```

### Scenario 4: Multi-Metric Analysis
```bash
# Get multiple metrics for correlation analysis
GET /api/raw/multi-metric/?metrics=air_temp,humidity,wind_speed&limit=500&year=2023
```

## 6. Error Handling

Both API types return consistent error responses:

```json
{
  "success": false,
  "error": "Error description"
}
```

Common error scenarios:
- Invalid date formats
- Exceeding limit maximums
- Invalid depth or metric parameters
- Database connection issues

## 7. Testing

Use the provided test script to verify API functionality:

```bash
cd AMOD5640Project/dashboard_api/tests/
python test_separated_apis.py
```

The test script covers:
- Raw data API functionality
- Averaged chart API functionality
- Performance comparisons
- Data structure validation
- Error handling

## 8. Migration Notes

If you were using the previous chart APIs:
- Raw data needs: Use `/api/raw/` endpoints
- Chart visualizations: Use `/api/charts/` endpoints
- The old chart endpoints have been replaced with the new separated structure
- All existing functionality is preserved with improved performance 