from bbot.broccoli import Broccoli

class FarmingLogic:
    def __init__(self):
        self.min_diameter = 10
        self.max_diameter = 150
        self.max_depth = 1000

        self.harvested = 0
        self.skipped = 0

        self.last_y = 0

    def is_harvestable(self, broccoli: Broccoli):
        if broccoli.get_diameter() < self.min_diameter:
            return False
        elif broccoli.get_diameter() > self.max_diameter:
            return False
        elif broccoli.get_depth() > self.max_depth:
            return False
        else:
            return True

    def count(self, broccoli):
        x, y = broccoli.get_box().get_center()

        if y > 220 and self.last_y < 100:
            self.last_y = y

            if broccoli.is_harvestable():
                self.harvested += 1
            else:
                self.skipped += 1

        print('count y: {} last: {}'.format(y, self.last_y))

    def set_min_diameter(self, min_diameter):
        # print('set_min_diameter {}'.format(min_diameter))
        self.min_diameter = min_diameter

    def set_max_diameter(self, max_diameter):
        # print('set_max_diameter {}'.format(max_diameter))
        self.max_diameter = max_diameter

    def set_max_depth(self, max_depth):
        # print('set_max_depth {}'.format(max_depth))
        self.max_depth = max_depth

    def get_harvested(self):
        return self.harvested

    def get_skipped(self):
        return self.skipped
