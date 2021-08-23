from datetime import date
import json
import os
import sys
from logs import log_message
import time


def strToFloat(value):
    if not isinstance(value, float):
        value = float(value)
    return value


def floatToStr(value):
    if not isinstance(value, str):
        value = str(value)
    return value


def sleep(var):
    # ints are equivalent to seconds
    time.sleep(var)


if __name__ == '__main__':
    pass
