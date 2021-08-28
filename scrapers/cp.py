from datetime import datetime

from scrapers.base.core import ScraperBase
from scrapers.base.response import SOLD_OUT


class Scraper(ScraperBase):
    name = "CP"

    def _load_data(self, request):
        params = {
            "From": request.src,
            "FromHidden": "",
            "To": request.dst,
            "ToHidden": "",
            "AdvancedForm.Via[0]": "",
            "AdvancedForm.ViaHidden[0]": "",
            "Date": request.date.strftime("%d.%m.%Y"),
            "Time": "",
            "IsArr": "False"
        }

        res = self.client.post("https://cp.hnonline.sk/vlakbusmhd/spojenie/", data=params)

    def _check_data(self, data):
        pass

    def _parse_data(self, data):
        pass


if __name__ == "__main__":
    Scraper().scrape_cli()
