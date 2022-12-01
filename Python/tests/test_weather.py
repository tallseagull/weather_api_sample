import os
from weather_api import Weather

api_key = os.environ.get("API_KEY")
weather = Weather(api_key)

test_cases = [(39.0817985, -77.1516844, 'T'),
              (5000, -22, 'E'),
              (32.1773471, 34.907459, 'T')]

class GeoLocMock:
    pass

for lat, lon, expected in test_cases:
    glm = GeoLocMock()
    glm.lat = lat
    glm.lon = lon
    try:
        res = weather.current_weather(glm)
    except Exception as e:
        assert expected=='E', Exception(f"for data {lat},{lon} expected result {expected}, got exception {e}")
        res = None
    if res is not None:
        assert expected=='T', Exception(f"for data {lat},{lon} expected result {expected}, got a result")
        # Check all fields are in the result:
        fields = ['temp', 'humidity', 'wind_speed', 'clouds', 'description']
        assert all(f in res for f in fields), Exception(f"for data {lat},{lon} not all fields in res: {res}")