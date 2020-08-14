from typing import List, Dict


def process_stories(stories: List[Dict[str, str]]):
    return [{"headline": story["title"], "url": story["url"]} for story in stories]
