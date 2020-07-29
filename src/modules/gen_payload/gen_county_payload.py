import logging
from typing import List, Dict, Any

from src.assets.chart_index import CHART_INDEX
from src.assets.data_index import DATA_INDEX
from src.modules.gen_chart.gen_chart import gen_chart


def gen_county_payload(
    county_name: str, *, data_clean, county_data, gdf
) -> List[Dict[str, Any]]:
    """
    A subassembly function that builds charts and a list of dictionaries with county-specific data needed to construct
    newsletter.

    Args:
        county_name (str): Name of county. Eg. "Dauphin"
        data_clean (Dict[str, pd.DataFrame]): Dict of unprocessed cases, deaths, tests data for all counties.
        county_data (Dict[str, pd.DataFrame]: Processed cases, deaths, tests, etc data for a specific county.
        gdf (geopandas.GeoDataFrame): Pa geodataframe with cases, deaths, tests data merged on to it.

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
                county_name,
                data_type,
                data_clean=data_clean,
                data_index=DATA_INDEX,
                chart_dict=chart_dict,
                county_data=county_data,
                gdf=gdf,
                primary_color=primary_color,
                secondary_color=secondary_color,
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
