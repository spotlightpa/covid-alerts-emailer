from typing import List, Dict

from src.modules.helper.add_utm_params import add_utm_params


def process_stories(stories: List[Dict[str, str]]):
    return [
        {"headline": story["title"], "url": add_utm_params(story["url"])}
        for story in stories
    ]
