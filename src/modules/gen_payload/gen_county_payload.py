import logging
from typing import List, Dict, Any

from src.assets.chart_index import CHART_INDEX
from src.assets.data_index import DATA_INDEX
from src.modules.gen_chart.gen_chart import gen_chart
from src.definitions import AWS_BUCKET, AWS_DIR


def gen_county_payload(
    county_name_clean: str,
    *,
    data_clean,
    county_data,
    gdf,
    aws_bucket: str = AWS_BUCKET,
    aws_dir: str = AWS_DIR,
) -> List[Dict[str, Any]]:
    """
    A subassembly function that builds charts, uploads those charts to S3, and returns
     a list of dictionaries with county-specific data needed to construct newsletter.

    Args:
        county_name_clean (str): Name of county without 'County' suffix. Eg. "Dauphin"
        data_clean (Dict[str, pd.DataFrame]): Dict of pandas dfs of cases, deaths, tests data for all Pa. counties
            that has has some minimal cleaning.
        county_data (Dict[str, pd.DataFrame]: Processed cases, deaths, tests, etc data for a specific county.
        gdf (geopandas.GeoDataFrame): Pa geodataframe with cases, deaths, tests data merged on to it.
        aws_bucket (optional, str): AWS bucket where charts will be uploaded to. Defaults to value stored in
        definitions.py
        aws_dir (optional, str): Directory within AWS bucket where charts will be uploaded. Defaults to value stored in
        definitions.py

    Returns:
        List[Dict[str, Any]]: Data for a specific county for email payload
    """
    county_payload = []
    for data_type, chart_index_dict in CHART_INDEX.items():
        logging.info(f"Creating payload for: {data_type}")
        primary_color = chart_index_dict["theme"]["colors"]["primary"]
        secondary_color = chart_index_dict["theme"]["colors"]["secondary"]

        # create charts
        chart_payload = []
        for chart_dict in chart_index_dict["charts"]:
            chart_payload_item = gen_chart(
                county_name_clean=county_name_clean,
                data_type=data_type,
                data_clean=data_clean,
                data_index=DATA_INDEX,
                chart_dict=chart_dict,
                county_data=county_data,
                gdf=gdf,
                primary_color=primary_color,
                secondary_color=secondary_color,
                aws_bucket=aws_bucket,
                aws_dir=aws_dir,
            )
            chart_payload.append(chart_payload_item)

        # add to email payload
        county_payload.append(
            {
                "title": f"{data_type.upper()}",
                "charts": chart_payload,
                "colors": {"primary": primary_color, "secondary": secondary_color,},
            }
        )
    return county_payload
