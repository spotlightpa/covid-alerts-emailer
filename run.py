from definitions import DIR_DATA, PATH_OUTPUT_HTML
from src.gen_html.gen_html import gen_html
from src.helper.encode import encode_str_base64
from src.init.init_program import init_program

import altair as alt
from vega_datasets import data
from altair_saver import save
import requests


def main():

    # init
    init_program()

    # rget data

    # data

    # Create altair graphic
    cars = data.cars()
    chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(x="Horsepower", y="Miles_per_Gallon", color="Origin",)
    )
    # chart.show()
    path = DIR_DATA / "chart.svg"
    # save(chart, str(path))
    svg_str = save(chart, fmt="svg")
    svg_encoded = encode_str_base64(svg_str)

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

    html = gen_html(templates_path="src/templates", template_vars=newsletter_vars)
    with open(PATH_OUTPUT_HTML, "w") as fout:
        fout.writelines(html)


if __name__ == "__main__":
    main()
