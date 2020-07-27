import pytest

from src.assets.data_index import data_index
from src.modules.process_data.process_individual_county import process_individual_county


def test_process_individual_county(data_clean):
    state_data = process_individual_county(data_clean, data_index, county="Total")
    df_cases = state_data["cases"]

    df_cases = df_cases.set_index("date")
    cases_total_july_27 = df_cases.at["2020-07-27", "total"]
    cases_moving_avg_july_27 = df_cases.at["2020-07-27", "moving_avg"]
    print(df_cases)
    assert cases_total_july_27 == 108264
    assert cases_moving_avg_july_27 == 932
