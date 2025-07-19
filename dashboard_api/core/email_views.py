"""
Email testing views module
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .services import send_email_with_smtp

# Set up logger
logger = logging.getLogger(__name__)


class TestEmailView(APIView):
    """Test email configuration view"""
    permission_classes = [IsAuthenticated]
    
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
    """Test multiple email accounts view"""
    permission_classes = [IsAuthenticated]
    
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