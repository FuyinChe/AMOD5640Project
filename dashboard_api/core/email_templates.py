import datetime

def get_verification_email_content(verification_code, expires_at, is_resend=False):
    """
    Returns (subject, plain_text_body, html_body) for the verification email.
    :param verification_code: The code to include in the email
    :param expires_at: A datetime.datetime object for expiry
    :param is_resend: Whether this is a resend email
    """
    if is_resend:
        subject = '🔄 New Verification Code - Trent Farm Data'
        icon = '🔄'
        title = 'New Verification Code'
        subtitle = 'A new verification code has been generated for your account:'
        info_html = f'<div class="info"><strong>ℹ️ Note:</strong> This is a new verification code. Any previous codes are no longer valid.</div>'
    else:
        subject = '🔐 Your Verification Code - Trent Farm Data'
        icon = '🔐'
        title = 'Email Verification'
        subtitle = 'Please use the following verification code to complete your registration:'
        info_html = ''

    expires_time = expires_at.strftime('%H:%M:%S')
    expires_date = expires_at.strftime('%B %d, %Y')

    plain_text = f"""Email Verification Code\n\nYour verification code is: {verification_code}\n\nThis code will expire in 10 minutes at {expires_time}.\n\nBest regards,\nTrent Farm Data Team"""

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
                    <strong>⏰ Expires at:</strong> {expires_time} ({expires_date})
                </div>
                {info_html}
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
    return subject, plain_text, html_body 