class Box:
    def __init__(self, bbox):
        self.x_center, self.y_center, self.width, self.height = bbox
        self.x = int(self.x_center - self.width / 2)
        self.y = int(self.y_center - self.height / 2)

    def get_max_size(self):
        if self.width > self.height:
            return self.width
        else:
            return self.height

    def get_top_left(self):
        return (self.x, self.y)

    def get_bottom_right(self):
        return (self.x + self.width, self.y + self.height)

    def get_bottom_left(self):
        return (self.x, self.y + self.height)

    def get_center(self):
        return (self.x_center, self.y_center)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
