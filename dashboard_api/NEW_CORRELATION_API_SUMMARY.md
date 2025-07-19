# Correlation Analysis API - Implementation Summary

## Overview

A new correlation analysis API has been added to the environmental data dashboard to provide statistical correlation analysis for multiple environmental metrics. This API is specifically designed for frontend integration with Angular and Plotly.js.

## New API Endpoint

**URL:** `/api/charts/statistical/correlation/`

**Method:** GET

**Authentication:** JWT authentication required

**Purpose:** Generate correlation matrices, p-values, and pairwise correlation data for environmental metrics

## Key Features

### 1. Multiple Correlation Methods
- **Pearson Correlation** (default) - Linear relationships
- **Spearman Correlation** - Rank-based relationships  
- **Kendall Correlation** - Ordinal relationships

### 2. Comprehensive Analysis
- **Correlation Matrix** - Complete matrix of all metric correlations
- **P-Value Matrix** - Statistical significance for each correlation
- **Pairwise Correlations** - Detailed breakdown of each metric pair
- **Correlation Statistics** - Summary of strong, moderate, and weak correlations

### 3. Default 2023 Date Range
- **Automatic Default**: If no dates are provided, defaults to entire year 2023 (2023-01-01 to 2023-12-31)
- **Flexible Date Ranges**: Custom date ranges can still be specified
- **User-Friendly**: No need to always specify dates for basic analysis

### 4. Performance Optimized
- **Smart Sampling**: Large datasets are automatically sampled for performance
- **Configurable Sample Size**: Default 10,000 records, adjustable up to 50,000
- **Efficient Processing**: Optimized for large environmental datasets

### 5. Frontend Ready
- **Plotly.js Compatible**: Data format optimized for heatmaps and scatter plots
- **Angular Integration**: TypeScript interfaces and service examples provided
- **Real-time Analysis**: Fast response times for interactive dashboards

## API Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `start_date` | No | "2023-01-01" | Start date (YYYY-MM-DD) |
| `end_date` | No | "2023-12-31" | End date (YYYY-MM-DD) |
| `metrics` | No | All metrics | List of metric names |
| `correlation_method` | No | "pearson" | Correlation method |
| `depth` | No | "5cm" | Soil temperature depth |
| `include_p_values` | No | true | Include p-values |
| `sample_size` | No | 10000 | Maximum sample size |

## Available Metrics

- **humidity** - Relative humidity percentage
- **temperature** - Air temperature in Celsius
- **wind_speed** - Wind speed in m/s
- **rainfall** - Rainfall in mm
- **snow_depth** - Snow depth in cm
- **shortwave_radiation** - Shortwave radiation in W/m²
- **atmospheric_pressure** - Atmospheric pressure in kPa
- **soil_temperature** - Soil temperature in Celsius (configurable depth)

## Example Usage

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

## Response Format

The API returns a comprehensive JSON response including:

```json
{
  "success": true,
  "data": {
    "correlation_matrix": [[1.0, 0.2345, -0.1234], ...],
    "p_value_matrix": [[0.0, 0.001234, 0.056789], ...],
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
    "correlation_method": "pearson",
    "sample_size": 10000
  }
}
```

## Frontend Integration

### Angular Service Example
```typescript
@Injectable()
export class CorrelationService {
  getCorrelationAnalysis(params?: any) {
    const token = localStorage.getItem('jwt_token');
    return this.http.get('/api/charts/statistical/correlation/', { 
      params,
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
  }
}
```

### Plotly.js Heatmap
```typescript
createHeatmap(data: any) {
  const trace = {
    z: data.correlation_matrix,
    x: data.metric_names,
    y: data.metric_names,
    type: 'heatmap',
    colorscale: 'RdBu'
  };
  
  Plotly.newPlot('heatmap', [trace], layout);
}
```

## Files Modified/Created

### 1. Core Implementation
- **`core/averaged_chart_views.py`** - Added `CorrelationAnalysisView` class
- **`core/urls.py`** - Added URL pattern for correlation endpoint

### 2. Documentation
- **`docs/CORRELATION_API.md`** - Comprehensive API documentation
- **`NEW_CORRELATION_API_SUMMARY.md`** - This summary document

### 3. Testing
- **`tests/test_correlation_api.py`** - Complete test suite including default date range testing

## Testing

Run the comprehensive test suite:

```bash
cd tests/
python test_correlation_api.py
```

Tests include:
- ✅ Default 2023 date range functionality
- ✅ Custom date ranges
- ✅ Different correlation methods (Pearson, Spearman, Kendall)
- ✅ Parameter validation
- ✅ Error handling
- ✅ Performance with large datasets

## Benefits

### 1. User Experience
- **Simplified Usage**: No need to always specify dates
- **Consistent Results**: Default 2023 provides reliable baseline data
- **Quick Analysis**: Immediate access to correlation insights

### 2. Developer Experience
- **Easy Integration**: Simple API calls with sensible defaults
- **Comprehensive Documentation**: Complete examples and TypeScript interfaces
- **Robust Testing**: Thorough test coverage

### 3. Performance
- **Optimized Processing**: Efficient handling of large datasets
- **Smart Sampling**: Automatic performance optimization
- **Fast Response**: Quick analysis for interactive dashboards

## Future Enhancements

1. **Caching Layer**: Redis caching for frequently requested analyses
2. **Real-time Updates**: WebSocket integration for live data correlation
3. **Advanced Visualizations**: Additional Plotly.js chart types
4. **Export Functionality**: CSV/Excel export of correlation results
5. **Batch Processing**: Support for multiple date ranges in single request

## Dependencies

The API requires:
- **numpy** - Numerical computations
- **pandas** - Data manipulation  
- **scipy** - Statistical functions

All dependencies are already included in `requirements.txt`.

## Conclusion

The Correlation Analysis API provides a powerful, user-friendly tool for environmental data analysis with:
- **Default 2023 date range** for immediate usability
- **Comprehensive statistical analysis** with multiple correlation methods
- **Frontend-optimized data format** for Angular and Plotly.js integration
- **Performance optimization** for large datasets
- **Complete documentation and testing** for reliable deployment

This API enables sophisticated environmental data analysis while maintaining simplicity for end users and developers. 