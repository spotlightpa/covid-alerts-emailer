from src.modules.helper.formatters import format_commas
from src.modules.helper.time import (
    est_now_formatted_brief,
    est_now_ap_brief,
)
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
    brief_date = est_now_ap_brief()
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
        "section_welcome": f"{brief_date}: Read on for more information about how cases, deaths, and tests are trending "
        f"in {county_name} and the surrounding area.",
        "section_donate": {
            "blurb": "If you value this public service, <b>please donate now</b> at <a "
            'href="https://www.spotlightpa.org/donate/">spotlightpa.org/donate</a>'
        },
        "sections_data": county_payload,
        "section_dash": {
            "title": "Want more stats?",
            "blurb": "For the latest COVID-19 statistics on Pennsylvania and surrounding states, check out our <a "
            'class="dash__link" '
            'href="https://www.spotlightpa.org/news/2020/03/pa-coronavirus-updates-cases-map-live-tracker/" '
            'target="_blank">live coronavirus tracker</a>. For a round-up of the best accountability reporting in '
            'Pennsylvania, sign up for our weekly <a href="https://www.spotlightpa.org/newsletters/" target="_blank">'
            "newsletter</a>.",
        },
        "section_footnote": {
            "footnote": "Cases include both lab-confirmed positive results and cases deemed probable based on "
            "federal criteria. Total test numbers are calculated by adding together positive and negative "
            "lab results. Total and positive test numbers prior to July 13 may include a small number of probable "
            "cases in addition to lab-confirmed results. Also note that county rankings of per capita "
            "cases and deaths use dense ranking. Ranks are incremented by only one regardless of how many counties "
            "share the same rank. For instance, if three counties are ranked as having the highest number of new cases "
            "per capita, the next highest ranking county or group of counties will be "
            'considered the "second highest".',
            "sources": "Pa. Department of Health data compiled by Spotlight PA and The Philadelphia "
            "Inquirer.",
        },
        "footer": {
            "about": "Spotlight PA is an independent, non-partisan newsroom powered by The Philadelphia Inquirer, the PennLive/The Patriot-News and other media partners."
        },
        "unsubscribe_preferences_link": "{{{unsubscribe_preferences}}}",
        "unsubscribe_link": "{{{unsubscribe}}}",
    }
    return payload
