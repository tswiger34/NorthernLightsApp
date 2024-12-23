from datascraping.datascraper import *
url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'
scraper = ForecastScraper(url=url)
