import geopandas
import altair as alt
from altair_saver import save
from pathlib import Path

def map_choropleth(gdf: geopandas.GeoDataFrame, path_output_file:Path) -> None:
    """
    Creates a choropleth map of covid data from a geopandas dataframe.

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe of covid data.
        path_output_file (Path): path to where file should be saved.

    Returns:
        None.
    """
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
    save(chart, str(path_output_file))
    return
