import time
from PySide2.QtCore import QObject, QFile, QThread, Qt, Signal
from PySide2.QtWidgets import QApplication
from bbot.detection_algorithm import DetectionAlgorithm
from bbot.farming_logic import FarmingLogic
from bbot.image_editor import ImageEditor
from bbot.camera import Camera
from operator import attrgetter
from csv import Csv

class Robot(QObject):
    update_data = Signal(list)

    def __init__(self):
        super().__init__()
        self.fps = 0
        self.min_score = 0.5

        self.csv = Csv()
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

                # Find broccoli's, run YOLO model (filter: class and scores)
                broccolis = self.detection_algorithm.get_broccolis(color_frame, self.min_score)

                # Determine depth and size for each broccoli
                for broccoli in broccolis:
                    box = broccoli.get_box()
                    broccoli.set_depth(self.camera.get_depth_in_mm(box))
                    broccoli.set_diameter(self.camera.get_diameter_in_mm(box))
                    broccoli.set_haravestable(self.farming_logic.is_harvestable(broccoli))

                    # Update image
                    color_frame = self.image_editor.draw_broccoli(color_frame, broccoli)

                # Find closest broccoli and count
                broccoli_closest_to_machine = min(broccolis, key=attrgetter('get_box.get_y_center'))
                if broccoli_closest_to_machine:
                    self.farming_logic.count(broccoli_closest_to_machine)
                    broccoli_closest_to_machine.set_id(self.farming_logic.get_broccolis_count())

                # Store data
                if self.farming_logic.get_new_broccoli_detected():
                    print('store new broccoli')
                    raw_image = self.camera.get_color_frame()
                    color_filename = self.image_editor.store_image(color_frame, 'color')
                    raw_filename = self.image_editor.store_image(raw_image, 'raw')
                    self.csv.writerow(broccoli_closest_to_machine, color_filename, raw_filename)

                # Calculate FPS
                self.calculate_fps()

                # Display frame
                qt_image = self.image_editor.convert_to_qt_format(color_frame)

                # img, harvested, skipped, fps
                self.update_data.emit((qt_image, self.farming_logic.get_harvested(), self.farming_logic.get_skipped(), self.fps))
                self.start_time = time.time()
                QApplication.processEvents()
                time.sleep(0.1)

        except Exception as e:
            print('Error in thread: {}'.format(e))

    def calculate_fps(self):
        self.fps = int(1.0 / (time.time() - self.start_time))

    def set_min_score(self, min_score):
        print('set_min_score {}'.format(min_score))
        self.min_score = round(min_score, 2)
