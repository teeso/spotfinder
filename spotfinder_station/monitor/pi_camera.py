import os


class PiCamera():

	def __init__(self, dir_path, lapse_time= 10):
		"""
		class to handle operations to upload files to dropbox

		:param dir_path: the directory path
		:type dir_path: :py:class:`str`

		:param lapse_time: the app secret key
		:type lapse_time: :py:class:`int`

		"""
		self.dir_path= dir_path
		self.lapse_time= lapse_time

	def capture_image(self, image_fname):
		"""
		capture image

		:param image_fname: the image file name
		:type image_fname: :py:class:`str`
		"""
		os.system("raspistill -o {0}".format(image_fname))
		return "{}/{}".format(self.dir_path, image_fname)

	def delete_image(self, image_fname):
		"""
		delete image

		:param image_fname: the image file name
		:type image_fname: :py:class:`str`
		"""
		os.system("rm {0}".format(image_fname))

	def record_video(self, video_file='video.h264'):
		"""
		record a video

		:param video_file: the video filename
		:type video_file: :py:class:`str`
		"""
		os.system("raspivid -fps 90 -w 640 -h 480 -t 5000 -o camera/%s"%(video_file))

	def streaming_video(self, server_ip, stream_name, stream_key):
		"""
		stream a video on Youtube

		:param server_ip: the server IP
		:type server_ip: :py:class:`str`

		:param stream_name: the stream channel
		:type stream_name: :py:class:`str`

		:param stream_key: the stream channel key
		:type stream_key: :py:class:`str`
		"""
		os.system("raspivid -o - -t 0 -hf -w 640 -h 480 -fps 12 | ffmpeg -i - -vcodec copy -an -r 25 -f flv -metadata streamName={} tcp://{0}:6666".format(stream_name, server_ip))
