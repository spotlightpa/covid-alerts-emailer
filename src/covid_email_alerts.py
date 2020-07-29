import json
import logging
import altair as alt
from altair_saver import save
from definitions import (
    PATH_OUTPUT_HTML,
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    PATH_PA_GEOJSON,
    AWS_BUCKET,
    AWS_DIR_TEST,
)
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_payload.gen_county_payload import gen_county_payload
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_clean import process_clean
from src.modules.process_data.process_individual_county import process_individual_county
from src.assets.data_index import DATA_INDEX
from src.modules.process_data.process_geo import process_geo
from src.modules.process_data.process_stats import process_stats
from src.modules.s3.copy_to_s3 import copy_to_s3
from src.modules.send_email.count_subscribers import count_subscribers
from src.modules.send_email.send_email_list import send_email_list


def main():

    test_counties = {
        "42053": {
            "id": "84912f53-a7c7-46ed-ba80-10d4a07e9d48",
            "name": "Forest County",
        },
        "42043": {
            "id": "0724edae-40a6-48e6-8330-cc06b3c67ede",
            "name": "Dauphin County",
        },
    }

    # init
    init_program()

    # fetch
    with open(PATH_COUNTY_LIST) as f:
        counties = json.load(f)
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    data_raw = fetch_data(dir, DATA_INDEX)

    # clean, filter, process
    data_clean = process_clean(data_raw)
    data_state = process_individual_county(data_clean, DATA_INDEX, county_name="Total")
    state_stats = process_stats(data_state)
    gdf_raw = process_geo(PATH_PA_GEOJSON)
    gdf_processed = merge_geo(gdf_raw, data_clean)

    # loop over counties and get charts + add newsletter text
    for fips, county_dict in test_counties.items():
        # skip county if there are no subscribers to email list
        county_name = county_dict["name"]
        email_list_id = county_dict["id"]
        subscriber_count = count_subscribers(email_list_id)
        if subscriber_count == 0:
            logging.info(
                f"No subscribers in {county_name} email list, moving on to next county..."
            )
            continue
        logging.info(
            f"Creating newsletter payload for {county_name}, which has {subscriber_count} subscribers."
        )

        county_name_clean = county_name.replace(" County", "")
        county_data = process_individual_county(
            data_clean, DATA_INDEX, county_name=county_name_clean
        )
        county_stats = process_stats(county_data)

        # create email payload
        county_payload = gen_county_payload(
            county_name_clean,
            data_clean=data_clean,
            county_data=county_data,
            gdf=gdf_processed,
        )

        # Generate HTML
        subject = f"COVID-19 Report: {county_name}"
        newsletter_browser_link = f"https://{AWS_BUCKET}/{AWS_DIR_TEST}/newsletter.html"
        newsletter_vars = gen_jinja_vars(
            county_name=county_name,
            county_payload=county_payload,
            newsletter_browser_link=newsletter_browser_link,
        )
        html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)

        # Upload copy of HTML to s3
        with open(PATH_OUTPUT_HTML, "w") as fout:
            fout.writelines(html)
        copy_to_s3(PATH_OUTPUT_HTML, AWS_BUCKET, AWS_DIR_TEST, content_type="text/html")

        # Send email
        quit()
        logging.info(f"Sending email for {county_name}...")
        send_email_list(html, email_list_id, subject=subject)
        logging.info("...email sent")


if __name__ == "__main__":
    main()
