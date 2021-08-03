import csv
from bbot.broccoli import Broccoli
import os
import datetime

class Csv:
    def __init__(self):
        self.path = 'data-collection/reports/'
        os.makedirs(self.path, exist_ok=True)

    def writerow(self, broccoli: Broccoli, color_path: str, raw_path: str):
        now = datetime.datetime.now()
        file_name = now.strftime("%Y-%m-%d-data.csv")

        with open(self.path + file_name) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                broccoli.get_id(),
                broccoli.get_score(),
                broccoli.get_diameter(),
                broccoli.get_depth(),
                color_path,
                raw_path
            ])
