import pandas as pd
import geopandas
import altair as alt
from altair_saver import save
import gpdvega

from definitions import DIR_DATA


def map_choropleth(gdf):
    print(gdf)
    print(gdf.info())
    gdf = gdf.drop(["id"], axis=1)
    print(gdf)
    chart = (
        alt.Chart(gdf)
        .mark_geoshape()
        .project()
        .encode(
            color="population",  # shorthand infer types as for regular pd.DataFrame
            # tooltip="id:Q",  # GeoDataFrame.index is accessible as id
        )
        .properties(width=500, height=300)
    )
    save(chart, str(DIR_DATA / "map.png"))
