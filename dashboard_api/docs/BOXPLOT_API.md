# Multi-Metric Boxplot API Documentation

## Overview

The Multi-Metric Boxplot API provides statistical analysis capabilities for environmental data across different time periods. It generates boxplot data that includes quartiles, median, outliers, and other statistical measures for multiple environmental metrics.

## Endpoint

```
GET /api/charts/statistical/boxplot/
```

## Purpose

Generate boxplot data for multiple environmental metrics across different time periods for statistical analysis and visualization.

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | Yes | - | Start date in ISO format (YYYY-MM-DD) |
| `end_date` | string | Yes | - | End date in ISO format (YYYY-MM-DD) |
| `metrics` | array | No | All metrics | List of metric names to analyze (optional) |
| `include_outliers` | boolean | No | true | Whether to include outlier data in statistics |
| `depth` | string | No | "5cm" | Soil temperature depth (only for soil_temperature metric) |

### Available Metrics

- `humidity` - Relative humidity percentage
- `temperature` - Air temperature in degrees Celsius
- `wind_speed` - Wind speed in meters per second
- `rainfall` - Rainfall in millimeters
- `snow_depth` - Snow depth in centimeters
- `shortwave_radiation` - Shortwave radiation in W/m²
- `atmospheric_pressure` - Atmospheric pressure in kPa
- `soil_temperature` - Soil temperature in degrees Celsius (requires depth parameter)

### Processing Method

The API processes the **entire date range as one dataset** for maximum performance and simplicity. This provides overall statistical measures for the specified period without time-based grouping.

### Soil Temperature Depths

- `5cm` - 5 centimeters depth
- `10cm` - 10 centimeters depth
- `20cm` - 20 centimeters depth
- `25cm` - 25 centimeters depth
- `50cm` - 50 centimeters depth

## Response Format

### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "temperature": [
      {
        "period": "Overall",
        "period_code": "overall",
        "statistics": {
          "min": 8.0,
          "q1": 9.0,
          "median": 10.0,
          "q3": 11.0,
          "max": 12.0,
          "outliers": [7.5, 13.2],
          "count": 365
        }
      }
    ],
    "humidity": [
      {
        "period": "Overall",
        "period_code": "overall",
        "statistics": {
          "min": 45.0,
          "q1": 55.0,
          "median": 60.0,
          "q3": 65.0,
          "max": 70.0,
          "outliers": [40.0, 75.0],
          "count": 365
        }
      }
    ]
  },
  "metadata": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "metrics": ["temperature", "humidity"],
    "group_by": "overall",
    "include_outliers": true,
    "depth": null
  }
}
```

### Error Response (400 Bad Request)

```json
{
  "success": false,
  "error": "start_date and end_date are required parameters"
}
```

## Example Usage

### Specific Metrics Boxplot

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=temperature&metrics=humidity"
```

### All Metrics (Default)

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31"
```

### Soil Temperature with Custom Depth

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=soil_temperature&depth=10cm"
```

### Multiple Metrics Analysis

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/boxplot/?start_date=2023-01-01&end_date=2023-12-31&metrics=temperature&metrics=humidity&metrics=wind_speed&metrics=rainfall"
```

## Statistical Measures

The API calculates the following statistical measures for each metric and time period:

- **Min**: Minimum value (excluding outliers if `include_outliers=false`)
- **Q1**: First quartile (25th percentile)
- **Median**: Middle value (50th percentile)
- **Q3**: Third quartile (75th percentile)
- **Max**: Maximum value (excluding outliers if `include_outliers=false`)
- **Outliers**: Values outside 1.5 × IQR from Q1 and Q3
- **Count**: Number of data points in the period

## Notes

- Outliers are calculated using the standard 1.5 × IQR method
- When `include_outliers=false`, min and max values exclude outliers
- The API automatically filters out null/missing values for each metric
- Date ranges are inclusive of both start and end dates
- All numerical values are rounded to 2 decimal places
- The API supports all environmental metrics available in the database

## Error Handling

The API returns appropriate error messages for:

- Missing required parameters
- Invalid date formats
- Invalid metric names
- Invalid group_by options
- Invalid soil temperature depths
- Database connection issues

## Performance Considerations

- Large date ranges may result in slower response times
- Multiple metrics increase processing time
- Consider using appropriate date ranges for your analysis needs
- The API includes data point counts to help assess data quality 