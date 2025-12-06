"""Module containing all of the URLs to scrape from"""
from dataclasses import dataclass
@dataclass
class NoaaURLs:
    LUNAR_BASE_URL = "https://www.timeanddate.com/moon/phases/?year="
    SOLAR_WIND_URL = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json"
    GEO_SCALES_URL = "https://services.swpc.noaa.gov/products/noaa-scales.json"
    SMAG_URL = "https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json"
    PLASMA_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
    RADIO_FLUX_URL = "https://services.swpc.noaa.gov/products/10cm-flux-30-day.json"
    KP_THREE_DAY_URL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    KP_PREDICTED_URL = "https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt"
    KP_HISTORICAL_URL = "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt"
    SOLAR_INDICES_URL = "https://services.swpc.noaa.gov/text/daily-solar-indices.txt"
    SUN_SPOTS_URL = "https://services.swpc.noaa.gov/json/sunspot_report.json"
