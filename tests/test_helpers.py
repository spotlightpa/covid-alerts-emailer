from src.modules.helper.add_utm_params import add_utm_params
from src.modules.helper.stack_df import stack_df
from src.modules.helper.time import (
    est_now_ap_brief,
    convert_iso_to_datetime,
    est_now_iso,
)
from src.modules.helper.get_county_pop import get_county_pop
from src.modules.helper.get_neighbors import get_neighbors
from src.modules.helper.rank_text import rank_text
from src.modules.helper.sort_counties_by_pop import sort_counties_by_pop


def test_get_neighbors(gdf_processed):
    neighbors = get_neighbors("Dauphin", gdf_processed)
    assert "Lebanon" in neighbors
    assert "Allegheny" not in neighbors
    print(neighbors)


def test_get_county_pop():
    pop = get_county_pop("Dauphin")
    assert type(pop) == int
    assert pop == 278299


def test_get_county_pop_lowercase():
    pop = get_county_pop("dauphin")
    assert pop == 278299


def test_get_county_pop_total():
    pop = get_county_pop("Total")
    print(pop)


def test_sort_counties_by_pop():
    neighbors = ["dauphin", "juniata", "cumberland", "york", "lancaster", "lebanon"]
    neighbors = sort_counties_by_pop(neighbors)
    assert neighbors == [
        "lancaster",
        "york",
        "dauphin",
        "cumberland",
        "lebanon",
        "juniata",
    ]
    assert neighbors != [
        "dauphin",
        "juniata",
        "cumberland",
        "york",
        "lancaster",
        "lebanon",
    ]


def test_est_ap_style():
    datetime_obj1 = convert_iso_to_datetime("2020-08-01")
    result1 = est_now_ap_brief(datetime_obj1)
    assert result1 == "Aug. 1, 2020"

    datetime_obj2 = convert_iso_to_datetime("2020-07-30")
    result2 = est_now_ap_brief(datetime_obj2)
    assert result2 == "July 30, 2020"


def test_rank_text():
    rank = rank_text(1, 67)
    assert rank == "highest"
    rank = rank_text(1, 2)
    assert rank == "highest"
    rank = rank_text(2, 1)
    assert rank == "lowest"
    rank = rank_text(3, 7)
    assert rank == "3rd highest"
    rank = rank_text(7, 2)
    assert rank == "2nd lowest"
    rank = rank_text(5, 5)
    assert rank == "same"


def test_rank_equal():
    """Tests situations where all items are equally ranked"""
    rank = rank_text(1, 1)
    assert rank == "same"
    print(rank)


def test_stack_df(dauphin_county_data):
    df = dauphin_county_data["cases"]
    df = stack_df(
        df,
        x_axis_col="date",
        stack_cols=[
            "added_since_prev_day",
            "total_per_capita",
            "moving_avg",
            "moving_avg_per_capita",
        ],
    )
    df_total_per_capita = df.loc[df["category"].str.contains("total_per_capita")]
    df_total_per_capita = df_total_per_capita.set_index("date")
    total_per_capita_june_20 = df_total_per_capita.loc["2020-06-20", "value"]
    assert round(total_per_capita_june_20) == 627


def test_add_utm_params_to_simple_url():
    url = "https://www.spotlightpa.org"
    new_url = add_utm_params(url)
    expected_url = f"https://www.spotlightpa.org?utm_source=covid_alerts&utm_medium=email&utm_campaign={est_now_iso()}"
    assert new_url == expected_url
    print(new_url)


def test_add_utm_params_to_url_with_existing_params():
    url = "https://www.spotlightpa.org?test=yes&fake=yes"
    new_url = add_utm_params(url)
    expected_url = (
        f"https://www.spotlightpa.org?test=yes&fake=yes&utm_source=covid_alerts&utm_medium=email"
        f"&utm_campaign={est_now_iso()}"
    )
    assert new_url == expected_url


def test_add_utm_params_to_url_and_encode_spaces():
    url = "https://www.spotlightpa.org?test=yes&fake=yes"
    new_url = add_utm_params(url, source="brand new campaign")
    expected_url = f"https://www.spotlightpa.org?test=yes&fake=yes&utm_source=brand+new+campaign&utm_medium=email&utm_campaign={est_now_iso()}"
    print(new_url)
    assert new_url == expected_url
