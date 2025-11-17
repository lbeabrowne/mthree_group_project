import requests

API_KEY = "a7cbcd75e87343a788e115600251411"

# Include region info for ambiguous cities
uk_cities = [
    "Bath", "Birmingham", "Bradford", "Brighton & Hove", "Bristol", "Cambridge",
    "Canterbury", "Carlisle", "Chelmsford", "Chester", "Chichester", "Colchester",
    "Coventry", "Derby", "Doncaster", "Durham", "Ely", "Exeter", "Gloucester",
    "Hereford", "Kingston upon Hull", "Lancaster", "Leeds", "Leicester", "Lichfield",
    "Lincoln", "Liverpool", "London", "Manchester", "Milton Keynes", "Newcastle upon Tyne",
    "Norwich", "Nottingham", "Oxford", "Peterborough", "Plymouth", "Portsmouth",
    "Preston", "Ripon", "Salford", "Salisbury", "Sheffield", "Southampton",
    "Southend-on-Sea", "St Albans", "Stoke on Trent", "Sunderland", "Truro",
    "Wakefield", "Wells", "Westminster", "Winchester", "Wolverhampton", "Worcester",
    "York", "Armagh", "Bangor, Northern Ireland", "Belfast", "Lisburn", "Londonderry",
    "Newry", "Aberdeen", "Dundee", "Dunfermline", "Edinburgh", "Glasgow", "Inverness",
    "Perth", "Stirling", "Bangor, Wales", "Cardiff", "Newport, Wales", "St Asaph",
    "St Davids", "Swansea", "Wrexham"
]

# change this part so that user chooses date
date = "2025-11-21"

max_temp = -100
min_rain = 100
best_city = ""

for city in uk_cities:
    try:
        url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": API_KEY,
            "q": city,
            "dt": date,
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check that the city is in the UK
        if "forecast" in data and data["location"]["country"] == "United Kingdom":
            forecast_day = data["forecast"]["forecastday"][0]["day"]
            temp = forecast_day["maxtemp_c"] # max temperature
            rain = forecast_day["daily_chance_of_rain"] # percentage chance of rain

            if temp > max_temp and rain < min_rain :
                max_temp = temp
                min_rain = rain
                region = data["location"]["region"] or ""
                best_city = f"{data['location']['name']}, {region}" if region else data['location']['name']
    except Exception as e:
        print(f"Skipping {city} due to error: {e}")

print(f"On date: {date}")
print(f"Maximum Temp (C): {max_temp}")
print(f"Chance of Rain (%): {min_rain}")
print(f"Best City: {best_city}")