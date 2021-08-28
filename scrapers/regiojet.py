from datetime import datetime

from scrapers.base.core import ScraperBase
from scrapers.base.response import SOLD_OUT


class Scraper(ScraperBase):
    name = "REGIOJET"

    search_currency = "CZK"


    def _load_data(self, request):
        params = {
            "departureDate": request.date.strftime("%Y-%m-%d"),
            "fromLocationId": request.src,
            "fromLocationType": "STATION",
            "locale": "cs",
            "tariffs": "REGULAR",
            "toLocationId": request.dst,
            "toLocationType": "STATION",
        }

        self.client.headers = {"X-Currency": self.search_currency}

        response = self.client.get(
            "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple", params=params
        )
        return response.json()

    def _check_data(self, data):
        msg = data.get("message")
        if msg:
            if "departureDate.invalid" in msg or "arrivalDate.invalid" in msg:
                raise Exception("invalid date")

            raise Exception("unhandled error")

        if not data["routes"]:
            raise Exception("no routes in response")

    def _parse_data(self, data):
        for trip in data["routes"]:
            time_format = "%Y-%m-%dT%H:%M:%S.000%z"
            dept_time = datetime.strptime(trip["departureTime"], time_format)
            arrv_time = datetime.strptime(trip["arrivalTime"], time_format)

            if not trip["bookable"]:
                fare = SOLD_OUT
            else:
                fare = {
                    "amount": float(trip["priceFrom"]),
                    "currency": self.search_currency,
                }

            yield {
                "departure_datetime": dept_time,
                "arrival_datetime": arrv_time,
                "source": "AAA",
                "destination": "BBB",
                "type": trip["vehicleTypes"][0],
                "free_seats": trip["freeSeatsCount"],
                "carrier": self.name,
                "fare": fare,
            }


if __name__ == "__main__":
    Scraper().scrape_cli()
