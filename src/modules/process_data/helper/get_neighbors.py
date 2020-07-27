import geopandas as gpd
from typing import List


def get_neighbors(
    county_name: str,
    gdf: gpd.GeoDataFrame,
    field_county_name="NAME",
    field_neighbors: str = "NEIGHBORS",
) -> List:
    """
    Gets the neighboring counties of a specified county from a gdf that contains a field with a list of neighbors

    Args:
        county_name (str): County name to get neigbhors for.
        gdf (gpd.GeoDataFrame): geopandas dataframe that includes a field that has info about a county's neighbors
        field_county_name (str, optional): field name in gdf that contains county names. Defaults to "NAME"
        field_neighbors (str, optional): field name in gdf that contains a list of neighbors. Defaults to "NEIGHBORS"

    Returns:
        A list of strings representing a county's neighbors.
    """
    gdf = gdf.set_index(field_county_name)
    neighbors = gdf.at[county_name, field_neighbors]
    return neighbors.split(",")
