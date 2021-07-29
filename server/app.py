import utm
from typing import List
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, APIRouter, Request, Form

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


# API Routes
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


# GUI Routes
gui_router = APIRouter()


@gui_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": {}})


@gui_router.post("/", response_class=HTMLResponse)
async def index(request: Request):
    data = dict(await request.form())
    all_converted = []
    if data["conversion_type"] == "ll2utm":
        dtypes = [float, float]
        func = utm.from_latlon

    elif data["conversion_type"] == "utm2ll":
        dtypes = [float, float, int, str]
        func = utm.to_latlon

    for coord in data["input_text"].split("\n"):
        payload = [dtype(param.strip()) for dtype, param in zip(dtypes, coord.split(","))]
        converted = func(*payload)
        all_converted.append(",".join([str(param) for param in converted]))

    data["output_text"] = "\n".join(all_converted)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


app.include_router(gui_router, prefix="", tags=["gui"])
app.include_router(api_router, prefix="/api", tags=["api"])
