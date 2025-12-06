import bcrypt


def get_current_weather(api_key: str, location: str) -> dict:
    import requests

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def format_weather_data(weather_data: dict) -> str:
    location = weather_data["location"]["name"]
    temperature = weather_data["current"]["temp_c"]
    condition = weather_data["current"]["condition"]["text"]
    return f"The current temperature in {location} is {temperature}°C with {condition}."


def send_alert(alert_message: str, user_contact: str) -> None:
    # Placeholder for alert sending logic (e.g., email, SMS)
    print(f"Sending alert to {user_contact}: {alert_message}")


def validate_location(location: str) -> bool:
    # Placeholder for location validation logic
    return bool(location) and isinstance(location, str) and len(location) > 0


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password to hash

    Returns:
        str: Hashed password
    """
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password to check against

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
