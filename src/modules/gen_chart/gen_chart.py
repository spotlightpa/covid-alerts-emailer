from typing import Dict, Union, List

from typing_extensions import TypedDict
import altair as alt
import logging
import pandas as pd
import geopandas
from altair_saver import save
from definitions import DIR_OUTPUT, AWS_BUCKET, AWS_DIR_TEST
from src.modules.gen_chart.CustomLegend import CustomLegend
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.map_choropleth import map_choropleth
from src.modules.gen_chart.multi_line import multi_line
from src.modules.gen_chart.stacked_area import stacked_area
from src.modules.gen_desc.desc_area_tests import desc_area_tests
from src.modules.gen_desc.desc_choro import desc_choro
from src.modules.gen_desc.desc_daily import desc_daily
from src.modules.process_data.compare_counties import compare_counties
from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.helper.sort_counties_by_pop import sort_counties_by_pop
from src.modules.process_data.helper.stack_df import stack_df
from src.modules.process_data.process_cumulative_tests import process_cumulative_tests
from src.modules.s3.copy_to_s3 import copy_to_s3

ChartPayloadItem = TypedDict(
    "ChartPayloadItem",
    {
        "title": str,
        "custom_legend": Union[List[Dict[str, str]], None],
        "image_path": str,
        "description": str,
    },
)


def gen_chart(
    county_name: str,
    data_type: str,
    *,
    data_index: Dict,
    chart_dict: Dict,
    data_clean: Dict,
    county_data: Dict[str, pd.DataFrame],
    gdf: geopandas.GeoDataFrame,
    primary_color: str,
    secondary_color: str,
) -> ChartPayloadItem:
    """
    Creates a chart PNG using Altair and moves its to s3. Returns an URL to the image, a Dict representing a legend
    for the chart

    Args:
        county_name (str): Name of county. Eg. "Dauphin"
        data_type (str): Type of data. Eg. "cases".
        data_index (Dict): Config settings for data.
        chart_dict (Dict): Config settings for chart.
        data_clean (Dict[str, pd.DataFrame]): Dict of unprocessed cases, deaths, tests data for all counties.
        county_data (Dict[str, pd.DataFrame]: Processed cases, deaths, tests, etc data for a specific county.
        gdf (geopandas.GeoDataFrame): Pa geodataframe with cases, deaths, tests data merged on to it.
        primary_color (str): Hex code for color theme.
        secondary_color (str): Hex code for color theme.


    Returns:
        A chart_payload_item.
    """
    chart_type = chart_dict["type"]
    chart_desc = ""
    custom_legend = None
    fmt = "png"
    content_type = "image/png"

    if "daily_and_avg" in chart_type:
        chart = daily_and_avg(
            data_type=data_type,
            df=county_data[data_type],
            line_color=primary_color,
            bar_color=secondary_color,
        )
        custom_legend = chart_dict.get("custom_legend")
        chart_desc = desc_daily(county_name=county_name, data_type=data_type)

    elif "choropleth" in chart_type:
        chart = map_choropleth(
            gdf,
            color_field=chart_dict["color_field"],
            highlight_polygon=county_name,
            min_color=secondary_color,
            max_color=primary_color,
            legend_title=chart_dict["legend_title"],
        )
        chart_desc = desc_choro(county_name, data_type=data_type)

    elif "neigbhors_per_capita" in chart_type:
        compare_field = chart_dict["compare_field"]
        neighbor_limit = chart_dict["neighbor_limit"]
        neighbors = get_neighbors("Dauphin", gdf)
        neighbors = sort_counties_by_pop(neighbors)
        neighbors = neighbors[0:neighbor_limit]
        compare_list = ["Dauphin"] + neighbors
        data_clean_cases = data_clean["cases"]
        clean_rules = data_index["cases"]["clean_rules"]
        df_multi_county = compare_counties(
            data_clean_cases,
            clean_rules=clean_rules,
            compare_field=compare_field,
            counties=compare_list,
        )
        county_list = [col for col in df_multi_county.columns if col != "date"]
        df_multi_county = stack_df(
            df_multi_county, stack_cols=county_list, x_axis_col="date"
        )
        legend_obj = CustomLegend(county_list)
        chart = multi_line(
            df_multi_county,
            x_axis_col="date",
            y_axis_col="value",
            category_col="category",
            domain=legend_obj.labels,
            range_=legend_obj.colors,
        )
        custom_legend = legend_obj.legend(title_case=True)
        chart_desc = "Testing multi line chart!"

    elif "stacked_area" in chart_type:
        df = process_cumulative_tests(county_data["confirmed"], county_data["tests"])
        chart = stacked_area(
            df,
            x_axis_col="date",
            y_axis_col="count",
            category_col="data_type",
            domain=["positive", "negative"],
            range_=[primary_color, secondary_color],
        )
        custom_legend = chart_dict.get("custom_legend")
        chart_desc = desc_area_tests(data=df, county=county_name)
    else:
        raise Exception("Chart type not found")

    image_filename = f"{county_name.lower()}_{data_type}_{chart_type}.{fmt}"
    image_path = DIR_OUTPUT / image_filename
    save(chart, str(image_path))
    logging.info("...saved")

    # Move to s3
    copy_to_s3(image_path, AWS_BUCKET, AWS_DIR_TEST, content_type=content_type)

    return {
        "title": chart_dict.get("title", ""),
        "custom_legend": custom_legend,
        "image_path": f"https://{AWS_BUCKET}/{AWS_DIR_TEST}/{image_filename}",
        "description": chart_desc,
    }
