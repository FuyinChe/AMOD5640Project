#!/usr/bin/env python3
"""
Quick email test to troubleshoot university email blocking
"""
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

def test_email_with_personal_address():
    """Test email sending to a personal email address"""
    
    # Get email settings from environment
    email_host = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER', 'apikey')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@trentfarmdata.org')
    
    print("🔍 Email Configuration Test")
    print("=" * 50)
    print(f"Host: {email_host}")
    print(f"Port: {email_port}")
    print(f"User: {email_user}")
    print(f"Password: {email_password[:4]}..." if email_password else "Password: NOT SET")
    print(f"From Email: {default_from_email}")
    print()
    
    if not all([email_host, email_user, email_password]):
        print("❌ Missing email configuration!")
        print("Please check your .env file has:")
        print("EMAIL_HOST=smtp.sendgrid.net")
        print("EMAIL_PORT=587")
        print("EMAIL_HOST_USER=apikey")
        print("EMAIL_HOST_PASSWORD=your-sendgrid-api-key")
        return False
    
    # Get personal email for testing
    personal_email = input("Enter your personal email (Gmail, Outlook, etc.): ")
    
    verification_code = generate_verification_code()
    code_expires_at = datetime.now() + timedelta(minutes=10)
    
    print(f"\n📧 Sending test to: {personal_email}")
    print(f"🔐 Code: {verification_code}")
    print(f"⏰ Expires: {code_expires_at.strftime('%H:%M:%S')}")
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
        
        print("4. Creating test email...")
        msg = MIMEMultipart('alternative')
        msg['From'] = default_from_email
        msg['To'] = personal_email
        msg['Subject'] = '🔍 Email Test - Trent Farm Data (Personal Email)'
        
        # Plain text version
        text_body = f"""Email Test - Personal Email

This is a test email to verify if your personal email can receive messages from our system.

Test verification code: {verification_code}
Expires: {code_expires_at.strftime('%H:%M:%S')}

If you received this email, the email system is working correctly.
The issue is likely with university email restrictions.

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
                .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .test-icon {{ font-size: 48px; margin-bottom: 20px; }}
                .title {{ font-size: 24px; margin-bottom: 10px; font-weight: bold; }}
                .subtitle {{ font-size: 16px; opacity: 0.9; margin-bottom: 30px; }}
                .message {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }}
                .code-box {{ background: #f8f9fa; border: 2px dashed #28a745; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0; }}
                .verification-code {{ font-size: 32px; font-weight: bold; color: #28a745; letter-spacing: 4px; font-family: 'Courier New', monospace; }}
                .info {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #0c5460; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="test-icon">🔍</div>
                <div class="title">Email Test - Personal Email</div>
                <div class="subtitle">Trent Farm Data System</div>
            </div>
            <div class="content">
                <div class="message">
                    <h3>🔍 Email System Test</h3>
                    <p>This is a test email to verify if your personal email can receive messages from our system.</p>
                    
                    <div class="code-box">
                        <div class="verification-code">{verification_code}</div>
                    </div>
                    
                    <div class="info">
                        <strong>ℹ️ Test Results:</strong><br>
                        • If you received this email → Email system is working ✅<br>
                        • If you didn't receive it → Check spam folder or email configuration ❌<br>
                        • University emails (@trentu.ca) may be blocked by firewall 🏛️
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Best regards,</strong><br>
                    Trent Farm Data Team</p>
                    <p style="font-size: 12px; color: #999;">
                        This is a test email. Please do not reply to this message.
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
        server.sendmail(default_from_email, personal_email, text)
        print("   ✓ Test email sent successfully!")
        
        print("6. Closing connection...")
        server.quit()
        print("   ✓ Connection closed")
        
        print(f"\n🎉 SUCCESS: Test email sent to {personal_email}!")
        print(f"📧 Check your email (including spam folder) for code: {verification_code}")
        print("\n💡 Next Steps:")
        print("1. Check your personal email inbox and spam folder")
        print("2. If received → Email system works, university email is blocked")
        print("3. If not received → Email configuration issue")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("   Check your SendGrid API key")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   Check network/firewall settings")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Trent Farm Data - Email Troubleshooting Test")
    print("=" * 60)
    print("✅ All valid email addresses are now accepted")
    print("This test will help determine if the issue is:")
    print("• Email system configuration")
    print("• University email restrictions")
    print("• Network/firewall blocking")
    print()
    print("💡 Purpose: Test if your email system can send emails")
    print("   This is NOT for registration testing - use test_registration.py for that")
    print()
    
    test_email_with_personal_address() 