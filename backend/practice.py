import requests

API_KEY = "a7cbcd75e87343a788e115600251411"
city = "New York"

url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

response = requests.get(url)
data = response.json()

print("City:", data["location"]["name"])
print("Temperature (C):", data["current"]["temp_c"])
print("Condition:", data["current"]["condition"]["text"])