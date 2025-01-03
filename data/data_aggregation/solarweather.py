import requests
import json
import pandas as pd

class SolarWeatherScraper:
    def __init__(self):
        self.swind_url = 'https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json'
        self.smag_url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json'
        self.plasma_url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'
        self.histkp_url = 'https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt'
        self.predkp_url = 'https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt'
        self.solarindeces_url = 'https://services.swpc.noaa.gov/text/daily-solar-indices.txt'
        self.geoscales_url = 'https://services.swpc.noaa.gov/products/noaa-scales.json'
        self.rf_url = 'https://services.swpc.noaa.gov/products/10cm-flux-30-day.json'
        self.sunspots_url = 'https://services.swpc.noaa.gov/json/sunspot_report.json'
    
    def get_swind(self) -> list:
        try:
            response = requests.get(self.swind_url)
            response.raise_for_status()
            info = response.json()
            self.swind_info = info
            return info
        except Exception as e:
            print("Returned with exception: ", e)
            return e
    
    def get_smag(self) -> list:
        try:
            response = requests.get(self.smag_url)
            response.raise_for_status()
            info = response.json()
            self.swind_info = info
            return info
        except Exception as e:
            pass
    
    def get_plasma(self) -> dict:
        try:
            response = requests.get(self.plasma_url)
            response.raise_for_status()
            info = response.json()
            self.swind_info = info
            return info
        except Exception as e:
            pass
    
    def get_histkp(self):
        try:
            response = requests.get(self.histkp_url)
            response.raise_for_status()
            output = response.text
            with open('data/TestCSVs/histkp.txt', 'w') as f:
                f.writelines(output)     
        except:
            pass
    
    def get_predictedkp(self):
        try:
            pass

        except:
            pass
    
    def clean_histkp(self) -> pd.DataFrame:
        def parse_k_values(section):
            """Parse the A and K values from a section."""
            values = [val for val in section.split('  ') if val]
            a_value = values[0]
            k_values = values[1].split()
            return a_value, k_values

        with open('data/TestCSVs/histkp.txt', 'r') as f:
            lines = f.readlines()

        dates = []
        mid_a, high_a, planet_a = [], [], []
        mid_k, high_k, planet_k = [[] for _ in range(8)], [[] for _ in range(8)], [[] for _ in range(8)]

        for line in lines[:-1]:
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


if __name__ == "__main__":
    scraper = SolarWeatherScraper()
    df = scraper.clean_histkp()
    print(df)