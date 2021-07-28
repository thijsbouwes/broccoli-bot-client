class Broccoli:
    def __init__(self):
        self.diameter = 0
        self.depth = 0
        self.harvestable = False
        self.box = False
        self.score = 0

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box

    def set_depth(self, depth):
        self.depth = depth

    def get_depth(self):
        return self.depth

    def set_diameter(self, diameter):
        self.diameter = diameter

    def get_diameter(self):
        return self.diameter

    def set_haravestable(self, harvestable):
        self.harvestable = harvestable

    def is_harvestable(self):
        return self.harvestable

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
