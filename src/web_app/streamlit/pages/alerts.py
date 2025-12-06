import streamlit as st


def display_alerts(alerts):
    if alerts:
        for alert in alerts:
            st.subheader(alert["title"])
            st.write(alert["description"])
            st.write(f"Severity: {alert['severity']}")
            st.write(f"Date: {alert['date']}")
            st.markdown("---")
    else:
        st.write("No alerts available.")


def main():
    alerts = None
    display_alerts(alerts)


if __name__ == "__main__":
    main()
