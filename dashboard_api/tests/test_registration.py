#!/usr/bin/env python3
"""
Test script for user registration with integrated email testing
"""
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.email_templates import get_verification_email_content

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, using system environment variables")
    pass

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))

def send_verification_email(email, verification_code):
    """Send verification code email using fancy template"""
    
    # Get email settings from environment
    email_host = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER', 'apikey')
    email_password = os.getenv('EMAIL_HOST_PASSWORD') or ''
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    
    if not all([email_host, email_user, email_password]):
        print("❌ Missing email configuration. Cannot send verification email.")
        return False
    
    code_expires_at = datetime.now() + timedelta(minutes=10)
    subject, text_body, html_body = get_verification_email_content(verification_code, code_expires_at, is_resend=False)
    
    try:
        print("📧 Sending verification email...")
        server = smtplib.SMTP(email_host, email_port)
        
        if email_port == 587:
            server.starttls()
        
        server.login(email_user, email_password)
        
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        text = msg.as_string()
        server.sendmail(default_from_email, email, text)
        server.quit()
        
        print("✅ Verification email sent successfully!")
        print(f"📧 Code: {verification_code}")
        print(f"⏰ Expires: {code_expires_at.strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send verification email: {e}")
        return False

def test_registration(email, password):
    """Test user registration"""
    
    url = "http://127.0.0.1:8000/api/register/"
    
    data = {
        "email": email,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing registration for: {email}")
    print("=" * 50)
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            print("📧 Please check your email for the verification code.")
            return True
        else:
            print("❌ Registration failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_verification(email, code):
    """Test email verification"""
    
    url = "http://127.0.0.1:8000/api/verify/"
    
    data = {
        "email": email,
        "code": code
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"\nTesting verification for: {email}")
    print("=" * 50)
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Verification successful!")
            return True
        else:
            print("❌ Verification failed")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Trent Farm Data Registration Test")
    print("=" * 50)
    print("✅ All valid email addresses are now accepted")
    print("   No domain restrictions - any email format works")
    print()
    
    # Test registration
    test_email = input("Enter email to register (any valid email address): ")
    test_password = input("Enter password: ")
    
    registration_success = test_registration(test_email, test_password)
    
    if registration_success:
        print(f"\n📧 Verification code sent to: {test_email}")
        code_to_use = input("Enter the verification code from your email: ").strip()
        test_verification(test_email, code_to_use)
    else:
        print("\n❌ Registration failed. Cannot proceed with verification.") 