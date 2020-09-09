from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse
from src.modules.helper.time import est_now_iso


def add_utm_params(
    url, source="covid_alerts", medium="email",
):
    """
    Takes a URL and returns a new URL with UTM parameters appended. UTM parameters are used for analytics.

    Args:
        url (str): URL
        source (str, optional): Campaign source. Defaults to "covid_alerts"
        medium (str, optional): Campaign medium. Defaults to "email"

    Returns:
        str: a URL with UTM parameters.
        Eg. "https://www.spotlightpa/?utm_source=covid_alerts&utm_medium=email&utm_campaign=2020-09-09"
    """
    args = {"utm_source": source, "utm_medium": medium, "utm_campaign": est_now_iso()}
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(args)
    url_parts[4] = urlencode(query)
    new_url = urlunparse(url_parts)
    return new_url
