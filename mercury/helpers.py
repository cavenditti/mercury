from pathlib import Path
from datetime import datetime
import time
import sys

def safe_filename(string : str) -> str:
    """
    Keeps special characters that are usually found in filenames.
    >>> safe_filename("spaces dots.underscores_work")
    'spaces dots.underscores_work'
    """
    keepcharacters = (' ','.','_')
    return "".join(c for c in string if c.isalnum() or c in keepcharacters).rstrip()

def create_path(the_path : str) -> str:
    Path(the_path).mkdir(parents=True, exist_ok=True)

def days_between(d1 : str, d2 : str) -> int:
    """
    Returns the number of days between two given date in YYYY-MM-DD format.
    >>> d1 = '2021-01-01'
    >>> d2 = '2021-02-01'
    >>> days_between(d1, d2)
    31
    """
    if type(d1) == str:
        d1 = datetime.strptime(d1, "%Y-%m-%d")
    if type(d2) == str:
        d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def months_between(d1 : str, d2 : str) -> int:
    """
    Returns the number of months between two given date in YYYY-MM-DD format,
    rounding to the nearest integer.
    >>> d1 = '2021-03-01'
    >>> d2 = '2021-05-15'
    >>> d3 = '2021-05-16'
    >>> months_between(d1, d2)
    2
    >>> months_between(d1, d3)
    3
    """
    return round(days_between(d1,d2)/30)

def duration(d1 : str, d2 : str) -> str:
    """
    Returns the number of days or months between two given date in YYYY-MM-DD format.
    The number of months is rounded to the nearest integer.
    >>> d1 = '2021-03-01'
    >>> d2 = '2021-05-16'
    >>> d3 = '2021-03-02'
    >>> duration(d1, d2)
    '3 months'
    >>> duration(d1, d3)
    '1 days'
    """
    days = days_between(d1, d2)
    if days < 60:
        return str(days) + ' days'
    else:
        return str(round(days_between(d1,d2)/30)) + ' months'

def print_date_interval(d1 : datetime, d2 : datetime) -> str:
    print('[', d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'), '->', duration(d1,d2), ']')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
