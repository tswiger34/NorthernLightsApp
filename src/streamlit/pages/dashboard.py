import streamlit as st
import requests
import pandas as pd

# Set the title of the dashboard
st.title("Solar Weather Dashboard")

# Function to fetch weather data from the FastAPI backend
def fetch_weather_data():
    try:
        response = requests.get("http://localhost:8000/weather")  # Adjust the URL as needed
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

# Function to display weather data
def display_weather_data(data):
    if data:
        df = pd.DataFrame(data)
        st.write("### Weather Data", df)
    else:
        st.warning("No weather data available.")

# Fetch and display the weather data
weather_data = fetch_weather_data()
display_weather_data(weather_data)

# Placeholder for alerts management
st.sidebar.header("Alerts Management")
st.sidebar.write("Manage your alerts here.")  # Placeholder for future functionality

# Additional visualizations or components can be added below
st.write("### Additional Visualizations")
# Placeholder for charts or other visual components