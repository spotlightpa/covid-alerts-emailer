import pytest

from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.helper.get_county_pop import get_county_pop
from src.modules.process_data.helper.get_neighbors import get_neighbors
from src.modules.process_data.helper.sort_counties_by_pop import sort_counties_by_pop


def test_get_neighbors(gdf):
    neighbors = get_neighbors("Dauphin", gdf)
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
