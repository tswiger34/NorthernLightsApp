from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
import time

logger = logging.getLogger(__name__)

class ForecastScraper:
    def __init__(self):
        self.url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'
        start_time = time.asctime()
        logger.info(f"Beginning Forecast Scraping at {start_time}")

    def get_text(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.text_output = response.text
            with open('data/kp_table.txt', 'w') as f:
                f.writelines(self.text_output)

        else:
            logger.error(f"Failed to get Kp forecast data, returned status code: {response.status_code}")
            raise Exception("Failed to download the file. Status code:", response.status_code)
        return self.text_output
    
    def get_data(self):
        try:
            lines = self.text_output.splitlines()
            # Get Dates
            start_line = next(i for i, line in enumerate(lines) if "NOAA Kp index breakdown" in line)
            self.data_lines = lines[start_line + 2:start_line + 11]
            date_parts = lines[start_line+2].strip().split()        
            dates = []
            for i in range(0, 5, 2):
                month = date_parts[i]
                day = date_parts[i+1]
                full_date = f'{month}-{day}'
                dates.append(full_date)
            self.dates = dates
            
            # Get time periods and values
            time_periods = []
            values = []
            for line in self.data_lines[1:]:
                # Skip empty lines
                if not line.strip():
                    continue
                # Seperate Values and Time Periods
                parts = line.split()
                time_periods.append(parts[0])
                values.append(parts[1:])
            self.values = values
            self.time_periods = time_periods
            return self.dates, self.data_lines, self.values, self.time_periods
        
        except Exception as e: 
            logger.error(f"Failed to retrieve Kp forecast data in get_data method, failed with error: {e}")
            raise

    def create_df(self):
        try:
            # Create DataFrame
            df = pd.DataFrame(self.values, columns=self.dates, index=self.time_periods)
            df.index.name = "Time Range"
            # Convert values to numeric
            df = df.apply(pd.to_numeric)
            return df

        except Exception as e:
            logger.error(f"Failed to convert forecast info to dataframe due to error: {e}")
            raise
    
    def check_data_shape(self):
        pass
    
    def main(self):
        try:
            text_output = self.get_text()
            dates, data_lines, values, time_periods = self.get_data()
            df = self.create_df()
            end_time = time.asctime()
            logger.info(f"Successfully retrieved Kp forecast data, finished at {end_time}")
            return df
        except Exception as e:
            logger.error(f"Failed during main function of datascraper due to error: {e}")

if __name__ == '__main__':
    scraper = ForecastScraper()
    scraper.main()