class Box:
    def __init__(self, bounding_box):
        self.x_center, self.y_center, self.width, self.height = bounding_box
        self.x = int(self.x_center - self.width / 2)
        self.y = int(self.y_center - self.height / 2)

    def get_max_size(self) -> tuple:
        if self.width > self.height:
            return self.get_left_center() + self.get_right_center()
        else:
            return self.get_top_center() + self.get_bottom_center()

    def get_top_left(self) -> tuple:
        return (self.x, self.y)

    def get_bottom_right(self) -> tuple:
        return (self.x + self.width, self.y + self.height)

    def get_bottom_left(self) -> tuple:
        return (self.x, self.y + self.height)

    def get_left_center(self) -> tuple:
        return (max(self.x, 0), self.y_center)

    def get_right_center(self) -> tuple:
        return (min(self.x + self.width, 1919), self.y_center)

    def get_top_center(self):
        return (self.x_center, self.y)

    def get_bottom_center(self):
        return (self.x_center, self.y + self.height)

    def get_center(self) -> tuple:
        return (self.x_center, self.y_center)

    def get_x_center(self) -> int:
        return self.x_center

    def get_y_center(self) -> int:
        return self.y_center

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_height(self) -> int:
        return self.height

    def get_width(self) -> int:
        return self.width
