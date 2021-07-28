import utm
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="coord-convertr", version="0.1.0", docs_url="/api")
templates = Jinja2Templates(directory="templates")

# Models
class LatLonCoord(BaseModel):
    latitude: float
    longitude: float


class UTMCoord(BaseModel):
    easting: float
    northing: float
    zone_number: int
    zone_letter: str


# Routes
api_router = APIRouter()


@api_router.post("/latlon-to-utm", response_model=List[UTMCoord], status_code=200)
def latlon_to_utm(coords: List[LatLonCoord]):
    utms = []
    for coord in coords:
        converted = utm.from_latlon(coord.latitude, coord.longitude)
        utms.append(
            {
                "easting": converted[0],
                "northing": converted[1],
                "zone_number": converted[2],
                "zone_letter": converted[3],
            }
        )
    return utms


@api_router.post("/utm-to-latlon", response_model=List[LatLonCoord], status_code=200)
def utm_to_latlon(coords: List[UTMCoord]):
    latlons = []
    for coord in coords:
        converted = utm.to_latlon(
            coord.easting, coord.northing, coord.zone_number, coord.zone_letter
        )
        latlons.append({"latitude": converted[0], "longitude": converted[1]})
    return latlons


# @app.get("/", response_class=HTMLResponse)
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/", response_class=HTMLResponse)
# async def result(request: Request):
#     data = await request.form()
#     out = process(data)
#     return templates.TemplateResponse("results.html", {"request": request, "result": out})

app.include_router(api_router, prefix="/api", tags=["api"])
