import pytest
from data.data_aggregation.solarweather import SolarWeatherScraper

class TestClass:
    def __init__(self):
        pass

    def test_swind(self):
        scraper = SolarWeatherScraper()
        info = scraper.get_swind()
        assert type(info) == dict, "SWind did not return a dictionary"
        print("Swind Passed")

if __name__ == "__main__":
    test = TestClass()
    test.test_swind()