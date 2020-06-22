from definitions import PATH_OUTPUT_HTML, DIR_TEMPLATES
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.process_data import process_data
from vega_datasets import data as vega_data
import altair as alt


def main():

    # init
    init_program()

    # fetch
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    dataIndex = {
        "cases": {
            "name": "cases",
            "filename": "pa-cases.csv",
            "clean_rules": {
                "added_since_prev_day": True,
                "moving_avg": "added_since_prev_day",
            },
        },
        "deaths": {
            "name": "deaths",
            "filename": "pa-deaths.csv",
            "clean_rules": {
                "added_since_prev_day": True,
                "moving_avg": "added_since_prev_day",
            },
        },
        "tests": {"filename": "pa-tests.csv", "clean_rules": {"moving_avg": "total"},},
    }

    data = fetch_data(dir, dataIndex)

    # clean and filter
    data = process_data(data, dataIndex, "Dauphin")

    # create chart
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")
    svg_encoded = daily_and_avg(data["cases"])

    newsletter_vars = {
        "head": {"title": "The latest COVID-19 statistics from Spotlight PA"},
        "hero": {
            "title": "COVID-19 Report",
            "tagline": "The latest coronavirus statistics on Dauphin County",
            "date": "July 24, 2020",
        },
        "section_list": [
            {"title": "State overview", "content": "Map and stats for Pennsylvania",},
            {
                "title": "Cases in Dauphin County",
                "content": "Info about cases",
                "image": svg_encoded,
            },
            {"title": "Deaths in Dauphin County", "content": "Info about deaths"},
            {"title": "Tests in Dauphin County", "content": "Info about tests"},
        ],
    }

    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(PATH_OUTPUT_HTML, "w") as fout:
        fout.writelines(html)


if __name__ == "__main__":
    main()
