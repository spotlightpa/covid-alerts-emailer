import json
import logging
import altair as alt
from altair_saver import save
from definitions import (
    PATH_OUTPUT_HTML,
    DIR_TEMPLATES,
    PATH_DATA_COUNTY_LIST,
    DIR_DATA,
)
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.process_data import process_data
from assets.data_index import data_index
from src.modules.s3.copy_to_s3 import copy_to_s3
from src.modules.send_email.send_email_list import send_email_list


def main():

    # init
    init_program()
    bucket_name = "interactives.data.spotlightpa.org"
    bucket_dest_dir = "assets/covid-email-alerts/test"

    # fetch
    with open(PATH_DATA_COUNTY_LIST) as f:
        counties = json.load(f)
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    data = fetch_data(dir, data_index)

    # clean and filter
    county = "carbon"
    data = process_data(data, data_index, county)

    # create email payload
    county_info = []
    for key, item in data_index.items():
        logging.info(f"Creating payload for: {key}")

        # create charts
        alt.themes.register("spotlight", spotlight)
        alt.themes.enable("spotlight")
        for chart_generator in item["charts"]:
            fmt = "png"
            # content_type = "image/svg+xml"
            content_type = "image/png"
            chart = chart_generator(
                data_type=key,
                df=data[key],
                save_chart=True,
                fmt=fmt,
                line_color=item["theme"]["colors"]["primary"],
                bar_color=item["theme"]["colors"]["secondary"],
            )
            image_filename = f"{county}_{key}.{fmt}"
            image_path = DIR_DATA / image_filename
            save(chart, str(image_path))
            logging.info("...saved")

            # move to s3
            copy_to_s3(
                image_path, bucket_name, bucket_dest_dir, content_type=content_type
            )

        # add to email payload
        county_info.append(
            {
                "title": f"{key.title()} in {county.title()} County",
                "content": f"Info about {key.title()}",
                "image_path": f"http://{bucket_name}/{bucket_dest_dir}/{image_filename}",
            }
        )

    # Generate HTML
    newsletter_vars = {
        "preview_text": "COVID-19 case trend information",
        "newsletter_browser_link": f"https://{bucket_name}/{bucket_dest_dir}/newsletter.html",
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
    copy_to_s3(PATH_OUTPUT_HTML, bucket_name, bucket_dest_dir, content_type="text/html")

    # Send email
    logging.info("Sending email...")
    send_email_list(html, counties["42043"]["id"], subject="Test alert!")
    logging.info("...email sent")


if __name__ == "__main__":
    main()
