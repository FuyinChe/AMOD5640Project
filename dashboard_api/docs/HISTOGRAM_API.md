# Multi-Metric Histogram API Documentation

## Overview

The Multi-Metric Histogram API provides data distribution analysis capabilities for environmental data across a specified date range. It generates histogram data that includes bin counts, percentages, and statistical measures for multiple environmental metrics. The API processes the entire date range as one dataset for maximum performance and simplicity.

## Endpoint

```
GET /api/charts/statistical/histogram/
```

## Purpose

Generate histogram data for multiple environmental metrics to analyze data distribution patterns and frequency across a date range. The API provides overall statistical measures for the specified period without time-based grouping.

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | Yes | - | Start date in ISO format (YYYY-MM-DD) |
| `end_date` | string | Yes | - | End date in ISO format (YYYY-MM-DD) |
| `metrics` | array | No | All metrics | List of metric names to analyze (optional) |
| `bins` | integer | No | 20 | Number of histogram bins (1-100) |
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

The API processes the **entire date range as one dataset** for maximum performance and simplicity. This provides overall distribution analysis for the specified period without time-based grouping (no daily, monthly, or yearly breakdowns).

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
    "temperature": {
      "bins": [
        { "bin_start": -30, "bin_end": -25, "count": 5, "percentage": 0.1 },
        { "bin_start": -25, "bin_end": -20, "count": 12, "percentage": 0.3 },
        { "bin_start": -20, "bin_end": -15, "count": 45, "percentage": 1.1 },
        { "bin_start": -15, "bin_end": -10, "count": 156, "percentage": 3.8 },
        { "bin_start": -10, "bin_end": -5, "count": 423, "percentage": 10.2 },
        { "bin_start": -5, "bin_end": 0, "count": 892, "percentage": 21.5 },
        { "bin_start": 0, "bin_end": 5, "count": 1256, "percentage": 30.3 },
        { "bin_start": 5, "bin_end": 10, "count": 987, "percentage": 23.8 },
        { "bin_start": 10, "bin_end": 15, "count": 234, "percentage": 5.6 },
        { "bin_start": 15, "bin_end": 20, "count": 89, "percentage": 2.1 },
        { "bin_start": 20, "bin_end": 25, "count": 23, "percentage": 0.6 },
        { "bin_start": 25, "bin_end": 30, "count": 8, "percentage": 0.2 },
        { "bin_start": 30, "bin_end": 35, "count": 2, "percentage": 0.05 }
      ],
      "statistics": {
        "mean": 13.6,
        "median": 14.2,
        "std_dev": 7.1,
        "min": -32.3,
        "max": 32.6,
        "total_count": 4140
      }
    },
    "humidity": {
      "bins": [
        { "bin_start": 0, "bin_end": 10, "count": 0, "percentage": 0.0 },
        { "bin_start": 10, "bin_end": 20, "count": 2, "percentage": 0.01 },
        { "bin_start": 20, "bin_end": 30, "count": 15, "percentage": 0.09 },
        { "bin_start": 30, "bin_end": 40, "count": 89, "percentage": 0.54 },
        { "bin_start": 40, "bin_end": 50, "count": 234, "percentage": 1.42 },
        { "bin_start": 50, "bin_end": 60, "count": 567, "percentage": 3.44 },
        { "bin_start": 60, "bin_end": 70, "count": 1234, "percentage": 7.48 },
        { "bin_start": 70, "bin_end": 80, "count": 3456, "percentage": 20.95 },
        { "bin_start": 80, "bin_end": 90, "count": 6789, "percentage": 41.16 },
        { "bin_start": 90, "bin_end": 100, "count": 500, "percentage": 3.03 }
      ],
      "statistics": {
        "mean": 77.8,
        "median": 80.1,
        "std_dev": 15.2,
        "min": 17.7,
        "max": 99.8,
        "total_count": 16488
      }
    }
  },
  "metadata": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "metrics": ["temperature", "humidity"],
    "bins": 20,
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

### All Metrics (Default)

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/histogram/" \
  -H "accept: application/json" \
  -G \
  -d "start_date=2023-01-01" \
  -d "end_date=2023-12-31"
```

### Specific Metrics with Custom Bins

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/histogram/" \
  -H "accept: application/json" \
  -G \
  -d "start_date=2023-01-01" \
  -d "end_date=2023-12-31" \
  -d "metrics=temperature" \
  -d "metrics=humidity" \
  -d "bins=15"
```

### Soil Temperature with Custom Depth

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/histogram/" \
  -H "accept: application/json" \
  -G \
  -d "start_date=2023-01-01" \
  -d "end_date=2023-12-31" \
  -d "metrics=soil_temperature" \
  -d "depth=10cm" \
  -d "bins=12"
```

### Single Metric Analysis

```bash
curl -X GET "http://localhost:8000/api/charts/statistical/histogram/" \
  -H "accept: application/json" \
  -G \
  -d "start_date=2023-01-01" \
  -d "end_date=2023-12-31" \
  -d "metrics=wind_speed" \
  -d "bins=25"
```

## Data Structure

### Bin Information
Each bin contains:
- **`bin_start`**: Lower bound of the bin (inclusive)
- **`bin_end`**: Upper bound of the bin (exclusive)
- **`count`**: Number of data points in this bin
- **`percentage`**: Percentage of total data points in this bin

### Statistics
Each metric includes:
- **`mean`**: Arithmetic mean of all values
- **`median`**: Middle value (50th percentile)
- **`std_dev`**: Standard deviation
- **`min`**: Minimum value
- **`max`**: Maximum value
- **`total_count`**: Total number of data points

## Notes

- Bins are automatically calculated based on the data range and specified number of bins
- The API automatically filters out null/missing values for each metric
- Date ranges are inclusive of both start and end dates
- All numerical values are rounded to 2 decimal places
- The API supports all environmental metrics available in the database
- Bin edges are calculated using numpy's histogram function for optimal distribution

## Error Handling

The API returns appropriate error messages for:

- Missing required parameters
- Invalid date formats
- Invalid metric names
- Invalid bin counts (must be between 1 and 100)
- Invalid soil temperature depths
- Database connection issues

## Performance Considerations

- Large date ranges may result in slower response times
- Multiple metrics increase processing time
- More bins provide finer granularity but increase response time
- Consider using appropriate date ranges and bin counts for your analysis needs
- The API includes data point counts to help assess data quality

## Use Cases

- **Data Distribution Analysis**: Understand how environmental data is distributed
- **Outlier Detection**: Identify unusual patterns in data
- **Quality Assessment**: Check data completeness and distribution
- **Trend Analysis**: Compare distributions across different time periods
- **Statistical Modeling**: Use histogram data for further statistical analysis 