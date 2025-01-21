"""
This script will manage the alerts systems for both email and text alerts. 

Contact and alert preference info is input into the info.json file in the data folder following the template format.
Set TextAlerts and/or EmailAlerts to 1 if you would like to receive alerts through that medium. Enter your email and/or phone number in the designated location.

Class Args:
None

Class Returns:
None
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from utils.helpers import validate_string

# Load environment variables
logger = logging.getLogger(__name__)

class CreateAlerts:
    """
    This class handles sending the alerts to the user.

    Methods:
    - get_info: Gets the user preferences from the config/json file
    - email_alerts: constructs and sends the email to the user
    """
    def __init__(self, config_path):
        # Retrieve contact info/preferences
        try:
            with open(config_path, 'r') as f:
                self.contact_info = json.load(f)
                self.get_info()
        except FileNotFoundError:
            logger.error("User config file not found in the data directory.")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise

    def get_info(self):
        """
        Extract user preferences and contact details from the JSON file.
        """
        try:
            self.send_emails = self.contact_info.get("EmailAlerts", 0) == 1
            self.email = self.contact_info.get("Email") if self.send_emails else None

            self.send_texts = self.contact_info.get("TextAlerts", 0) == 1
            self.phone_number = self.contact_info.get("PhoneNumber") if self.send_texts else None
        except Exception as e:
            logger.error(f"Error getting contact info/preferences: {e}")
            raise

    def email_alerts(self, message):
        """
        Send an email alert to the user's registered email address.

        Args:
            message (str): Message body of the email
        """

        # Ensure self.email is not missing and that it is the correct data type
        validate_string(self.email, "Email in user config", logger=logger)
        
        try:
            sender_email = self.contact_info['Email']
            sender_password = self.contact_info['APP_PASS']
        except Exception as e:
            logger.error(f"Could not use user_config file due to error: {e}")
            raise

        # Send email alert
        try:
            # Setup the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = self.email
            msg['Subject'] = "Northern Lights Alert"

            msg.attach(MIMEText(message, 'plain'))
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", 587))

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                logger.info("starting email send")
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            logger.info(f"Email alert sent to {self.email}")

        except Exception as e:
            logger.error(f"Email alert raised error: {e}")
            raise