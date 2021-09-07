from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection, Row

from app.enums import VehicleType
from app.models import Journeys

# * in function definition enforces the rest of the parameters to be positional ones


def create(connection: Connection, *, journey: Dict[str, Any]) -> Optional[Row]:
    """Try to create a journey.
    
    If such a journey exists, `None` is returned to the caller.
    """
    query = insert(Journeys).values(**journey).returning("*").on_conflict_do_nothing()
    executed_query = connection.execute(query)
    return executed_query.one_or_none()


def get_many(
    connection: Connection,
    *,
    source: Optional[str] = None,
    destination: Optional[str] = None,
    departure_datetime: Optional[datetime] = None,
    arrival_datetime: Optional[datetime] = None,
    carrier: Optional[str] = None,
    vehicle_types: Optional[List[VehicleType]] = None,
) -> List[Row]:
    """Get a list of journeys based on specified conditions."""
    conditions = []
    if source is not None:
        conditions.append(Journeys.c.source == source)
    if destination is not None:
        conditions.append(Journeys.c.destination == destination)
    if departure_datetime is not None:
        conditions.append(Journeys.c.departure_datetime >= departure_datetime)
    if arrival_datetime is not None:
        conditions.append(Journeys.c.arrival_datetime <= arrival_datetime)
    if carrier is not None:
        conditions.append(Journeys.c.carrier == carrier)
    if vehicle_types is not None:
        conditions.append(Journeys.c.vehicle_type.in_([vehicle_type.value for vehicle_type in vehicle_types]))
    
    query = select(Journeys).where(*conditions)
    executed_query = connection.execute(query)
    return executed_query.fetchall()
