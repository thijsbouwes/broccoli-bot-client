# import bbot.darknet as darknet
from bbot.broccoli import Broccoli
from bbot.box import Box
import cv2
import os

class DetectionAlgorithm:
    width = 416
    height = 416

    def setup(self):
        print('setup netwerk')
        return
        self.network, self.class_names, class_colors = darknet.load_network(
            os.path.join(os.path.dirname(__file__), 'cfg/yolo-obj.cfg'), # 'yolov4-tiny-custom.cfg'
            os.path.join(os.path.dirname(__file__), 'obj.data'),
            os.path.join(os.path.dirname(__file__), 'weights/weights/yolo-obj_best.weights'), # 'yolov4-tiny-custom_best.weights'
            batch_size=1
        )

    def get_broccolis(self, image, min_core):
        broccoli = Broccoli()
        box = Box((320, 240, 50, 50))
        broccoli.set_box(box)

        return [broccoli]

        frame_resized = cv2.resize(image, (self.width, self.height),interpolation=cv2.INTER_LINEAR)
        img_for_detect = darknet.make_image(self.width, self.height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())

        detections = darknet.detect_image(self.network, self.class_names, img_for_detect, thresh=min_core)
        darknet.free_image(img_for_detect)

        broccolis = []
        for label, confidence, bbox in detections:
            broccoli = Broccoli()
            box = self.convert2original(image, bbox)
            broccoli.set_box(Box(box))
            broccoli.set_score(confidence)
            broccolis.append(broccoli)

        print("Found {} broccolis".format(len(broccolis)))
        return broccolis

    def convert2relative(self, bbox):
        """
        YOLO format use relative coordinates for annotation
        """
        x, y, w, h  = bbox
        _height     = self.height
        _width      = self.width

        return x/_width, y/_height, w/_width, h/_height

    def convert2original(self, image, bbox):
        x, y, w, h = self.convert2relative(bbox)

        image_h, image_w, __ = image.shape

        orig_x       = int(x * image_w)
        orig_y       = int(y * image_h)
        orig_width   = int(w * image_w)
        orig_height  = int(h * image_h)

        bbox_converted = (orig_x, orig_y, orig_width, orig_height)

        return bbox_converted
