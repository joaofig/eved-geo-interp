import numpy as np

from typing import Dict
from datetime import datetime
from src.math import num_haversine
from pytz import timezone


def datetime_from_str(date_str: str, tz=timezone("America/Detroit")) -> datetime:
    year, month, day = date_str[:10].split("-")
    hour, minute = date_str[11:].split(":")
    return datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=tz)


class MeteoSource:
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 timestamps: list[datetime],
                 temperatures: list[float]):
        self._latitude = latitude
        self._longitude = longitude
        self._timestamps = np.array([ts.timestamp() for ts in timestamps])
        self._temperatures = np.array(temperatures)

    def get_temperature(self, timestamp: datetime) -> float:
        return float(np.interp(timestamp.timestamp(),
                               self._timestamps,
                               self._temperatures))

    def distance(self, latitude: float, longitude: float) -> float:
        return num_haversine(latitude, longitude,
                             self._latitude, self._longitude)

    @staticmethod
    def from_temp_source(temp_source: Dict) -> 'MeteoSource':
        latitude = temp_source['latitude']
        longitude = temp_source['longitude']
        tz = timezone(temp_source['timezone'])
        timestamps = [datetime_from_str(dt, tz=tz)
                      for dt in temp_source["hourly"]["time"]]
        temperatures = temp_source["hourly"]["temperature_2m"]
        return MeteoSource(latitude, longitude, timestamps, temperatures)


class MeteoPredictor:
    def __init__(self, sources: list[MeteoSource]):
        self._sources = sources

    def predict(self,
                latitude: float,
                longitude: float,
                timestamp: datetime,
                power: int = 1) -> float:
        temperatures = np.array([src.get_temperature(timestamp) for src in self._sources])
        distances = np.array([src.distance(latitude, longitude) for src in self._sources])

        dp = distances ** power
        num = np.sum(temperatures / dp)
        den = np.sum(1.0 / dp)
        return float(num / den)
