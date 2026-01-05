import requests
from pydantic import BaseModel, Field
from typing import Dict, Any

class WeatherToolInput(BaseModel):
    location: str
    days: int = Field(3, ge=1, le=7)

def weather_tool_call(data: Dict[str, Any]) -> Dict[str, Any]:
    inp = WeatherToolInput(**data)

    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": inp.location, "count": 1},
        timeout=10
    ).json()

    place = geo["results"][0]
    lat, lon = place["latitude"], place["longitude"]

    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": inp.days,
            "timezone": "auto",
        },
        timeout=10
    ).json()

    return {"ok": True, "location": place["name"], "forecast": forecast["daily"]}
