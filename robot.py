import time
from operator import attrgetter
from PySide2.QtCore import QObject, QFile, QThread, Qt, Signal
from PySide2.QtWidgets import QApplication
from bbot.detection_algorithm import DetectionAlgorithm
from bbot.farming_logic import FarmingLogic
from bbot.image_editor import ImageEditor
from bbot.camera import Camera
from bbot.csv import Csv

class Robot(QObject):
    update_data = Signal(list)

    def __init__(self):
        super().__init__()
        self.fps = 0
        self.min_score = 0.75

        self.csv = Csv()
        self.farming_logic = FarmingLogic()
        self.camera = Camera()
        self.image_editor = ImageEditor()
        self.detection_algorithm = DetectionAlgorithm()

    def run(self) -> None:
        try:
            # Setup dependencies
            self.camera.setup()
            self.detection_algorithm.setup()
            self.start_time = time.time()

            while True:
                # Get image from camera
                self.camera.take_photo()
                color_frame = self.camera.get_color_frame()
                raw_image = color_frame.copy()

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
                if broccolis:
                    broccoli_closest_to_machine = min(broccolis, key=attrgetter('box.y_center'))
                    if broccoli_closest_to_machine:
                        self.farming_logic.count(broccoli_closest_to_machine)
                        broccoli_closest_to_machine.set_id(self.farming_logic.get_broccoli_count())

                    # Store data
                    if self.farming_logic.get_new_broccoli_detected():
                        color_filename = self.image_editor.store_image(color_frame, 'color')
                        raw_filename = self.image_editor.store_image(raw_image, 'raw')
                        self.csv.write_row(broccoli_closest_to_machine, color_filename, raw_filename)

                # Calculate FPS
                self.calculate_fps()

                # Convert to QT image
                qt_image = self.image_editor.convert_to_qt_format(color_frame)

                # img, harvested, skipped, fps
                self.update_data.emit((qt_image, self.farming_logic.get_broccoli_count(), self.farming_logic.get_harvested(), self.farming_logic.get_skipped(), self.fps))
                self.start_time = time.time()

                # Process events
                QApplication.processEvents()
                time.sleep(0.001)

        except Exception as e:
            print('Error in: {}'.format(e))

    def save_ground_truth(self, ground_truth_diameter: int, ground_truth_depth: int) -> None:
        broccoli_id = self.farming_logic.get_broccoli_count()
        if broccoli_id:
            self.csv.update_row(broccoli_id, ground_truth_diameter, ground_truth_depth)

    def calculate_fps(self) -> None:
        self.fps = int(1.0 / (time.time() - self.start_time))

    def set_min_score(self, min_score: float) -> None:
        self.min_score = round(min_score, 2)
