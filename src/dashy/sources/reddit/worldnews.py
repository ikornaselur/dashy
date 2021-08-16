from textwrap import wrap
from typing import Iterator, List, Tuple

import requests

from dashy.sources.reddit.types import WorldNews

REDDIT_URL = "https://www.reddit.com/r/worldnews/top.json?sort=top&t=day"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
)

# Most upvotes will fit within 6 characters (up to 100k), with a rare
# every now and then being above 100k
UPS_WIDTH = 6
SEPERATOR = " | "

Header = Tuple[int, str]  # Score + Title


def _get_source(max_entries: int = 5) -> List[Header]:
    response = requests.get(REDDIT_URL, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    response_json: WorldNews = response.json()
    data = response_json["data"]
    entries = data["children"][:max_entries]

    return [(entry["data"]["ups"], entry["data"]["title"]) for entry in entries]


def top_news(max_width: int) -> Iterator[str]:
    title_width = max_width - UPS_WIDTH - len(SEPERATOR)
    for entry in _get_source():
        ups = f"{entry[0]:>{UPS_WIDTH},}"
        title = entry[1]
        if len(title) < title_width:
            yield f"{ups}{SEPERATOR}{title}"
            continue

        for line in wrap(title, title_width):
            yield f"{ups}{SEPERATOR}{line}"
            ups = " " * UPS_WIDTH
