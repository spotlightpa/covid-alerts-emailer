import pytest

from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.helper.get_county_pop import get_county_pop
from src.modules.process_data.helper.get_neighbors import get_neighbors


def test_get_neighbors(gdf):
    neighbors = get_neighbors("Dauphin", gdf)
    assert "Lebanon" in neighbors
    assert "Allegheny" not in neighbors


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
