from covid_email_alerts.modules.helper.time import (
    est_now_ap_brief,
    convert_iso_to_datetime,
)
from covid_email_alerts.modules.helper.get_county_pop import get_county_pop
from covid_email_alerts.modules.helper.get_neighbors import get_neighbors
from covid_email_alerts.modules.helper.rank_text import rank_text
from covid_email_alerts.modules.helper.sort_counties_by_pop import sort_counties_by_pop


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
    assert rank == "5th highest"
