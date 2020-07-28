from typing import List
from src.modules.process_data.helper.get_county_pop import get_county_pop


def sort_counties_by_pop(county_list: List[str]) -> List:
    """
    Sorts a list of Pa. counties based on their population. Most populated to least.

    Args:
        county_list (List): List of counties

    Returns:
        List[str]: Updated list of counties, sorted by population highest to lowest.
    """

    county_list.sort(key=get_county_pop, reverse=True)
    return county_list
