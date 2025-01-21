from datascraping.datascraper import *
from alerts.alert_manager import *
from utils.logging_config import *
from gui.setupwizard import *
import pandas as pd
import tkinter as tk
import os
import json

logger = setup_logging()
class NLApp:
    """
    This is the main class for the app, it orchestrates the web scraper, alerts manager, and setup wizard.
    It then analyzes the forecast data, and creates the email message body for the alert.

    Methods:
    - kp_analysis: analyzes the data frame containing the forecasted data and decides if/when the Northern Lights will be visible
    - create message: Uses the dates and times when the Northern Lights will be visible to create a report to be used in the email alerts 
    - main: Runs all of the necessary components

    Attributes:
    - app_dir (str): The root directory where to store/run the app
    - data_path (str): The root directory where to strore the data
    - config_path (str): The file path for the user config file
    - alerts (CreateAlerts): An instance of the CreateAlerts class for sending the alerts 
    - forecast_scraper (ForecastScraper): An instance of the ForecastScraper class for fetching the data from NOAA
    """
    def __init__(self) -> None:
        self.app_dir = os.path.expanduser(r"~\.northern_lights_alert")
        self.data_path = os.path.join(self.app_dir, "data")
        self.config_path = os.path.join(self.app_dir, r"data\user_config.json")
        if not os.path.exists(self.config_path):
            SetupWizard()
            self.alerts = CreateAlerts(self.config_path)
            self.forecast_scraper = ForecastScraper(self.data_path)
            self.main()
        else:
            self.alerts = CreateAlerts(self.config_path)
            self.forecast_scraper = ForecastScraper(self.data_path)
            self.main()
    
    def kp_analysis(self, df: pd.DataFrame) -> dict:
        """
        This method analyzes the Kp index data, and uses if-else logic to determine if the northern lights
        will be visible.

        Args:
        - df (DataFrame): a pandas DataFrame containing the forecast data

        Returns:
        - kp_dict (dict): Returns a dictionary of all the dates and times when the Northen Lights may be visible
        """
        try:
            cols = df.columns
            kp_dict = {}
            for col in cols:
                high_kp = []
                new_df = df.copy()
                day = col
                day_series = new_df[day]
                day_vals = day_series.values
                if day_vals.max() >= 5.00:
                    for i in day_series.items():
                        val = i[1]
                        tr = i[0]
                        if val >= 5.00:
                            high_kp.append({tr:val})
                kp_dict.update({day:high_kp})
            return kp_dict
        except Exception as e:
            logger.error(f"Failed to create the kp_dict in the kp_analysis method due to: {e}")
            raise
    
    def create_message(self, kp_dict: dict) -> str:
        """
        Creates the message body for the alert email.

        Args:
        - kp_dict (dict): The dictionary output from kp_analysis method

        Returns
        - final_message (str): The message body of the email alert
        """
        try:
            days = kp_dict.keys()
            final_message = "Here is your Northern Lights report:\n"
            for day in days:
                kp_list = kp_dict.get(day)
                if len(kp_list) == 0:
                    final_message = f"{final_message}There is no chance of seeing the Northern Lights on {day}.\n"
                else:
                    final_message = f"{final_message}On {day} there will be a chance to see the Northern Lights!\n"
                    final_message = f"{final_message}The Kp Index will be above 5.00 at these times:\n"
                    for kp in kp_list:
                        tr = list(kp.keys())[0]
                        final_message = f"{final_message}At {tr} the Kp will be {kp.get(tr)}.\n"
            return final_message
        except Exception as e:
            logger.error(f"Failed to create the message body in the create_message method due to: {e}")
            raise

    def main(self):
        """
        Runs everything together
        """
        kp_df = self.forecast_scraper.main()
        kp_dict = self.kp_analysis(kp_df)
        message = self.create_message(kp_dict)
        self.alerts.email_alerts(message)
        logger.info("Successfully completed run of main NLApp method")

if __name__ == "__main__":
    alerts = NLApp()