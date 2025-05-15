# src/h3_to_polygons.py
import h3
from shapely.geometry import Polygon

def h3_to_polygon(h3_index):
    # cell_to_boundary devuelve lista de (lat, lon)
    boundary = h3.cell_to_boundary(h3_index)
    # Shapely espera (x, y) = (lon, lat)
    return Polygon([(lon, lat) for lat, lon in boundary])

def attach_geometry(df_h3):
    df = df_h3.copy()
    df["geometry"] = df["res_8"].apply(h3_to_polygon)
    return df
