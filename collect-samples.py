import os
import time

import numpy as np
import polars as pl

from src.openmeteo import get_hist_temp
from src.models import MeteoSource
from datetime import datetime, timedelta
from pytz import timezone


def get_sample_df(folder="data/eVED/",
                  cache="data/samples.csv") -> pl.DataFrame:
    if os.path.exists(cache):
        sample_df = pl.read_csv(cache)
    else:
        temp_samples = [pl.read_csv(f"{folder}{file}",
                                    columns=["DayNum",
                                             "Timestamp(ms)",
                                             "Latitude[deg]",
                                             "Longitude[deg]",
                                             "OAT[DegC]"],
                                    schema_overrides={"DayNum": pl.Float64,
                                                      "Timestamp(ms)": pl.Float64,
                                                      "Latitude[deg]": pl.Float64,
                                                      "Longitude[deg]": pl.Float64,
                                                      "OAT[DegC]": pl.Float64})
                        .filter(pl.col("OAT[DegC]").is_not_nan())
                        .sample(n=50)
                        for file in os.listdir(folder)]
        sample_df = pl.concat(temp_samples, rechunk=True)
        sample_df.write_csv(cache)
    return sample_df


def get_temperature(dt: datetime,
                    latitude: float,
                    longitude: float) -> float:

    dt_ini = dt.date()
    dt_end = dt.date() + timedelta(days=1)
    date_ini = f"{dt_ini.year}-{dt_ini.month:02}-{dt_ini.day:02}"
    date_end = f"{dt_end.year}-{dt_end.month:02}-{dt_end.day:02}"

    source = get_hist_temp(latitude, longitude, date_ini, date_end)
    meteo_source = MeteoSource.from_temp_source(source)
    return meteo_source.get_temperature(dt)


def main():
    sample_df = get_sample_df()
    sample_arr = sample_df.to_numpy()

    base_dt = datetime(year=2017, month=11, day=1, tzinfo=timezone("America/Detroit"))
    t_arr = np.zeros(sample_arr.shape[0], dtype=np.float64)
    for i, sample in enumerate(sample_arr):
        day_num, timestamp, latitude, longitude, oat = sample
        dt = base_dt + timedelta(days=day_num - 1) + timedelta(milliseconds=timestamp)
        t = get_temperature(dt, latitude, longitude)

        t_arr[i] = t
        print(f"{dt}: {oat:.2f} / {t:.2f} [{i}]")

        if i % 100 == 0:
            print("Sleeping for 10 seconds...")
            time.sleep(10)

            # temperature_df = sample_df.with_columns(pl.Series(name="Temp[DegC]", values=t_arr))
            # temperature_df.write_csv("data/temperatures.csv")

    temperature_df = sample_df.with_columns(pl.Series(name="Temp[DegC]", values=t_arr))
    temperature_df.write_csv("data/temperatures.csv")


if __name__ == "__main__":
    main()
