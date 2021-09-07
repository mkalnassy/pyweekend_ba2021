from sqlalchemy import Column, Integer, MetaData, Numeric, Sequence, String, Table, TEXT, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP

metadata = MetaData()

# this definition creates the same table in the DB but Journeys is no longer a class that would represent a journey
# a Dict of values is used when querying and the same should be used for inserting


Journeys = Table(
    "journeys",
    metadata,
    # columns
    Column(
        "id",
        Integer,
        Sequence("journeys_seq"),
        primary_key=True,
        comment="Autoincremented primary identifier of a journey.",
    ),
    Column("source", TEXT, nullable=False, comment="Lower-cased name of the origin of a journey."),
    Column("destination", TEXT, nullable=False, comment="Lower-cased destination of a journey."),
    Column("departure_datetime", TIMESTAMP, nullable=False),
    Column("arrival_datetime", TIMESTAMP, nullable=False),
    Column(
        "carrier",
        TEXT,
        index=True,
        nullable=False,
        comment=(
            "Lower-cased name of a carrier that operates a journey. "
            "It is usually an IATA code for airlines or a name of a ground carrier."
        ),
    ),
    Column("vehicle_type", ENUM("airplane", "bus", "train", name="vehicle_type_enum"), nullable=False),
    Column(
        "price",
        Numeric(20, 6),
        nullable=False,
        comment=(
            "Numeric representation of a price."
            "It is adviced to use this type for storing monetary amounts."
            "This numeric specifies that it has max 20 digits while 6 of them can be to the right of the decimal point."
        ),
    ),
    Column("currency", String(3), nullable=False, comment="ISO-formated currency of a price."),
    # constraints
    UniqueConstraint(
        "source", "destination", "departure_datetime", "arrival_datetime", "carrier", name="unique_journey"
    ),
)   
