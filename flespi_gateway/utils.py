"""Helpers to work with python wrapper of flespi api 
"""


from datetime import datetime
import pytz


def convert_unix_ts(timestamp, timezone = "Europe/Berlin"):
    """Utility function to help converting flespi utc unix time output to human readable.

    Parameters:
    -----------
    timestamp: int
        Unix time generated py flespi platform.

    timezone: str
        Time zone of the user. Defaoults to: Europe/Berlin

    Returns:
    --------
    date: str
        Human readable time with a following format: %Y-%m-%d %H:%M:%S
    """
    timezone = pytz.timezone(timezone)
    date = datetime.fromtimestamp(timestamp, timezone)

    return date.strftime('%Y-%m-%d %H:%M:%S')
