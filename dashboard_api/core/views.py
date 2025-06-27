from datetime import datetime, timedelta
import random
import logging
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .permissions import IsAdmin
from .models import Customer
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.contrib.auth.hashers import make_password

#import environmental data model and serializer
from rest_framework import generics
from .models import EnvironmentalData
from .serializers import EnvironmentalDataSerializer

# Set up logger
logger = logging.getLogger(__name__)


#send email with smtp
def send_email_with_smtp(to_email, subject, message, email_config=None):
    """Send email using explicit SMTP connection"""
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
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        
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

class VerifyEmailView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
            customer = Customer.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.verification_code != code:
            return Response({'error': 'Incorrect verification code'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.code_expires_at and timezone.now() > customer.code_expires_at:
            return Response({'error': 'Verification code expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate user and mark email as verified
        user.is_active = True
        user.save()

        customer.email_verified = True
        customer.verification_code = None
        customer.code_expires_at = None
        customer.save()

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    permission_classes = []  # allow unauthenticated registration

    def post(self, request):
        data = request.data
        print(f"DEBUG: Registration request received with data: {data}")

        # Validate email (accepts all valid email formats)
        email = data.get('email')
        if not email or '@' not in email or '.' not in email.split('@')[1]:
            return Response({'error': 'Valid email address is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password
        password = data.get('password')
        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if User with email exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create inactive User with hashed password
            username = email  # Use full email as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False
            )
            print(f"DEBUG: User created successfully: {user.username}")

            # Generate verification code & expiry
            verification_code = str(random.randint(100000, 999999))
            code_expires_at = timezone.now() + timedelta(minutes=10)

            # Create related Customer profile
            customer = Customer.objects.create(
                user=user,
                verification_code=verification_code,
                code_expires_at=code_expires_at,
                email_verified=False
            )
            print(f"DEBUG: Customer profile created with verification code: {verification_code}")

            # Send verification email
            email_sent = False
            try:
                success = send_email_with_smtp(
                    email,
                    'Trent Farm Data - Email Verification Code',
                    f'Your verification code is: {verification_code}\n\nThis code will expire in 10 minutes.'
                )
                if success:
                    logger.info(f"Verification email sent successfully to {email}")
                    email_sent = True
                    print(f"DEBUG: Email sent successfully to {email}")
                else:
                    logger.error(f"Failed to send verification email to {email}")
                    print(f"DEBUG: Email sending failed for {email}")
            except Exception as e:
                # Log the error but don't fail the registration
                logger.error(f"Failed to send email to {email}: {e}")
                print(f"DEBUG: Email exception for {email}: {e}")

            # Return success response with verification code for testing
            response_data = {
                'message': 'User created successfully. Please check your email for the verification code.',
                'user_id': user.id,
                'email': email,
                'email_sent': email_sent
            }
            
            print(f"DEBUG: Registration successful for {email}")
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"DEBUG: Registration failed with exception: {e}")
            logger.error(f"Registration failed for {email}: {e}")
            return Response({'error': f'Registration failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResendVerificationCodeView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
            customer = Customer.objects.get(user=user)
        except (User.DoesNotExist, Customer.DoesNotExist):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if customer.email_verified:
            return Response({'error': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate new verification code
        verification_code = str(random.randint(100000, 999999))
        code_expires_at = timezone.now() + timedelta(minutes=10)

        customer.verification_code = verification_code
        customer.code_expires_at = code_expires_at
        customer.save()

        # Send new verification email
        try:
            success = send_email_with_smtp(
                email,
                'Trent Farm Data - New Verification Code',
                f'Your new verification code is: {verification_code}\n\nThis code will expire in 10 minutes.'
            )
            if success:
                logger.info(f"Resend verification email sent successfully to {email}")
                return Response({'message': 'New verification code sent'}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed to resend verification email to {email}")
                return Response({'error': 'Failed to send verification code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Failed to resend email to {email}: {e}")
            return Response({'error': 'Failed to send verification code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome, Admin!'})

class EnvironmentalDataList(generics.ListAPIView):
    queryset = EnvironmentalData.objects.all().order_by('-Year', '-Month', '-Day')[:3000]  # return 3000
    serializer_class = EnvironmentalDataSerializer

class SampleEnvironmentalDataList(generics.ListAPIView):
    permission_classes = [AllowAny]  # No authentication required
    serializer_class = EnvironmentalDataSerializer
    
    # return 40 random value with filtered data
    def get_queryset(self):
        print(EnvironmentalData.objects.filter(
                    SnowDepth_cm__isnull=False,
                    RelativeHumidity_Pct__isnull=False,
                    ShortwaveRadiation_Wm2__isnull=False,
                    Rainfall_mm__isnull=False,
                    SoilTemperature_5cm_degC__isnull=False,
                    WindSpeed_ms__isnull=False,
                ).count()
            )
        return EnvironmentalData.objects.filter(
            Q(SnowDepth_cm__isnull=False) &
            Q(RelativeHumidity_Pct__isnull=False) &           
            Q(Rainfall_mm__isnull=False) &
            Q(SoilTemperature_5cm_degC__isnull=False) 
        ).order_by('-Year', '-Month', '-Day')[:40]

class TestEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Test endpoint to verify email configuration"""
        test_email = request.data.get('email')
        if not test_email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optional: Test with different email config
        email_config = request.data.get('email_config', None)
        
        try:
            success = send_email_with_smtp(
                test_email,
                'Test Email from Trent Farm Data',
                'This is a test email to verify your email configuration is working.',
                email_config
            )
            if success:
                logger.info(f"Test email sent successfully to {test_email}")
                return Response({'message': 'Test email sent successfully'}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed to send test email to {test_email}")
                return Response({'error': 'Failed to send test email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Failed to send test email to {test_email}: {e}")
            return Response({'error': f'Failed to send test email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestMultipleEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Test endpoint to test different Gmail accounts"""
        test_email = request.data.get('email')
        if not test_email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get email configuration from request
        email_config = {
            'EMAIL_HOST': request.data.get('email_host', 'smtp.gmail.com'),
            'EMAIL_PORT': int(request.data.get('email_port', 587)),
            'EMAIL_HOST_USER': request.data.get('email_host_user'),
            'EMAIL_HOST_PASSWORD': request.data.get('email_host_password'),
            'DEFAULT_FROM_EMAIL': request.data.get('default_from_email', 'no-reply@trentfarmdata.org')
        }
        
        # Validate required fields
        if not email_config['EMAIL_HOST_USER'] or not email_config['EMAIL_HOST_PASSWORD']:
            return Response({'error': 'email_host_user and email_host_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            success = send_email_with_smtp(
                test_email,
                'Test Email from Trent Farm Data (Multiple Accounts)',
                f'This is a test email sent using {email_config["EMAIL_HOST_USER"]}',
                email_config
            )
            if success:
                logger.info(f"Test email sent successfully to {test_email} using {email_config['EMAIL_HOST_USER']}")
                return Response({
                    'message': 'Test email sent successfully',
                    'used_account': email_config['EMAIL_HOST_USER']
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed to send test email to {test_email}")
                return Response({'error': 'Failed to send test email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Failed to send test email to {test_email}: {e}")
            return Response({'error': f'Failed to send test email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            # Add more fields as needed
        })



