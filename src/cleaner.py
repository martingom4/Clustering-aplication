# src/cleaner.py

import dask.dataframe as dd

def clean_data(df):
    df = df.dropna(subset=["latitude", "longitude", "dt_pos_utc", "mmsi", "nav_status"])
    df = df[(df["latitude"] >= -90) & (df["latitude"] <= 90)]
    df = df[(df["longitude"] >= -180) & (df["longitude"] <= 180)]

    df["dt_pos_utc"] = dd.to_datetime(df["dt_pos_utc"], errors="coerce")
    df = df.dropna(subset=["dt_pos_utc"])

    return df
