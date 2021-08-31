from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://172.20.10.8:8000",
        "http://172.20.10.2:8000",
        "http://0.0.0.0:8000",
        "http://localhost:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse(
        "item.html",
        {"request": request, "id": "kokot"},
    )


def search_journeys(origin, destination, time_from, time_to) -> List[dict]:
    return [
        {
            "carrier": "Flixbus",
            "origin": origin,
            "destination": destination,
            "departure": str(time_from.isoformat()),
            "arrival": str(time_to.isoformat()),
        }
    ] * 5


@app.post("/search")
def search(
    request: Request,
    origin: Optional[str] = Form(None),
    destination: Optional[str] = Form(None),
    time_from: Optional[datetime] = Form(None),
    time_to: Optional[datetime] = Form(None),
):
    journeys = search_journeys(origin, destination, time_from, time_to)
    response = {
        "journeys": journeys,
        "origin": origin,
        "destination": destination,
        "time_from": str(time_from.isoformat()) if time_from else None,
        "time_to": str(time_to.isoformat()) if time_to else None,
    }
    if request.headers["accept"] == "application/json":
        return JSONResponse(response)
    response["request"] = request
    return templates.TemplateResponse("search_results.html", response)


@app.get("/whisperer")
def whisperer(field: str, term: str):
    return [term] * 3
