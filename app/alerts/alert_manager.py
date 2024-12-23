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
from dotenv import load_dotenv
import os
import logging
from utils.helpers import validate_string

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

class CreateAlerts:
    def __init__(self):
        # Retrieve contact info/preferences
        try:
            with open('data/info.json', 'r') as f:
                self.contact_info = json.load(f)
                self.get_info()
        except FileNotFoundError:
            logger.error("info.json file not found in the data directory.")
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
        validate_string(self.email, "Email in info.json", logger=logger)
        
        # Retrieve sensitive email info from .env file
        try:
            # Get Email credentials
            sender_email = os.getenv("EMAIL_USER")
            sender_password = os.getenv("APP_PASS")
            # Ensure sender email and password are retrieved in correct format and are not missing
            validate_string(sender_email, "Sender Email from .env", logger=logger)
            validate_string(sender_password, "Sender Email Password from .env", logger=logger)

        except Exception as e:
            logger.error(f"Error retrieving sender email info from .env: {e}")
            print(f"Error retrieving sender email info from .env: {e}")
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
                print("starting email send")
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            logger.info(f"Email alert sent to {self.email}")

        except Exception as e:
            logger.error(f"Email alert raised error: {e}")
            raise