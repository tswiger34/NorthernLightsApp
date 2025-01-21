import requests
import pandas as pd
from typing import Dict
import json

class SolarWeatherScraper:
    def __init__(self):
        self.url_dict = {
        'SWind':'https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json',
        'SMag':'https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json',
        'Plasma':'https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json',
        'HistKp':'https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt',
        'PredictedKp':'https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt',
        'SolarIndeces':'https://services.swpc.noaa.gov/text/daily-solar-indices.txt',
        'GeoScales':'https://services.swpc.noaa.gov/products/noaa-scales.json',
        'RadioFlux':'https://services.swpc.noaa.gov/products/10cm-flux-30-day.json',
        'SunSpots':'https://services.swpc.noaa.gov/json/sunspot_report.json'
        }
        self.main()

    def get_json_urls(self, url: str, name: str) -> dict:
        """
        Fetches JSON data from a URL and saves it to a file.

        Args:
            url (str): The URL to fetch the JSON data from.
            name (str): The name of the file to save the JSON data to.

        Returns:
            dict: The parsed JSON data as a Python dictionary.

        Raises:
            Exception: Propagates exceptions from failed requests or JSON operations.
        """
        try:
            # Fetch the JSON data
            response = requests.get(url)
            response.raise_for_status()
            output = response.json()
            
            # Save JSON data to a file
            file_path = f'data/TestCSVs/{name}.json'
            with open(file_path, 'w') as f:
                json.dump(output, f, indent=4)  # Use indent=4 for pretty formatting
            
            return output
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            raise  # Re-raise the exception to propagate it
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {json_err}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def get_txt_urls(self, url: str, name: str) -> str:
        """
        Fetches text data from a URL and saves it to a file.

        Args:
            url (str): The URL to fetch the text data from.
            name (str): The name of the file to save the text data to.

        Returns:
            str: The text content retrieved from the URL.

        Raises:
            Exception: Propagates exceptions from failed requests or file operations.
        """
        try:
            # Fetch the text data
            response = requests.get(url)
            response.raise_for_status()
            output = response.text
            
            # Save the text data to a file
            file_path = f'data/TestCSVs/{name}.txt'
            with open(file_path, 'w') as f:
                f.write(output)  # Write the string directly
            
            return output
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            raise  # Re-raise the exception to propagate it
        except IOError as io_err:
            print(f"File writing error: {io_err}")
            raise

    
    def main(self):
        try:
            for name, url in self.url_dict.items():
                if url[-5:] == '.json':
                    self.get_json_urls(url, name)
                elif url[-4:] == '.txt':
                    self.get_txt_urls(url, name)
                else:
                    raise ValueError("Invalid URL passed")
        except Exception as e:
            print(e)

class SolarWeatherCleaner:
    def __init__(self):
        predicted_kp_file_path = 'data/TestCSVs/PredicctedKp.txt'
        with open(predicted_kp_file_path, 'r') as f:
            predicted_kp_lines = f.readlines()
        self.predicted_kp_lines = predicted_kp_lines
        self.search_strings = [
            ':Prediction_dates:',
            '# Predicted 3-hour Middle latitude k-indices',
            '# Predicted 3-hour High latitude k-indices',
            '# Probability of Geomagnetic conditions at Middle Latitude',
            '# Probability of Geomagnetic conditions at High Latitude',
            ':Polar_cap:',
            ':10cm_flux:',
            ':Whole_Disk_Flare_Prob:',
            '# Region Flare Probabilities for'
        ]
        self.line_numbers = self.find_line_numbers('data/TestCSVs/predictedkp.txt')
        self.prediction_dates = self.get_predicted_dates()
        # Get Lines
    def find_line_numbers(self, file_path: str) -> dict:
        """Find the line numbers for the given search strings in a file."""
        self.line_numbers = {string: None for string in self.search_strings}
        
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                for string in self.search_strings:
                    if string in line and self.line_numbers[string] is None:
                        self.line_numbers[string] = line_number
        
        return self.line_numbers    
    
    def get_predicted_dates(self) -> list:
     
        # Get Dates
        date_vals = self.predicted_kp_lines[int(self.line_numbers.get(':Prediction_dates:'))-1].split('   ')
        dates = []
        for date in date_vals[-3:]:
            dates.append(date[:11])
        self.prediction_dates = dates
        return dates
        
    def clean_predictions_kp(self, line_id:int, start_add:int, end_add:int):        
        # Initialize value lists
        times = []
        day_1_vals = []
        day_2_vals = []
        day_3_vals = []
        
        # Identify and append prediction values 
        prediction_table = self.predicted_kp_lines[int(self.line_numbers.get(self.search_strings[line_id]))+start_add:int(self.line_numbers.get(self.search_strings[line_id]))+end_add]
        for line in prediction_table:
            vals = line.split('             ')
            times.append(vals[0].split('/')[1])
            day_1_vals.append(int(vals[1]))
            day_2_vals.append(int(vals[2]))
            day_3_vals.append(int(vals[3]))
        prediction_df =  pd.DataFrame({
            'Times': times,
            f'{self.prediction_dates[0]}':day_1_vals,
            f'{self.prediction_dates[1]}': day_2_vals,
            f'{self.prediction_dates[2]}': day_3_vals
        })

        return prediction_df 
    
    def clean_magstorm_predictions(self, line_id:int, start_add:int, end_add:int):
        # Initialize value lists
        storm_levels = []
        day_1_vals = []
        day_2_vals = []
        day_3_vals = []    

        # Identify and append prediction values 
        prediction_table = self.predicted_kp_lines[int(self.line_numbers.get(self.search_strings[line_id]))+start_add:int(self.line_numbers.get(self.search_strings[line_id]))+end_add]
        for line in prediction_table:
            vals = line[25:].split('           ')
            storm_levels.append(line[:25].split('/')[1])
            day_1_vals.append(int(vals[0]))
            day_2_vals.append(int(vals[1]))
            day_3_vals.append(int(vals[2]))
        prediction_df =  pd.DataFrame({
            'StormLevels': storm_levels,
            f'{self.prediction_dates[0]}':day_1_vals,
            f'{self.prediction_dates[1]}': day_2_vals,
            f'{self.prediction_dates[2]}': day_3_vals
        })

        return prediction_df
    
    def clean_histkp(self) -> pd.DataFrame:
        def parse_k_values(section:str):
            """Parse the A and K values from a section."""
            values = [val for val in section.split('  ') if val]
            a_value = values[0]
            k_values = values[1].split()
            return a_value, k_values

        dates = []
        mid_a, high_a, planet_a = [], [], []
        mid_k, high_k, planet_k = [[] for _ in range(8)], [[] for _ in range(8)], [[] for _ in range(8)]

        for line in self.predicted_kp_lines[:-1]:
            parts = line.split('   ')
            if len(parts) == 5:
                # Process date
                dates.append(parts[0].replace(' ', '-'))

                # Process Mid-latitude values
                mid_a_val, mid_k_vals = parse_k_values(parts[1])
                mid_a.append(int(mid_a_val))
                for i, val in enumerate(mid_k_vals):
                    mid_k[i].append(int(val))

                # Process High-latitude values
                high_a_val, high_k_vals = parse_k_values(parts[2])
                high_a.append(int(high_a_val))
                for i, val in enumerate(high_k_vals):
                    high_k[i].append(int(val))

                # Process Planetary values
                planet_a.append(int(parts[3]))
                for i, val in enumerate(parts[4].split()):
                    planet_k[i].append(float(val))

        # Create dictionary for DataFrame
        vals_dict = {
            'Date': dates,
            'MidLatA': mid_a,
            **{f'MidK{hour:02d}': mid_k[i] for i, hour in enumerate(range(0, 24, 3))},
            'HighLatA': high_a,
            **{f'HighK{hour:02d}': high_k[i] for i, hour in enumerate(range(0, 24, 3))},
            'PlanetA': planet_a,
            **{f'PlanetK{hour:02d}': planet_k[i] for i, hour in enumerate(range(0, 24, 3))},
        }

        return pd.DataFrame(vals_dict)
    
    def get_absorbtion(self) -> str:
        absorbtion = self.predicted_kp_lines[int(self.line_numbers.get(self.search_strings[5]))]
        return absorbtion.strip()
    
    def get_flux(self) -> pd.DataFrame:
        rf_vals = self.predicted_kp_lines[int(self.line_numbers.get(self.search_strings[6]))]
        rf_vals = rf_vals[len('                      '):]
        rf_vals = rf_vals.split('           ')
        
        for i in range(len(rf_vals)):
            rf_vals[i] = int(rf_vals[i].strip())
        df = pd.DataFrame({
            f'{self.prediction_dates[0]}': [rf_vals[0]],
            f'{self.prediction_dates[1]}': [rf_vals[1]],
            f'{self.prediction_dates[2]}': [rf_vals[2]]
        })
        return df
    
    def clean_flare_probs(self):
        flare_probs = self.predicted_kp_lines[int(self.line_numbers.get(self.search_strings[7])):int(self.line_numbers.get(self.search_strings[7]))+3]
        flare_classes = []
        prob_day_1 = []
        prob_day_2 = []
        prob_day_3 = []
        for line in flare_probs:
            flare_class = line[:len('Class_M                  ')].strip()
            flare_classes.append(flare_class)
            probs = line[len('Class_M                  '):].strip().split()
            print(probs)
            prob_day_1.append(int(probs[0].strip()))
            prob_day_2.append(int(probs[1].strip()))
            prob_day_3.append(int(probs[2].strip()))
        data_dict = {
            'FlareClasss':flare_classes,
            f'{self.prediction_dates[0]}': prob_day_1,
            f'{self.prediction_dates[1]}': prob_day_2,
            f'{self.prediction_dates[2]}': prob_day_3
        }
        return pd.DataFrame(data_dict)

if __name__ == "__main__":
    scraper = SolarWeatherScraper()
    cleaner = SolarWeatherCleaner()
    mid_lat_kp = cleaner.clean_predictions_kp(1,1,9)
    print(mid_lat_kp)
    high_lat_kp = cleaner.clean_predictions_kp(2,1,9)
    print(high_lat_kp)
    mid_lat_storm = cleaner.clean_magstorm_predictions(3,1,4)
    print(mid_lat_storm)
    high_lat_storm = cleaner.clean_magstorm_predictions(4,1,4)
    print(high_lat_storm)
    absorbtion = cleaner.get_absorbtion()
    print(absorbtion)
    rf_vals = cleaner.get_flux()
    print(rf_vals)
    flare_df = cleaner.clean_flare_probs()
    print(flare_df)