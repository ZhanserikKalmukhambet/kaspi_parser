import time as tm

from datetime import datetime, timedelta


def convert_datetime_to_milliseconds(date_time):
    """ Method to convert datetime object to milliseconds """

    return int(tm.mktime(date_time.timetuple()) * 1000)


def convert_datetime_from_milliseconds(milliseconds: int):
    """ Method to convert milliseconds to datetime object """

    return datetime.fromtimestamp(milliseconds / 1000.0).date()