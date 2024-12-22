from bs4 import BeautifulSoup
import requests
import pandas as pd

class forecast_scraper:
    def __init__(self, url) -> None:
        self.url = url
        return None

    def get_text(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.text_output = response.text
        else:
            raise Exception("Failed to download the file. Status code:", response.status_code)
        return self.text_output
    
    def get_data(self):
        try:
            lines = self.text_output.splitlines()
            # Get Dates
            start_line = next(i for i, line in enumerate(lines) if "NOAA Kp index breakdown" in line)
            self.data_lines = lines[start_line + 2:start_line+11]
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

            # Ensure data shape is correct
            assert len(dates) == 3
            assert len(self.data_lines) == 8
            assert len(self.values) == 8
            assert len(self.time_periods) == 8
            return self.dates, self.data_lines, self.values, self.time_periods
        except:
            print('Failed')

    def create_df(self):
        try:
            # Create DataFrame
            df = pd.DataFrame(self.values, columns=self.dates, index=self.time_periods)
            df.index.name = "Time Range"

            # Convert values to numeric
            df = df.apply(pd.to_numeric)
            print(df)

            assert df.shape == (4,9)
        except:
            print('Failed')
    
    def main(self):
        try:
            text_output = self.get_text()
            dates, data_lines, values, time_periods = self.get_data()
            df = self.create_df()
            return df
        except:
            print('Failed')