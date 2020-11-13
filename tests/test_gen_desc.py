import pytest

from src.modules.gen_stats.gen_stats import GenStats


def test_gen_desc_dauphin(data_clean, gdf_processed):
    print("\n", gdf_processed)
    gen_desc = GenStats("Dauphin", gdf=gdf_processed)
    result = gen_desc.gen_desc_area_tests()
    print(result)


def test_gen_desc_greene(data_clean, gdf_processed):
    gen_desc = GenStats("Greene", gdf=gdf_processed)
    result = gen_desc.gen_desc_neighbors("deaths")
    print(result)


def test_gen_desc_greene(data_clean, gdf_processed):
    gen_desc = GenStats("Greene", gdf=gdf_processed)
    result = gen_desc.gen_desc_choro("deaths")
    print(result)
