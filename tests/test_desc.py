import pytest

from src.modules.gen_desc.gen_desc import GenDesc


def test_gen_desc_dauphin(data_clean, dauphin_county_data, gdf_processed):
    print("\n", gdf_processed)
    gen_desc = GenDesc("Dauphin", dauphin_county_data, gdf=gdf_processed)
    result = gen_desc.area_tests()
    print(result)


def test_gen_desc_greene(data_clean, greene_county_data, gdf_processed):
    gen_desc = GenDesc("Greene", greene_county_data, gdf=gdf_processed)
    result = gen_desc.neighbors("deaths")
    print(result)


def test_gen_desc_greene(data_clean, greene_county_data, gdf_processed):
    gen_desc = GenDesc("Greene", greene_county_data, gdf=gdf_processed)
    result = gen_desc.choro("deaths")
    print(result)
