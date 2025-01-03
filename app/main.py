from datascraping.datascraper import *
from alerts.alert_manager import *
from utils.logging_config import *
from gui.setupwizard import *
import pandas as pd
import tkinter as tk
import os
import json


'''
This is the main functionality of the of the app

On init:
'''
logger = setup_logging()
class NLApp:
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
    
    def kp_analysis(self, df: pd.DataFrame):
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
    
    def create_message(self, kp_dict: dict):
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
        kp_df = self.forecast_scraper.main()
        kp_dict = self.kp_analysis(kp_df)
        message = self.create_message(kp_dict)
        self.alerts.email_alerts(message)
        logger.info("Successfully completed run of main NLApp method")

if __name__ == "__main__":
    alerts = NLApp()