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
from src.modules.gen_chart.daily_and_avg import daily_and_avg
from src.modules.gen_chart.stacked_area import stacked_area
from src.modules.gen_chart.themes import spotlight
from src.modules.gen_html.gen_html import gen_html
from src.modules.init.init_program import init_program
from src.modules.fetch.fetch import fetch_data
from src.modules.process_data.helper.stack_df import stack_df
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
    county = "dauphin"
    data = process_data(data, data_index, county)

    # create email payload
    county_payload = []
    for key, item in data_index.items():
        chart_payload = []
        logging.info(f"Creating payload for: {key}")

        # create charts
        alt.themes.register("spotlight", spotlight)
        alt.themes.enable("spotlight")
        for chart_obj in item["charts"]:
            chart_type = chart_obj["type"]
            chart_title = chart_obj["title"]
            fmt = "png"
            content_type = "image/png"
            primary_color = item["theme"]["colors"]["primary"]
            secondary_color = item["theme"]["colors"]["secondary"]
            if "daily_and_avg" in chart_type:
                chart = daily_and_avg(
                    data_type=key,
                    df=data[key],
                    line_color=primary_color,
                    bar_color=secondary_color,
                )
            elif "stacked_area" in chart_type:
                df_cases = data["cases"]
                df_tests = data["tests"]
                df_cases = df_cases[["date", "total"]]
                df_tests = df_tests[["date", "total"]]
                df_tests = df_tests[df_tests["total"] > 0]
                # We merge data to ensure that we're using a common date range
                df = df_cases.merge(
                    df_tests,
                    left_on="date",
                    right_on="date",
                    how="inner",
                    suffixes=("_cases", "_tests"),
                )
                df["negative"] = df["total_tests"] - df["total_cases"]
                print("Merged df", df)
                df = df.rename(columns={"total_cases": "positive"})
                df = stack_df(
                    df,
                    xAxisCol="date",
                    stackCols=["positive", "negative"],
                    yAxisLabel="count",
                    categoryLabel="data_type",
                )
                print("Stacked df", df)
                chart = stacked_area(
                    df,
                    x_axis_col="date",
                    y_axis_col="count",
                    category_col="data_type",
                    domain=["positive", "negative"],
                    range_=[primary_color, secondary_color],
                )
            image_filename = f"{county}_{key}_{chart_type}.{fmt}"
            image_path = DIR_DATA / image_filename
            save(chart, str(image_path))
            logging.info("...saved")

            # move to s3
            copy_to_s3(
                image_path, bucket_name, bucket_dest_dir, content_type=content_type
            )

            chart_payload.append(
                {
                    "title": f"{chart_title.title()}",
                    "image_path": f"http://{bucket_name}/{bucket_dest_dir}/{image_filename}",
                    "description": f"Info about {key.title()} {chart_title} chart for {county}",
                }
            )

        # add to email payload
        county_payload.append(
            {
                "title": f"{key.title()} in {county.title()} County",
                "charts": chart_payload,
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
        "sections": county_payload,
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
