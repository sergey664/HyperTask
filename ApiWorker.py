import sys
from io import BytesIO

import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter
from PIL import Image


class ApiWorker:

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    static_maps_server = "https://static-maps.yandex.ru/1.x/"

    def __init__(self):
        self.geocoder_parameters = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "format": "json",
            "geocode": "",
        }

        self.static_maps_parameters = {
            "l": "map",
            "ll": "",
            "spn": "",
            "pt": ""
        }

    @staticmethod
    def get_ll(toponym):
        return ",".join(toponym["Point"]["pos"].split(" "))

    @staticmethod
    def get_spn(toponym):
        envelope = toponym["boundedBy"]["Envelope"]

        left, bottom = envelope["lowerCorner"].split(" ")
        right, top = envelope["upperCorner"].split(" ")

        return ",".join([str(abs(float(left) - float(right)) / 2), str(abs(float(bottom) - float(top)) / 2)])

    def load_geocoder_info(self, geocode):
        try:
            self.geocoder_parameters["geocode"] = geocode

            session = requests.Session()
            retry = Retry(total=10, connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('https://', adapter)

            response = session.get(self.geocoder_api_server, params=self.geocoder_parameters)

            self.geocoder_parameters["geocode"] = ""

            assert response

            return response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        except AssertionError and Exception:
            print("GEOCODER ERROR!")
            sys.exit()

    def load_static_map_info(self, geocode, pt=None):
        try:
            toponym = self.load_geocoder_info(geocode)

            self.static_maps_parameters["ll"] = self.get_ll(toponym)
            self.static_maps_parameters["spn"] = self.get_spn(toponym)
            if pt:
                self.static_maps_parameters["pt"] = ",".join([self.static_maps_parameters["ll"], pt])

            session = requests.Session()
            retry = Retry(total=10, connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('https://', adapter)

            response = session.get(self.static_maps_server, params=self.static_maps_parameters)

            assert "image" in response.headers.get("Content-Type")

            im = BytesIO(response.content)
            im.seek(0)
            opened_image = Image.open(im)
            opened_image.save("map.png", format='PNG')

        except AssertionError and Exception:
            print("STATIC-MAPS ERROR!")
            sys.exit()