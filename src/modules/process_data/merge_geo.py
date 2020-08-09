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
    Merges a geopandas geodataframe with data stored on a dict of pandas dataframes representing
    cases, deaths, etc. Adds new fields

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe with boundaries and other important ID fields
        data (Dict[str, pd.DataFrame]): Dict of pandas dataframes that contains case, deaths, etc. data for merging
        add_per_capita (bool): Adds a new column for each dataframe in data that represents per capita info. Assumes
            that gdf has an existing column called 'population' with pop data for each county. Defaults to True.

    Returns:
        geopandas.GeoDataFrame: An updated geodataframe with new columns relating to cases, deaths, and tests for
        each county.
    """
    logging.info("Merging covid data with geo data...")
    for data_type, df in data.items():
        df = df.drop("Total", axis=1)

        # creates a new df with four rows: date, total, total_15_days_ago, added_past_two_weeks
        # we subtract current total from value 15 days ago in order to get all new values added over past 14 days.
        col_15_days_ago = f"{data_type}_total_15_days_ago"
        col_total = f"{data_type}_total"
        col_added_past_two_weeks = f"{data_type}_added_past_two_weeks"

        df_truncated = df.iloc[[-15, -1]]  # to get t
        df_truncated = df_truncated.set_index("date")
        df_truncated = df_truncated.transpose()
        df_truncated.rename(
            columns={df_truncated.columns[0]: col_15_days_ago}, inplace=True
        )
        df_truncated.rename(columns={df_truncated.columns[1]: col_total}, inplace=True)
        df_truncated[col_added_past_two_weeks] = (
            df_truncated[col_total] - df_truncated[col_15_days_ago]
        )

        # merge data with gdf
        gdf = gdf.merge(df_truncated, how="left", left_on="NAME", right_index=True)
        gdf = gdf.astype(
            {col_15_days_ago: "int", col_total: "int", col_added_past_two_weeks: "int",}
        )

        if add_per_capita:
            col_total_per_capita = f"{data_type}_total_per_capita"
            col_added_past_two_weeks_per_capita = (
                f"{data_type}_added_past_two_weeks_per_capita"
            )
            gdf[col_total_per_capita] = (
                gdf[col_total] / gdf["population"]
            ) * 100000  # calculate rate per 100k people
            gdf[col_added_past_two_weeks_per_capita] = (
                gdf[col_added_past_two_weeks] / gdf["population"]
            ) * 100000  # calculate rate per 100k people

    logging.info("Data merged")
    return gdf
