import requests
import os

GEO_API_BASE = os.environ.get("GEO_API_BASE", "http://api.openweathermap.org/geo/1.0/direct").strip('/')

class GeoLoc:
    """
    This class uses the geo-location API. It accepts a location by country, state, city, zip code, and saves the lat-long
    """

    def __init__(self, api_key):
        """
        Init the class. Provide the user's API key
        :param api_key: The API key for the user
        """
        self.api_key = api_key
        self.lat = None
        self.lon = None

    def find_location(self, country, state=None, city=None):
        """
        Queries the API for a location
        :param country: Must have a country name - should be the 2 or 3 letter code according to ISO-3166
        :param state: A state 2 letter code (optional, can be None)
        :param city: A city name (can be None if zip code is provided)
        :return: True for success, False for failed to find location
        """
        loc = country
        if state:
            # Add the state to the query
            loc = f"{state},{loc}"
        if city:
            # Add the city to the query
            loc = f"{city},{loc}"

        params = {"q": loc,
                  "limit": 1,
                  "appid": self.api_key}
        response = requests.get(GEO_API_BASE, params=params)
        if response.status_code != 200:
            raise Exception(f"Error in geo loc request. Got error code {response.status_code}: {response.content}")
        loc_result = response.json()
        if len(loc_result) > 0:
            # We found a location. Take the first one returned:
            self.lat = loc_result[0]["lat"]
            self.lon = loc_result[0]["lon"]
            self.country = loc_result[0].get("country")
            self.state = loc_result[0].get("state")
            self.city = loc_result[0].get("name")
            return True
        return False