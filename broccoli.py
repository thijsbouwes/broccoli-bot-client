from box import Box

class Broccoli:
    def __init__(self):
        self.diameter = 0
        self.depth = 0
        self.harvestable = False
        self.box = False
        self.score = 0

    def get_box(self) -> Box:
        return self.box

    def set_box(self, box: Box):
        self.box = box

    def set_depth(self, depth: int):
        self.depth = depth

    def get_depth(self) -> int:
        return self.depth

    def set_diameter(self, diameter: int):
        self.diameter = diameter

    def get_diameter(self) -> int:
        return self.diameter

    def set_haravestable(self, harvestable: bool):
        self.harvestable = harvestable

    def is_harvestable(self) -> bool:
        return self.harvestable

    def set_score(self, score: float):
        self.score = score

    def get_score(self) -> float:
        return self.score
