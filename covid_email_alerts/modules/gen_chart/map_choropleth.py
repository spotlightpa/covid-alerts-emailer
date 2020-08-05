import geopandas
import altair as alt
from covid_email_alerts.modules.helper.convert_gfp_to_alt import convert_gfp_to_alt
from colour import Color


def map_choropleth(
    gdf: geopandas.GeoDataFrame,
    color_field,
    *,
    highlight_polygon: str = "",
    min_color: str = "#F4D2D2",
    max_color: str = "#CC0000",
    color_steps: int = 5,
    legend_title: str = None,
) -> alt.Chart:
    """
    Creates a choropleth map of covid data from a geopandas dataframe.

    Args:
        gdf (geopandas.GeoDataFrame): geodataframe of covid data.
        color_field (str): Column from gdf that will be used for the choropleth map.
        highlight_polygon (str, optional): Creates a border around a selected polygon to emphasise it.
        min_color (str, optional): HSL, RGB, HEX, WEB of min color of choropleth range. Defaults to
            "#F4D2D2"
        max_color (str, optional): HSL, RGB, HEX, WEB of  max color of choropleth range. Defaults to "#CC0000"
        color_steps (int, optional): Number of steps between min and max for final choropleth color range.
            Defaults to 5.
        legend_title (str, optional): Title for legend. Defaults to color_field value.

    Returns:
        Altair chart instance.
    """

    gdf = gdf.drop(
        ["id"], axis=1
    )  # dropping ID col to avoid warning message from gpdvega/altair
    data = convert_gfp_to_alt(gdf)
    color_range = list(Color(min_color).range_to(Color(max_color), color_steps))
    color_range = [x.hex for x in color_range]
    legend_title = color_field if not legend_title else legend_title

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
                scale=alt.Scale(type="quantize", nice=True, range=color_range,),
                legend=alt.Legend(orient="top", title=legend_title, titleLimit=200),
            )
        )
        .properties(width=600, height=460)
    )

    if highlight_polygon:
        gdf_highlight = gdf[gdf["NAME"].str.contains(highlight_polygon, case=False)]
        data_highlight = convert_gfp_to_alt(gdf_highlight)
        chart_highlight = (
            alt.Chart(data_highlight)
            .mark_geoshape(
                strokeWidth=2,
                stroke="#0E0E0E",
                # stroke="white",
                fill=None,
            )
            .project()
        )
        final_chart = chart + chart_highlight
    else:
        final_chart = chart
    return final_chart
