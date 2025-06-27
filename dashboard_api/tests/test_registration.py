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
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    
    if not all([email_host, email_user, email_password]):
        print("❌ Missing email configuration. Cannot send verification email.")
        return False
    
    code_expires_at = datetime.now() + timedelta(minutes=10)
    
    try:
        print("📧 Sending verification email...")
        server = smtplib.SMTP(email_host, email_port)
        
        if email_port == 587:
            server.starttls()
        
        server.login(email_user, email_password)
        
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = email
        msg['Subject'] = '🔐 Your Verification Code - Trent Farm Data'
        
        # Plain text version
        text_body = f"""Email Verification Code

Your verification code is: {verification_code}

This code will expire in 10 minutes at {code_expires_at.strftime('%H:%M:%S')}.

Best regards,
Trent Farm Data Team"""
        
        # HTML version
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .verification-icon {{ font-size: 48px; margin-bottom: 20px; }}
                .title {{ font-size: 24px; margin-bottom: 10px; font-weight: bold; }}
                .subtitle {{ font-size: 16px; opacity: 0.9; margin-bottom: 30px; }}
                .message {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #007bff; }}
                .code-box {{ background: #f8f9fa; border: 2px dashed #007bff; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .verification-code {{ font-size: 32px; font-weight: bold; color: #007bff; letter-spacing: 4px; font-family: 'Courier New', monospace; }}
                .expiry {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
                .warning {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #721c24; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="verification-icon">🔐</div>
                <div class="title">Email Verification</div>
                <div class="subtitle">Trent Farm Data System</div>
            </div>
            <div class="content">
                <div class="message">
                    <h3>🔐 Your Verification Code</h3>
                    <p>Please use the following verification code to complete your registration:</p>
                    
                    <div class="code-box">
                        <div class="verification-code">{verification_code}</div>
                    </div>
                    
                    <div class="expiry">
                        <strong>⏰ Expires at:</strong> {code_expires_at.strftime('%H:%M:%S')} ({code_expires_at.strftime('%B %d, %Y')})
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong> Never share this code with anyone. Trent Farm Data will never ask for this code via phone or email.
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Best regards,</strong><br>
                    Trent Farm Data Team</p>
                    <p style="font-size: 12px; color: #999;">
                        This is an automated verification email. Please do not reply to this message.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
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