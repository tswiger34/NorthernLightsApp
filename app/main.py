from datascraping.datascraper import *
from alerts.alert_manager import *
import schedule
import time
import pandas as pd
'''
This is the main functionality of the of the app

On init:
'''
class NLApp:
    def __init__(self) -> None:
        self.alerts = CreateAlerts()
        self.forecast_scraper = ForecastScraper()
        self.main()
    
    def kp_analysis(self, df: pd.DataFrame):
        cols = df.columns
        kp_dict = {}
        for col in cols:
            high_kp = []
            new_df = df.copy()
            day = col
            day_series = new_df[day]
            day_vals = day_series.values
            if day_vals.max() >= 2.67:
                for tr, val in day_series.items():
                    if val >= 2.67:
                        high_kp.append({tr:val})
            kp_dict.update({day:high_kp})
        return kp_dict
    
    def create_message(self, kp_dict: dict):
        days = kp_dict.keys()
        final_message = "Here is your Northern Lights report:\n"
        for day in days:
            kp_list = kp_dict.get(day)
            if kp_list is None:
                final_message = f"{final_message}There is no chance of seeing the Northern Lights on {day}.\n"
            else:
                final_message = f"{final_message}On {day} there will be a chance to see the Northern Lights!\n"
                final_message = f"{final_message}The Kp Index will be above 5.00 at these times:\n"
                for kp in kp_list:
                    time_range, kp_val = kp.items()
                    final_message = f"{final_message}At {time_range[0]} the Kp will be {kp_val[0]}.\n"
        return final_message

    def main(self):
        kp_df = self.forecast_scraper.main()
        kp_dict = self.kp_analysis(kp_df)
        message = self.create_message(kp_dict)
        self.alerts.email_alerts(message)
        print("Complete!")

if __name__ == 'main':
    NLApp.main()