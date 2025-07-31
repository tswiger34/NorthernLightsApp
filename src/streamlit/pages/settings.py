import streamlit as st

def settings_page():
    st.title("Settings")
    
    st.header("User Preferences")
    st.subheader("Notification Settings")
    email_notifications = st.checkbox("Enable Email Notifications", value=True)
    sms_notifications = st.checkbox("Enable SMS Notifications", value=False)
    
    st.subheader("Data Preferences")
    data_refresh_rate = st.selectbox("Select Data Refresh Rate", options=["1 Minute", "5 Minutes", "10 Minutes", "30 Minutes"])
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
        # Here you would typically save the settings to a database or a configuration file

if __name__ == "__main__":
    settings_page()