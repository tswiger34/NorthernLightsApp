import streamlit as st
from src.streamlit.pages.dashboards.solar_weather import three_day_forecast
from src.datascraping.noaa_scraper import NoaaScraper

# Set the title of the dashboard
st.title("Solar Weather Dashboard")

noaa_client = NoaaScraper()
forecast = noaa_client.get_kp_three_day()
parsed_forecast = noaa_client.parse_kp_three_day(forecast)
three_day_forecast.display_kp_forecast(data=parsed_forecast)
