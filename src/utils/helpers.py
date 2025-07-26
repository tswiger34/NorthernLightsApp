def get_current_weather(api_key: str, location: str) -> dict:
    import requests

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def format_weather_data(weather_data: dict) -> str:
    location = weather_data['location']['name']
    temperature = weather_data['current']['temp_c']
    condition = weather_data['current']['condition']['text']
    return f"The current temperature in {location} is {temperature}°C with {condition}."

def send_alert(alert_message: str, user_contact: str) -> None:
    # Placeholder for alert sending logic (e.g., email, SMS)
    print(f"Sending alert to {user_contact}: {alert_message}")

def validate_location(location: str) -> bool:
    # Placeholder for location validation logic
    return bool(location) and isinstance(location, str) and len(location) > 0