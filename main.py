import requests
import os
import sys
from twilio.rest import Client

print("=== Rain Alert Script Started ===")

# Get environment variables
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

print(f"OWM_API_KEY loaded: {bool(api_key)}")
print(f"ACCOUNT_SID loaded: {bool(account_sid)}")
print(f"AUTH_TOKEN loaded: {bool(auth_token)}")

# Validate environment variables
if not all([api_key, account_sid, auth_token]):
    print("ERROR: Missing environment variables!")
    sys.exit(1)

# Weather API parameters
weather_params = {
    "lat": 33.518589,
    "lon": -86.810356,
    "appid": api_key,
    "cnt": 4,
}

# Fetch weather data
try:
    print("Fetching weather data...")
    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()
    print("✓ Weather data retrieved successfully")
except Exception as e:
    print(f"✗ Weather API error: {e}")
    sys.exit(1)

# Check for rain
will_rain = False
print("Checking weather conditions...")
for i, hour_data in enumerate(weather_data["list"]):
    try:
        condition_code = hour_data["weather"][0]["id"]
        condition_desc = hour_data["weather"][0]["main"]
        print(f"  Hour {i}: Code={condition_code}, Description={condition_desc}")
        if int(condition_code) < 700:
            will_rain = True
    except (KeyError, IndexError) as e:
        print(f"  Hour {i}: Error parsing weather data: {e}")

print(f"Will rain: {will_rain}")

# Send SMS if rain detected
if will_rain:
    try:
        print("Sending SMS via Twilio...")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☔.",
            from_="+17252378952",
            to="+351963693017",
        )
        print(f"✓ Message sent! Status: {message.status}")
        print(f"  Message SID: {message.sid}")
    except Exception as e:
        print(f"✗ Twilio error: {e}")
        sys.exit(1)
else:
    print("No rain detected, message not sent")

print("=== Script Completed Successfully ===")
