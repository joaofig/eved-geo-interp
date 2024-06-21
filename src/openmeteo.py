import requests

from typing import List, Dict


def get_hist_weather(lat: float, lng: float,
                     start_date: str, end_date: str,
                     hourly: List[str] = None,
                     daily: List[str] = None,
                     timezone: str = "auto") -> Dict:
    url = "https://archive-api.open-meteo.com/v1/archive"
    url_params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": hourly,
        "daily": daily,
        "timezone": timezone
    }
    response = requests.get(url, params=url_params)
    return response.json()


def get_hist_temp(lat: float, lng: float,
                  start_date: str, end_date: str,
                  timezone: str = "auto") -> Dict:
    return get_hist_weather(lat, lng, start_date, end_date,
                            hourly=["temperature_2m"], daily=[],
                            timezone=timezone)
