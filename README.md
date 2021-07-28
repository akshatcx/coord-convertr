# Coord Convertr
Application to convert various formats of coordinates.


## Running the Application
```bash
pip install -r requirements.txt
python main.py
```

OpenAPI Spec (Swagger UI) available at https://0.0.0.0:8888/api

## Testing the Application
```bash
pip install pytest
pytest
```

## API Specification
### Routes
- `/api/latlon-to-utm` (to convert from latlong to UTM format)
- `/api/utm-to-latlon` (to convert from UTM to latlong format)

### Models

```python
class LatLonCoord(BaseModel):
    latitude: float
    longitude: float

class UTMCoord(BaseModel):
    easting: float
    northing: float
    zone_number: int
    zone_letter: str
```

