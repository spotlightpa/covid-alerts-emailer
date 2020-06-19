import os

from definitions import PATH_OUTPUT_HTML, DIR_TEMPLATES
from src.gen_chart.gen_chart import gen_chart
from src.gen_html.gen_html import gen_html
from src.init.init_program import init_program
from src.fetch.fetch import fetch_data
from src.clean.clean import clean


def main():

    # init
    init_program()

    # fetch
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    dataIndex = {
        "cases": {
            "name": "cases",
            "filename": "pa-cases.csv",
            "clean_rules": {"addedSincePrevDay": True},
        },
        "deaths": {
            "name": "deaths",
            "filename": "pa-deaths.csv",
            "clean_rules": {"addedSincePrevDay": True},
        },
        "tests": {
            "filename": "pa-tests.csv",
            "clean_rules": {"addedSincePrevDay": True},
        },
    }

    data = fetch_data(dir, dataIndex)

    # clean and filter
    data = clean(data, dataIndex, "Dauphin")
    quit()

    # Create altair graphic
    cars = data.cars()
    svg_encoded = gen_chart(cars, y="Miles_per_Gallon", x="Horsepower")

    newsletter_vars = {
        "head": {"title": "The latest COVID-19 statistics from Spotlight PA"},
        "hero": {
            "title": "COVID-19 Report",
            "tagline": "The latest coronavirus statistics on Dauphin County",
            "date": "July 24, 2020",
        },
        "section_list": [
            {
                "title": "State overview",
                "content": "Map and stats for Pennsylvania",
                "image": svg_encoded,
            },
            {"title": "Cases in Dauphin County", "content": "Info about cases"},
            {"title": "Deaths in Dauphin County", "content": "Info about deaths"},
            {"title": "Tests in Dauphin County", "content": "Info about tests"},
        ],
    }

    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(PATH_OUTPUT_HTML, "w") as fout:
        fout.writelines(html)


if __name__ == "__main__":
    main()
