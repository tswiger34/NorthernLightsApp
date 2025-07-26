import streamlit as st
import pandas as pd
import plotly.express as px

def plot_line_chart(data: pd.DataFrame, title: str, x_col: str, y_col: str):
    """Plots an interactive line chart using Plotly."""
    fig = px.line(data, x=x_col, y=y_col, title=title, markers=True)
    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)
    st.plotly_chart(fig, use_container_width=True)

def plot_bar_chart(data: pd.DataFrame, title: str, x_col: str, y_col: str):
    """Plots an interactive bar chart using Plotly."""
    fig = px.bar(data, x=x_col, y=y_col, title=title)
    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)
    st.plotly_chart(fig, use_container_width=True)

def plot_pie_chart(data: pd.Series, title: str):
    """Plots an interactive pie chart using Plotly."""
    fig = px.pie(values=data.values, names=data.index, title=title)
    st.plotly_chart(fig, use_container_width=True)

def display_weather_charts(weather_data: pd.DataFrame):
    st.header("Weather Data Charts")
    
    if not weather_data.empty:
        st.subheader("Temperature Over Time")
        plot_line_chart(weather_data, "Temperature Over Time", "Date", "Temperature")
        
        st.subheader("Precipitation Distribution")
        plot_bar_chart(weather_data, "Precipitation Distribution", "Date", "Precipitation")
        
        st.subheader("Weather Condition Distribution")
        condition_counts = weather_data['Condition'].value_counts()
        plot_pie_chart(condition_counts, "Weather Condition Distribution")
    else:
        st.warning("No weather data available to display charts.")