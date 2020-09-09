from src.modules.helper.add_utm_params import add_utm_params
from src.modules.helper.formatters import format_commas
from src.modules.helper.time import est_now_ap_brief
from typing import List, Dict


def gen_jinja_vars(
    county_name: str,
    *,
    county_payload: List[Dict],
    newsletter_browser_link: str,
    story_promo: List[Dict[str, str]],
) -> Dict:
    """
    Creates a dict of variables for jinja HTML templates.

    Args:
        county_name (str): Name of county
        county_payload (List[Dict]): List of dictionaries containing county info, like links to chart images.
        newsletter_browser_link (str): Hyperlink to HTML of final newsletter.
        story_promo (List[Dict[str,str]]): Spotlight stories to promo

    Returns:
        A dictionary of newsletter variables.
        
    """
    # constants
    brief_date = est_now_ap_brief()
    promo_1_url = (
        "https://www.inquirer.com/newsletters/election/sign-up/?utm_source=email&utm_campaign=mktg_pa2020_"
        "leadgen&utm_medium=referral&utm_content=spotlightpa&utm_term=&int_promo="
    )
    spotlight_url = add_utm_params("https://www.spotlightpa.org")
    subscribe_url = add_utm_params("https://www.spotlightpa.org/newsletters/covid")
    dashboard_url = add_utm_params(
        "https://www.spotlightpa.org/news/2020/03/pa-coronavirus-updates-cases-map-live-tracker/"
    )
    newsletter_url = add_utm_params("https://www.spotlightpa.org/newsletters/")
    unsubscribe_url = add_utm_params(
        "https://www.spotlightpa.org/newsletters/covid-alerts-manage"
    )
    donate_url = add_utm_params("https://www.spotlightpa.org/donate/")

    # large text blocks
    promo_1_tagline = (
        "<strong>Pennsylvania is a critical state in determining who wins the White House this "
        "year</strong>. The "
        "Philadelphia Inquirer just launched a weekly newsletter with exclusive reporting covering "
        "the entire state on issues that impact you, plus fact-checks, guides to voting, and more. "
        f'Sign up to follow along at <a href="{promo_1_url}" target="_blank">Inquirer.com/PA2020</a>.'
    )
    footer_about = (
        f'<a href="{spotlight_url}" target="_blank">Spotlight PA</a> is an independent, '
        f"non-partisan "
        "newsroom powered by The Philadelphia Inquirer in partnership with PennLive/The Patriot-News, "
        "TribLIVE/Pittsburgh Tribune-Review and WITF Public Media."
    )

    # final payload dict
    payload = {
        "head": {
            "title": f"The latest COVID-19 statistics for {county_name} from Spotlight PA."
        },
        "preview_text": f"Here are the latest stats on cases, deaths, and testing in {county_name}",
        "newsletter_browser_link": newsletter_browser_link,
        "subscribe_link": subscribe_url,
        "hero": {
            "title": "Weekly Coronavirus Update".upper(),
            "tagline": county_name.upper(),
        },
        "promos": {
            1: {
                "image_path": "https://interactives.data.spotlightpa.org/assets/promos/newsletter-promo__pa2020.png",
                "url": promo_1_url,
                "tagline": promo_1_tagline,
            }
        },
        "section_welcome": f"{brief_date}: Read on for more information about how cases, deaths, and tests are trending "
        f"in {county_name} and the surrounding area.",
        "section_stories": story_promo,
        "section_donate": {
            "blurb": "If you value this public service, <b>please donate now</b> at <a "
            f'href="{donate_url}">spotlightpa.org/donate</a>'
        },
        "sections_data": county_payload,
        "section_dash": {
            "title": "Want more stats?",
            "blurb": "For the latest COVID-19 statistics on Pennsylvania and surrounding states, check out our <a "
            'class="dash__link" '
            f'href="{dashboard_url}" '
            'target="_blank">live coronavirus tracker</a>. For a round-up of the best accountability reporting in '
            f'Pennsylvania, sign up for our weekly <a href="{newsletter_url}" target="_blank">'
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
        "footer": {"about": footer_about},
        # Note that SendGrid will automatically try to include unsubscribe links in final email HTML if either its
        # default preferences or unsubscribe magic links are not included in the email.
        "sg_unsubscribe_preferences_link": "{{{unsubscribe_preferences}}}",
        "sg_unsubscribe_link": "{{{unsubscribe}}}",
        "spotlight_unsubscribe_link": unsubscribe_url,
    }
    return payload
