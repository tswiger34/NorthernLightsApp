import requests
import pandas as pd
import logging
import time

logger = logging.getLogger(__name__)

class ForecastScraper:
    """
    This class scrapes data from the NOAA 3-day aurora forecast website

    Methods:
    - get_text: scrapes the website and writes the info to a text file
    - get_data: isolates the important data points in the text including the Kp index, dates, and times
    - create_df: turns the isolated data into a dataframe from analysis
    - main: 

    Args:
    - data_path: The root path for where to write the text file to, also the any other relevant data

    Attributes:
    - data_lines (list[str]): The lines of the text output containing relevant data
    - url (str): the url where the data is fetched from
    - text_output (str): the full text  output from webscraping
    - dates (list[str]): The dates in UTC being forecasted for
    - values (list[float]): The Kp values of the forecast
    - time_periods (list[str]): The three hour time periods in the forecast
    - text_path (str): the path
    """
    def __init__(self, data_path:str):
        self.url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'
        start_time = time.asctime()
        logger.info(f"Beginning Forecast Scraping at {start_time}")
        self.data_path = data_path

    def get_text(self) -> str:
        """
        This creates an https request to the NOAA forecast website and gets the text for the forecast

        Returns:
        - text_output (str): the text of the website

        Raises:
        - An exception if the response code is not 200
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            self.text_output = response.text
            text_path = f'{self.data_path}/kp_table.txt'
            with open(text_path, 'w') as f:
                f.writelines(self.text_output)

        else:
            logger.error(f"Failed to get Kp forecast data, returned status code: {response.status_code}")
            raise Exception("Failed to download the file. Status code:", response.status_code)
        return self.text_output
    
    def get_data(self) -> tuple[list[str], list[str], list[float], list[str]]:
        """
        This takes the text output, cleans it, and isolates the  dates, data_lines, values, and time_periods 
        to be transformed into a pandas data frame for further analysis.

        Returns:
        - tuple[list[str], list[str], list[float], list[str]]
            1. dates (list[str]): this is a list of strings for the dates being forecasted in UTC
            2. data_lines (list[str]): this is a list of the lines that contains the data
            3. values (list[float]): This is a list of the Kp indeces being stored as floats
            4. time_periods (list[str]): This is a list of the 3 hour time periods being forecasted for in UTC
        
        Raises:
        - Exception detailing the issue that occurred while running this method
        """
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
                for i in parts:
                    if '(' in i:
                        parts.remove(i)
                time_periods.append(parts[0])
                values.append(parts[1:])
            self.values = values
            self.time_periods = time_periods
            return self.dates, self.data_lines, self.values, self.time_periods
        
        except Exception as e: 
            logger.error(f"Failed to retrieve Kp forecast data in get_data method, failed with error: {e}")
            raise

    def create_df(self) -> pd.DataFrame:
        """
        This takes the outputs of the get_data method, and turns them into a pandas data frame

        Returns:
        - df (DataFrame): a pandas dataframe containing forecast data

        Raises:
        - Exception detailing the issue that occurred while running this method
        """
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
    
    def main(self) -> pd.DataFrame:
        """
        The main function the organizes all of the previous methods into one function that starts with scraping
        the forecast, and outputs a pandas DataFrame of the forecast
        """
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
    scraper = ForecastScraper('data')
    scraper.main()
