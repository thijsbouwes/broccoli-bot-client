from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QWidget, QMainWindow, QLCDNumber, QPushButton, QSpinBox, QLabel, QDoubleSpinBox
from PySide2.QtCore import QFile, QThread, Qt, Signal
from PySide2.QtUiTools import QUiLoader
from pathlib import Path
from bbot.robot import Robot
import os

class Ui(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        loader = QUiLoader()
        file = QFile(os.fspath(Path(__file__).resolve().parent / "form.ui"))
        file.open(QFile.ReadOnly)
        loader.load(file, self)
        file.close()

        # Setup buttons
        self.reset_count_btn = self.findChild(QPushButton, 'resetCount')
        self.reset_count_btn.clicked.connect(self.reset_counters)
        self.save_ground_truth_btn = self.findChild(QPushButton, 'saveGroundTruth')
        self.save_ground_truth_btn.clicked.connect(self.save_ground_truth)

        # Setup counters
        self.fps_lcd = self.findChild(QLCDNumber, 'fps')
        self.harvested_lcd = self.findChild(QLCDNumber, 'harvested')
        self.skipped_lcd = self.findChild(QLCDNumber, 'skipped')
        self.broccoli_id_lcd = self.findChild(QLCDNumber, 'broccoliId')

        # Setup settings
        self.min_diameter = self.findChild(QSpinBox, 'minDiameter')
        self.max_diameter = self.findChild(QSpinBox, 'maxDiameter')
        self.max_depth = self.findChild(QSpinBox, 'maxDepth')
        self.min_score = self.findChild(QDoubleSpinBox, 'minScore')
        self.broccoli_diameter = self.findChild(QSpinBox, 'broccoliDiameter')
        self.broccoli_depth = self.findChild(QSpinBox, 'broccoliDepth')

        # Setup image
        self.image = self.findChild(QLabel, 'image')

        # Start Robot
        self.robot_thread = QThread()
        self.robot = Robot()

        # Connect events
        self.min_diameter.valueChanged.connect(self.robot.farming_logic.set_min_diameter)
        self.max_diameter.valueChanged.connect(self.robot.farming_logic.set_max_diameter)
        self.max_depth.valueChanged.connect(self.robot.farming_logic.set_max_depth)
        self.min_score.valueChanged.connect(self.robot.set_min_score)

        # self.update_settings.connect(self.robot.update_settings_slot)
        self.robot.update_data.connect(self.update_data)

        self.robot_thread.started.connect(self.robot.run)
        self.robot_thread.finished.connect(self.robot.deleteLater)

        self.robot.moveToThread(self.robot_thread)
        self.robot_thread.start()

    def set_image(self, image):
        self.image.setPixmap(QtGui.QPixmap.fromImage(image))

    def save_ground_truth(self):
        self.robot.save_ground_truth(self.broccoli_diameter.value(), self.broccoli_depth.value())

    def reset_counters(self):
        self.robot.farming_logic.set_skipped(0)
        self.robot.farming_logic.set_harvested(0)

    def update_data(self, data):
        self.set_image(data[0])
        self.broccoli_id_lcd.display(data[1])
        self.harvested_lcd.display(data[2])
        self.skipped_lcd.display(data[3])
        self.fps_lcd.display(data[4])
