import requests
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str
    days: int = Field(3, ge=1, le=7)

def weather_tool_call(data):
    inp = WeatherInput(**data)

    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": inp.location, "count": 1}
    ).json()

    place = geo["results"][0]
    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": inp.days,
            "timezone": "auto"
        }
    ).json()

    return {"ok": True, "location": place["name"], "forecast": forecast}
