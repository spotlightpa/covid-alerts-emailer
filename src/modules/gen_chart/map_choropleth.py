import geopandas
import altair as alt
from altair_saver import save
from pathlib import Path
import logging

from src.modules.process_data.helper.convert_gfp_to_alt import convert_gfp_to_alt


def map_choropleth(
    gdf: geopandas.GeoDataFrame, path_output_file: Path, highlight_polygon=""
) -> None:
    """
    Creates a choropleth map of covid data from a geopandas dataframe.

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe of covid data.
        path_output_file (Path): path to where file should be saved.
       highlight_polygon (str) OPTIONAL: Creates a border around a selected polygon to emphasise it.

    Returns:
        None.
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
                "properties.cases_per_capita:Q",
                scale=alt.Scale(
                    type="quantize",
                    nice=True,
                    # scheme="reds"
                    range=["#F4D2D2", "#EA9E9E", "#E06969", "#D63535", "#CC0000"],
                ),
                legend=alt.Legend(
                    orient="top", title="Cases per 100,000 people", titleLimit=200
                ),
            )
        )
        .properties(width=600, height=460)
    )

    if highlight_polygon:
        gdf_highlight = gdf[gdf["NAME"].str.contains(highlight_polygon)]
        data_highlight = convert_gfp_to_alt(gdf_highlight)
        chart_highlight = (
            alt.Chart(data_highlight)
            .mark_geoshape(strokeWidth=2, stroke="#0E0E0E", fill=None)
            .project()
        )
        final_chart = chart + chart_highlight
    else:
        final_chart = chart

    save(final_chart, str(path_output_file))
    return
