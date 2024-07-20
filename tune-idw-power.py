import numpy as np
import polars as pl

from datetime import datetime, timedelta
from pytz import timezone
from src.utils import create_meteo_predictor


def main():
    predictor = create_meteo_predictor()

    base_dt = datetime(year=2017, month=11, day=1, tzinfo=timezone("America/Detroit"))
    temp_df = pl.read_csv("data/temperatures.csv")

    rmse_arr = np.zeros(10, dtype=float)

    for power in range(1, 11):
        temp_arr = temp_df.to_numpy()
        pred_arr = np.zeros(temp_arr.shape[0])
        for i, (day_num, timestamp, lat, lon, oat, temp) in enumerate(temp_arr):
            # print(i, day_num, timestamp, lat, lon, oat, temp)
            dt = base_dt + timedelta(days=day_num - 1) + timedelta(milliseconds=timestamp)
            pred_arr[i] = predictor.predict(lat, lon, dt, power=power)

        final_df = temp_df.with_columns(pl.Series(name="Pred[DegC]", values=pred_arr))
        diff_arr = final_df.select(pl.col("Temp[DegC]", "Pred[DegC]")).to_numpy()
        rmse = float(np.sqrt(np.mean((diff_arr[:, 0] - diff_arr[:, 1]) ** 2)))

        print(f"Power: {power}, RMSE: {rmse}")
        rmse_arr[power-1] = rmse

    rmse_df = pl.DataFrame([pl.Series(name="Power", values=list(range(1, 11))),
                            pl.Series(name="RMSE", values=rmse_arr)])
    rmse_df.write_csv("data/out/power_tune.csv")


if __name__ == "__main__":
    main()
