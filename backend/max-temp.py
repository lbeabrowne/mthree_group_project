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

max_temp = -100
max_temp_city = ""

for city in uk_cities:
    try:
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": API_KEY,
            "q": city
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check that the city is in the UK
        if "current" in data and data["location"]["country"] == "United Kingdom":
            temp = data["current"]["temp_c"]
            if temp > max_temp:
                max_temp = temp
                max_temp_city = f"{data['location']['name']}, {data['location']['region']}"
    except Exception as e:
        print(f"Skipping {city} due to error: {e}")

print(f"Maximum Temp (C): {max_temp}")
print(f"City: {max_temp_city}")