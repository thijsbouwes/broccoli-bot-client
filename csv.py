import csv
import os
import datetime
import shutil
from bbot.broccoli import Broccoli
from tempfile import NamedTemporaryFile

class Csv:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.path = os.path.join(dirname, 'data-collection/reports/')
        os.makedirs(self.path, exist_ok=True)

        now = datetime.datetime.now()
        self.file_name = now.strftime("%Y-%m-%d-%H-%M-%f-data.csv")

        self.headers = [
            'id',
            'score',
            'diameter',
            'depth',
            'edited_image_path',
            'raw_image_path',
            'ground_truth_diameter',
            'ground_truth_depth'
        ]

    def write_row(self, broccoli: Broccoli, edited_image_path: str, raw_image_path: str):
        file_exists = os.path.isfile(self.path + self.file_name)

        with open(self.path + self.file_name, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'id': broccoli.get_id(),
                'score': broccoli.get_score(),
                'diameter': broccoli.get_diameter(),
                'depth': broccoli.get_depth(),
                'edited_image_path': edited_image_path,
                'raw_image_path': raw_image_path
            })

    # Update broccoli with ground truth
    # Use temp file for updating CSV
    def update_row(self, broccoli_id: int, ground_truth_diameter: int, ground_truth_depth: int):
        temp_file = NamedTemporaryFile('w', delete=False)

        with open(self.path + self.file_name, 'r') as csv_file, temp_file:
            reader = csv.DictReader(csv_file, fieldnames=self.headers)
            writer = csv.DictWriter(temp_file, fieldnames=self.headers)

            for row in reader:
                if row['id'] == str(broccoli_id):
                    row['ground_truth_diameter'] = ground_truth_diameter
                    row['ground_truth_depth'] = ground_truth_depth
                writer.writerow(row)

        shutil.move(temp_file.name, self.path + self.file_name)

    def get_file_name(self):
        now = datetime.datetime.now()

        return now.strftime("%Y-%m-%d-%H-%M-%f-data.csv")
