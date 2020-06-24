from src.modules.gen_chart.daily_and_avg import daily_and_avg

data_index = {
    "cases": {
        "name": "cases",
        "filename": "pa-cases.csv",
        "theme": {"colors": {"primary": "#CC0000", "secondary": "#F4D2D2"}},
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
        "charts": [{"type": "daily_and_avg", "title": "Daily"}],
    },
    "deaths": {
        "name": "deaths",
        "filename": "pa-deaths.csv",
        "theme": {"colors": {"primary": "#1D204E", "secondary": "#CCCEE5"}},
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
        "charts": [{"type": "daily_and_avg", "title": "Daily"}],
    },
    "tests": {
        "filename": "pa-tests.csv",
        "theme": {"colors": {"primary": "#009999", "secondary": "#CBECEC"}},
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
            "set_first_non_zero_val_to_zero": "added_since_prev_day",
        },
        "charts": [
            {"type": "daily_and_avg", "title": "Daily"},
            {"type": "stacked_area", "title": "Cumulative"},
        ],
    },
}
