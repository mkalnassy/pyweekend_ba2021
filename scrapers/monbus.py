from datetime import datetime

from scrapers.base.core import ScraperBase
from scrapers.base.response import SOLD_OUT


class Scraper(ScraperBase):
    name = "MONBUS"

    search_currency = "EUR"

    def _load_data(self, request):
        src_data = self.station_mapping.get(request.src)
        dst_data = self.station_mapping.get(request.dst)

        self.client.cookies = {"USERLANG": "en"}

        params = {
            'route': '/src/net/monbus/horarios/trigger/results.php',
            'data[captcha]': '0',
            'data[searchType]': '1',
            'data[paradaOrigenAC]': src_data["name"],
            'data[paradaOrigen]': src_data["location_id"],
            'data[paradaDestinoAC]': dst_data["name"],
            'data[paradaDestino]': dst_data["location_id"],
            'data[nViajeros]': 1,  # let's search for 1 pax only
            'data[tipoBillete]': '1',
            'data[fechaIda]': request.date.strftime('%d/%m/%Y')
        }
        resp = self.client.get('https://www.monbus.es/', params=params)
        return resp


    def _check_data(self, data):
        pass

    def _parse_data(self, data):
        pass


if __name__ == "__main__":
    Scraper().scrape_cli()
