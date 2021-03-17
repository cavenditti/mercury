from datetime import datetime, timedelta

import time

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


class time_interval:
    def __init__(self, start: datetime, ending: [datetime, timedelta]):
        self.start = start
        if type(ending) == timedelta:
            self.end = start + ending
        else:
            self.end = ending

    def days_between(self) -> str:
        return days_between(self.start,self.end)

    def months_between(self) -> str:
        return months_between(self.start,self.end)

    #def years(

    def duration(self):
        return timedelta(self.start, self.end)
