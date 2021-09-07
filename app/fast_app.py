from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.engine import Connection

from app.database import db_connection, engine
from app.models import metadata
from app.schemas import InJourney, OutJourney
from app.storage import journeys as journeys_storage

app = FastAPI()


@app.on_event("startup")
def on_startup_event():
    """This function is called by the framework on starup.
    
    Ensure that all the DB objects are created and exist in the current DB.
    """
    metadata.create_all(engine)


@app.get("/search", response_model=List[OutJourney])
def search(
    source: Optional[str] = None,
    destination: Optional[str] = None,
    departure_datetime: Optional[datetime] = None,
    connection: Connection = Depends(db_connection),
):
    """Look for all direct journeys between source and destination."""
    journeys = journeys_storage.get_many(
        connection, source=source, destination=destination, departure_datetime=departure_datetime
    )

    return [OutJourney.from_record(journey) for journey in journeys]


@app.post("/create", response_model=OutJourney)
def create(journey: InJourney, connection: Connection = Depends(db_connection)):
    """Create a new journey based on provided attributes.
    
    If no journey was created, it means that it is duplicate so we raise a 409 duplicate error.
    """
    created_journey = journeys_storage.create(connection, journey=journey.to_record())

    if created_journey is not None:
        return OutJourney.from_record(created_journey)
    
    raise HTTPException(409, "A journey like this already exists.")
