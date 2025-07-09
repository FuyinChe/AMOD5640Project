"""
Authentication and user management views module
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .permissions import IsAdmin
from .services import (
    create_user_with_verification,
    verify_user_email,
    resend_verification_code,
    send_email_with_smtp
)

# Set up logger
logger = logging.getLogger(__name__)


class VerifyEmailView(APIView):
    """Email verification view"""
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        success, message = verify_user_email(email, code)
        
        if success:
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    """User registration view"""
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
            # Create user with verification
            user, customer, verification_code = create_user_with_verification(email, password)
            print(f"DEBUG: User created successfully: {user.username}")

            # Send verification email
            email_sent = False
            try:
                from .email_templates import get_verification_email_content
                from django.utils import timezone
                from datetime import timedelta
                
                code_expires_at = timezone.now() + timedelta(minutes=10)
                subject, text_body, html_body = get_verification_email_content(
                    verification_code, code_expires_at, is_resend=False
                )
                success = send_email_with_smtp(
                    email,
                    subject,
                    text_body,
                    html_message=html_body
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
    """Resend verification code view"""
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        
        success, message = resend_verification_code(email)
        
        if success:
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class AdminDashboardView(APIView):
    """Admin dashboard view"""
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome, Admin!'})


class UserInfoView(APIView):
    """User information view"""
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