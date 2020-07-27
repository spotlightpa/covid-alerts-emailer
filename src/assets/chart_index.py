# Config file for chart creation

chart_index = {
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
                "color_field": "cases_per_capita",
                "legend_title": "Cases per 100,000",
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
                "color_field": "deaths_per_capita",
                "legend_title": "Deaths per 100,000",
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
                    {"label": "Daily deaths", "color": "#CBECEC"},
                    {"label": "7 day avg", "color": "#009999"},
                ],
            },
            {
                "type": "stacked_area",
                "title": "Running total",
                "custom_legend": [
                    {"label": "Total tests", "color": "#CBECEC"},
                    {"label": "Positive", "color": "#009999"},
                ],
            },
        ],
    },
}
