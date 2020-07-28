from palettable.tableau import Tableau_10
from typing import List


class CustomLegend:
    def __init__(self, labels: List):
        colors = Tableau_10.hex_colors
        field_count = len(labels)
        self.colors = colors[0:field_count]
        self.labels = labels

    def __repr__(self):
        return "<CustomLegend labels:%s colors:%s>" % (self.labels, self.colors)

    def legend(self):
        return [{"label": x, "color": y} for x, y in zip(self.labels, self.colors)]
