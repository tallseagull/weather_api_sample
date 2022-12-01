from geo_loc import GeoLoc
import os
import math

api_key = os.environ.get("API_KEY")
geo_loc = GeoLoc(api_key)

# Test cases: each is a tuple of:
#   * The parameters
#   * The expected result ('T' - success, 'F' - failed, 'E' - exception)
#   * lat expected result
#   * lon expected result
test_cases = [({'country': 'US', 'state': 'MD', 'city': 'Rockville'}, 'T', 39.0817985, -77.1516844),
              ({'country': 'IL', 'city': 'Kfar Saba'}, 'T', 32.1773471, 34.907459),
              ({'country': 'US', 'state': 'CA'}, 'F', None, None),  # Need a city
              ({}, 'E', None, None),    # No data - fails on exception for no argument for country
              ({'country': 'ABCDEFG', 'city': 'XTYZ'}, 'F', None, None) # Invalid names
              ]

for test_data, test_result, lat, lon in test_cases:
    try:
        res = geo_loc.find_location(**test_data)
    except Exception as e:
        # We caught an exception.
        assert test_result == 'E', Exception(f"Got an exception {e} for {test_data}, expected result {test_result}")
        res = None
    if res is True:
        assert test_result == 'T', Exception(f"Got result {res} for {test_data}, expected result {test_result}")
        # Only in this case we compare the lat/lon:
        assert math.isclose(geo_loc.lat, lat, rel_tol=1e-3) & math.isclose(geo_loc.lon, lon, rel_tol=1e-3), \
            Exception(f"Mismatch in lat/lon for {test_data}: got lat={geo_loc.lat}, lon={geo_loc.lon}")
    elif res is False:
        assert test_result == 'F', Exception(f"Got result {res} for {test_data}, expected result {test_result}")

