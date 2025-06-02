import pytest
from unittest.mock import patch, MagicMock
from app.services.email_service import EmailService
from app.models.contact import Contact
from app.models.template import EmailTemplate

@pytest.fixture
def mock_smtp():
    with patch('smtplib.SMTP') as mock:
        yield mock

def test_send_email_success(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    
    service = EmailService()
    result = service.send_email(
        "test@example.com",
        "Test Subject",
        "<html>Test</html>",
        "Test"
    )
    
    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()

def test_send_email_failure(mock_smtp):
    mock_smtp.return_value.__enter__.return_value.starttls.side_effect = Exception("SMTP Error")
    
    service = EmailService()
    result = service.send_email(
        "test@example.com",
        "Test Subject",
        "<html>Test</html>"
    )
    
    assert result is False
