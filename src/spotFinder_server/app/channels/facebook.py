from flask import request
from app.analysis.nlu.nlu import NLUParser
from app.analysis.gis.spatial_indexer import SpatialIndexer
from app.config.config import LRU_SERVER, COUNTRY, CITY
from app.resources.constants import PARKING_SEARCH, ENTITY, ENTITY_LOCATION
import sys
import requests
import json


class FacebookHandler():
    """
        The class interfaces facebook's Messenger API
    """
    DEFAULT_ENDPOINT = "https://graph.facebook.com/v2.6/"
    LRU_SERVER = LRU_SERVER

    def __init__(self, access_token, verify_token, sensors_collection):
        """
        class to handle operations facebook's Messenger API

        :param access_token: the access token 
        :type access_token: :py:class:`str`

        :param verify_token: the verify token to validate the auth 
        :type verify_token: :py:class:`str`

        :param sensors_collection: cursor for mongdb collection
        :type sensors_collection: :pymongo:class:`cursor`
        """

        self.access_token = access_token
        self.verify_token = verify_token
        self.nlu_parser = NLUParser(self.LRU_SERVER)
        self.spatial_indexer = SpatialIndexer(sensors_collection)
        self._params = {"access_token": self.access_token}
        self._headers = {'Content-type': 'application/json'}

    def verify(self, *args, **kwargs):
        """
        verify facebook's Messenger API

        :param args: args 
        :type args: :py:class:`dict`

        :param args: kwargs 
        :type args: :py:class:`dict`

        """
        if request.args.get('hub.verify_token', '') == self.verify_token:
            return request.args.get('hub.challenge', '')
        else:
            return "Error! Please correct the verify_token"

    def encode_message(self, item):
        """
        encode the message that we get from db

        :param item: an item from db that hold time-encoded information  
        :type item: :py:class:`dict`

        """
        return "We found {} parking slot. You can use Google Maps to find the best route to reach the place {}\n".format(
            item.get('nbr_spots'), item.get('link'))

    def messaging_events(self, data):
        """
        parsing messages we get from FB chatbot 

        :param data: data that we get from chat   
        :type data: :py:class:`dict`

        """

        if data["object"] == "page":

            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]
                        message_text = messaging_event["message"]["text"]
                        intent, entities = self.nlu_parser.parse(message=message_text)

                        if intent == PARKING_SEARCH:
                            if entities > 0:
                                try:
                                    if entities[0][ENTITY] == ENTITY_LOCATION:
                                        location_value = entities[0][u'value']
                                        street_name = location_value.replace("street", "")
                                        point_coordinates = self.spatial_indexer.get_place_geo_info(street_name, CITY,
                                                                                                    COUNTRY)
                                        items = self.spatial_indexer.find_nearest_station(point_coordinates)
                                        response_text = self.encode_message(items[0])

                                        self.send_message(sender_id, response_text)

                                except Exception as e:
                                    self.send_message(sender_id,
                                                      "Where do you want to park?. Can you specify the place?")
                                    pass
                                    # response please specify location
                            else:
                                self.send_message(sender_id, "Are you looking for a parking place ?")
                                # response please specify location

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

    def send_message(self, recipient, text):
        """Send the message text to recipient with id recipient.
        
        :param recipient: recipient
        :type recipient: :py:class:`str`

        :param text: text
        :type text: :py:class:`str`
        """

        r = requests.post(self.DEFAULT_ENDPOINT + "/me/messages",
                          params=self._params,
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"text": text}
                          }),
                          headers=self._headers)
        if r.status_code != requests.codes.ok:
            print(r.text)
