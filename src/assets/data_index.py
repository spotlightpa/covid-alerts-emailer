# Config file for data fetching and cleaning

data_index = {
    "cases": {
        "filename": "pa-cases.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
    },
    "confirmed": {
        "filename": "pa-confirmed.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
    },
    "deaths": {
        "filename": "pa-deaths.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
    },
    "tests": {
        "filename": "pa-tests.csv",
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
            "set_first_non_zero_val_to_zero": "added_since_prev_day",
        },
    },
}
