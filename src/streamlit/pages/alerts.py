import streamlit as st
import requests

def fetch_alerts():
    response = requests.get("http://localhost:8000/api/alerts")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch alerts.")
        return []

def display_alerts(alerts):
    if alerts:
        for alert in alerts:
            st.subheader(alert['title'])
            st.write(alert['description'])
            st.write(f"Severity: {alert['severity']}")
            st.write(f"Date: {alert['date']}")
            st.markdown("---")
    else:
        st.write("No alerts available.")

def main():
    st.title("Weather Alerts")
    alerts = fetch_alerts()
    display_alerts(alerts)

if __name__ == "__main__":
    main()