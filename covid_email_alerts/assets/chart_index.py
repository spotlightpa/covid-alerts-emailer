# Config file for chart creation. Determines what charts appear and how they look.

CHART_INDEX = {
    "cases": {
        "name": "cases",
        "theme": {"colors": {"primary": "#CC0000", "secondary": "#F4D2D2"}},
        "charts": [
            {
                "type": "daily_and_avg",
                "title": "Daily trend",
                "custom_legend": [
                    {"label": "Daily cases", "color": "#F4D2D2"},
                    {"label": "7 day avg", "color": "#CC0000"},
                ],
            },
            {
                "type": "choropleth",
                "title": "Per capita rate",
                "color_field": "cases_added_past_two_weeks_per_capita",
                "legend_title": "Cases per 100,000",
            },
            {
                "type": "neigbhors_per_capita",
                "title": "Regional comparison",
                "compare_field": "moving_avg_per_capita",
                "neighbor_limit": 4,
            },
        ],
    },
    "deaths": {
        "name": "deaths",
        "theme": {"colors": {"primary": "#1D204E", "secondary": "#CCCEE5"}},
        "charts": [
            {
                "type": "daily_and_avg",
                "title": "Daily trend",
                "custom_legend": [
                    {"label": "Daily deaths", "color": "#CCCEE5"},
                    {"label": "7 day avg", "color": "#1D204E"},
                ],
            },
            {
                "type": "choropleth",
                "title": "Per capita rate",
                "color_field": "deaths_added_past_two_weeks_per_capita",
                "legend_title": "Deaths per 100,000",
            },
            {
                "type": "neigbhors_per_capita",
                "title": "Regional comparison",
                "compare_field": "moving_avg_per_capita",
                "neighbor_limit": 4,
            },
        ],
    },
    "tests": {
        "theme": {"colors": {"primary": "#009999", "secondary": "#CBECEC"}},
        "charts": [
            {
                "type": "daily_and_avg",
                "title": "Daily trend",
                "custom_legend": [
                    {"label": "Daily tests", "color": "#CBECEC"},
                    {"label": "7 day avg", "color": "#009999"},
                ],
            },
            {
                "type": "stacked_area",
                "title": "Running totals",
                "custom_legend": [
                    {"label": "Total tests", "color": "#CBECEC"},
                    {"label": "Positive", "color": "#009999"},
                ],
            },
        ],
    },
}
