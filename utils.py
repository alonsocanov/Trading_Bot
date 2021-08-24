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


def readJson(file_path):
    if os.path.isfile(file_path):
        file = open(file_path)
        data = json.load(file)
        file.close()
        return data
    else:
        message = ['Could find file:', file_path]
        log_message('ERROR', message)


if __name__ == '__main__':
    pass
