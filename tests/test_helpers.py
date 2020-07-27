import pytest

from src.modules.init.pandas_opts import pandas_opts
from src.modules.process_data.helper.get_neighbors import get_neighbors


def test_get_neighbors(gdf):
    pandas_opts()
    get_neighbors("Dauphin", gdf)
