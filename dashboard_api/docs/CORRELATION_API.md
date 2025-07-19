# Correlation Analysis API Documentation

## Overview

The Correlation Analysis API provides statistical correlation analysis for environmental data metrics. It generates correlation matrices, p-values, and pairwise correlation data optimized for frontend visualization with Plotly.js.

**⚠️ Authentication Required**: This API requires JWT authentication. Include the Authorization header with your JWT token.

## Endpoint

```
GET /api/charts/statistical/correlation/
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | No | "2023-01-01" | Start date in YYYY-MM-DD format |
| `end_date` | string | No | "2023-12-31" | End date in YYYY-MM-DD format |
| `metrics` | array | No | All metrics | List of metric names to analyze |
| `correlation_method` | string | No | "pearson" | Correlation method: pearson, spearman, kendall |
| `depth` | string | No | "5cm" | Soil temperature depth (5cm, 10cm, 20cm, 25cm, 50cm) |
| `include_p_values` | boolean | No | true | Include p-values in response |
| `sample_size` | integer | No | 10000 | Maximum sample size for analysis |

## Default Behavior

If no `start_date` and `end_date` are provided, the API will automatically use the entire year 2023 (2023-01-01 to 2023-12-31) as the default date range.

## Authentication

This API requires JWT authentication. Include your JWT token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Example Requests

### Basic Request (Uses Default 2023 Date Range)
```bash
curl -H "Authorization: Bearer <your_jwt_token>" "http://localhost:8000/api/charts/statistical/correlation/"
```

### Custom Date Range
```bash
curl -H "Authorization: Bearer <your_jwt_token>" "http://localhost:8000/api/charts/statistical/correlation/?start_date=2023-06-01&end_date=2023-08-31"
```

### Specific Metrics with Spearman Correlation
```bash
curl -H "Authorization: Bearer <your_jwt_token>" "http://localhost:8000/api/charts/statistical/correlation/?metrics=humidity&metrics=temperature&correlation_method=spearman"
```

### With Custom Sample Size
```bash
curl -H "Authorization: Bearer <your_jwt_token>" "http://localhost:8000/api/charts/statistical/correlation/?sample_size=5000&include_p_values=false"
```

## Response Format

```json
{
  "success": true,
  "data": {
    "correlation_matrix": [
      [1.0, 0.2345, -0.1234],
      [0.2345, 1.0, 0.5678],
      [-0.1234, 0.5678, 1.0]
    ],
    "p_value_matrix": [
      [0.0, 0.001234, 0.056789],
      [0.001234, 0.0, 0.000123],
      [0.056789, 0.000123, 0.0]
    ],
    "metric_names": ["humidity", "temperature", "wind_speed"],
    "pairwise_correlations": [
      {
        "metric1": "humidity",
        "metric2": "temperature",
        "correlation": 0.2345,
        "p_value": 0.001234,
        "sample_size": 8760
      }
    ],
    "statistics": {
      "total_records": 8760,
      "valid_pairs": 3,
      "strong_correlations": 1,
      "moderate_correlations": 1,
      "weak_correlations": 1
    }
  },
  "metadata": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "metrics": ["humidity", "temperature", "wind_speed"],
    "correlation_method": "pearson",
    "include_p_values": true,
    "sample_size": 10000,
    "depth": null
  }
}
```

## Available Metrics

- `humidity` - Relative humidity percentage
- `temperature` - Air temperature in Celsius
- `wind_speed` - Wind speed in m/s
- `rainfall` - Rainfall in mm
- `snow_depth` - Snow depth in cm
- `shortwave_radiation` - Shortwave radiation in W/m²
- `atmospheric_pressure` - Atmospheric pressure in kPa
- `soil_temperature` - Soil temperature in Celsius (specify depth)

## Correlation Methods

1. **Pearson** (default) - Linear correlation coefficient
   - Range: -1 to +1
   - Assumes linear relationship
   - Sensitive to outliers

2. **Spearman** - Rank-based correlation
   - Range: -1 to +1
   - Monotonic relationships
   - Robust to outliers

3. **Kendall** - Ordinal correlation
   - Range: -1 to +1
   - Concordant/discordant pairs
   - Good for small samples

## Correlation Strength Interpretation

- **Strong**: |r| ≥ 0.7
- **Moderate**: 0.3 ≤ |r| < 0.7
- **Weak**: |r| < 0.3

## Frontend Integration with Angular and Plotly.js

### Heatmap Visualization
```typescript
// Angular component
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Plotly from 'plotly.js-dist';

@Component({
  selector: 'app-correlation-heatmap',
  template: '<div id="correlationHeatmap"></div>'
})
export class CorrelationHeatmapComponent implements OnInit {
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadCorrelationData();
  }
  
  loadCorrelationData() {
    // Get JWT token from localStorage or auth service
    const token = localStorage.getItem('jwt_token');
    
    this.http.get('/api/charts/statistical/correlation/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .subscribe((response: any) => {
      if (response.success) {
        this.createHeatmap(response.data);
      }
    });
  }
  
  createHeatmap(data: any) {
    const trace = {
      z: data.correlation_matrix,
      x: data.metric_names,
      y: data.metric_names,
      type: 'heatmap',
      colorscale: 'RdBu',
      zmid: 0,
      colorbar: {
        title: 'Correlation Coefficient'
      }
    };
    
    const layout = {
      title: 'Environmental Metrics Correlation Matrix',
      width: 600,
      height: 500
    };
    
    Plotly.newPlot('correlationHeatmap', [trace], layout);
  }
}
```

### Scatter Plot Matrix
```typescript
createScatterMatrix(data: any) {
  const traces = [];
  
  data.pairwise_correlations.forEach((pair: any) => {
    traces.push({
      x: pair.metric1_data,
      y: pair.metric2_data,
      mode: 'markers',
      type: 'scatter',
      name: `${pair.metric1} vs ${pair.metric2}`,
      text: `r = ${pair.correlation}<br>p = ${pair.p_value}`,
      hovertemplate: '%{text}<extra></extra>'
    });
  });
  
  const layout = {
    title: 'Pairwise Correlations',
    grid: {rows: 2, columns: 2, pattern: 'independent'}
  };
  
  Plotly.newPlot('scatterMatrix', traces, layout);
}
```

## Error Handling

### Common Error Responses

```json
{
  "success": false,
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

```json
{
  "success": false,
  "error": "Invalid correlation_method: invalid. Valid methods: ['pearson', 'spearman', 'kendall']"
}
```

```json
{
  "success": false,
  "error": "Invalid metrics: ['invalid_metric']. Valid metrics: ['humidity', 'temperature', ...]"
}
```

## Performance Considerations

- **Sample Size**: Large datasets are automatically sampled to maintain performance
- **Date Range**: Consider using smaller date ranges for better performance
- **Metrics**: Limit the number of metrics for faster analysis
- **Caching**: Results can be cached on the frontend for repeated requests

## Testing

Run the test script to verify API functionality:

```bash
cd tests/
python test_correlation_api.py
```

This will test:
- Default 2023 date range functionality
- Custom date ranges
- Different correlation methods
- Parameter validation
- Error handling 