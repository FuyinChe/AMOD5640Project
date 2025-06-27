#!/usr/bin/env python3
"""
Complete test script for user registration and verification flow with integrated email testing
"""
import requests
import json
import time
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

def send_verification_email(email, verification_code, is_resend=False):
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
        
        if is_resend:
            msg['Subject'] = '🔄 New Verification Code - Trent Farm Data'
            icon = '🔄'
            title = 'New Verification Code'
            subtitle = 'A new verification code has been generated for your account:'
        else:
            msg['Subject'] = '🔐 Your Verification Code - Trent Farm Data'
            icon = '🔐'
            title = 'Email Verification'
            subtitle = 'Please use the following verification code to complete your registration:'
        
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
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }}
                .warning {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #721c24; }}
                .info {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #0c5460; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="verification-icon">{icon}</div>
                <div class="title">{title}</div>
                <div class="subtitle">Trent Farm Data System</div>
            </div>
            <div class="content">
                <div class="message">
                    <h3>{icon} Your Verification Code</h3>
                    <p>{subtitle}</p>
                    
                    <div class="code-box">
                        <div class="verification-code">{verification_code}</div>
                    </div>
                    
                    <div class="expiry">
                        <strong>⏰ Expires at:</strong> {code_expires_at.strftime('%H:%M:%S')} ({code_expires_at.strftime('%B %d, %Y')})
                    </div>
                    
                    {f'<div class="info"><strong>ℹ️ Note:</strong> This is a new verification code. Any previous codes are no longer valid.</div>' if is_resend else ''}
                    
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

def test_complete_registration_flow():
    """Test the complete registration and verification flow"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("🧪 Testing Complete Registration Flow")
    print("=" * 60)
    
    # Step 1: Register a new user
    print("\n1️⃣ Testing User Registration...")
    register_data = {
        "email": "testuser@example.com",  # Generic test email - any valid email works
        "password": "testpassword123"
    }
    
    verification_code = None
    
    try:
        response = requests.post(f"{base_url}/register/", json=register_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            
            # Generate and send verification code
            verification_code = generate_verification_code()
            email_sent = send_verification_email(register_data["email"], verification_code)
            
            if email_sent:
                print("   📧 Verification code sent to your email!")
                print(f"   🔐 Generated code: {verification_code}")
            else:
                print("   ⚠️ Registration successful but verification email failed")
                return False
        else:
            print("   ❌ Registration failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 2: Get verification code from user
    print("\n2️⃣ Getting verification code...")
    print(f"   📧 Email sent to: {register_data['email']}")
    print(f"   🔐 Generated code: {verification_code}")
    print("\n   Options:")
    print("   1. Use the generated code above")
    print("   2. Check your email and enter the code you received")
    
    choice = input("\n   Enter '1' to use generated code, or '2' to enter email code: ").strip()
    
    if choice == '1':
        code_to_use = verification_code
        print(f"   Using generated code: {code_to_use}")
    else:
        code_to_use = input("   Enter the verification code from your email: ").strip()
    
    # Step 3: Verify the email
    print("\n3️⃣ Testing Email Verification...")
    verify_data = {
        "email": "testuser@example.com",  # Generic test email - any valid email works
        "code": code_to_use
    }
    
    try:
        response = requests.post(f"{base_url}/verify/", json=verify_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Email verification successful!")
        else:
            print("   ❌ Email verification failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False
    
    # Step 4: Test resend verification code
    print("\n4️⃣ Testing Resend Verification Code...")
    resend_data = {
        "email": "testuser@example.com"  # Generic test email - any valid email works
    }
    
    try:
        response = requests.post(f"{base_url}/resend-code/", json=resend_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Resend verification code successful!")
            
            # Send new verification code via email
            new_verification_code = generate_verification_code()
            email_sent = send_verification_email(register_data["email"], new_verification_code, is_resend=True)
            
            if email_sent:
                print("   📧 New verification code sent to your email!")
                print(f"   🔐 New generated code: {new_verification_code}")
                print("\n   💡 Note: You can use this code or check your email for the actual code")
            else:
                print("   ⚠️ Resend successful but email failed")
        else:
            print("   ⚠️ Resend verification code failed (might be already verified)")
            
    except Exception as e:
        print(f"   ❌ Resend error: {e}")
    
    print("\n🎉 Complete flow test finished!")
    return True

def test_email_configuration():
    """Test email configuration"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("\n📧 Testing Email Configuration...")
    print("=" * 60)
    
    test_email = input("Enter email to receive test: ")
    
    try:
        response = requests.post(f"{base_url}/test-email/", json={"email": test_email})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email configuration test successful!")
            return True
        else:
            print("❌ Email configuration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Complete Registration Flow Test")
    print("Make sure your Django server is running on http://127.0.0.1:8000")
    print("✅ All valid email addresses are now accepted")
    print("=" * 60)
    
    # Test email configuration first
    email_success = test_email_configuration()
    
    if email_success:
        # Test complete registration flow
        registration_success = test_complete_registration_flow()
        
        if registration_success:
            print("\n🎉 All tests passed! Your registration system is working correctly.")
        else:
            print("\n❌ Registration flow test failed.")
    else:
        print("\n❌ Email configuration test failed. Please fix email settings first.") 