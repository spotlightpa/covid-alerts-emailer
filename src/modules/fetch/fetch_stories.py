from typing import List, Dict
import requests


def fetch_stories(story_count: int) -> List[Dict[str, str]]:
    """
    Fetches summaries and links to Spotlight PA stories from Spotlight PA story feed.

    Args:
        story_count (int): Number of stories to return

    Returns:
        List[Dict[str, str]]: Spotlight PA stories
    """

    url = "https://www.spotlightpa.org/news/feed-summary.json"
    r = requests.get(url)
    stories = r.json()["items"][0:story_count]
    return stories
