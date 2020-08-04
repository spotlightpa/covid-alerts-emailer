from src.modules.helper.get_county_pop import get_county_pop
from typing import Union


def calc_county_per_capita_rate(
        county_name_clean: str,
        total_over_period: Union[int, float],
        _round=True,
        num_of_people:int=100000
):
    """ Calculates a rate per 100,000 people for a specific county

    Args:
        county_name_clean (str): County name to get population for. Eg "Dauphin"
        total_over_period (Union[int, float]): Number to calculate rate for. Eg. 1000 deaths.
        _round (bool, optional): Whether to round the result.
        num_of_people (int, optional): Number of people to use as per capita rate. Defaults to 100000.

    Return:
        Union[int, float]: Per capita rate for county.

    """
    county_pop = get_county_pop(county_name_clean)
    per_capita_rate = (total_over_period / county_pop) * num_of_people
    per_capita_rate = round(per_capita_rate) if _round else per_capita_rate
    return per_capita_rate
