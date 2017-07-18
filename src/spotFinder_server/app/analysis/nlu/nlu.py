import os
import requests


class NLUParser():
	def __init__(self, server_ip):
		"""
		:param server_ip: server IP where r u hosting rasa NLU server
		:type server_ip: :py:class:`str`
		"""
		self.server_ip = server_ip

	def _get(self, url, **queryparams):
		"""
		Handle authenticated POST requests

		:param url: The url for the endpoint including path parameters
		:type url: :py:class:`str`

		:param queryparams: The query string parameters
		:type queryparams: :py:class:`dict`

		:returns: The Reponse from the API
		"""
		try:
			if queryparams.get('data', None) != None:
				response = requests.get(url, params=queryparams.get('data'))
			return response

		except requests.exceptions.RequestException as e:
			raise Exception(
				'Invalid API server response.\n%s' % response)

	def parse(self, message):
		"""
		parsing the message to get intent of the user

		:param message: message from client to be parsed
		:type message: :py:class:`str`

		"""
		response = self._get("{}/parse".format(self.server_ip), data={"q": message})
		parsed_data = response.json()

		if parsed_data['intent']['confidence'] < 0.30:
			intent = 'None'
			entities = []
		else:
			intent = parsed_data['intent']['name']
			entities = parsed_data['entities']

		return intent, entities
