import csv
from bbot.broccoli import Broccoli
import os
import datetime

class Csv:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.path = os.path.join(dirname, 'data-collection/reports/')
        os.makedirs(self.path, exist_ok=True)

    def writerow(self, broccoli: Broccoli, edited_image_path: str, raw_image_path: str):
        now = datetime.datetime.now()
        file_name = now.strftime("%Y-%m-%d-data.csv")
        file_exists = os.path.isfile(self.path + file_name)

        with open(self.path + file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            headers = [
                'id',
                'score',
                'diameter',
                'depth',
                'edited_image_path',
                'raw_image_path'
            ]

            if not file_exists:
                writer.writerow(headers)

            writer.writerow([
                broccoli.get_id(),
                broccoli.get_score(),
                broccoli.get_diameter(),
                broccoli.get_depth(),
                edited_image_path,
                raw_image_path
            ])
