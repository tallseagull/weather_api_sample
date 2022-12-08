import os
import requests

API_BASE = os.environ.get("WEATHER_API_BASE", "https://api.openweathermap.org/data/2.5/weather").strip('/')

class Weather:
    """
    Class to interface with openweathermap.org API
    """
    def __init__(self, api_key):
        """
        Init the class. Provide the user's API key
        :param api_key: The API key for the user
        """
        self.api_key = api_key

    def current_weather(self, geo_loc):
        """
        Get the weather for a location
        :param geo_loc: A location specification (should be an instance of the GeoLoc class)
        :return: The weather data as a dict with values for []
        """
        params = {'lat': geo_loc.lat,
                  'lon': geo_loc.lon,
                  'units': 'metric',
                  'appid': self.api_key}
        response = requests.get(API_BASE, params=params)
        if response.status_code != 200:
            raise Exception(f"Error in request. Got error code {response.status_code}: {response.content}")
        weather = response.json()

        # Extract the main components from the response:
        result = {'temp': weather['main']['temp'],
                  'humidity': weather['main']['humidity'],
                  'wind_speed': weather['wind']['speed'],
                  'clouds': weather['clouds']['all'],
                  'description': weather['weather'][0]['description']}
        return result
