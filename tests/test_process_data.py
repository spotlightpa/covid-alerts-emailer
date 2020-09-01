from src.assets.data_index import DATA_INDEX
from src.definitions import PATH_PA_GEOJSON
from src.modules.helper.get_neighbors import get_neighbors
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_clean import process_clean
from src.modules.process_data.process_geo import process_geo
from src.modules.process_data.process_individual_county import process_individual_county
from src.modules.process_data.compare_counties import compare_counties
from src.modules.process_data.process_stories import process_stories
import pandas as pd


def test_process_individual_county_total(data_clean):
    state_data = process_individual_county(data_clean, DATA_INDEX, county_name="Total")
    df_cases = state_data["cases"]
    df_cases = df_cases.set_index("date")

    # assertions
    cases_total_july_27 = df_cases.at["2020-07-27", "total"]
    cases_moving_avg_july_27 = df_cases.at["2020-07-27", "moving_avg"]
    assert cases_total_july_27 == 108264
    assert int(cases_moving_avg_july_27) == 932


def test_process_individual_county_dauphin(data_clean):
    county_data = process_individual_county(
        data_clean, DATA_INDEX, county_name="Dauphin"
    )
    df_cases = county_data["cases"]
    df_cases = df_cases.set_index("date")

    # assertions
    cases_total_july_27 = df_cases.at["2020-07-27", "total"]
    cases_total_per_capita_july_27 = df_cases.at["2020-07-27", "total_per_capita"]
    assert cases_total_july_27 == 2559
    assert int(round(cases_total_per_capita_july_27)) == 920


def test_process_individual_county_greene(data_clean):
    county_data = process_individual_county(
        data_clean, DATA_INDEX, county_name="Greene"
    )

    df_deaths = county_data["deaths"]
    print("\n", df_deaths)


def test_process_individual_county_washington(data_clean):
    county_data = process_individual_county(
        data_clean, DATA_INDEX, county_name="Washington"
    )

    df_deaths = county_data["deaths"]
    print("\n", df_deaths)


def test_process_geo():
    df = process_geo(PATH_PA_GEOJSON)
    print("\n", df)


def test_merge_geo(gdf_raw, data_clean):
    df_merged = merge_geo(gdf_raw, data_clean, add_per_capita=True)
    # print("\n", df_merged)
    # should have 67 rows, one for each county
    assert len(df_merged.index) == 67
    # df_merged = df_merged.set_index("NAME")
    wash = df_merged.loc[df_merged["NAME"] == "Washington"]
    print(wash)


def test_process_neighbors_total(data_clean, gdf_processed):
    neighbors = get_neighbors("Dauphin", gdf_processed)
    compare_list = ["Dauphin"] + neighbors
    data_clean_cases = data_clean["cases"]
    clean_rules = DATA_INDEX["cases"]["clean_rules"]
    df = compare_counties(
        data_clean_cases,
        clean_rules=clean_rules,
        compare_field="total",
        counties=compare_list,
    )
    df = df.set_index("date")
    cases_lebanon_july_26 = df.at["2020-07-26", "lebanon"]
    cases_lebanon_july_23 = df.at["2020-07-23", "cumberland"]
    assert cases_lebanon_july_26 == 1544
    assert cases_lebanon_july_23 == 1066


def test_process_neighbors_per_capita(data_clean, gdf_processed):
    neighbors = get_neighbors("Dauphin", gdf_processed)
    compare_list = ["Dauphin"] + neighbors
    data_clean_cases = data_clean["cases"]
    clean_rules = DATA_INDEX["cases"]["clean_rules"]
    df = compare_counties(
        data_clean_cases,
        clean_rules=clean_rules,
        compare_field="moving_avg_per_capita",
        counties=compare_list,
    )
    df = df.set_index("date")
    print(df)


def test_compare_counties(data_clean, gdf_processed):
    neighbors = get_neighbors("Greene", gdf_processed)
    compare_list = ["Greene"] + neighbors
    data_clean_deaths = data_clean["deaths"]
    clean_rules = DATA_INDEX["deaths"]["clean_rules"]
    result = compare_counties(
        data_clean_deaths,
        clean_rules=clean_rules,
        compare_field="moving_avg_per_capita",
        counties=compare_list,
    )
    print("\n", result)


def test_process_stories(stories_raw):
    clean_stories = process_stories(stories_raw)
    print(clean_stories)


def test_process_clean_bad_death_data(raw_pa_deaths_with_strings):
    """ Test that data_clean can clean a CSV that includes strings without crashing"""
    data_raw = {"deaths": raw_pa_deaths_with_strings}
    data_clean = process_clean(data_raw)
    df = data_clean["deaths"]
    assert isinstance(df, pd.DataFrame)
    df = df.set_index("date")
    # check string values are now set to 0
    assert df.at["2020-08-25", "Sullivan"] == 0
    assert df.at["2020-08-25", "Forest"] == 0
