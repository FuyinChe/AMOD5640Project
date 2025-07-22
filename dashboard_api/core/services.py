"""
Services module for business logic and utility functions
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

from .email_templates import get_verification_email_content

# Set up logger
logger = logging.getLogger(__name__)


def generate_verification_code():
    """Generate a random 6-digit verification code for email verification purposes."""
    return str(random.randint(100000, 999999))


def send_email_with_smtp(to_email, subject, message, html_message=None, email_config=None):
    """Send email using explicit SMTP connection, supporting both plain text and HTML."""
    try:
        # Use provided config or default settings
        if email_config:
            email_host = email_config.get('EMAIL_HOST', settings.EMAIL_HOST)
            email_port = email_config.get('EMAIL_PORT', settings.EMAIL_PORT)
            email_user = email_config.get('EMAIL_HOST_USER', settings.EMAIL_HOST_USER)
            email_password = email_config.get('EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD)
            from_email = email_config.get('DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
        else:
            email_host = settings.EMAIL_HOST
            email_port = settings.EMAIL_PORT
            email_user = settings.EMAIL_HOST_USER
            email_password = settings.EMAIL_HOST_PASSWORD
            from_email = settings.DEFAULT_FROM_EMAIL
        
        print(f"DEBUG: Starting email send to {to_email}")
        print(f"DEBUG: EMAIL_HOST = {email_host}")
        print(f"DEBUG: EMAIL_PORT = {email_port}")
        print(f"DEBUG: EMAIL_HOST_USER = {email_user}")
        print(f"DEBUG: DEFAULT_FROM_EMAIL = {from_email}")
        print(f"DEBUG: EMAIL_HOST_PASSWORD = {email_password[:4]}..." if email_password else "Password: NOT SET")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        if html_message:
            msg.attach(MIMEText(html_message, 'html'))
        
        print("DEBUG: Creating SMTP connection...")
        # Create SMTP session
        server = smtplib.SMTP(email_host, email_port)
        print("DEBUG: SMTP connection created")
        
        # For SendGrid, we might not need STARTTLS depending on the port
        if email_port == 587:
            print("DEBUG: Starting TLS...")
            server.starttls()  # Enable TLS
            print("DEBUG: TLS started")
        
        print("DEBUG: Attempting login...")
        # For SendGrid, username is usually 'apikey' and password is your API key
        server.login(email_user, email_password)
        print("DEBUG: Login successful")
        
        # Send email
        text = msg.as_string()
        print("DEBUG: Sending email...")
        # For SendGrid, we can use the actual from_email as envelope sender
        server.sendmail(from_email, to_email, text)
        print("DEBUG: Email sent successfully")
        
        server.quit()
        print("DEBUG: SMTP connection closed")
        
        logger.info(f"Email sent successfully to {to_email} using {email_user}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"DEBUG: SMTP Authentication Error: {e}")
        logger.error(f"SMTP Authentication failed for {to_email}: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"DEBUG: SMTP Connect Error: {e}")
        logger.error(f"SMTP Connection failed for {to_email}: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"DEBUG: SMTP Exception: {e}")
        logger.error(f"SMTP error for {to_email}: {e}")
        return False
    except Exception as e:
        print(f"DEBUG: General Exception: {e}")
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


def send_verification_email(email, verification_code, code_expires_at, is_resend=False):
    """Send verification email to user"""
    try:
        subject, text_body, html_body = get_verification_email_content(
            verification_code, code_expires_at, is_resend=is_resend
        )
        success = send_email_with_smtp(
            email,
            subject,
            text_body,
            html_message=html_body
        )
        return success
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")
        return False


def create_user_with_verification(email, password):
    """Create a new user and associated Customer profile, generate a verification code, and set its expiry."""
    from django.contrib.auth.models import User
    from .models import Customer
    
    try:
        # Create inactive User with hashed password
        username = email  # Use full email as username
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        
        # Generate verification code & expiry
        verification_code = generate_verification_code()
        code_expires_at = timezone.now() + timedelta(minutes=10)

        # Create related Customer profile
        customer = Customer.objects.create(
            user=user,
            verification_code=verification_code,
            code_expires_at=code_expires_at,
            email_verified=False
        )
        
        return user, customer, verification_code
    except Exception as e:
        logger.error(f"Failed to create user {email}: {e}")
        raise e


def verify_user_email(email, code):
    """Verify a user's email using the provided verification code. Returns a tuple (success, message)."""
    from django.contrib.auth.models import User
    from .models import Customer
    
    try:
        user = User.objects.get(email=email)
        customer = Customer.objects.get(user=user)
        
        if customer.verification_code != code:
            return False, "Incorrect verification code"
            
        if customer.code_expires_at and timezone.now() > customer.code_expires_at:
            return False, "Verification code expired"
            
        # Activate user and mark email as verified
        user.is_active = True
        user.save()

        customer.email_verified = True
        customer.verification_code = None
        customer.code_expires_at = None
        customer.save()
        
        return True, "Email verified successfully"
    except User.DoesNotExist:
        return False, "Invalid email"
    except Customer.DoesNotExist:
        return False, "Customer profile not found"
    except Exception as e:
        logger.error(f"Error verifying email for {email}: {e}")
        return False, f"Verification failed: {str(e)}"


def resend_verification_code(email):
    """Resend verification code to user"""
    from django.contrib.auth.models import User
    from .models import Customer
    
    try:
        user = User.objects.get(email=email)
        customer = Customer.objects.get(user=user)
        
        if customer.email_verified:
            return False, "Email is already verified"
            
        # Generate new verification code
        verification_code = generate_verification_code()
        code_expires_at = timezone.now() + timedelta(minutes=10)

        customer.verification_code = verification_code
        customer.code_expires_at = code_expires_at
        customer.save()
        
        # Send new verification email
        success = send_verification_email(email, verification_code, code_expires_at, is_resend=True)
        
        if success:
            return True, "New verification code sent"
        else:
            return False, "Failed to send verification code"
    except (User.DoesNotExist, Customer.DoesNotExist):
        return False, "User not found"
    except Exception as e:
        logger.error(f"Error resending verification code to {email}: {e}")
        return False, f"Failed to resend verification code: {str(e)}" 