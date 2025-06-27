#!/usr/bin/env python3
"""
Standalone email test script to verify SMTP configuration and registration flow
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
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

def test_email_config():
    """Test email configuration independently"""
    
    # Get email settings from environment
    email_host = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER', 'apikey')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    test_email_address = os.getenv('TEST_EMAIL_ADDRESS', default_from_email)
    
    print("=== Email Configuration Test ===")
    print(f"Host: {email_host}")
    print(f"Port: {email_port}")
    print(f"User: {email_user}")
    print(f"Password: {email_password[:4]}..." if email_password else "Password: NOT SET")
    print(f"From Email: {default_from_email}")
    print(f"Test Email: {test_email_address}")
    print()
    
    if not all([email_host, email_user, email_password]):
        print("ERROR: Missing required email configuration!")
        print("Please check your .env file has:")
        print("EMAIL_HOST=smtp.sendgrid.net")
        print("EMAIL_PORT=587")
        print("EMAIL_HOST_USER=apikey")
        print("EMAIL_HOST_PASSWORD=your-sendgrid-api-key")
        print("DEFAULT_FROM_EMAIL=no-reply@trentfarmdata.org")
        print("TEST_EMAIL_ADDRESS=your-email@example.com")
        return False
    
    try:
        print("1. Creating SMTP connection...")
        server = smtplib.SMTP(email_host, email_port)
        print("   ✓ SMTP connection created")
        
        if email_port == 587:
            print("2. Starting TLS...")
            server.starttls()
            print("   ✓ TLS started")
        
        print("3. Attempting login...")
        server.login(email_user, email_password)
        print("   ✓ Login successful")
        
        print("4. Creating test message...")
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = test_email_address
        msg['Subject'] = '✅ Email Configuration Test - Trent Farm Data'
        
        # Plain text version
        text_body = """Email Configuration Test

This is a test email to verify your SendGrid email configuration is working correctly.

If you received this email, your email system is properly configured and ready for production use.

Best regards,
Trent Farm Data Team"""
        
        # HTML version
        html_body = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .success-icon { font-size: 48px; margin-bottom: 20px; }
                .title { font-size: 24px; margin-bottom: 10px; font-weight: bold; }
                .subtitle { font-size: 16px; opacity: 0.9; margin-bottom: 30px; }
                .message { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }
                .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }
                .highlight { background: #e8f5e8; padding: 15px; border-radius: 5px; border: 1px solid #28a745; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="success-icon">✅</div>
                <div class="title">Email Configuration Test</div>
                <div class="subtitle">Trent Farm Data System</div>
            </div>
            <div class="content">
                <div class="message">
                    <h3>🎉 Configuration Successful!</h3>
                    <p>This is a test email to verify your <strong>SendGrid email configuration</strong> is working correctly.</p>
                    <div class="highlight">
                        <strong>✅ If you received this email, your email system is properly configured and ready for production use.</strong>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Best regards,</strong><br>
                    Trent Farm Data Team</p>
                    <p style="font-size: 12px; color: #999;">
                        This is an automated test email. Please do not reply to this message.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        print("5. Sending test email...")
        text = msg.as_string()
        server.sendmail(default_from_email, test_email_address, text)
        print("   ✓ Test email sent successfully!")
        
        print("6. Closing connection...")
        server.quit()
        print("   ✓ Connection closed")
        
        print("\n🎉 SUCCESS: SendGrid email configuration is working!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("   This usually means:")
        print("   - Your SendGrid API key is incorrect")
        print("   - The API key doesn't have SMTP permissions")
        print("   - Username should be 'apikey' for SendGrid")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   This usually means:")
        print("   - Network/firewall is blocking SMTP")
        print("   - SendGrid server is unreachable")
        print("   - Wrong host/port configuration")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def test_verification_code_email():
    """Test sending verification code email (matches API functionality)"""
    
    # Get email settings from environment
    email_host = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER', 'apikey')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    test_email_address = os.getenv('TEST_EMAIL_ADDRESS', default_from_email)
    
    print("\n=== Verification Code Email Test ===")
    
    if not all([email_host, email_user, email_password]):
        print("ERROR: Missing required email configuration!")
        return False
    
    # Generate verification code (same as API)
    verification_code = generate_verification_code()
    code_expires_at = datetime.now() + timedelta(minutes=10)
    
    print(f"Generated verification code: {verification_code}")
    print(f"Code expires at: {code_expires_at}")
    print(f"Test Email: {test_email_address}")
    print()
    
    try:
        print("1. Creating SMTP connection...")
        server = smtplib.SMTP(email_host, email_port)
        print("   ✓ SMTP connection created")
        
        if email_port == 587:
            print("2. Starting TLS...")
            server.starttls()
            print("   ✓ TLS started")
        
        print("3. Attempting login...")
        server.login(email_user, email_password)
        print("   ✓ Login successful")
        
        print("4. Creating verification email...")
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = test_email_address
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
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }}
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
        
        print("5. Sending verification email...")
        text = msg.as_string()
        server.sendmail(default_from_email, test_email_address, text)
        print("   ✓ Verification email sent successfully!")
        
        print("6. Closing connection...")
        server.quit()
        print("   ✓ Connection closed")
        
        print(f"\n🎉 SUCCESS: Verification code email sent!")
        print(f"📧 Check your email for code: {verification_code}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def test_resend_verification_email():
    """Test resending verification code email"""
    
    # Get email settings from environment
    email_host = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER', 'apikey')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    test_email_address = os.getenv('TEST_EMAIL_ADDRESS', default_from_email)
    
    print("\n=== Resend Verification Code Email Test ===")
    
    if not all([email_host, email_user, email_password]):
        print("ERROR: Missing required email configuration!")
        return False
    
    # Generate new verification code
    new_verification_code = generate_verification_code()
    code_expires_at = datetime.now() + timedelta(minutes=10)
    
    print(f"Generated new verification code: {new_verification_code}")
    print(f"Code expires at: {code_expires_at}")
    print(f"Test Email: {test_email_address}")
    print()
    
    try:
        print("1. Creating SMTP connection...")
        server = smtplib.SMTP(email_host, email_port)
        print("   ✓ SMTP connection created")
        
        if email_port == 587:
            print("2. Starting TLS...")
            server.starttls()
            print("   ✓ TLS started")
        
        print("3. Attempting login...")
        server.login(email_user, email_password)
        print("   ✓ Login successful")
        
        print("4. Creating resend verification email...")
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = test_email_address
        msg['Subject'] = '🔄 New Verification Code - Trent Farm Data'
        
        # Plain text version
        text_body = f"""New Verification Code

Your new verification code is: {new_verification_code}

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
                .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .resend-icon {{ font-size: 48px; margin-bottom: 20px; }}
                .title {{ font-size: 24px; margin-bottom: 10px; font-weight: bold; }}
                .subtitle {{ font-size: 16px; opacity: 0.9; margin-bottom: 30px; }}
                .message {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff6b6b; }}
                .code-box {{ background: #f8f9fa; border: 2px dashed #ff6b6b; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .verification-code {{ font-size: 32px; font-weight: bold; color: #ff6b6b; letter-spacing: 4px; font-family: 'Courier New', monospace; }}
                .expiry {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }}
                .warning {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #721c24; }}
                .info {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #0c5460; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="resend-icon">🔄</div>
                <div class="title">New Verification Code</div>
                <div class="subtitle">Trent Farm Data System</div>
            </div>
            <div class="content">
                <div class="message">
                    <h3>🔄 Your New Verification Code</h3>
                    <p>A new verification code has been generated for your account:</p>
                    
                    <div class="code-box">
                        <div class="verification-code">{new_verification_code}</div>
                    </div>
                    
                    <div class="expiry">
                        <strong>⏰ Expires at:</strong> {code_expires_at.strftime('%H:%M:%S')} ({code_expires_at.strftime('%B %d, %Y')})
                    </div>
                    
                    <div class="info">
                        <strong>ℹ️ Note:</strong> This is a new verification code. Any previous codes are no longer valid.
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
        
        print("5. Sending resend verification email...")
        text = msg.as_string()
        server.sendmail(default_from_email, test_email_address, text)
        print("   ✓ Resend verification email sent successfully!")
        
        print("6. Closing connection...")
        server.quit()
        print("   ✓ Connection closed")
        
        print(f"\n🎉 SUCCESS: Resend verification code email sent!")
        print(f"📧 Check your email for new code: {new_verification_code}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Trent Farm Data Email Testing Suite")
    print("=" * 50)
    
    # Test basic email configuration
    basic_success = test_email_config()
    
    if basic_success:
        # Test verification code email
        verification_success = test_verification_code_email()
        
        if verification_success:
            # Test resend verification email
            resend_success = test_resend_verification_email()
            
            if resend_success:
                print("\n🎉 All email tests passed! Your email system is ready for production.")
            else:
                print("\n⚠️ Resend verification email test failed.")
        else:
            print("\n❌ Verification code email test failed.")
    else:
        print("\n❌ Basic email configuration test failed. Please fix your .env file.") 