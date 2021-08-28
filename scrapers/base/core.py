import os
import json

from abc import ABC, abstractmethod
from typing import Iterator, Any

from httpx import Client, Response

from scrapers.base.request import Request
from scrapers.base.response import TripResponse

# TODO
# 1. tests
# 2. docstrings
# 3. data validation (inputs, outputs)
# 4. print -> logging


class ScraperBase(ABC):
    name = None

    def __init__(self):
        # if we didn't care about lazy evaluation
        # self.client = Client()

        self._client = None
        self._mapping = None

    @property
    def station_mapping(self) -> dict:
        if self._mapping is None:
            path = os.path.join(os.path.dirname(__file__), "mappings.json")

            with open(path) as f:
                self._mapping = json.load(f)[self.name]

        return self._mapping

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client()

        return self._client

    def scrape_cli(self):
        request = Request.from_cli()

        list(self.scrape_iter(request))

    def scrape_iter(self, request: Request) -> Iterator[TripResponse]:
        raw_response = self._load_data(request)

        self._check_data(raw_response)

        for trip in self._parse_data(raw_response):
            trip_response = TripResponse(trip)

            print(trip_response.readable)
            yield trip_response

    @abstractmethod
    def _load_data(self, request: Request) -> Any:
        return

    @abstractmethod
    def _check_data(self, data: Any) -> None:
        return

    @abstractmethod
    def _parse_data(self, data: Any) -> dict:
        return

    # or simply a dummy way for abstract class (without inheriting from ABC)
    # def _load_data(self, request):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def _check_data(self, data):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def _parse_data(self, data):
    #     raise NotImplementedError

