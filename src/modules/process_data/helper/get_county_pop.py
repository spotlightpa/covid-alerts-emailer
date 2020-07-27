from definitions import PATH_PA_POP
import pandas as pd


def get_county_pop(county_name: str) -> int:
    """
    Gets a county's population based only on its name.
    
    Args:
        county_name (str): Name of county to get pop for.
    
    Returns:
        int: population of selected county.
    """
    county_name = county_name.lower()
    df_pop = pd.read_csv(PATH_PA_POP)

    if county_name == "total":
        return df_pop["population"].sum()
    else:
        df_pop["name"] = df_pop["name"].str.lower()
        df_pop = df_pop.set_index("name")
        county_pop = df_pop.at[county_name, "population"]
        return int(county_pop)
