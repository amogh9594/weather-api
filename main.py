from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI(
    title="My Free Weather API",
    description="Fetch current weather and 3-day forecast without needing any API key.",
    version="2.0.0"
)

WTTR_URL = "https://wttr.in"

# --- Current Weather Endpoint ---
@app.get("/weather")
def get_weather(city: str = Query(..., description="Name of the city")):
    """
    Fetch live current weather data for a given city using wttr.in
    """
    url = f"{WTTR_URL}/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": "Could not fetch weather data from wttr.in"}
            )

        data = response.json()
        current = data["current_condition"][0]

        weather_data = {
            "city": city.title(),
            "temperature_C": current["temp_C"],
            "feels_like_C": current["FeelsLikeC"],
            "weather_desc": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind_speed_kmph": current["windspeedKmph"],
            "pressure_mb": current["pressure"],
        }

        return weather_data

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --- 3-Day Forecast Endpoint ---
@app.get("/forecast")
def get_forecast(city: str = Query(..., description="Name of the city")):
    """
    Fetch 3-day weather forecast for a given city using wttr.in
    """
    url = f"{WTTR_URL}/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": "Could not fetch weather data from wttr.in"}
            )

        data = response.json()
        forecast_data = []

        for day in data["weather"][:3]:  # next 3 days
            forecast_data.append({
                "date": day["date"],
                "avg_temp_C": day["avgtempC"],
                "max_temp_C": day["maxtempC"],
                "min_temp_C": day["mintempC"],
                "sunrise": day["astronomy"][0]["sunrise"],
                "sunset": day["astronomy"][0]["sunset"],
                "hourly_summary": [
                    {
                        "time": hour["time"],
                        "temp_C": hour["tempC"],
                        "description": hour["weatherDesc"][0]["value"]
                    }
                    for hour in day["hourly"][::4]  # every ~6 hours
                ]
            })

        return {"city": city.title(), "forecast": forecast_data}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def home():
    return {
        "message": "Welcome to My Weather API 🌤️",
        "usage": {
            "current_weather": "/weather?city=CityName",
            "forecast": "/forecast?city=CityName"
        },
        "example": {
            "current_weather": "/weather?city=London",
            "forecast": "/forecast?city=London"
        }
    }
