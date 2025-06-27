# Trent Farm Data - Test Suite

This folder contains all test scripts for the Trent Farm Data registration and email system.

## 📁 Test Files Overview

### 🔧 Email Configuration Tests

#### `test_email.py`
**Purpose**: Comprehensive email system testing
- **Email System**: Direct SMTP (standalone)
- **User Input**: ❌ Auto-generated codes
- **Best For**: Email configuration setup and validation
- **Features**:
  - Tests basic email configuration
  - Tests verification code emails
  - Tests resend verification emails
  - Beautiful HTML templates
  - No Django server required

**Usage**:
```bash
python tests/test_email.py
```

#### `test_email_quick.py`
**Purpose**: Quick email troubleshooting
- **Email System**: Direct SMTP (standalone)
- **User Input**: ❌ Auto-generated codes
- **Best For**: Quick debugging and troubleshooting
- **Features**:
  - Fast email configuration test
  - Personal email testing
  - Troubleshooting guidance
  - No Django server required

**Usage**:
```bash
python tests/test_email_quick.py
```

### 🧪 Registration Flow Tests

#### `test_registration.py`
**Purpose**: Registration and verification flow testing
- **Email System**: Integrated + API
- **User Input**: ✅ User choice (generated or email)
- **Best For**: Development testing
- **Features**:
  - Tests registration API
  - Tests verification API
  - Integrated email sending
  - User choice for verification codes
  - Realistic testing options

**Usage**:
```bash
python tests/test_registration.py
```

#### `test_complete_flow.py`
**Purpose**: Complete end-to-end testing
- **Email System**: Integrated + API
- **User Input**: ✅ User choice (generated or email)
- **Best For**: End-to-end testing
- **Features**:
  - Complete registration flow
  - Email verification
  - Resend verification
  - Integrated email sending
  - User choice for verification codes

**Usage**:
```bash
python tests/test_complete_flow.py
```

#### `test_api_only.py`
**Purpose**: Pure API testing with Django emails
- **Email System**: Django only (no integrated sending)
- **User Input**: ✅ Required (check real emails)
- **Best For**: Production testing
- **Features**:
  - Tests Django API endpoints only
  - Uses actual Django email system
  - Requires checking real emails
  - No integrated email sending
  - Most realistic testing

**Usage**:
```bash
python tests/test_api_only.py
```

## 🚀 Testing Workflow

### 1. Email System Setup
```bash
# First, test email configuration
python tests/test_email.py

# If issues, troubleshoot quickly
python tests/test_email_quick.py
```

### 2. Development Testing
```bash
# Test registration flow with options
python tests/test_registration.py

# Test complete flow
python tests/test_complete_flow.py
```

### 3. Production Testing
```bash
# Test with real Django emails
python tests/test_api_only.py
```

## 📧 Email Configuration

All tests require proper email configuration in your `.env` file:

```bash
# SendGrid SMTP Settings
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key-here
DEFAULT_FROM_EMAIL=no-reply@trentfarmdata.org

# Test Email Address (optional)
TEST_EMAIL_ADDRESS=your-email@example.com
```

## 🎯 Test File Selection Guide

| Use Case | Recommended Test | Why |
|----------|------------------|-----|
| **Email Setup** | `test_email.py` | Comprehensive email testing |
| **Quick Debug** | `test_email_quick.py` | Fast troubleshooting |
| **Development** | `test_registration.py` | Flexible testing options |
| **End-to-End** | `test_complete_flow.py` | Complete flow testing |
| **Production** | `test_api_only.py` | Real Django email testing |

## ✅ Prerequisites

1. **Django Server Running**: For API tests
   ```bash
   python manage.py runserver
   ```

2. **Email Configuration**: Proper `.env` file setup

3. **Dependencies**: Required Python packages installed
   ```bash
   pip install requests python-dotenv
   ```

## 🔍 Troubleshooting

### Email Not Received?
1. Check spam folder
2. Verify email configuration
3. Use `test_email_quick.py` for troubleshooting
4. Try personal email instead of university email

### API Connection Error?
1. Ensure Django server is running
2. Check server URL in test files
3. Verify API endpoints are accessible

### Verification Code Issues?
1. Check email for actual codes
2. Use generated codes for quick testing
3. Verify code format (6 digits)

## 📝 Notes

- **Domain Restrictions**: All valid email addresses are now accepted
- **University Emails**: May be blocked by firewall/spam filters
- **Personal Emails**: Recommended for testing (Gmail, Outlook, etc.)
- **Generated Codes**: Available for quick testing without email checking
- **Real Emails**: Required for production-like testing

## 🎉 Success Indicators

- ✅ Email configuration tests pass
- ✅ Registration API returns 201 status
- ✅ Verification API returns 200 status
- ✅ Emails received in inbox
- ✅ Verification codes work correctly 