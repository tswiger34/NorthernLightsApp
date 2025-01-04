import pytest
from data.data_aggregation.solarweather import SolarWeatherScraper

class TestClass:
    def __init__(self):
        self.scraper = SolarWeatherScraper()

    def test_swind(self):
        info = self.scraper.get_swind()
        assert type(info) == list, f"SWind did not return a list received: {type(info)}"
        assert len(info) > 0, "The list returned from the swind info URL was 0"

        print("Swind Passed")
    
    def test_smag(self):
        info = self.scraper.get_smag()
        assert type(info) == list, f"SMag did not return a list received: {type(info)}"
        assert len(info) > 0, "The list returned from the smag info URL was 0"

        print("Smag Passed")
    
    def test_plasma(self):
        info = self.scraper.get_plasma()
        assert type(info) == list, f"Plasma did not return a list received: {type(info)}"
        assert len(info) > 0, "The list returned from the plasma info URL was 0"
        
        print("Plasma Passed")

if __name__ == "__main__":
    test = TestClass()
    test.test_swind()
    test.test_smag()
    test.test_plasma()