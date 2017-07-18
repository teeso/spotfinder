from src.analyze.tf_object_detection import TFObjDetector
from src.monitor.pi_camera import PiCamera
from src.uploadr.s3_uploadr import S3DataUploader
from src.config.config import *
from src.resources.contants import *
from threading import Thread
import time
import sys
from datetime import datetime 
import logging 


class NodePi(Thread):
	def __init__(self, node_id, capacity, latitude, longitude, link, lapse_time, db_collection):
		"""
		Initialize the NodePi Claas

		:param node_id: id of a sensor
		:type node_id: :py:class:`str`

		:param capacity: initial capacity
		:type capacity: :py:class:`str`

		:param latitude: latitude
		:type latitude: :py:class:`str`

		:param longitude: longitude
		:type longitude: :py:class:`str`

		:param link: link to google maps
		:type link: :py:class:`str`

		:param lapse_time: id of a sensor
		:type lapse_time: :py:class:`int`

		:param db_collection: id of a sensor
		:type db_collection: :pymongo:class:`cursor`
		"""

		Thread.__init__(self)
		self.node_id = node_id
		self.location =  { "coordinates": [latitude, longitude], "type": "Point".} #{LATITUDE: None, LONGITUDE: None}
		self.lapse_time = lapse_time
		self.hosting_service = S3
		self.db_collection = db_collection
		self.link = link
		self.seconds = SECONDS
		self.total_capacity= capacity

	def run(self):
		"""
		running the thread, and constantly monitor parking. It takes a picture, count the number of cars and then insert to database
		"""
		s3_data_uploadr = S3DataUploader(S3_BUCKET, S3_PATH, S3_ACCESS_KEY, S3_SECRET_KEY)
		pi_camera = PiCamera(dir_path= CAMERA_PATH, lapse_time= 1*60)
		tf_obj_detector = TFObjDetector(model_name= TF_OBJ_DETECTOR)

		try:
			while (True):

				image_fname = "{}/{}.png".format(IMAGE_EXT, time.strftime("%Y_%m_%d_%H_%M_%S"))
				image_path = pi_camera.capture_image(image_fname)
				lst_obj, nbr_cars = tf_obj_detector.detect_obj(image_path, viz= False)
				if UPLOAD_TO_SERVER:
					image_shared_link = s3_data_uploadr.upload_file(image_path)
					# insert to db
				else:
					image_shared_link = None

				data = {NODE_ID: self.node_id, COORDINATES : self.location, TIME: datetime.now(), IMAGE: image_shared_link, NBR_CARS: nbr_cars, AVAILABLE_SPOTS: (self.total_capacity - nbr_cars) }

				self.db_collection.insert(data)

				time.sleep(self.seconds)

		except KeyboardInterrupt:
			logging.warn("\nExit requested, terminating normally")
			sys.exit(0)