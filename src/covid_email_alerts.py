import json
import logging
from definitions import (
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    PATH_PA_GEOJSON,
    AWS_BUCKET,
    AWS_DIR_TEST,
    FETCH_DIR_URL,
    DIR_OUTPUT,
)
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.gen_payload.gen_county_payload import gen_county_payload
from src.modules.helper.condense_whitespace import condense_whitespace
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_clean import process_clean
from src.modules.process_data.process_individual_county import process_individual_county
from src.assets.data_index import DATA_INDEX
from src.modules.process_data.process_geo import process_geo
from src.modules.aws.copy_to_s3 import copy_to_s3
from src.modules.send_email.count_subscribers import count_subscribers
from src.modules.send_email.send_email_list import send_email_list
from src.modules.gen_html.minify import minify_email_html
from src.modules.helper.time import est_now_iso, est_now_ap_brief
from typing import List, Dict


def main(
    counties: Dict[str, Dict],
    email_send: bool = True,
    custom_subject_line: str = None,
    condense_email: bool = True,
) -> None:
    """
    Generates a unique newsletter based on COVID-19 data and emails it to selected counties.
    
    Args:
        counties (Dict[str, Dict]): Dict of dicts representing county names and sendgrid email ID,
        email_send (bool, optional): Whether to send emails. Defaults to True. Useful for testing program without
            sending emails.
        custom_subject_line (str, optional): A custom subject line that overwrites the programmatically generated
            subject line. Useful for testing purposes. Disabled by default.
        condense_email (bool, optional): Condenses multiple white spaces in email HTML into single spaces before
            sending. Defaults to True.

    Returns:
        None.
    """

    # set up basic settings
    init_program()

    # fetch COVID-19 data
    data_raw = fetch_data(FETCH_DIR_URL, DATA_INDEX)

    # clean, filter, process data
    data_clean = process_clean(data_raw)
    data_state = process_individual_county(data_clean, DATA_INDEX, county_name="Total")
    gdf_raw = process_geo(PATH_PA_GEOJSON)
    gdf_processed = merge_geo(gdf_raw, data_clean)

    # loop over dict of counties and generate charts and chatter
    for fips, county_dict in counties.items():
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

        # create email payload
        county_payload = gen_county_payload(
            county_name_clean=county_name_clean,
            data_clean=data_clean,
            county_data=county_data,
            gdf=gdf_processed,
        )

        # Generate HTML
        newsletter_filename = f"newsletter_{county_name_clean}_{est_now_iso()}.html"
        newsletter_local_path = DIR_OUTPUT / newsletter_filename
        newsletter_browser_link = (
            f"https://{AWS_BUCKET}/{AWS_DIR_TEST}/{newsletter_filename}"
        )
        newsletter_vars = gen_jinja_vars(
            county_name=county_name,
            county_payload=county_payload,
            newsletter_browser_link=newsletter_browser_link,
        )
        html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)

        # Upload copy of HTML to s3
        with open(newsletter_local_path, "w") as fout:
            fout.writelines(html)
        copy_to_s3(
            newsletter_local_path, AWS_BUCKET, AWS_DIR_TEST, content_type="text/html"
        )

        # Send email
        if email_send:
            html = html if not condense_email else condense_whitespace(html)
            subject = (
                f"COVID-19 Update: {county_name} ({est_now_ap_brief()})"
                if not custom_subject_line
                else custom_subject_line
            )
            logging.info(f"Sending email for {county_name}...")
            logging.info(f"Subject line: {subject}")
            send_email_list(html, email_list_id, subject=subject)
            logging.info("...email sent")
        else:
            logging.info("No email has been sent because 'email_send' option is False")


if __name__ == "__main__":
    # Get dict of county dicts
    with open(PATH_COUNTY_LIST) as f:
        selected_counties = json.load(f)
    main(selected_counties)
