# for current weather

import requests

API_KEY = "a7cbcd75e87343a788e115600251411"
city = "New York"

url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

response = requests.get(url)
data = response.json()

print("City:", data["location"]["name"])
print("Temperature (C):", data["current"]["temp_c"])
print("Condition:", data["current"]["condition"]["text"])

# for forecast

import requests

API_KEY = "8d69cc8d4b80497eb68134844251711"
city = "New York"
date = "2025-11-20"  # format: YYYY-MM-DD

# Fetch forecast for the specific date
url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&dt={date}"
response = requests.get(url)
data = response.json()

# Access forecast for the given date
forecast = data["forecast"]["forecastday"][0]["day"]

print("City:", data["location"]["name"])
print("Date:", date)
print("Max Temperature (C):", forecast["maxtemp_c"])
print("Chance of Rain (%):", forecast["daily_chance_of_rain"])
print("Condition:", forecast["condition"]["text"])