import re
import json
from datetime import datetime
import requests


class SpatialIndexer():
    MAX_DISTANCE = 10000

    def __init__(self, db_collection):
        """
        class to handle spatial operations

        :param db_collection: db collection cursor
        :type db_collection: :pymongo:class:`cursor`
        """
        self.url = "http://nominatim.openstreetmap.org/"
        self.db_collection = db_collection

    def get_place_geo_info(self, street, city, country):
        """
        get lat/lng of an address 

        :param street: street
        :type street: :py:class:`str`

        :param city: city
        :type city: :py:class:`str`

        :param country: country 
        :type country: :py:class:`str`
        """
        url = "{}?format=json&street={}&city={}&country={}".format(self.url, street, city, country)
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            try:
                result = response.json()[0]
                return {'lat': float(result['lat']), 'lon': float(result['lon'])}
            except Exception as e:
                return {'Status': '404', 'Message': 'Error!'}

    def find_nearest_station(self, point):
        """
        find nearest station for a given point 

        :param street: street
        :type street: :py:class:`str`
        """
        return self.db_collection.find({'coordinates': {
            '$near': {'$geometry': {'type': "Point", "coordinates": point}, '$maxDistance': self.MAX_DISTANCE}}},
                                       {"_id": False}).sort({"time": -1}).limit(1)
