import pandas as pd
import geopandas
from typing import Dict
import logging


def merge_geo(
    gdf: geopandas.GeoDataFrame,
    data: Dict[str, pd.DataFrame],
    add_per_capita: bool = True,
) -> geopandas.GeoDataFrame:
    """
    Processes a geopandas geodataframe by merging it with data stored on a dict of pandas dataframes representing
    cases, deaths, etc.

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe with boundaries and other important ID fields
        data (Dict[str, pd.DataFrame]): Dict of pandas dataframes that contains case, deaths, etc. data for merging
        add_per_capita (bool): Adds a new column for each dataframe in data that represents per capita info. Eg.
            per_capita_cases, per_capita_deaths. Defaults to True.

    Returns:
        An updated geopandas geodataframe.
    """
    logging.info("Merging covid data with geo data...")
    for data_type, df in data.items():
        df = df.drop("Total", axis=1)
        df_most_recent = df.tail(1)
        df_most_recent = df_most_recent.set_index("date")
        df_most_recent = df_most_recent.transpose()
        col_name = f"{data_type}_total"
        df_most_recent.columns = [col_name]
        gdf = gdf.merge(df_most_recent, how="left", left_on="NAME", right_index=True)
        gdf[col_name] = gdf[col_name].astype("int")

        if add_per_capita:
            col_name_capita = f"{data_type}_per_capita"
            gdf[col_name_capita] = (
                gdf[col_name] / gdf["population"]
            ) * 100000  # calculate rate per 100k people

    logging.info("Data merged")
    return gdf
