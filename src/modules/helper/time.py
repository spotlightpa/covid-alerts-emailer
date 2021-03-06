from datetime import datetime
import pytz
import logging
import iso8601


def utc_now() -> datetime:
    return pytz.utc.localize(datetime.utcnow())


def convert_utc_to_est(utc: datetime) -> datetime:
    return utc.astimezone(pytz.timezone("US/Eastern"))


def format_datetime_eastern(datetime_obj: datetime):
    # Formats a datetime obj into a pretty string in US/Eastern timezone
    est_time = convert_utc_to_est(datetime_obj)
    return est_time.strftime("%b %-d %Y, %I:%M %p")


def est_now_formatted_brief() -> str:
    # Provides current EST time as a pretty string in US/Eastern timezone
    now = utc_now()
    est_time = convert_utc_to_est(now)
    return est_time.strftime("%b %-d, %Y")


def est_now_ap_brief(datetime_obj: datetime = None) -> str:
    """ Converts current EST date into AP-style formatted string. Eg. Aug. 13, 2020

    Args:
        datetime_obj (datetime, optional): Instead of getting current datetime, this datetime obj will be
            convert to AP-style string instead.

    Returns:
         AP formatted date string. Eg. Aug. 13, 2020
    """
    replace_list = {
        "January": "Jan.",
        "February": "Feb.",
        "August": "Aug.",
        "September": "Sept.",
        "October": "Oct.",
        "December": "Dec.",
    }
    if not datetime_obj:
        now = utc_now()
        datetime_obj = convert_utc_to_est(now)

    date_str = datetime_obj.strftime("%B %-d, %Y")
    for key, item in replace_list.items():
        date_str = date_str.replace(key, item)
    return date_str


def est_now_iso() -> str:
    # Provides current EST time as ISO formatted string
    now = utc_now()
    est_time = convert_utc_to_est(now)
    return est_time.strftime("%Y-%m-%d")


def convert_iso_to_datetime(iso_str) -> datetime:
    # Converts ISO string into datetime obj
    logging.info(f"Converting from ISO to datetime obj...")
    datetime_obj = iso8601.parse_date(iso_str)
    assert isinstance(datetime_obj, datetime), (
        f"Failed to convert date into " f"datetime obj"
    )
    logging.info(f"Datetime obj: {iso_str}")
    return datetime_obj
