class Csv:
    def __init__(self):
        self.x_center, self.y_center, self.width, self.height = bbox
        self.x = int(self.x_center - self.width / 2)
        self.y = int(self.y_center - self.height / 2)

    def write_line(self, broccoli):
