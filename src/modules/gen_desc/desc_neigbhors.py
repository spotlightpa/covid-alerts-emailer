def desc_neighbors(county_name_clean: str, data_type: str) -> str:

    output = (
        f"Compared to its XXXX neighboring counties, {county_name_clean} County had the XXX lowest number of {data_type} per "
        f"100,000 people over the past two weeks. Here's how {county_name_clean} "
        f"compares to its four most populous neighbors:"
    )
    return output
