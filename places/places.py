import os

from places.providers.google import GooglePlacesProvider

PROVIDERS = [
    GooglePlacesProvider(os.getenv('GOOGLE_PLACES_API_KEY'))
]


def get_places(query, lat, lng):
    places = []

    for provider in PROVIDERS:
        query_result = provider.get_places(query, lat, lng)
        places.extend(query_result)

    return places
