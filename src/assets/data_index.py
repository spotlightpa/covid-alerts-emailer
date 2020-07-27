# Config file for data fetching and cleaning

data_index = {
    "cases": {
        "filename": "pa-cases.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "total_per_capita": True,
            "moving_avg": "added_since_prev_day",
            "moving_avg_per_capita": True,
        },
    },
    "confirmed": {
        "filename": "pa-confirmed.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "total_per_capita": True,
            "moving_avg": "added_since_prev_day",
            "moving_avg_per_capita": True,
        },
    },
    "deaths": {
        "filename": "pa-deaths.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "total_per_capita": True,
            "moving_avg": "added_since_prev_day",
            "moving_avg_per_capita": True,
        },
    },
    "tests": {
        "filename": "pa-tests.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "total_per_capita": True,
            "moving_avg": "added_since_prev_day",
            "moving_avg_per_capita": True,
            "set_first_non_zero_val_to_zero": "added_since_prev_day",
        },
    },
}
