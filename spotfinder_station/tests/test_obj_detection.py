# coding=utf-8

import types
import six
import unittest

from src.analyze.tf_object_detection.tf_obj_detector import TFObjDetector

class TFObjDetectorTests(unittest.TestCase):
	
	def test_detect_obj(self):
		tf_obj_detector = TFObjDetector(model_name= 'ssd_mobilenet_v1_coco_11_06_2017')
		lst, nbr_cars = tf_obj_detector.detect_obj('test_images/image1.jpeg')
		self.assertNotEqual(nbr_cars, None)


if __name__ == '__main__':
	unittest.main()