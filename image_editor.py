from PySide2 import QtGui
import os
import cv2
import datetime
import numpy as np
from bbot.broccoli import Broccoli

class ImageEditor:
    def draw_broccoli(self, image: np.ndarray, broccoli: Broccoli) -> np.ndarray:
        top_left = broccoli.get_box().get_top_left()
        bottom_right = broccoli.get_box().get_bottom_right()
        text_x, text_y = broccoli.get_box().get_bottom_left()

        if broccoli.is_harvestable():
            color = (0,255,0)
        else:
            color = (0,0,255)

        cv2.rectangle(image, top_left, bottom_right, color, 2)
        cv2.rectangle(image, (text_x, text_y), (text_x + 275, text_y + 30), color, -1)
        cv2.putText(image, 'D: {} mm Z: {} mm S: {}'.format(broccoli.get_diameter(), broccoli.get_depth(), broccoli.get_score()), (text_x + 10, text_y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        return image

    def store_image(self, image: np.ndarray, type: str) -> str:
        now = datetime.datetime.now()
        dirname = os.path.dirname(__file__)
        image_path = os.path.join(dirname, now.strftime("data-collection/%Y/%m/%d/"))
        image_filename = now.strftime("%H-%M-%f-{}-image.jpg").format(type)

        # Create dir and image
        os.makedirs(image_path, exist_ok=True)
        cv2.imwrite(image_path + image_filename, image)

        return image_path + image_filename

    def convert_to_qt_format(self, frame) -> QtGui.QImage:
        h, w, ch = frame.shape
        bytes_per_line = ch * w

        return QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
