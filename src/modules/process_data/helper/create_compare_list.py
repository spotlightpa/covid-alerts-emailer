from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.helper.sort_counties_by_pop import sort_counties_by_pop
import geopandas
from typing import List


def create_compare_list(
    county_name, gdf: geopandas.GeoDataFrame, neighbor_limit: int = 10
) -> List:
    """
    Creates a list of counties in a region. The first county in the list is the specified county,
    the other counties are bordering counties sorted from most populous to least.

    Args:
        county_name (str): Name of county.
        gdf (geopandas.GeoDataFrame): Pa geodataframe with cases, deaths, tests data merged on to it.
        neighbor_limit (optional, int): Max number of counties. Defaults to 10.
    """
    neighbors = get_neighbors("Dauphin", gdf)
    neighbors = sort_counties_by_pop(neighbors)
    neighbors = neighbors[0:neighbor_limit]
    return [county_name] + neighbors
