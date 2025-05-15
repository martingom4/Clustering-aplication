# src/h3_cluster.py
import pandas as pd
import h3
from sklearn.cluster import DBSCAN

def h3_centroid(h3_index):
    # cell_to_latlng devuelve (lat, lon)
    lat, lon = h3.cell_to_latlng(h3_index)
    return (lon, lat)

def cluster_hexagons(df_h3, eps=0.01, min_samples=2):
    df = df_h3.compute() if hasattr(df_h3, "compute") else df_h3.copy()
    df["centroid"] = df["res_8"].apply(h3_centroid)
    coords = pd.DataFrame(df["centroid"].tolist(), columns=["lon", "lat"])
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(coords)
    df["cluster"] = labels
    return df
