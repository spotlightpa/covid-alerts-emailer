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
        .mark_geoshape(
            strokeWidth=1, stroke="#fff",
            # width=300,height=200
            )
        .project()
        .encode(
            color=alt.Color(
                "properties.cases_per_capita:Q", scale=alt.Scale(type="quantize", nice=True),
            legend=alt.Legend(orient="top", title="Cases per 100,000 people", titleLimit=200)
            )
        )
        # .properties(width=580, height=380)
    )
    print(chart.to_dict())
    print(chart)
    save(chart, str(DIR_DATA / "map.png"))
    return