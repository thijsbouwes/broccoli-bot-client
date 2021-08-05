from bbot.broccoli import Broccoli

class FarmingLogic:
    def __init__(self):
        self.min_diameter = 10
        self.max_diameter = 150
        self.max_depth = 1000
        self.image_height = 720

        self.harvested = 0
        self.skipped = 0
        self.broccoli_count = 0

        self.count_offset = self.image_height * 0.25
        self.count_border = self.image_height / 2
        self.count_new_broccoli = False
        self.new_broccoli_detected = False

    def is_harvestable(self, broccoli: Broccoli) -> bool:
        if broccoli.get_diameter() < self.min_diameter:
            return False
        elif broccoli.get_diameter() > self.max_diameter:
            return False
        elif broccoli.get_depth() > self.max_depth:
            return False
        else:
            return True

    def count(self, broccoli: Broccoli) -> None:
        x, y = broccoli.get_box().get_center()

        if y <= self.count_offset:
            self.count_new_broccoli = True

        if y >= self.count_border and self.count_new_broccoli:
            self.broccoli_count += 1
            self.count_new_broccoli = False
            self.new_broccoli_detected = True

            if broccoli.is_harvestable():
                self.harvested += 1
            else:
                self.skipped += 1
        else:
            self.new_broccoli_detected = False

        print('count y: {} new: {} count new: {}'.format(y, self.new_broccoli_detected, self.count_new_broccoli))

    def set_min_diameter(self, min_diameter: int):
        self.min_diameter = min_diameter

    def set_max_diameter(self, max_diameter: int):
        self.max_diameter = max_diameter

    def set_max_depth(self, max_depth: int):
        self.max_depth = max_depth

    def get_broccoli_count(self) -> int:
        return self.broccoli_count

    def get_harvested(self) -> int:
        return self.harvested

    def get_skipped(self) -> int:
        return self.skipped

    def get_new_broccoli_detected(self) -> bool:
        return self.new_broccoli_detected
