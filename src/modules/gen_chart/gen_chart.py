from typing import Dict, Union, List, Any
import logging
import pandas as pd
import geopandas
from altair_saver import save
from src.definitions import DIR_OUTPUT
from src.modules.gen_chart.custom_legend import CustomLegend
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.map_choropleth import map_choropleth
from src.modules.gen_chart.multi_line import multi_line
from src.modules.gen_chart.stacked_area import stacked_area
from src.modules.gen_desc.gen_desc import GenDesc
from src.modules.process_data.compare_counties import compare_counties
from src.modules.helper.get_neighbors import get_neighbors
from src.modules.helper.sort_counties_by_pop import sort_counties_by_pop
from src.modules.helper.stack_df import stack_df
from src.modules.process_data.process_cumulative_tests import process_cumulative_tests
from src.modules.aws.copy_to_s3 import copy_to_s3


def gen_chart(
    county_name_clean: str,
    data_type: str,
    *,
    data_index: Dict,
    chart_dict: Dict,
    data_clean: Dict,
    county_data: Dict[str, pd.DataFrame],
    gdf: geopandas.GeoDataFrame,
    primary_color: str,
    secondary_color: str,
    aws_bucket: str,
    aws_dir: str,
) -> Dict[str, Union[Union[str, None, List[Dict[str, str]]], Any]]:
    """
    Creates a chart PNG using Altair and moves its to s3. Returns an URL to the image, a Dict representing a legend
    for the chart

    Args:
        county_name_clean (str): Name of county without 'County' suffix. Eg. "Dauphin"
        data_type (str): Type of data. Eg. "cases".
        data_index (Dict): Config settings for data.
        chart_dict (Dict): Config settings for chart.
        data_clean (Dict[str, pd.DataFrame]): Dict of pandas dfs of cases, deaths, tests data for all Pa. counties
            that has has some minimal cleaning.
        county_data (Dict[str, pd.DataFrame]: Processed cases, deaths, tests, etc data for a specific county.
        gdf (geopandas.GeoDataFrame): Pa geodataframe with cases, deaths, tests data merged on to it.
        primary_color (str): Hex code for color theme.
        secondary_color (str): Hex code for color theme.
        aws_bucket (str): AWS bucket where charts will be uploaded to. Defaults to value stored in
        definitions.py
        aws_dir (str): Directory within AWS bucket where charts will be uploaded. Defaults to value stored in
        definitions.py

    Returns:
        Dict[str, Union[Union[str, None, List[Dict[str, str]]], Any]]: Dict with keys relating to chart, legend,
        and chart descriptive text.
    """

    chart_type = chart_dict["type"]
    custom_legend = None
    fmt = "png"
    content_type = "image/png"
    gen_desc = GenDesc(county_name_clean, county_data=county_data, gdf=gdf)

    if "daily_and_avg" in chart_type:
        chart = daily_and_avg(
            data_type=data_type,
            df=county_data[data_type],
            line_color=primary_color,
            bar_color=secondary_color,
        )
        custom_legend = chart_dict.get("custom_legend")
        chart_desc = gen_desc.daily(data_type=data_type)

    elif "choropleth" in chart_type:
        chart = map_choropleth(
            gdf,
            color_field=chart_dict["color_field"],
            highlight_polygon=county_name_clean,
            min_color=secondary_color,
            max_color=primary_color,
            legend_title=chart_dict["legend_title"],
        )
        chart_desc = gen_desc.choro(data_type=data_type)

    elif "neigbhors_per_capita" in chart_type:
        compare_field = chart_dict["compare_field"]
        neighbor_limit = chart_dict["neighbor_limit"]
        neighbors = get_neighbors(county_name_clean, gdf)
        neighbors = sort_counties_by_pop(neighbors)
        neighbors = neighbors[0:neighbor_limit]
        compare_list = [county_name_clean] + neighbors
        data_clean_cases = data_clean[data_type]
        clean_rules = data_index[data_type]["clean_rules"]
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
        chart_desc = gen_desc.neighbors(data_type=data_type)

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
        chart_desc = gen_desc.area_tests()
    else:
        raise Exception(
            "Chart type not found. Did you provide a valid chart type in chart_index?"
        )

    image_filename = f"{county_name_clean.lower()}_{data_type}_{chart_type}.{fmt}"
    image_path = DIR_OUTPUT / image_filename
    save(chart, str(image_path))
    logging.info("...saved")

    # Move to s3
    copy_to_s3(image_path, aws_bucket, aws_dir, content_type=content_type)

    return {
        "title": chart_dict.get("title", "").upper(),
        "custom_legend": custom_legend,
        "image_path": f"https://{aws_bucket}/{aws_dir}/{image_filename}",
        "description": chart_desc,
    }
