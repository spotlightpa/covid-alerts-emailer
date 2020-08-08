from typing import Any
import inflect

from src.modules.helper.decorators import tag_dtype, tag
from src.modules.helper.get_neighbors import get_neighbors
from src.modules.helper.rank_text import rank_text

p = inflect.engine()


class GenDesc:
    """ Generates chatter for charts """

    def __init__(self, county_name_clean, county_data, gdf):
        self.county_name_clean = county_name_clean
        self.county_data = county_data
        self.gdf = gdf

    def __gdf_cell_accessor(self, col_name: str, _round=False) -> Any:
        """
        Gets a value from self.gdf based on the intersection of county's name and
        specified column. Args are concatenated to get the full column name.
        Eg. datatype of "cases" and column_suffix of "total_two_weeks_ago" becomes
        "cases_total_two_weeks_Ago".

        Args:
            col_name (str): Suffix of column. eg "total_two_weeks_ago"
            _round (bool, optional) Rounds final number if it's a float. Defaults to true.

        Returns:
            Any: Value stored at cell.
        """
        gdf = self.gdf.set_index("NAME").copy(deep=True)
        value = gdf.at[self.county_name_clean, col_name]
        if isinstance(value, float) and _round:
            return round(value)
        return value

    def gdf_get_ranking(self, gdf, sort_col):
        """ Ranks a given df by given field. Field is converted to int before ranking."""
        gdf = gdf.copy(deep=True)
        sort_col_clean = f"{sort_col}_clean"
        gdf[sort_col_clean] = gdf[sort_col].round(1)
        gdf = gdf.sort_values(sort_col_clean, ascending=False)
        # We use 'dense' ranking in the case of ties, which produces a more intuitive ranking
        gdf["rank_from_top"] = gdf[sort_col_clean].rank(method="dense", ascending=False)
        gdf["rank_from_bottom"] = gdf[sort_col_clean].rank(
            method="dense", ascending=True
        )
        gdf = gdf.set_index("NAME")
        rank_from_top = round(gdf.at[self.county_name_clean, "rank_from_top"])
        rank_from_bottom = round(gdf.at[self.county_name_clean, "rank_from_bottom"])
        others_with_same_rank = (
            len(gdf[(gdf["rank_from_top"] == rank_from_top)]) - 1
        )  # remove 1 to exclude
        # selected county
        return rank_from_top, rank_from_bottom, others_with_same_rank

    @tag_dtype
    def daily(self, *, data_type: str) -> str:
        total = self.__gdf_cell_accessor(f"{data_type}_total")
        total_past_two_weeks = self.__gdf_cell_accessor(
            f"{data_type}_added_past_two_weeks"
        )
        return (
            f"There has been a total of [b]{total:,}[/b] reported {p.singular_noun(data_type, total)} in"
            f" {self.county_name_clean} "
            f"County "
            f"since the start of the outbreak. Over the past two weeks, the county has had "
            f"[b]{total_past_two_weeks:,}[/b] new {p.singular_noun(data_type, total_past_two_weeks)}. "
            f"Here’s how its trend looks since March:"
        )

    @tag_dtype
    def choro(self, *, data_type: str) -> str:
        target_col = f"{data_type}_added_past_two_weeks_per_capita"
        two_week_per_capita_avg = self.__gdf_cell_accessor(target_col)
        rank_from_top, rank_from_bottom, others_with_same_rank = self.gdf_get_ranking(
            self.gdf, target_col
        )
        per_capita_rank = rank_text(rank_from_top, rank_from_bottom)
        if per_capita_rank == "same":
            sentence_frag = f"same per capita rate of {data_type} as Pennsylvania's other 66 counties over that time."
        else:
            sentence_frag = (
                f"[b]{per_capita_rank}[/b] per capita rate of {data_type} among Pennsylvania’s 67 counties "
                f"over that time."
            )
            if others_with_same_rank > 0:
                sentence_frag = (
                    f"{sentence_frag} [b]{others_with_same_rank}[/b] other "
                    f"{p.singular_noun('counties', others_with_same_rank)} "
                    f"had the same per capita rate of {data_type}."
                )
        return (
            f"Over the past two weeks, {self.county_name_clean} County had an average of [b]"
            f"{two_week_per_capita_avg:,.1f}[/b]"
            f" {p.singular_noun(data_type, two_week_per_capita_avg)} per 100,000 people. "
            f"That means it ranked as having the {sentence_frag}"
        )

    @tag_dtype
    def neighbors(self, *, data_type: str) -> str:
        neighbor_list = get_neighbors(self.county_name_clean, self.gdf)
        neighbor_count = len(neighbor_list)
        region_list = [self.county_name_clean] + neighbor_list
        region_gdf = self.gdf[self.gdf["NAME"].isin(region_list)]
        rank_from_top, rank_from_bottom, others_with_same_rank = self.gdf_get_ranking(
            region_gdf, f"{data_type}_added_past_two_weeks_per_capita"
        )
        per_capita_rank_among_neighbors = rank_text(rank_from_top, rank_from_bottom)
        if others_with_same_rank > 0 and others_with_same_rank != neighbor_count:
            sentence_frag = (
                f"[b]{others_with_same_rank}[/b] other "
                f"{p.singular_noun('counties', others_with_same_rank)} had the same per capita rate of"
                f" {data_type}."
            )
        else:
            sentence_frag = ""

        return (
            f"Compared to its {p.number_to_words(neighbor_count)} neighboring counties, {self.county_name_clean} "
            f"County had the [b]{per_capita_rank_among_neighbors}[/b] number of {data_type} per 100,000 people over "
            f"the past two weeks. {sentence_frag} Here's how {self.county_name_clean}'s per capita 7-day moving average compares to "
            f"its neighbors:"
        )

    @tag(class_name_partial="tests")
    def area_tests(self) -> str:
        tests_added_past_two_weeks = self.__gdf_cell_accessor(
            "tests_added_past_two_weeks"
        )
        confirmed_added_past_two_weeks = self.__gdf_cell_accessor(
            "confirmed_added_past_two_weeks"
        )
        percent_confirmed = round(
            ((confirmed_added_past_two_weeks / tests_added_past_two_weeks) * 100), 1
        )
        return (
            f"Of the [b]{tests_added_past_two_weeks:,}[/b] new test results reported for {self.county_name_clean} "
            f"County over the past two weeks, [b]{confirmed_added_past_two_weeks:,}[/b] ({percent_confirmed}%) were "
            f"positive. Here's how the number of positive tests has trended in {self.county_name_clean}:"
        )
