# src/density_filter.py

import dask.dataframe as dd
from src.config import DENSITY_THRESHOLD


def filter_low_density(df):
    density = df.groupby("res_8").size()
    density = density.reset_index()
    density = density.rename(columns={0: "count"})

    valid_cells = density[density["count"] >= DENSITY_THRESHOLD][["res_8"]]

    df_filtered = df.merge(valid_cells, on="res_8", how="inner")

    return df_filtered
