from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def find_best_city(date: str):
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

            if "forecast" in data and data["location"]["country"] == "United Kingdom":
                forecast_day = data["forecast"]["forecastday"][0]["day"]
                temp = forecast_day["maxtemp_c"]
                rain = forecast_day["daily_chance_of_rain"]

                if temp > max_temp and rain < min_rain:
                    max_temp = temp
                    min_rain = rain
                    region = data["location"]["region"] or ""
                    best_city = (
                        f"{data['location']['name']}, {region}"
                        if region
                        else data["location"]["name"]
                    )
        except Exception as e:
            print(f"Skipping {city} due to error: {e}")

    return {
        "date": date,
        "max_temp": max_temp,
        "min_rain": min_rain,
        "best_city": best_city,
    }


@app.get("/best-city")
def best_city_endpoint(date: str):
    if not date:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'date' is required, e.g. /best-city?date=2025-11-21",
        )

    result = find_best_city(date)

    if not result["best_city"]:
        raise HTTPException(status_code=404, detail="No suitable city found")

    return result