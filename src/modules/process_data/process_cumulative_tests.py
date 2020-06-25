from src.modules.process_data.helper.stack_df import stack_df
from pandas import DataFrame


def process_cumulative_tests(df_cases: DataFrame, df_tests: DataFrame) -> DataFrame:
    """
    Take a df of total tests per day and a df of total positive cases per day data and stacks the data on top of
    itself for use in an Altair area chart.

    Args:
         df_cases (pd.DataFrame): Cases data
         df_tests (pd.DataFrame): Tests data

    Returns:
        pd.DataFrame
    """
    df_cases = df_cases[["date", "total"]]
    df_tests = df_tests[["date", "total"]]
    # df_tests = df_tests[df_tests["total"] > 0]
    # We merge data to ensure that we're using a common date range
    df = df_cases.merge(
        df_tests,
        left_on="date",
        right_on="date",
        how="inner",
        suffixes=("_cases", "_tests"),
    )
    df["negative"] = df["total_tests"] - df["total_cases"]
    df["negative"] = df["negative"].apply(
        lambda x: x if x >= 0 else 0
    )  # default value to 0 if its negative

    print("Merged df", df)
    df = df.rename(columns={"total_cases": "positive"})
    df = stack_df(
        df,
        xAxisCol="date",
        stackCols=["positive", "negative"],
        yAxisLabel="count",
        categoryLabel="data_type",
    )
    return df
