import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, MarkerCluster


def create_interactive_map(gdf_hulls, df_points, color_map,
                           start_zoom=8, tiles="CartoDB Positron"):
    """
    Devuelve un objeto folium.Map con:
      - Capa de polígonos H3 (gdf_hulls GeoDataFrame con 'cluster','geometry')
      - Capa de puntos AIS (df_points DataFrame con 'latitude','longitude','nav_status','mmsi')
      - Heatmap opcional
      - Control de capas
    """
    # Centro en el conjunto de polígonos
    centroid = gdf_hulls.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x],
                   zoom_start=start_zoom,
                   tiles=tiles)

    # 1) Polígonos H3 (solo cluster + geometry para serialización)
    geo_df = gdf_hulls[["cluster", "geometry"]].copy()
    fg_hulls = folium.FeatureGroup(name="Polígonos H3")
    folium.GeoJson(
        data=geo_df.__geo_interface__,
        style_function=lambda feat: {
            "color": plt.cm.tab20(feat["properties"]["cluster"] % 20),
            "weight": 1,
            "fillOpacity": 0.3
        },
        tooltip=folium.GeoJsonTooltip(fields=["cluster"], aliases=["Cluster"])
    ).add_to(fg_hulls)
    fg_hulls.add_to(m)

    # 2) Puntos AIS
    fg_points = folium.FeatureGroup(name="Puntos AIS")
    mc = MarkerCluster().add_to(fg_points)
    for _, row in df_points.iterrows():
        folium.CircleMarker(
            [row["latitude"], row["longitude"]],
            radius=2,
            color=color_map.get(row["nav_status"], "#000000"),
            fill=True,
            fill_opacity=0.6,
            popup=f"MMSI: {row['mmsi']}<br>Status: {row['nav_status']}"
        ).add_to(mc)
    fg_points.add_to(m)

    # 3) Heatmap
    heat = HeatMap(
        list(zip(df_points["latitude"], df_points["longitude"])),
        name="Heatmap",
        radius=8, blur=12
    )
    m.add_child(heat)

    # 4) Control de capas
    folium.LayerControl(collapsed=False).add_to(m)

    return m
