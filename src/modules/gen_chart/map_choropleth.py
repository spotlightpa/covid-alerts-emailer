import geopandas
import altair as alt
from altair_saver import save
from pathlib import Path
import logging
from typing import List
from src.modules.process_data.helper.convert_gfp_to_alt import convert_gfp_to_alt


def map_choropleth(
    gdf: geopandas.GeoDataFrame,
    color_field,
    *,
    highlight_polygon: str = "",
    color_range: List[str] = ["#F4D2D2", "#EA9E9E", "#E06969", "#D63535", "#CC0000"],
) -> alt.Chart:
    """
    Creates a choropleth map of covid data from a geopandas dataframe.

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe of covid data.
        color_field (str): Column from gdf that will be used for the choropleth map.
       highlight_polygon (str, optional): Creates a border around a selected polygon to emphasise it.
       color_range (List[str], optional): List of hex codes for choropleth colors
    Returns:
        Altair chart instance.
    """
    gdf = gdf.drop(
        ["id"], axis=1
    )  # dropping ID col to avoid warning message from gpdvega/altair
    data = convert_gfp_to_alt(gdf)

    chart = (
        alt.Chart(data)
        .mark_geoshape(
            strokeWidth=1,
            stroke="#fff",
            # width=300,height=200
        )
        .project()
        .encode(
            color=alt.Color(
                f"properties.{color_field}:Q",
                scale=alt.Scale(
                    type="quantize",
                    nice=True,
                    # scheme="blues"
                    range=color_range,
                ),
                legend=alt.Legend(
                    orient="top", title="Cases per 100,000 people", titleLimit=200
                ),
            )
        )
        .properties(width=600, height=460)
    )

    if highlight_polygon:
        gdf_highlight = gdf[gdf["NAME"].str.contains(highlight_polygon, case=False)]
        data_highlight = convert_gfp_to_alt(gdf_highlight)
        chart_highlight = (
            alt.Chart(data_highlight)
            .mark_geoshape(strokeWidth=2, stroke="#0E0E0E", fill=None)
            .project()
        )
        final_chart = chart + chart_highlight
    else:
        final_chart = chart
    return final_chart
