from pathlib import Path
from datetime import datetime
import time
import sys

def safe_filename(string):
    keepcharacters = (' ','.','_')
    return "".join(c for c in string if c.isalnum() or c in keepcharacters).rstrip()

def create_path(the_path):
    Path(the_path).mkdir(parents=True, exist_ok=True)

def days_between(d1, d2):
    if type(d1) == str:
        d1 = datetime.strptime(d1, "%Y-%m-%d")
    if type(d2) == str:
        d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def months_between(d1, d2):
    return round(days_between(d1,d2)/30)

def duration_str(d1, d2):
    days = days_between(d1, d2)
    if days < 60:
        return str(days) + ' days'
    else:
        return str(round(days_between(d1,d2)/30)) + ' months'

def years_between(d1, d2) -> float:
    return days_between(d1,d2)/252

def print_date_interval(d1, d2):
    print('[', d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'), '->', duration_str(d1,d2), ']')

