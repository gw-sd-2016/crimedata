from web import settings as websettings
from urllib.request import urlopen
from urllib.parse import urlencode
import json


def addr2coord(street_address):
    # Read in API key and URL from settings (local_settings.py has the actual values)
    google_api_key = websettings.GOOGLE_GEOCODE['API_KEY']
    google_api_url = websettings.GOOGLE_GEOCODE['API_URL']

    # Google API takes the street address and API key
    query_vars = {
        "address": street_address,
        "key": google_api_key,
    }

    # Encode query string ("?address=blah&key=123")
    encoded_query = urlencode(query_vars)
    # Concatenate the query string to the base URL
    geocode_url = "%s?%s" % (google_api_url, encoded_query)

    # Call out to Google API
    webreq = urlopen(geocode_url)
    response = webreq.read()
    response_parse = json.loads(response.decode(webreq.info().get_param('encoding') or "utf_8"))
    # TODO: Add error handling (API key limits, internet access issues, etc)

    # Return the complete response JSON received from Google
    return response_parse


def cached_addr2coord(street_address):
    # TODO: Build out caching mechanism for API results
    return addr2coord(street_address)