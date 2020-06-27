import pandas as pd
import geopandas

from definitions import PATH_PA_GEOJSON


def process_neighbors(df):
    df = geopandas.read_file(PATH_PA_GEOJSON)
    print(df.head(4))
    # quit()
    df["NEIGHBORS"] = None  # add NEIGHBORS column

    for index, country in df.iterrows():
        # get 'not disjoint' countries
        neighbors = df[~df.geometry.disjoint(country.geometry)].NAME.tolist()
        # remove own name from the list
        neighbors = [name for name in neighbors if country.NAME != name]
        # add names of neighbors as NEIGHBORS value
        df.at[index, "NEIGHBORS"] = ", ".join(neighbors)
    print(df[["NAME", "NEIGHBORS"]])
    quit()
