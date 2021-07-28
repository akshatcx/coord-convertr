from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

# test /api/latlon-to-utm
def test_latlon_to_utm():
	payload = [{
		"latitude": 51.20,
		"longitude": 7.50
	}]
	response = client.post("/api/latlon-to-utm", json=payload)
	assert response.status_code == 200
	
	utm = response.json()[0]
	assert round(utm['easting'], 2) == 395201.31
	assert round(utm['northing'], 2) == 5673135.24
	assert utm['zone_number'] == 32
	assert utm['zone_letter'] == "U"

# test /api/utm-to-latlon
def test_utm_to_latlon():
	payload = [{
		"easting": 395201.31,
		"northing": 5673135.24,
		'zone_number': 32,
		'zone_letter': "U"
	}]
	response = client.post("/api/utm-to-latlon", json=payload)
	assert response.status_code == 200
	
	latlon = response.json()[0]
	assert round(latlon['latitude'], 2) == 51.20
	assert round(latlon['longitude'], 2) == 7.50