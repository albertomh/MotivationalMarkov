# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Helper functions. """

import time
import calendar


class Helpers:
    def __init__(self):
        pass

    @staticmethod
    def to_timestamp(date, date_format):
        return int(calendar.timegm(time.strptime(date, date_format)))
