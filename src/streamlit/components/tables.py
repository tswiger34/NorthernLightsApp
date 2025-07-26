from typing import List
import pandas as pd
import streamlit as st

def display_weather_data(data: List[dict]):
    if data:
        df = pd.DataFrame(data)
        st.write("### Weather Data")
        st.dataframe(df)
    else:
        st.write("No weather data available.")

def display_alerts(alerts: List[dict]):
    if alerts:
        df = pd.DataFrame(alerts)
        st.write("### Alerts")
        st.dataframe(df)
    else:
        st.write("No alerts available.")

def display_geo_weather_data(geo_data: List[dict]):
    if geo_data:
        df = pd.DataFrame(geo_data)
        st.write("### Geo-Weather Data")
        st.dataframe(df)
    else:
        st.write("No geo-weather data available.")