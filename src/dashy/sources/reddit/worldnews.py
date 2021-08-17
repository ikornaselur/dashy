from textwrap import wrap
from typing import Iterator, Tuple

import requests

from dashy.sources import Source
from dashy.sources.reddit import types

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


class WorldNews(Source):
    max_story_lines: int
    title_width: int

    def __init__(
        self, max_lines: int, max_width: int, *, max_story_lines: int = 3
    ) -> None:
        super().__init__(max_lines, max_width)
        self.max_story_lines = max_story_lines
        self.title_width = self.max_width - UPS_WIDTH - len(SEPERATOR)

    def _get_source(self) -> Iterator[Header]:
        response = requests.get(REDDIT_URL, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

        response_json: types.WorldNews = response.json()
        data = response_json["data"]
        entries = data["children"]

        for entry in entries:
            yield (entry["data"]["ups"], entry["data"]["title"])

    def _yield_story(self, ups: str, title: str) -> Iterator[str]:
        story_lines = 0

        wrapped_lines = wrap(title, self.title_width)

        for idx, line in enumerate(wrapped_lines):
            formatted_line = f"{ups}{SEPERATOR}{line}"
            ups = " " * UPS_WIDTH

            story_lines += 1
            if story_lines == self.max_story_lines:
                # Reached max story lines, check if we need to cut off the last word
                if idx == len(wrapped_lines) - 1:
                    # It's the last line, so we just yield
                    yield formatted_line
                else:
                    # We need to remove the last word potentially
                    line = wrap(line, self.title_width - 2)[0]
                    yield f"{ups}{SEPERATOR}{line}.."
                break

            yield formatted_line

    def get_lines(self) -> Iterator[str]:
        lines = 0

        for entry in self._get_source():
            ups = f"{entry[0]:>{UPS_WIDTH},}"
            title = entry[1]

            for story_line in self._yield_story(ups, title):
                yield story_line
                lines += 1
                if lines == self.max_lines:
                    return  # Reached max lines
