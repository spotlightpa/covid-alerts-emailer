import pandas as pd


def pandas_opts():
    # Sets desired pandas options
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_colwidth", 150)
    pd.set_option("display.width", 2000)
    pd.set_option("display.max_rows", 2000)
