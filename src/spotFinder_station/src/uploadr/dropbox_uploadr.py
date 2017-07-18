import ntpath
import logging


class DropboxDataUploader():

	def __init__(self, app_key, app_secret, access_token):
		"""
		class to handle operations to upload files to dropbox

		:param app_key: the app key
		:type app_key: :py:class:`str`

		:param app_secret: the app secret key
		:type app_secret: :py:class:`str`

		:param access_token: the app secret tokens
		:type access_token: :py:class:`str`

		"""

		self.app_key = app_key
		self.app_secret = app_secret
		self.access_token = access_token

	def upload_file(self, path, fname):
		"""
		upload files to dropbox

		:param path: the path to
		:type path: :py:class:`str`

		:param fname: the file name
		:type fname: :py:class:`str`

		"""
		local_fname = open("{}/{}".format(path, fname), 'rb')
		response = client.put_file(fname, local_fname)
		dir_media = client.media(fname)
		return dir_media.get(u'url')
