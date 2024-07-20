import os
import numpy as np
import polars as pl

from src.utils import create_meteo_predictor
from pytz import timezone
from datetime import datetime, timedelta


def main():
    power = 5
    predictor = create_meteo_predictor()
    base_dt = datetime(year=2017, month=11, day=1, tzinfo=timezone("America/Detroit"))

    schema_overrides = {"DayNum": pl.Float64,
                        "Timestamp(ms)": pl.Float64,
                        "Latitude[deg]": pl.Float64,
                        "Longitude[deg]": pl.Float64,
                        "OAT[DegC]": pl.Float64,
                        "Speed Limit[km/h]": pl.String}

    folder = "data/eVED/"
    for file in os.listdir(folder):
        if not os.path.isdir(os.path.join("data/out", file)):
            print(file)
            week_df = pl.read_csv(f"{folder}{file}", schema_overrides=schema_overrides)

            work_df = week_df.select(["DayNum",
                                      "Timestamp(ms)",
                                      "Latitude[deg]",
                                      "Longitude[deg]"])
            temp_arr = work_df.to_numpy()
            pred_arr = np.zeros(temp_arr.shape[0])

            for i, (day_num, timestamp, lat, lon) in enumerate(temp_arr):
                dt = base_dt + timedelta(days=day_num - 1) + timedelta(milliseconds=timestamp)
                pred_arr[i] = predictor.predict(lat, lon, dt, power=power)

            temperature_df = week_df.with_columns(pl.Series(name="Temp[DegC]", values=pred_arr))
            temperature_df.write_csv(f"data/out/{file}")


if __name__ == "__main__":
    main()
