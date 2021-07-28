import time
from random import randrange
from PySide2.QtCore import QObject, QFile, QThread, Qt, Signal
from PySide2.QtWidgets import QApplication
from bbot.farming_logic import FarmingLogic
from bbot.camera import Camera
from bbot.detection_algorithm import DetectionAlgorithm
from bbot.image_editor import ImageEditor
from bbot.camera import Camera

class Robot(QObject):
    update_data = Signal(list)

    def __init__(self):
        super().__init__()
        self.fps = 0
        self.min_score = 0.5

        self.farming_logic = FarmingLogic()
        self.camera = Camera()
        self.image_editor = ImageEditor()
        self.detection_algorithm = DetectionAlgorithm()

    def run(self):
        print('Robot: run')

        try:
            self.camera.setup()
            self.detection_algorithm.setup()
            self.start_time = time.time()

            while True:
                # Get image from camera
                self.camera.take_photo()
                color_frame = self.camera.get_color_frame()

                # Find broccoli's, run YOLACT model (filter: class and scores)
                # Returns array with masks / boxes
                broccolis = self.detection_algorithm.get_broccolis(color_frame, self.min_score)

                # # Determine depth and size for each broccoli
                for broccoli in broccolis:
                    box = broccoli.get_box()
                    broccoli.set_depth(self.camera.get_depth_in_mm(box))
                    broccoli.set_diameter(self.camera.get_diameter_in_mm(box))
                    broccoli.set_haravestable(self.farming_logic.is_harvestable(broccoli))

                    self.farming_logic.count(broccoli)
                    color_frame = self.image_editor.draw_broccoli(color_frame, broccoli)

                # Calculate FPS
                self.calculate_fps()

                # Display frame
                frame_path = self.image_editor.convert_to_qt_format(color_frame)

                # img, harvested, skipped, fps
                self.update_data.emit((frame_path, self.farming_logic.get_harvested(), self.farming_logic.get_skipped(), self.fps))
                self.start_time = time.time()
                QApplication.processEvents()
                time.sleep(0.001)

        except Exception as e:
            print('Error in thread: {}'.format(e))

    def calculate_fps(self):
        self.fps = int(1.0 / (time.time() - self.start_time))

    def set_min_score(self, min_score):
        print('set_min_score {}'.format(min_score))
        self.min_score = round(min_score, 2)
