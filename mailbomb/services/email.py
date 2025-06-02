import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional, Union, Dict
import logging
from pathlib import Path
import os
from mailbomb.core.config import settings
from mailbomb.models.contact import Contact
from mailbomb.models.template import EmailTemplate

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[Union[str, Dict[str, bytes]]]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send email with attachments and personalization
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML formatted message
            text_content: Plain text formatted message
            attachments: List of file paths or dicts with {'filename': bytes_content}
            cc: List of CC email addresses
            bcc: List of BCC email addresses
        """
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.default_from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)
        
        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Handle attachments
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, str):  # File path
                    file_path = Path(attachment)
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(
                            f.read(),
                            Name=file_path.name
                        )
                    part['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
                elif isinstance(attachment, dict):  # In-memory file
                    for filename, content in attachment.items():
                        part = MIMEApplication(
                            content,
                            Name=filename
                        )
                        part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_personalized_email(
        self,
        contact: Contact,
        template: EmailTemplate,
        attachments: Optional[List[Union[str, Dict[str, bytes]]]] = None
    ) -> bool:
        """
        Send personalized email to a specific contact
        
        Args:
            contact: Contact object with personal details
            template: EmailTemplate with placeholders
            attachments: Optional list of attachments
        """
        # Personalize content
        context = {
            'first_name': contact.first_name or 'Valued Customer',
            'last_name': contact.last_name or '',
            'email': contact.email,
            'company': contact.metadata.get('company', '')
        }
        
        subject = template.render_subject(context)
        html_content = template.render_html(context)
        text_content = template.render_text(context)
        
        return self.send_email(
            to_email=contact.email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            attachments=attachments
        )
