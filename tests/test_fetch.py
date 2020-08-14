from src.modules.fetch.fetch_stories import fetch_stories


def test_fetch_stories():
    stories = fetch_stories(3)
    assert len(stories) == 3
    print(stories)
