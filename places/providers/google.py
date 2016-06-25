import requests

from places.providers.base import BasePlacesProvider

SEARCH_RADIUS = 20000

PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={key}&location={lat}%2C{lng}&query={query}&language=ru&radius={radius}"


class GooglePlacesProvider(BasePlacesProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_places(self, query, lat, lng):
        url = PLACES_API_URL.format(
            key=self.api_key, lat=lat, lng=lng, query=query, radius=SEARCH_RADIUS)

        r = requests.get(url)
        return r.json()['results']
