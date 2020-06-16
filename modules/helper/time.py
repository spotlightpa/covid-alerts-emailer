from datetime import datetime
import pytz
import logging
import iso8601

def utc_now():
    return pytz.utc.localize(datetime.utcnow())


def convert_utc_to_est(utc):
    return utc.astimezone(pytz.timezone("US/Eastern"))


def format_datetime_eastern(datetime_obj):
    # Formats a datetime obj into a pretty string in US/Eastern timezone
    est_time = convert_utc_to_est(datetime_obj)
    return est_time.strftime("%b %-d %Y, %I:%M %p")


def convert_iso_to_datetime(iso_str):
    # Converts ISO string into datetime obj
    logging.info(f"Converting from ISO to datetime obj...")
    datetime_obj = iso8601.parse_date(iso_str)
    assert (isinstance(datetime_obj, datetime)), f"Failed to convert date into " \
                                                                 f"datetime obj"
    logging.info(f"Datetime obj: {iso_str}")
    return datetime_obj