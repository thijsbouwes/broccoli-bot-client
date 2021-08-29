import bbot.darknet as darknet
from bbot.broccoli import Broccoli
from bbot.box import Box
import cv2
import os
import numpy as np

class DetectionAlgorithm:
    width = 416
    height = 416

    def setup(self):
        self.network, self.class_names, class_colors = darknet.load_network(
            os.path.join(os.path.dirname(__file__), 'cfg/yolo-obj.cfg'),  # 'yolov4-tiny-custom.cfg'
            os.path.join(os.path.dirname(__file__), 'obj.data'),
            os.path.join(os.path.dirname(__file__), 'weights/yolo-obj_best_v2.weights'), # 'yolov4-tiny-custom_best.weights'
            batch_size=1
        )

    def get_broccolis(self, image: np.ndarray, min_score: int) -> list:
        # Resize frame to 416x416
        frame_resized = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
        img_for_detect = darknet.make_image(self.width, self.height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())

        detections = darknet.detect_image(self.network, self.class_names, img_for_detect, thresh=min_score)
        darknet.free_image(img_for_detect)

        broccolis = []
        for label, confidence, bbox in detections:
            broccoli = Broccoli()
            box = self.convert_to_original(image, bbox)
            broccoli.set_box(Box(box))
            broccoli.set_score(confidence)
            broccolis.append(broccoli)

        return broccolis

    def convert_to_relative(self, bbox) -> tuple:
        # YOLO format use relative coordinates for annotation
        x, y, w, h = bbox

        return (x / self.width, y / self.height, w / self.width, h / self.height)

    def convert_to_original(self, image, bbox) -> tuple:
        # Convert coordinates to original image size
        x, y, w, h = self.convert_to_relative(bbox)
        image_h, image_w, __ = image.shape
        orig_x = int(x * image_w)
        orig_y = int(y * image_h)
        orig_width = int(w * image_w)
        orig_height = int(h * image_h)

        return (orig_x, orig_y, orig_width, orig_height)
