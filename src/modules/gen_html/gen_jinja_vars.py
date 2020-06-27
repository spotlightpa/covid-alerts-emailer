from src.modules.helper.formatters import format_commas
from src.modules.helper.time import est_now_formatted_brief
from typing import List, Dict


def gen_jinja_vars(
    county: str,
    *,
    county_payload=List[Dict],
    state_stats: Dict,
    county_stats: Dict,
    newsletter_browser_link: str,
) -> Dict:
    """
    Creates a dict of variables for jinja HTML templates.

    Args:
        county (str): Name of county
        county_payload (List[Dict]): List of dictionaries containing county info, like links to chart images.
        state_stats (Dict): Dict of state statistics
        county_stats (Dict): Dict of county statistics
        newsletter_browser_link (str): Hyperlink to HTML of final newsletter.

    Returns:
        A dictionary of newsletter variables.
        
    """

    payload = {
        "stats_pa": {
            "title": "Pennsylvania",
            "stats_items": [
                {"label": "cases", "value": format_commas(state_stats["cases"]),},
                {"label": "deaths", "value": format_commas(state_stats["deaths"]),},
            ],
        },
        "stats_county": {
            "title": f"{county}",
            "stats_items": [
                {"label": "cases", "value": format_commas(county_stats["cases"]),},
                {"label": "deaths", "value": format_commas(county_stats["deaths"]),},
            ],
        },
        "preview_text": f"Here are the latest stats on cases, deaths, and testing in {county}",
        "newsletter_browser_link": newsletter_browser_link,
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
        "footnote": {
            "sources": "Pa. Department of Health data collected daily by Spotlight PA/the Philadelphia "
            "Inquirer.",
            "note": "Case totals include confirmed and probable cases. Note that data reporting tends to "
            "spike during the middle of the week and tail-off on the weekends. Similarly, "
            "sometimes the department revises it data, causing irregular patterns in its daily "
            "reported figures.",
        },
    }
    return payload
