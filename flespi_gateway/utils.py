"""Helpers to work with python wrapper of flespi api
"""


from datetime import datetime
import pytz


def convert_unix_ts(timestamp, timezone="Europe/Berlin"):
    """Utility function to help converting flespi utc unix time output to human readable.

    Parameters
    ----------
    timestamp : int
        Unix time generated py flespi platform.

    timezone : str
        Time zone of the user. Defaoults to: Europe/Berlin

    Returns
    -------
    date : str
        Human readable time with a following format: %Y-%m-%d %H:%M:%S
    """

    timezone = pytz.timezone(timezone)
    date = datetime.fromtimestamp(timestamp, timezone)

    return date.strftime('%Y-%m-%d %H:%M:%S')


def convert_human_ts(timestamp, timezone="Europe/Berlin"):
    """Utility function to help converting user given timestamp to flespi utc unix time.


    Parameters
    ----------
    timestamp : str
        Human readable timestamp.
        The following format is supported `2021-01-02 10:00:00`.

    Returns
    -------
    date : int
        Unix timestamp.

    Examples
    --------
    >>> ts = convert_human_ts('2021-01-02 10:00:00')
    >>> print(ts)
    1609578000
    """
    timezone = pytz.timezone(timezone)
    date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timezone_date_time_obj = timezone.localize(date_time_obj)
    return int(timezone_date_time_obj.timestamp())
