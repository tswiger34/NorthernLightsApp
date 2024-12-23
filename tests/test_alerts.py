import unittest
from unittest.mock import patch, mock_open, MagicMock
from app.alerts.alert_manager import CreateAlerts

# Mock JSON data
mock_json_data = '''
{
    "EmailAlerts": 1,
    "TextAlerts": 0,
    "Email": "test@example.com",
    "PhoneNumber": null
}
'''
mock_env = '''
{
    "EMAIL_USER": "test@example.com",
    "EMAIL_PASS": "mock_password",
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": "587"
}'''
class TestCreateAlerts(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=mock_json_data)
    def test_get_info(self, mock_file):
        alerts = CreateAlerts()
        self.assertTrue(alerts.send_emails)
        self.assertEqual(alerts.email, "test@example.com")
        self.assertFalse(alerts.send_texts)
        self.assertIsNone(alerts.phone_number)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_json_data)
    @patch("smtplib.SMTP")
    @patch.dict("os.environ", {"EMAIL_USER": "mock_user@example.com", "EMAIL_PASS": "mock_password"})
    def test_email_alerts(self, mock_smtp, mock_file):
        alerts = CreateAlerts()
        message = "This is a test alert."
        alerts.email_alerts(message)
        
        # Verify that the email was sent
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server = mock_smtp.return_value
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("mock_user@example.com", "mock_password")
        mock_server.send_message.assert_called_once()

if __name__ == "__main__":
    unittest.main()