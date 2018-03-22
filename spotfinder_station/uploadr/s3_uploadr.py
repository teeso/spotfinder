import boto
import ntpath
from boto.s3.connection import S3Connection
import logging


class S3DataUploader():
 
	def __init__(self, s3_bucket, s3_path, aws_access_key, aws_secret_key):
		"""
		class to handle operations to upload files to S3

		:param s3_bucket: the bucket name
		:type s3_bucket: :py:class:`str`

		:param s3_path: the path to bucket
		:type s3_path: :py:class:`str`

		:param aws_access_key: access key
		:type aws_access_key: :py:class:`str`

		:param aws_secret_key: secret key
		:type aws_secret_key: :py:class:`str`

		"""

		try:
			self.s3_bucket = s3_bucket
			self.s3_path = s3_path
			self.aws_access_key = aws_access_key
			self.aws_secret_key = aws_secret_key
			self.s3_conn = boto.connect_s3(aws_access_key_id=self.aws_access_key,
									   aws_secret_access_key=self.aws_secret_key,
									   calling_format=boto.s3.connection.OrdinaryCallingFormat())
		except Exception, e:
			logging.warn("Exception occurred in the initializer : {}".format(e))

	def get_bucket_name(self, bucket_name):
		"""
		get bucket name

		:param bucket_name: the bucket name
		:type bucket_name: :py:class:`str`

		"""
		return self.s3_conn.get_bucket(bucket_name)

	def delete_bucket_name(self, bucket_name):
		"""
		delete bucket name

		:param bucket_name: the bucket name
		:type bucket_name: :py:class:`str`

		"""

		self.s3_conn.delete_bucket(bucket_name)

	def get_all_buckets(self):
		"""
		get all bucket name

		"""
		lst_buckets = []
		for bucket in self.s3_conn.get_all_buckets():
			lst_buckets += [bucket.name]

		return lst_buckets

	def upload_file(self, lfname):
		"""
		upload the file

		:param lfname: path to host files
		:type lfname: :py:class:`str`

		"""

		try:
			path, fname = ntpath.split(lfname)
			bucket = self.s3_conn.get_bucket(self.s3_bucket)
			s3key = bucket.new_key(fname)
			s3key.name = fname
			s3key.set_contents_from_filename(lfname)
			s3key.make_public()
			url = s3key.generate_url(expires_in=0, query_auth=False)
			return url

		except Exception, e:
			logging.warn("Exception while uploading file to S3 : {}".format(e))

 