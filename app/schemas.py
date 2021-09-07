from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from pydantic import BaseModel, root_validator
from sqlalchemy.engine import Row

from app.enums import VehicleType


class Journey(BaseModel):
    source: str
    destination: str
    departure_datetime: datetime
    arrival_datetime: datetime
    carrier: str
    vehicle_type: VehicleType
    price: Decimal
    currency: str


class InJourney(Journey):
    @root_validator
    def validate_departure_arrival_datetimes(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["departure_datetime"] >= values["arrival_datetime"]:
            raise ValueError("Departure is later or at the same time as arrival.")
        return values

    def to_record(self) -> Dict[str, Any]:
        """Convert an object to dict representation processable on the DB level.
        
        This has to explicitly convert `VehicleType` value to string.
        """
        return {**self.dict(exclude={"vehicle_type"}), "vehicle_type": self.vehicle_type.value}


class OutJourney(Journey):
    id: int

    @classmethod
    def from_record(cls, record: Row) -> "OutJourney":
        return cls(
            id=record.id,
            source=record.source,
            destination=record.destination,
            departure_datetime=record.departure_datetime,
            arrival_datetime=record.arrival_datetime,
            carrier=record.carrier,
            vehicle_type=VehicleType(record.vehicle_type),
            price=record.price,
            currency=record.currency
        )
