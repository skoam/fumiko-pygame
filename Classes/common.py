# Different objects & functions that will be used often

import random
import datetime
import time


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def random_id():
    return random.randrange(0, 999999)


def read_dict_from_file(file_name):
    content = ""
    read = open(file_name, "r")
    for line in read:
        content += line
    read.close()

    return eval(content)


def debug(item=None, msg="", error=False):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    if not error:
        print "\033[95m" + str(timestamp) + " : " + msg + " :\033[92m"
    else:
        print "\033[95m" + str(timestamp) + " : " + msg + " :\033[91m"

    if hasattr(item, "__dict__"):
        for key, value in item.__dict__.items():
            if hasattr(value, "__dict__"):
                for k, v in value.__dict__.items():
                    print "        " + k + " : " + str(v)
            else:
                print key + " : " + str(value)
    elif hasattr(item, "items()"):
        for key, value in item.items():
            if hasattr(value, "__dict__"):
                for k, v in value.__dict__.items():
                    print k + " : " + str(v)
            else:
                print key + " : " + str(value)
    elif item:
        print item
