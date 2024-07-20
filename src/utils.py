import os
import json
import numpy as np
import polars as pl

from src.models import MeteoPredictor, MeteoSource
from typing import List, Dict
from src.openmeteo import get_hist_temp


def get_temp_locations(files: str = "data/eVED/*.csv") -> np.ndarray:
    lf = (pl.scan_csv(files)
          .select([pl.col("Matchted Latitude[deg]").alias("lat"),
                   pl.col("Matched Longitude[deg]").alias("lon")]))
    loc_max = lf.max().collect().to_numpy()[0]
    loc_min = lf.min().collect().to_numpy()[0]
    loc_mid = (loc_min + loc_max) / 2
    locations = np.array([
        (loc_min[0], loc_min[1]),
        (loc_min[0], loc_mid[1]),
        (loc_min[0], loc_max[1]),
        (loc_mid[0], loc_min[1]),
        (loc_mid[0], loc_mid[1]),
        (loc_mid[0], loc_max[1]),
        (loc_max[0], loc_min[1]),
        (loc_max[0], loc_mid[1]),
        (loc_max[0], loc_max[1])
    ])
    return locations


def get_temp_sources(temp_locations: np.ndarray) -> List[Dict]:
    temp_sources = []
    date_min = "2017-11-01"
    date_max = "2018-12-01"
    for i, location in enumerate(temp_locations):
        filename = f"./data/openmeteo/location_{i}.json"
        if not os.path.exists(filename):
            temperatures = get_hist_temp(*location, start_date=date_min, end_date=date_max)
            with open(filename, "w") as f:
                f.write(json.dumps(temperatures))
        else:
            with open(filename, "r") as f:
                temperatures = json.loads(f.read())
        temp_sources.append(temperatures)
    return temp_sources


def create_meteo_predictor() -> MeteoPredictor:
    temp_sources = get_temp_sources(get_temp_locations())
    sources = [MeteoSource.from_temp_source(temp_src) for temp_src in temp_sources]
    return MeteoPredictor(sources)
