import requests
from csv import DictReader, DictWriter
import json

from geo_loc import GeoLoc
from weather_api import Weather

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("locs_file", type=str, default="locations.csv", help="Locations CSV file with country, state, city columns")
    parser.add_argument("api_key_file", type=str, default="api_key.json", help='JSON file name with API key: {"api_key": [key]}')
    parser.add_argument("-o", "--output", default=None, type=str, help="Output file name (if None prints to screen)")
    args = parser.parse_args()

    if args.output:
        # Create the CSV writer:
        fieldnames = ['country', 'state', 'city', 'temp', 'wind_speed', 'clouds']
        outfile = open(args.output, 'w')
        writer = DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    else:
        writer = None

    # Read the credentials, and create the Weather and Geo Location class instances:
    creds = json.load(open(args.api_key_file, 'r'))
    weather = Weather(creds['api_key'])
    geo_loc = GeoLoc(creds['api_key'])

    # Open the locations file and read the lines
    with open(args.locs_file, 'r') as fp:
        reader = DictReader(fp)
        # Now go over the rows in the CSV input and add the weather for each:
        for row in reader:
            # Try to get the location from the row
            if(geo_loc.find_location(row['country'], row['state'], row['city'])):
                # Found the location. Add the weather:
                weather_data = weather.current_weather(geo_loc)
                # Add the weather data to the record:
                row['temp'] = weather_data['temp']
                row['wind_speed'] = weather_data['wind_speed']
                row['clouds'] = weather_data['clouds']
            else:
                # Didn't find the location. Write the row with an error to the console:
                print(f"Could not find location for {row}")
                continue
            # Now write the result row to the output:
            if writer is not None:
                writer.writerow(row)
            else:
                print(row)


