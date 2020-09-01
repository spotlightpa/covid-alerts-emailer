from src.assets.data_index import DATA_INDEX
from src.definitions import FETCH_DIR_URL
from src.modules.fetch.fetch_data import fetch_data
from src.modules.fetch.fetch_stories import fetch_stories


def test_fetch_stories():
    stories = fetch_stories(3)
    assert len(stories) == 3
    print(stories)


def test_fetch_covid_data():
    data_raw = fetch_data(FETCH_DIR_URL, DATA_INDEX)
    assert data_raw["cases"] is not None
    assert data_raw["deaths"] is not None
    assert data_raw["tests"] is not None
