from src.modules.helper.formatters import format_commas
from src.modules.helper.time import est_now_formatted_brief
from typing import List, Dict


def gen_jinja_vars(
    county_name: str, *, county_payload=List[Dict], newsletter_browser_link: str,
) -> Dict:
    """
    Creates a dict of variables for jinja HTML templates.

    Args:
        county_name (str): Name of county
        county_payload (List[Dict]): List of dictionaries containing county info, like links to chart images.
        newsletter_browser_link (str): Hyperlink to HTML of final newsletter.

    Returns:
        A dictionary of newsletter variables.
        
    """
    brief_date = est_now_formatted_brief()
    payload = {
        "head": {
            "title": f"The latest COVID-19 statistics for {county_name} from Spotlight PA."
        },
        "preview_text": f"Here are the latest stats on cases, deaths, and testing in {county_name}",
        "newsletter_browser_link": newsletter_browser_link,
        "hero": {
            "title": "Weekly Coronavirus Update".upper(),
            "tagline": county_name.upper(),
        },
        "section_welcome": f"{brief_date}:  Over the past two weeks, {county_name} has had XXX new cases and XXX new "
        f"deaths. Read on for more information about how cases, deaths, and tests are trending in "
        f"{county_name.replace(' County','')} and the surrounding area.",
        "sections_data": county_payload,
        "footnote": {
            "sources": "Pa. Department of Health data collected daily by Spotlight PA/the Philadelphia "
            "Inquirer.",
            "note": "Cases include both lab-confirmed positive results and cases deemed probable based on federal "
            "criteria. "
            "Total test numbers are calculated by adding together positive and negative lab results. ‘Total' and "
            "'positive' numbers prior to July 13 include a small number of probable cases in addition to lab-confirmed "
            "results.",
        },
        "unsubscribe_preferences_link": "{{{unsubscribe_preferences}}}",
        "unsubscribe_link": "{{{unsubscribe}}}",
    }
    return payload
