import streamlit as st
import requests

def main():
    st.title("Northern Lights Alerts")
    
    menu = ["Dashboard", "Alerts", "Settings"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Dashboard":
        display_dashboard()
    elif choice == "Alerts":
        manage_alerts()
    elif choice == "Settings":
        user_settings()

def display_dashboard():
    st.header("Dashboard")
    st.write("Fetching data")
    
    response = requests.get("http://localhost:8000/api/weather")
    if response.status_code == 200:
        weather_data = response.json()
        st.json(weather_data)
    else:
        st.error("Failed to fetch weather data.")

def manage_alerts():
    st.header("Manage Alerts")
    st.write("Here you can view and manage your alerts.")
    
    # Example API call to fetch alerts
    response = requests.get("http://localhost:8000/api/alerts")
    if response.status_code == 200:
        alerts = response.json()
        for alert in alerts:
            st.write(alert)
    else:
        st.error("Failed to fetch alerts.")

def user_settings():
    st.header("User Settings")
    st.write("Adjust your preferences here.")
    
    with st.form("settings_form"):
        st.text_input("Username")
        st.text_input("Email")
        submit_button = st.form_submit_button("Save Settings")
        
        if submit_button:
            st.success("Settings saved!")

if __name__ == "__main__":
    main()