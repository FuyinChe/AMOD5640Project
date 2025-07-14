# Trent Farm Data API

A comprehensive Django REST API for environmental data management and visualization, built for the AMOD 5640 course project.

## 🌟 Features

### 🔐 Authentication & User Management
- **User Registration**: Email-based registration with verification codes
- **Email Verification**: Secure email verification system with resend capability
- **Admin Dashboard**: Protected admin interface with role-based permissions
- **User Information**: Authenticated user data access

### 📊 Environmental Data APIs

#### Raw Data Endpoints
- **Snow Depth**: `/api/raw/snow-depth/`
- **Rainfall**: `/api/raw/rainfall/`
- **Humidity**: `/api/raw/humidity/`
- **Soil Temperature**: `/api/raw/soil-temperature/` (supports multiple depths: 5cm, 10cm, 20cm, 25cm, 50cm)
- **Multi-Metric**: `/api/raw/multi-metric/` (combines multiple metrics)

#### Chart Data Endpoints (Averaged)
- **Snow Depth Charts**: `/api/charts/snow-depth/`
- **Rainfall Charts**: `/api/charts/rainfall/`
- **Humidity Charts**: `/api/charts/humidity/`
- **Soil Temperature Charts**: `/api/charts/soil-temperature/`
- **Shortwave Radiation Charts**: `/api/charts/shortwave-radiation/`
- **Wind Speed Charts**: `/api/charts/wind-speed/`
- **Atmospheric Pressure Charts**: `/api/charts/atmospheric-pressure/`

#### Statistical Analysis Endpoints
- **Multi-Metric Boxplot**: `/api/charts/statistical/boxplot/`
- **Multi-Metric Histogram**: `/api/charts/statistical/histogram/`
- **Monthly Summary**: `/api/monthly-summary/`

### 📧 Email System
- **SMTP Integration**: SendGrid email service integration
- **HTML Templates**: Beautiful email templates for verification
- **Test Endpoints**: Email configuration testing and debugging
- **Multiple Email Support**: Test with various email providers

### 🔍 Data Filtering & Aggregation
- **Time Grouping**: Hourly, daily, weekly, monthly aggregations
- **Date Ranges**: Custom start/end date filtering
- **Year/Month Filters**: Specific time period selection
- **Performance Limits**: Optimized data retrieval with configurable limits

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL database
- SendGrid account (for email functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AMOD5640Project/dashboard_api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   # Copy example environment file
   cp env_example.txt .env
   
   # Edit .env with your configuration
   # Required settings:
   # - Database credentials
   # - SendGrid API key
   # - Django secret key
   ```

4. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **OpenAPI JSON**: [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)
- **OpenAPI YAML**: [http://localhost:8000/swagger.yaml](http://localhost:8000/swagger.yaml)

### API Endpoints Overview

#### Authentication
```
POST /api/register/           # User registration
POST /api/verify/             # Email verification
POST /api/resend-code/        # Resend verification code
GET  /api/userinfo/           # User information (authenticated)
GET  /api/admin-dashboard/    # Admin dashboard (admin only)
```

#### Environmental Data
```
GET /api/environmental-data/           # All environmental data
GET /api/sample/environmental-data/    # Sample data
GET /api/monthly-summary/              # Monthly aggregations
```

#### Raw Data APIs
```
GET /api/raw/snow-depth/              # Raw snow depth data
GET /api/raw/rainfall/                # Raw rainfall data
GET /api/raw/humidity/                # Raw humidity data
GET /api/raw/soil-temperature/        # Raw soil temperature data
GET /api/raw/multi-metric/            # Raw multi-metric data
```

#### Chart APIs (Averaged)
```
GET /api/charts/snow-depth/           # Snow depth charts
GET /api/charts/rainfall/             # Rainfall charts
GET /api/charts/humidity/             # Humidity charts
GET /api/charts/soil-temperature/     # Soil temperature charts
GET /api/charts/shortwave-radiation/  # Shortwave radiation charts
GET /api/charts/wind-speed/           # Wind speed charts
GET /api/charts/atmospheric-pressure/ # Atmospheric pressure charts
```

#### Statistical Analysis
```
GET /api/charts/statistical/boxplot/   # Multi-metric boxplot data
GET /api/charts/statistical/histogram/ # Multi-metric histogram data
```

#### Email Testing
```
POST /api/test-email/                 # Test email configuration
POST /api/test-multiple-email/        # Test multiple email accounts
```

## 🧪 Testing

### Comprehensive Test Suite
The project includes extensive testing capabilities:

#### Email System Tests
- `test_email.py` - Comprehensive email system testing
- `test_email_quick.py` - Quick email troubleshooting
- `test_registration.py` - Registration flow testing
- `test_complete_flow.py` - End-to-end testing
- `test_api_only.py` - Pure API testing

#### API Tests
- `test_chart_apis.py` - Chart API functionality
- `test_averaged_chart_apis.py` - Averaged chart APIs
- `test_boxplot_overall.py` - Boxplot API testing
- `test_histogram_api.py` - Histogram API testing
- `test_monthly_summary.py` - Monthly summary testing
- `test_separated_apis.py` - Separated API testing

#### Utility Tests
- `run_all_tests.py` - Run complete test suite
- `complete_registration.py` - Complete registration flow
- `debug_registration.py` - Registration debugging

### Running Tests
```bash
# Run all tests
cd tests
python run_all_tests.py

# Test specific functionality
python test_email.py
python test_chart_apis.py
python test_averaged_chart_apis.py
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=mysql://user:password@localhost/dbname

# Email (SendGrid)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=no-reply@trentfarmdata.org

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=https://trentfarmdata.org
```

### Security Features
- **CORS Protection**: Restricted to trusted domains
- **Authentication**: JWT and session-based authentication
- **Permissions**: Role-based access control
- **Rate Limiting**: API request throttling
- **Input Validation**: Comprehensive parameter validation

## 📁 Project Structure

```
dashboard_api/
├── core/                          # Main application logic
│   ├── auth_views.py             # Authentication views
│   ├── environmental_views.py    # Environmental data views
│   ├── raw_data_views.py         # Raw data endpoints
│   ├── averaged_chart_views.py   # Chart data endpoints
│   ├── email_views.py            # Email testing views
│   ├── models.py                 # Database models
│   ├── serializers.py            # API serializers
│   ├── services.py               # Business logic
│   ├── permissions.py            # Custom permissions
│   └── urls.py                   # URL routing
├── tests/                        # Comprehensive test suite
│   ├── test_email.py            # Email system tests
│   ├── test_chart_apis.py       # Chart API tests
│   ├── test_averaged_chart_apis.py # Averaged chart tests
│   └── run_all_tests.py         # Test runner
├── docs/                         # API documentation
│   ├── BOXPLOT_API.md           # Boxplot API docs
│   └── HISTOGRAM_API.md         # Histogram API docs
├── templates/                    # Email templates
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t trent-farm-api .
docker run -p 8000:8000 trent-farm-api
```

### Production Setup
1. Set `DEBUG=False` in environment
2. Configure production database
3. Set up proper CORS origins
4. Configure email service
5. Set up SSL/TLS certificates
6. Configure web server (nginx, Apache)

## 📊 Data Metrics

The API supports the following environmental metrics:

- **Air Temperature** (°C)
- **Relative Humidity** (%)
- **Wind Speed** (m/s)
- **Snow Depth** (cm)
- **Rainfall** (mm)
- **Soil Temperature** (°C) - Multiple depths
- **Shortwave Radiation** (W/m²)
- **Atmospheric Pressure** (kPa)

## 🔍 Query Parameters

### Standard Parameters
- `year` - Filter by specific year
- `month` - Filter by specific month
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)
- `group_by` - Time grouping (hour, day, week, month)
- `limit` - Maximum data points (performance limit: 10,000)

### Statistical Parameters
- `metrics` - List of metrics to analyze
- `bins` - Number of histogram bins
- `depth` - Soil temperature depth
- `include_outliers` - Include outlier data in boxplots

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions and support:
- **Email**: [admin@trentfarmdata.org](mailto:admin@trentfarmdata.org)
- **Documentation**: Check the `/docs/` folder for detailed API documentation
- **Issues**: Use the project's issue tracker

## 📄 License

This project is developed for the AMOD 5640 course at Trent University.

---

**Built with Django, Django REST Framework, and modern Python best practices.**
