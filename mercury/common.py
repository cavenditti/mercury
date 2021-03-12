from pathlib import Path
from datetime import datetime, timedelta
from threading import Lock
import time
import sys
import string

from .helpers import *

class HollowType(type):
    def __call__(cls, *a, **kw):
        raise TypeError('This class cannot be instantiated.')
    def __str__(self):
        return self.__name__.replace('_', ' ')
    def __repr__(self):
        return "<{}: '{}'>".format(self.__base__,str(self))

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


# from https://github.com/mmcloughlin/luhn
def luhn_checksum(numeric_string):
    """
    Compute the Luhn checksum for the provided string of digits. Note this
    assumes the check digit is in place.
    """
    digits = list(map(int, numeric_string))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10

class ISIN(str):
    def check(self):
        """
        Check if the provided string is a valid ISIN.
        """
        if len(self) != 12:
            return False

        numeric_isin = ''
        numeric_isin += string.ascii_letters.index(self[0])%26 + 10
        numeric_isin += string.ascii_letters.index(self[1])%26 + 10
        numeric_isin += self[2:]

        return (checksum(numeric_isin) == 0)

'''
--------------------------------------------------------------------------------
'''

t_print_lock = Lock()
def t_print(*a, **b):
    """Thread safe print function"""
    with t_print_lock:
        print(*a, **b)

class T_Counter:
    """ Thread-safe counter.
    TODO make this into a wrapper around pool.map() to do everything by itself
    """
    __instance__ = None

    def __init__(self, message, end):
        if type(end) is not int:
            raise TypeError('end should be \'int\', not {}'.format(type(end)))

        self.message = message
        self.end = end
        self.i = 0
        self.start_time = time.perf_counter()
        with t_print_lock:
            T_Counter.__instance__ = self
            sys.stdout.write("\r"+'{}: 0/{}'.format(self.message, self.end))
            sys.stdout.flush()

    @staticmethod
    def tick(name=None):
        """ Static method to update the counter.
        """
        with t_print_lock:
            if name is None:
                T_Counter.__instance__.i = T_Counter.__instance__.i + 1
                sys.stdout.write("\r"+'{}: {}/{}'.format(T_Counter.__instance__.message,
                    T_Counter.__instance__.i, T_Counter.__instance__.end))
                sys.stdout.flush()
            else:
                T_Counter.__instance__.i = T_Counter.__instance__.i + 1
                sys.stdout.write("\r"+'{}: {}/{}{:>50}'.format(T_Counter.__instance__.message,
                    T_Counter.__instance__.i, T_Counter.__instance__.end, T_Counter.__instance__.message))
                sys.stdout.flush()

    @staticmethod
    def done():
        with t_print_lock:
            elapsed = time.perf_counter() - T_Counter.__instance__.start_time
            sys.stdout.write("\r"+'{}: Done in {}s\n'.format(T_Counter.__instance__.message, elapsed))
            sys.stdout.flush()
            T_Counter.__instance__ = None
