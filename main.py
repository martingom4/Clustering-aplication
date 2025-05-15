from src.loader import load_data
from src.cleaner import clean_data
from src.density_filter import filter_low_density
from src.h3_cluster import cluster_hexagons
from src.h3_to_polygons import attach_geometry
from src.map_folium import create_interactive_map

import geopandas as gpd


def main():
    # 1. Cargar datos
    df = load_data()
    print("✅ Datos cargados")

    # 2. Limpiar datos
    df_clean = clean_data(df)
    print("✅ Datos limpiados")

    # 3. Filtrar por densidad H3 (res_8)
    df_filtered = filter_low_density(df_clean)
    print("✅ Filtro de densidad aplicado")

    import matplotlib.pyplot as plt
    from matplotlib import cm, colors

    # 1) Calcular conteo de estados y convertir a pandas para obtener la lista
    status_counts = df_filtered["nav_status"].value_counts().compute()
    statuses = status_counts.index.tolist()

    # 2) Generar colormap dinámico
    cmap = cm.get_cmap("tab10", len(statuses))
    hex_colors = [colors.rgb2hex(cmap(i)) for i in range(len(statuses))]
    color_map = dict(zip(statuses, hex_colors))

    # 4. Clustering sobre centroides de hexágonos
    df_clustered = cluster_hexagons(df_filtered)
    print("✅ Clustering sobre hexágonos realizado")

    # 5. Convertir hexágonos a polígonos
    df_with_geom = attach_geometry(df_clustered)
    gdf = gpd.GeoDataFrame(df_with_geom, geometry="geometry", crs="EPSG:4326")
    print("✅ Geometrías de polígonos generadas")

    # 6. Visualización en mapa interactivo
    df_points = df_filtered.compute()
    m = create_interactive_map(gdf, df_points, color_map, start_zoom=8, tiles="CartoDB Positron")
    m.save("mapa_interactivo.html")
    print("🌍 Mapa interactivo guardado en mapa_interactivo.html")


if __name__ == "__main__":
    main()
