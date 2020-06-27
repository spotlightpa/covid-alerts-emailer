import pandas as pd
import geopandas
from pathlib import Path
from definitions import PATH_PA_GEOJSON, PATH_OUTPUT_GEOJSON
import logging
from typing import Dict


def process_geo(
    path_geo_file: Path,
    *,
    path_pop_file: Path = None,
    centroids: bool = False,
    path_output_geojson: Path = None,
    data_state: Dict = None
) -> geopandas.GeoDataFrame:
    """
    Reads a given geographic file (eg. geojson), converts it to a geopandas geoDataFrame,
    adds a column for each polygon with a list of neighboring polygons, and adds a column
    for each polygon.

    Args:
        path_geo_file (Path): Path to geographic file (eg. geojson)
        path_pop_file (Path) OPTIONAL: Path to CSV with population data to merge to geo data.
        centroids (bool) OPTIONAL: Gets centroids of each polygon if selected. Defaults to false.
    """
    logging.info("Processing geo data...")
    gdf = geopandas.read_file(path_geo_file)
    if path_pop_file:
        df_pop = pd.read_csv(path_pop_file)
        gdf = gdf.merge(df_pop, left_on="NAME", right_on="name", how="left")
        gdf["population"] = gdf["population"].astype(int)
    gdf["NEIGHBORS"] = None  # add NEIGHBORS column

    for index, country in gdf.iterrows():
        # get 'not disjoint' countries
        neighbors = gdf[~gdf.geometry.disjoint(country.geometry)].NAME.tolist()
        # remove own name from the list
        neighbors = [name for name in neighbors if country.NAME != name]
        # add names of neighbors as NEIGHBORS value
        gdf.at[index, "NEIGHBORS"] = ", ".join(neighbors)

    if centroids:
        gdf["CENTROID"] = gdf["geometry"].centroid

    if data_state:
        pass
        # for data_type in data_state:
        # gdf = gdf.merge(left_on=)

    if path_output_geojson:
        gdf.to_file(path_output_geojson, driver="GeoJSON")

    logging.info("Processing complete")
    return gdf
