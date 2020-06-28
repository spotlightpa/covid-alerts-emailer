import pandas as pd
import geopandas
import altair as alt
from altair_saver import save
from definitions import DIR_DATA


def map_choropleth(gdf: geopandas.GeoDataFrame):
    gdf = gdf.drop(
        ["id"], axis=1
    )  # dropping ID col to avoid warning message from gpdvega/altair
    data = alt.InlineData(values=gdf.to_json(),  # geopandas to geojson string
                          # root object type is "FeatureCollection" but we need its features
                          format=alt.DataFormat(property='features', type='json'))
    chart = (
        alt.Chart(data)
        .mark_geoshape()
        .project()
        .encode(
            color="properties.cases_per_capita:Q",  # shorthand infer types as for regular pd.DataFrame
            # tooltip="id:Q",  # GeoDataFrame.index is accessible as id
        )
        .properties(width=500, height=300)
    )
    save(chart, str(DIR_DATA / "map.png"))
    return
