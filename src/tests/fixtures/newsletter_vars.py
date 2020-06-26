from src.modules.helper.formatters import format_commas
from src.modules.helper.time import est_now_formatted_brief
from assets.data_index import data_index


def gen_dummy_county_payload(bucket_name, bucket_dest_dir, county, data_index):
    payload = []
    for data_type, data_index_dict in data_index.items():
        for chart_dict in data_index_dict["charts"]:
            chart_type = chart_dict["type"]
            payload.append(
                {
                    "title": "",
                    "legend": chart_dict["legend"],
                    "image_path": f"https://{bucket_name}/{bucket_dest_dir}/{county}_{data_type}_{chart_type}.png",
                    "description": "Description of chart and stats, blah blah blah",
                }
            )
    return payload


def gen_dummy_template_vars(county):
    bucket_name = "interactives.data.spotlightpa.org"
    bucket_dest_dir = "assets/covid-email-alerts/test"

    county_payload = gen_dummy_county_payload(
        bucket_name, bucket_dest_dir, county, data_index
    )

    newsletter_vars = {
        "stats_pa": {
            "title": "Pennsylvania",
            "stats_items": [
                {"label": "cases", "value": format_commas(10000),},
                {"label": "deaths", "value": format_commas(1000),},
            ],
        },
        "stats_county": {
            "title": f"{county}",
            "stats_items": [
                {"label": "cases", "value": format_commas(2000),},
                {"label": "deaths", "value": format_commas(200),},
            ],
        },
        "preview_text": f"Here are the latest stats on cases, deaths, and testing in {county}",
        "newsletter_browser_link": f"https://{bucket_name}/{bucket_dest_dir}/newsletter.html",
        "unsubscribe_preferences_link": "{{{unsubscribe_preferences}}}",
        "unsubscribe_link": "{{{unsubscribe}}}",
        "head": {
            "title": f"The latest COVID-19 statistics for {county} from Spotlight PA."
        },
        "hero": {
            "title": "COVID-19 Report",
            "tagline": f"The latest COVID-19 statistics for {county}.",
            "date": est_now_formatted_brief(),
        },
        "sections": county_payload,
    }
