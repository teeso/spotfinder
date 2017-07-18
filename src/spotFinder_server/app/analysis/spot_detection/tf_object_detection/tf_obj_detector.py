import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import six.moves.urllib as urllib
import sys

sys.path.append("/usr/local/lib/python2.7/site-packages")
import tarfile
import zipfile
import logging
from os import listdir
from os.path import isfile, join, dirname, abspath
from matplotlib import pyplot as plt
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class TFObjDetector:
    """
	TFObjDetector 
	object recognition class using Google's TensorFlow Object Detection API and OpenCV.

	Source code is adapted based on the official repo: https://github.com/tensorflow/models/blob/master/object_detection/object_detection_tutorial.ipynb
	"""
    URL_BASE = 'http://download.tensorflow.org/models/object_detection/'
    NUM_CLASSES = 90
    CWD_PATH = os.getcwd()
    MODEL_NAMES = ['ssd_inception_v2_coco_11_06_2017', 'rfcn_resnet101_coco_11_06_2017',
                   'faster_rcnn_resnet101_coco_11_06_2017', 'faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017']

    def __init__(self, model_name):
        self.model_name = model_name
        self.mode_file = '{}.tar.gz'.format(self.model_name)
        self.path_to_ckpt = os.path.join(self.CWD_PATH, 'object_detection', self.model_name,
                                         'frozen_inference_graph.pb')
        self.path_to_labels = os.path.join(self.CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')

        # self.download_model()
        self.load_model()
        self.load_labels()
        self.init_model()

        logging.info("Init Model : {}".format(self.model_name))

    def download_model(self):
        opener = urllib.request.URLopener()
        opener.retrieve(self.URL_BASE + self.mode_file, self.mode_file)
        tar_file = tarfile.open(self.mode_file)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)

            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.getcwd())

    def load_model(self):
        self.det_graph = tf.Graph()

        with self.det_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                od_graph_def.ParseFromString(fid.read())
                tf.import_graph_def(od_graph_def, name='')

    def load_labels(self):
        label_map = label_map_util.load_labelmap(self.path_to_labels)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        return label_map, self.category_index, categories

    def load_images(self, img_dir):
        return [f for f in listdir(FILE_DIR) if isfile(join(FILE_DIR, f)) if "jpg" in f]

    def init_model(self, is_gpu_enabled=False):
        self.det_graph = tf.Graph()

        with self.det_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.image_tensor = self.det_graph.get_tensor_by_name('image_tensor:0')
        self.boxes = self.det_graph.get_tensor_by_name('detection_boxes:0')
        self.scores = self.det_graph.get_tensor_by_name('detection_scores:0')
        self.classes = self.det_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.det_graph.get_tensor_by_name('num_detections:0')

        if is_gpu_enabled:
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.05)

            self.sess = tf.Session(graph=self.det_graph, config=tf.ConfigProto(gpu_options=gpu_options))
        else:
            self.sess = tf.Session(graph=self.det_graph)

    @staticmethod
    def load_image_into_numpy_array(image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    @staticmethod
    def get_classes(boxes, classes, scores, category_index, min_score_thresh=.5):
        for i in range(boxes.shape[0]):
            # take only classes with good score
            if scores is None or scores[i] > min_score_thresh:
                if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                else:
                    class_name = 'N/A'

                display_str = '{}: {}%'.format(class_name, int(100 * scores[i]))

                yield (class_name, 100 * scores[i])

    def detect_obj(self, img_fname, viz=False):
        image = Image.open(img_fname)
        image_np = self.load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        (boxes, scores, classes, num_detections) = self.sess.run(
            [self.boxes, self.scores, self.classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        lst_obj = [x for x in
                   self.get_classes(np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores),
                                    self.category_index)]

        return lst_obj

        if viz == True:
            IMAGE_SIZE = (12, 8)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                self.category_index,
                use_normalized_coordinates=True,
                line_thickness=8)
            plt.figure(figsize=IMAGE_SIZE)
            plt.imshow(image_np)
            plt.show()
