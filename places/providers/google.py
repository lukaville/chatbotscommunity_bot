import requests

from places.providers.base import BasePlacesProvider

SEARCH_RADIUS = 20000

PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={key}&location={lat}%2C{lng}&query={query}&language=ru&radius={radius}"
PLACE_DETAIL_API_URL = "https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={key}&language=ru"
PLACE_LIMIT = 3

class GooglePlacesProvider(BasePlacesProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def get_place(self, place_id):
        detail_url = PLACE_DETAIL_API_URL.format(
            key=self.api_key,
            place_id=place_id
        )
        r = requests.get(detail_url)
        return r.json()['result']

    def get_places(self, query, lat, lng):
        url = PLACES_API_URL.format(
            key=self.api_key, lat=lat, lng=lng, query=query, radius=SEARCH_RADIUS
        )

        r = requests.get(url)
        places = r.json()['results'][:PLACE_LIMIT]

        for place in places:
            detail_place = self.get_place(place['place_id'])
            place.update(detail_place)

        return places
