import requests

def weather_tool(data):
    location = data.get("location", "Chennai")
    days = data.get("days", 3)

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = requests.get(
        geo_url,
        params={"name": location, "count": 1},
        timeout=10,
    ).json()

    if not geo_resp.get("results"):
        return {"ok": False, "error": "Location not found"}

    place = geo_resp["results"][0]
    lat, lon = place["latitude"], place["longitude"]

    forecast_url = "https://api.open-meteo.com/v1/forecast"
    forecast = requests.get(
        forecast_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": days,
            "timezone": "auto",
        },
        timeout=10,
    ).json()

    return {
        "ok": True,
        "location": place["name"],
        "forecast": forecast.get("daily", {}),
    }
