import requests
from bs4 import BeautifulSoup
import json

class SolarWeatherScraper:
    def __init__(self):
        self.swind_url = 'https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json'
        self.smag_url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json'
        self.plasma_url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'
        self.histkp_url = 'https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt'
        self.fckp_url = 'https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt'
        self.solarindeces_url = 'https://services.swpc.noaa.gov/text/daily-solar-indices.txt'
        self.geoscales_url = 'https://services.swpc.noaa.gov/products/noaa-scales.json'
        self.rf_url = 'https://services.swpc.noaa.gov/products/10cm-flux-30-day.json'
        self.sunspots_url = 'https://services.swpc.noaa.gov/json/sunspot_report.json'
    
    def get_swind(self) -> dict:
        try:
            response = requests.get(self.swind_url)
            with open(response, 'r') as f:
                info = json.loads(f)
            self.swind_info = info
            return info
        except Exception as e:
            pass
    
    def get_smag(self) -> dict:
        try:
            response = requests.get(self.smag_url)
            with open(response, 'r') as f:
                info = json.loads(f)
            self.smag_info = info
            return info
        except Exception as e:
            pass
    
    def get_smag(self) -> dict:
        try:
            response = requests.get(self.plasma_url)
            with open(response, 'r') as f:
                info = json.loads(f)
            self.plasma_info = info
            return info
        except Exception as e:
            pass