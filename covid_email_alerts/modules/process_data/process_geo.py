import pandas as pd
import geopandas
from pathlib import Path
from covid_email_alerts.definitions import PATH_OUTPUT_GEOJSON, PATH_PA_POP


def process_geo(
    path_geo_file: Path,
    *,
    add_pop: bool = True,
    add_neighbors: bool = True,
    add_centroids: bool = False,
    save_geojson: bool = False,
    path_pop_file: Path = PATH_PA_POP,
    path_output_geojson: Path = PATH_OUTPUT_GEOJSON,
) -> geopandas.GeoDataFrame:
    """
    Reads a given geographic file (eg. geojson), converts it to a geopandas geoDataFrame,
    adds a column for each polygon with a list of neighboring polygons, and adds a column
    for each polygon.

    Args:
        path_geo_file (Path): Path to geographic file (eg. geojson) that will be read.
        add_neighbors (bool): Adds a new column called NEIGBHORS for each county with all geographic regions that
            border each region. Defaults to True.
        add_pop (bool): Adds a new field with the population for each county. Defaults to True.
        save_geojson (bool): Whether to save file as geojson. Default to False.
        path_pop_file (Path) OPTIONAL: Path to CSV with population data to merge to geo data. Defaults to PATH_PA_POP.
        add_centroids (bool) OPTIONAL: Gets centroids of each polygon if selected. Defaults to false.
        path_output_geojson (Path. optional): Path to output geojson file.
    """
    gdf = geopandas.read_file(path_geo_file)

    # add population data
    if add_pop:
        df_pop = pd.read_csv(path_pop_file)
        gdf = gdf.merge(df_pop, left_on="NAME", right_on="name", how="left")
        gdf["population"] = gdf["population"].astype(int)

    # add NEIGHBORS column
    if add_neighbors:
        gdf["NEIGHBORS"] = None
        for index, country in gdf.iterrows():
            # get 'not disjoint' countries
            neighbors = gdf[~gdf.geometry.disjoint(country.geometry)].NAME.tolist()
            # remove own name from the list
            neighbors = [name for name in neighbors if country.NAME != name]
            # add names of neighbors as NEIGHBORS value
            gdf.at[index, "NEIGHBORS"] = ", ".join(neighbors)

    if add_centroids:
        gdf["CENTROID"] = gdf["geometry"].centroid

    if save_geojson:
        gdf.to_file(path_output_geojson, driver="GeoJSON")

    return gdf
