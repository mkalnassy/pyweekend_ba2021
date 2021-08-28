SOLD_OUT = object()


class TripResponse(dict):
    DEFAULT_KEYS = frozenset(
        [
            "departure_datetime",
            "arrival_datetime",
            "source",
            "destination",
            "carrier",
            "fare",
        ]
    )

    DEFAULT_FARE_KEYS = frozenset(["amount", "currency"])

    def __init__(self, data):
        super().__init__(data)

        self._check_data()

    def _check_data(self):
        # simply do some checks about data validity
        pass

    @property
    def readable(self) -> str:
        itin_parts = [
            self["departure_datetime"].replace(tzinfo=None),
            self["arrival_datetime"].replace(tzinfo=None),
            self["source"],
            self["destination"],
            self["carrier"],
        ]

        itin_parts = list(map(str, itin_parts))
        itin_out = "    ".join(itin_parts)

        if self["fare"] == SOLD_OUT:
            price_out = "sold_out"
        else:
            # convert price to eur here
            pass

            price_out = "{amount} {currency}".format(**self["fare"])

        return " | ".join([itin_out, price_out])

    def __repr__(self):
        return f"TripResponse({self.readable})"
