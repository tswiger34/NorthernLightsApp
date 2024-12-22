import unittest
from unittest.mock import patch, mock_open, MagicMock
from app.alerts import CreateAlerts
import json

class TestCreateAlerts(unittest.TestCase):

    def setUp(self):
        """
        Set up common test data and mocks for each test.
        """
        self.mock_json_data = json.dumps({
            "EmailAlerts": 1,
            "Email": "user@example.com",
            "TextAlerts": 0,
            "PhoneNumber": None
        })
        self.mock_env = {
            "EMAIL_USER": "sender@example.com",
            "EMAIL_PASS": "password123",
            "SMTP_SERVER": "smtp.test.com",
            "SMTP_PORT": "587"
        }

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_missing_json_file(self, mock_file):
        """
        Test behavior when the JSON configuration file is missing.
        """
        mock_file.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            CreateAlerts()

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_invalid_json_format(self, mock_file):
        """
        Test behavior when the JSON configuration file contains invalid JSON.
        """
        with self.assertRaises(json.JSONDecodeError):
            CreateAlerts()

    @patch("builtins.open", new_callable=mock_open, read_data=mock_json_data)
    @patch.dict("os.environ", {}, clear=True)
    def test_missing_env_variables(self, mock_file):
        """
        Test behavior when required environment variables are missing.
        """
        with self.assertRaises(ValueError):
            alerts = CreateAlerts()
            alerts.email_alerts("Test message")

    @patch("builtins.open", new_callable=mock_open, read_data= self.mock_json_data)
    @patch.dict("os.environ", self.mock_env)
    def test_valid_initialization(self, mock_file):
        """
        Test successful initialization of the class.
        """
        alerts = CreateAlerts()
        self.assertEqual(alerts.email, "user@example.com")
        self.assertTrue(alerts.send_emails)
        self.assertFalse(alerts.send_texts)

    @patch("smtplib.SMTP", autospec=True)
    @patch("builtins.open", new_callable=mock_open, read_data=mock_json_data)
    @patch.dict("os.environ", mock_env)
    def test_email_alerts_success(self, mock_file, mock_smtp):
        """
        Test successful sending of an email alert.
        """
        alerts = CreateAlerts()
        mock_server = mock_smtp.return_value.__enter__.return_value

        alerts.email_alerts("Test message")

        mock_smtp.assert_called_once_with(self.mock_env["SMTP_SERVER"], int(self.mock_env["SMTP_PORT"]))
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.mock_env["EMAIL_USER"], self.mock_env["EMAIL_PASS"])
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_not_called()  # Ensured within `with` context

    @patch("smtplib.SMTP", autospec=True)
    @patch("builtins.open", new_callable=mock_open, read_data=mock_json_data)
    @patch.dict("os.environ", mock_env)
    def test_email_alerts_failure(self, mock_file, mock_smtp):
        """
        Test failure scenario for sending an email alert.
        """
        alerts = CreateAlerts()
        mock_smtp.return_value.__enter__.side_effect = Exception("SMTP Error")

        with self.assertRaises(Exception):
            alerts.email_alerts("Test message")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "EmailAlerts": 1,
        "Email": None,
        "TextAlerts": 1,
        "PhoneNumber": "1234567890"
    }))
    def test_invalid_email_in_json(self, mock_file):
        """
        Test behavior when email in JSON is invalid or missing.
        """
        alerts = CreateAlerts()
        with self.assertRaises(ValueError):
            alerts.email_alerts("Test message")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "EmailAlerts": 0,
        "Email": None,
        "TextAlerts": 0,
        "PhoneNumber": None
    }))
    def test_no_alerts_enabled(self, mock_file):
        """
        Test behavior when no alerts are enabled in JSON.
        """
        alerts = CreateAlerts()
        self.assertFalse(alerts.send_emails)
        self.assertFalse(alerts.send_texts)


if __name__ == "__main__":
    unittest.main()