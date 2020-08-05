from palettable.tableau import Tableau_10
from typing import List, Dict


class CustomLegend:
    """Creates a custom legend based on provided labels."""

    def __init__(
        self, labels: List[str], *, colors: List[str] = None, limit_labels: int = None
    ):
        """
        Args:
            labels (List[str]): Labels for legend
            colors (List, optional): List of hex colors used for Legend. Defaults to Tableau_10 if not provided.
            limit_labels (int, optional): Limits legend to specified number of items. Defaults to None.
        """
        labels = labels if not limit_labels else labels[0:limit_labels]
        colors = colors if colors else Tableau_10.hex_colors
        field_count = len(labels)
        self.colors = colors[0:field_count]
        self.labels = labels

    def __repr__(self) -> str:
        return "<CustomLegend labels:%s colors:%s>" % (self.labels, self.colors)

    def legend(self, title_case=False) -> List[Dict[str, str]]:

        """Returns a list of dicts representing the legend

        Args:
            title_case (bool, optional): Ensures labels are in title case when legend method is called

        Returns:
            List[Dict[str, str]]: Legend
        """
        labels = self.labels if not title_case else [x.title() for x in self.labels]
        return [{"label": x, "color": y} for x, y in zip(labels, self.colors)]
