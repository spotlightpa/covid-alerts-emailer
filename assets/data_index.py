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
        "charts": [
            {
                "type": "daily_and_avg",
                "title": "Daily",
                "legend": [
                    {"label": "Daily cases", "color": "#F4D2D2"},
                    {"label": "7 day avg", "color": "#CC0000"},
                ],
            }
        ],
    },
    "deaths": {
        "name": "deaths",
        "filename": "pa-deaths.csv",
        "theme": {"colors": {"primary": "#1D204E", "secondary": "#CCCEE5"}},
        "clean_rules": {
            "added_since_prev_day": True,
            "moving_avg": "added_since_prev_day",
        },
        "charts": [
            {
                "type": "daily_and_avg",
                "title": "Daily",
                "legend": [
                    {"label": "Daily deaths", "color": "#CCCEE5"},
                    {"label": "7 day avg", "color": "#1D204E"},
                ],
            }
        ],
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
            {
                "type": "daily_and_avg",
                "title": "Daily",
                "legend": [
                    {"label": "Daily deaths", "color": "#CBECEC"},
                    {"label": "7 day avg", "color": "#009999"},
                ],
            },
            {
                "type": "stacked_area",
                "title": "Cumulative",
                "legend": [
                    {"label": "Positive", "color": "#CBECEC"},
                    {"label": "Negative", "color": "#009999"},
                ],
            },
        ],
    },
}
