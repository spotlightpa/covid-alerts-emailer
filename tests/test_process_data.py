import pytest
from src.assets.data_index import data_index
from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.process_individual_county import process_individual_county
from src.modules.process_data.process_neighbors import process_neighbors


def test_process_individual_county_total(data_clean):
    state_data = process_individual_county(data_clean, data_index, county_name="Total")
    df_cases = state_data["cases"]
    df_cases = df_cases.set_index("date")

    # assertions
    cases_total_july_27 = df_cases.at["2020-07-27", "total"]
    cases_moving_avg_july_27 = df_cases.at["2020-07-27", "moving_avg"]
    assert cases_total_july_27 == 108264
    assert cases_moving_avg_july_27 == 932


def test_process_individual_county_dauphin(data_clean):
    pandas_opts()
    county_data = process_individual_county(
        data_clean, data_index, county_name="Dauphin"
    )
    df_cases = county_data["cases"]
    df_cases = df_cases.set_index("date")

    # assertions
    cases_total_july_27 = df_cases.at["2020-07-27", "total"]
    cases_total_per_capita_july_27 = df_cases.at["2020-07-27", "total_per_capita"]
    assert cases_total_july_27 == 2559
    assert int(round(cases_total_per_capita_july_27)) == 920


def test_process_neighbors(data_clean, gdf):
    neighbors = get_neighbors("Dauphin", gdf)
    process_neighbors()

    print(neighbors)
