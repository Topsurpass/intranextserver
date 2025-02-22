import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import datetime

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True)
def send_welcome_email(self, recipient_email: str, first_name: str) -> None:
    """
    Asynchronously sends a styled welcome email to new users with retry capabilities.
    
    Features:
    - HTML and plain-text versions
    - Error logging and automatic retries
    - Professional email template design
    - Responsive layout for all devices
    - Brand-consistent styling

    Args:
        recipient_email (str): User's email address
        first_name (str): User's first name for personalization

    Raises:
        Exception: Logs error and triggers Celery retry mechanism
    """
    try:
        # Email configuration
        subject = "🎉 Welcome to Temz&Tech - Start Your Learning Journey!"
        from_email = f"Temz&Tech Team <{settings.DEFAULT_FROM_EMAIL}>"
        
        # Context for template rendering
        context = {
            'first_name': first_name,
            'support_email': settings.SUPPORT_EMAIL,
            'company_name': "Temz&Tech",
            'current_year': datetime.datetime.now().year
        }

        # Render HTML content from template
        html_content = render_to_string('emails/welcome.html', context)
        
        # Create plain text version by stripping HTML tags
        text_content = strip_tags(html_content)

        # Build email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[recipient_email],
            reply_to=[settings.EMAIL_HOST_USER]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Add email headers for analytics
        email.extra_headers = {
            'X-Email-Category': 'Welcome',
            'X-Email-Type': 'Transactional'
        }

        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Successfully sent welcome email to {recipient_email}")
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {recipient_email}: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)