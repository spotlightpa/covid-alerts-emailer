import logging
import geopandas
import altair as alt


def convert_gfp_to_alt(gdf: geopandas.geodataframe) -> alt.InlineData:
    """
    Converts a geopandas geoDataFrame into a Altair InlineData instance so it can be converted into a chart.

    Args:
        gdf (geopandas.geodataframe): Input geodataframe

    Returns:
        alt.InlineData: An instance of Altair's InlineData class.
    """
    data = alt.InlineData(
        values=gdf.to_json(),  # geopandas to geojson string
        # root object type is "FeatureCollection" but we need its features
        format=alt.DataFormat(property="features", type="json"),
    )
    return data
