import httpx
import pandas as pd
import numpy as np
from src.utils.data_urls import NoaaURLs
from src.utils.models import ThreeDayForecast, DayForecast


class NoaaScraper:
    def __init__(self):
        self.client = httpx.Client(
            base_url="https://services.swpc.noaa.gov",
        )
        self.urls = NoaaURLs()

    def get_kp_three_day(self) -> str:
        response = self.client.get(url=self.urls.KP_THREE_DAY_URL)
        response.raise_for_status()
        forecast = response.text
        return forecast

    def parse_kp_three_day(self, forecast: str) -> ThreeDayForecast:
        lines = forecast.splitlines()
        forecast_table_start = next(i for i, line in enumerate(lines) if "NOAA Kp index breakdown" in line)
        data_lines = lines[forecast_table_start + 2 : forecast_table_start + 11]
        date_parts = lines[forecast_table_start + 2].strip().split()
        dates = []
        for i in range(0, 5, 2):
            month = date_parts[i]
            day = date_parts[i + 1]
            full_date = f"{month}-{day}"
            dates.append(full_date)
        time_periods = []
        values = []
        for line in data_lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            for i in parts:
                if "(" in i:
                    parts.remove(i)
            time_periods.append(parts[0])
            values.append(parts[1:])
        values = values
        time_periods = time_periods

        return ThreeDayForecast(
            day_1=DayForecast(
                date=dates[0],
                time_00_03=values[0][0] if len(values[0]) > 0 else "",
                time_03_06=values[1][0] if len(values[1]) > 0 else "",
                time_06_09=values[2][0] if len(values[2]) > 0 else "",
                time_09_12=values[3][0] if len(values[3]) > 0 else "",
                time_12_15=values[4][0] if len(values[4]) > 0 else "",
                time_15_18=values[5][0] if len(values[5]) > 0 else "",
                time_18_21=values[6][0] if len(values[6]) > 0 else "",
                time_21_00=values[7][0] if len(values[7]) > 0 else "",
            ),
            day_2=DayForecast(
                date=dates[1],
                time_00_03=values[0][1] if len(values[0]) > 0 else "",
                time_03_06=values[1][1] if len(values[1]) > 0 else "",
                time_06_09=values[2][1] if len(values[2]) > 0 else "",
                time_09_12=values[3][1] if len(values[3]) > 0 else "",
                time_12_15=values[4][1] if len(values[4]) > 0 else "",
                time_15_18=values[5][1] if len(values[5]) > 0 else "",
                time_18_21=values[6][1] if len(values[6]) > 0 else "",
                time_21_00=values[7][1] if len(values[7]) > 0 else "",
            ),
            day_3=DayForecast(
                date=dates[2],
                time_00_03=values[0][2] if len(values[0]) > 0 else "",
                time_03_06=values[1][2] if len(values[1]) > 0 else "",
                time_06_09=values[2][2] if len(values[2]) > 0 else "",
                time_09_12=values[3][2] if len(values[3]) > 0 else "",
                time_12_15=values[4][2] if len(values[4]) > 0 else "",
                time_15_18=values[5][2] if len(values[5]) > 0 else "",
                time_18_21=values[6][2] if len(values[6]) > 0 else "",
                time_21_00=values[7][2] if len(values[7]) > 0 else "",
            ),
        )

    def get_historical_kps(self) -> str:
        resp = self.client.get(url=NoaaURLs().KP_HISTORICAL_URL)
        resp.raise_for_status()
        return resp.text

    def parse_historical_kps(self, historical_text: str) -> pd.DataFrame:
        """
        Parses the historical Kp data text and returns a pandas DataFrame.
        """
        lines = historical_text.splitlines()
        
        # Find the start of the data
        try:
            start_index = next(i for i, line in enumerate(lines) if "--- Planetary ---" in line) + 2
        except StopIteration:
            return pd.DataFrame() # Return empty dataframe if header not found

        data_lines = lines[start_index:]
        
        processed_data = []
        for line in data_lines:
            if not line.strip() or line.startswith("#"):
                continue
            
            parts = line.split()
            if len(parts) < 11: # Ensure there's enough data for date + k-values
                continue

            # Date is in the first 3 columns
            date = f"{parts[0]}-{parts[1]}-{parts[2]}"
            
            # Estimated Planetary K-indices are the last 8 values
            k_indices = parts[-8:]
            
            # Convert to numeric, setting invalid values like -1.00 to NaN
            numeric_k = [float(k) if k != "-1.00" else np.nan for k in k_indices]
            
            processed_data.append([date] + numeric_k)

        if not processed_data:
            return pd.DataFrame()

        columns = [
            "Date", "00-03", "03-06", "06-09", "09-12", 
            "12-15", "15-18", "18-21", "21-00"
        ]
        
        df = pd.DataFrame(processed_data, columns=columns)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
        
        return df


if __name__ == "__main__":
    scraper = NoaaScraper()
    # Test 3-day forecast
    forecast_text = scraper.get_kp_three_day()
    forecast_data = scraper.parse_kp_three_day(forecast=forecast_text)
    print("--- 3-Day Kp Forecast ---")
    print(forecast_data)
    print("\n" + "="*30 + "\n")
    
    # Test historical data
    historical_text = scraper.get_historical_kps()
    historical_df = scraper.parse_historical_kps(historical_text)
    print("--- Historical Kp Data ---")
    print(historical_df.tail()) # Print last 5 days for brevity
