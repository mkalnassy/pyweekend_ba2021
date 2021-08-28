import argparse

from collections import namedtuple
from datetime import datetime

# from typing import NamedTuple

DATETIME_SUPPORTED_FORMATS = ["%d-%m-%Y", "%Y-%m-%d"]

# We could do sth like this to add typing to our src/dst/date attributes
# class Request(NamedTuple):
#     src: str
#     dst: str
#     date: datetime


class Request(namedtuple("request", "src dst date")):
    @staticmethod
    def date_type(date_string):
        for fmt in DATETIME_SUPPORTED_FORMATS:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                pass

        msg = f"date {date_string} doesn't match formats {DATETIME_SUPPORTED_FORMATS}"
        raise NotImplementedError(msg)

    @classmethod
    def from_cli(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument("src", nargs="?")
        parser.add_argument("dst", nargs="?")
        parser.add_argument("date", nargs="?", type=cls.date_type)

        args = parser.parse_args()

        return cls(args.src, args.dst, args.date)
