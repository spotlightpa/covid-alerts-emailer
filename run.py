from definitions import PATH_OUTPUT_HTML, DIR_TEMPLATES, PATH_DATA_INDEX
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.process_data import process_data
import altair as alt
import json
import logging


def main():

    # init
    init_program()

    # fetch
    with open(PATH_DATA_INDEX) as f:
        data_index = json.load(f)
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    data = fetch_data(dir, data_index)

    # clean and filter
    county = "carbon"
    data = process_data(data, data_index, county)
    print(data)

    # create email payload
    county_info = []
    for key, item in data_index.items():
        logging.info(f"Creating payload for: {key}")

        # create chart
        alt.themes.register("spotlight", spotlight)
        alt.themes.enable("spotlight")
        svg_encoded = daily_and_avg(
            data_type=key,
            df=data[key],
            save_chart=True,
            line_color=item["theme"]["colors"]["primary"],
            bar_color=item["theme"]["colors"]["secondary"],
        )

        # add to email payload
        county_info.append(
            {
                "title": f"{key.title()} in {county.title()} County",
                "content": f"Info about {key.title()}",
                "image": svg_encoded,
            }
        )

    newsletter_vars = {
        "head": {"title": "The latest COVID-19 statistics from Spotlight PA"},
        "hero": {
            "title": "COVID-19 Report",
            "tagline": f"The latest coronavirus statistics on {county.title()} County",
            "date": "July 24, 2020",
        },
        "section_list": county_info,
    }

    html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
    with open(PATH_OUTPUT_HTML, "w") as fout:
        fout.writelines(html)


if __name__ == "__main__":
    main()
