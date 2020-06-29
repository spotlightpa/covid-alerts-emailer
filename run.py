import json
import logging
import altair as alt
from altair_saver import save
from definitions import (
    PATH_OUTPUT_HTML,
    DIR_TEMPLATES,
    PATH_COUNTY_LIST,
    DIR_DATA,
    PATH_PA_GEOJSON,
    PATH_PA_POP,
    PATH_OUTPUT_GEOJSON,
)
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.map_choropleth import map_choropleth
from src.modules.gen_chart.stacked_area import stacked_area
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_desc.desc_area_tests import desc_area_tests
from src.modules.gen_desc.desc_daily import desc_daily
from src.modules.gen_html.gen_html import gen_html
from src.modules.gen_html.gen_jinja_vars import gen_jinja_vars
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.merge_geo import merge_geo
from src.modules.process_data.process_clean import process_clean
from src.modules.process_data.process_cumulative_tests import process_cumulative_tests
from src.modules.process_data.process_individual_county import process_individual_county
from assets.data_index import data_index
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
    bucket_name = "interactives.data.spotlightpa.org"
    bucket_dest_dir = "assets/covid-email-alerts/test"

    # enable chart themes
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")

    # fetch
    with open(PATH_COUNTY_LIST) as f:
        counties = json.load(f)
    dir = "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
    data_raw = fetch_data(dir, data_index)
    # clean, filter, process
    data_clean = process_clean(data_raw)
    data_state = process_individual_county(data_clean, data_index, county="Total")
    state_stats = process_stats(data_state)
    gdf_pa = process_geo(
        PATH_PA_GEOJSON,
        path_pop_file=PATH_PA_POP,
        path_output_geojson=PATH_OUTPUT_GEOJSON,
    )
    gdf_pa = merge_geo(gdf_pa, data_clean)
    # test = gdf_pa.drop("NEIGHBORS", axis=1)
    gdf_pa.to_file(DIR_DATA / "pa_geodata.geojson", driver='GeoJSON')
    map_choropleth(gdf_pa, path_output_file=DIR_DATA/"map.png")
    # loop over counties and get charts + add newsletter text
    for fips, county_dict in test_counties.items():
        county = county_dict["name"]
        email_list_id = county_dict["id"]
        subscriber_count = count_subscribers(email_list_id)
        if subscriber_count == 0:
            logging.info(
                f"No subscribers in {county} email list, moving on to next county..."
            )
            continue
        logging.info(
            f"Creating newsletter payload for {county}, which has {subscriber_count} subscribers."
        )

        county_clean = county.replace(" County", "")
        county_data = process_individual_county(
            data_clean, data_index, county=county_clean
        )
        county_stats = process_stats(county_data)

        # create email payload
        county_payload = []
        for data_type, data_index_dict in data_index.items():
            chart_payload = []
            logging.info(f"Creating payload for: {data_type}")

            # create charts
            for chart_dict in data_index_dict["charts"]:
                chart_type = chart_dict["type"]
                chart_legend = chart_dict["legend"]
                chart_desc = ""
                fmt = "png"
                content_type = "image/png"
                primary_color = data_index_dict["theme"]["colors"]["primary"]
                secondary_color = data_index_dict["theme"]["colors"]["secondary"]
                if "daily_and_avg" in chart_type:
                    chart = daily_and_avg(
                        data_type=data_type,
                        df=county_data[data_type],
                        line_color=primary_color,
                        bar_color=secondary_color,
                    )
                    chart_desc = desc_daily(
                        data=county_data[data_type], data_type=data_type, county=county
                    )
                elif "stacked_area" in chart_type:
                    df = process_cumulative_tests(
                        county_data["cases"], county_data["tests"]
                    )
                    chart = stacked_area(
                        df,
                        x_axis_col="date",
                        y_axis_col="count",
                        category_col="data_type",
                        domain=["positive", "negative"],
                        range_=[primary_color, secondary_color],
                    )
                    chart_desc = desc_area_tests(data=df, county=county)

                image_filename = f"{county_clean}_{data_type}_{chart_type}.{fmt}"
                image_path = DIR_DATA / image_filename
                save(chart, str(image_path))
                logging.info("...saved")

                # generate county description

                # move to s3
                copy_to_s3(
                    image_path, bucket_name, bucket_dest_dir, content_type=content_type
                )

                chart_payload.append(
                    {
                        "title": "",
                        "legend": chart_legend,
                        "image_path": f"https://{bucket_name}/{bucket_dest_dir}/{image_filename}",
                        "description": chart_desc,
                    }
                )

            # add to email payload
            county_payload.append(
                {"title": f"{data_type.title()} in {county}", "charts": chart_payload,}
            )

        # Generate HTML
        subject = f"COVID-19 Report: {county}"
        newsletter_browser_link = (
            f"https://{bucket_name}/{bucket_dest_dir}/newsletter.html"
        )
        newsletter_vars = gen_jinja_vars(
            county,
            county_payload=county_payload,
            newsletter_browser_link=newsletter_browser_link,
            state_stats=state_stats,
            county_stats=county_stats,
        )
        html = gen_html(templates_path=DIR_TEMPLATES, template_vars=newsletter_vars)
        with open(PATH_OUTPUT_HTML, "w") as fout:
            fout.writelines(html)
        copy_to_s3(
            PATH_OUTPUT_HTML, bucket_name, bucket_dest_dir, content_type="text/html"
        )

        # Send email
        logging.info(f"Sending email for {county}...")
        send_email_list(html, email_list_id, subject=subject)
        logging.info("...email sent")


if __name__ == "__main__":
    main()
