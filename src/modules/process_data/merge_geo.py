import pandas as pd
import geopandas
from typing import Dict
import logging


def merge_geo(
    gdf: geopandas.GeoDataFrame, data: Dict[str, pd.DataFrame]
) -> geopandas.GeoDataFrame:
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
        col_name_capita = f"{data_type}_per_capita"
        gdf[col_name_capita] = (
            gdf[col_name] / gdf["population"]
        ) * 100000  # calculate rate per 100k people

    print(gdf)
    logging.info("Data merged")
    return gdf
