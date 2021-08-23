import datetime as dt
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

# Upvotes will fit within 4 characters, as it will be shortened to "ks",
# that is 56789 will be 57k, 123456 will be 123k
UPS_WIDTH = 4
SEP_WIDTH = 3
TOP_SEP = "┬"
SEP = "│"
BOTTOM_SEP = "┴"

Header = Tuple[int, str, int]  # score + title + age in hours


class WorldNews(Source):
    max_story_lines: int
    title_width: int

    def __init__(
        self,
        max_lines: int,
        max_width: int,
        *,
        max_story_lines: int = 3,
        max_age: int = 24,  # No stories can be above 24 hour old
    ) -> None:
        super().__init__(max_lines, max_width)
        self.max_story_lines = max_story_lines
        self.title_width = self.max_width - UPS_WIDTH - SEP_WIDTH
        self.max_age = max_age

    def _get_source(self) -> Iterator[Header]:
        response = requests.get(REDDIT_URL, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

        response_json: types.WorldNews = response.json()
        data = response_json["data"]
        entries = data["children"]

        for entry in entries:
            data = entry["data"]
            delta = dt.datetime.utcnow() - dt.datetime.fromtimestamp(
                data["created_utc"]
            )
            age_in_hours = delta.seconds // 3600
            if age_in_hours > self.max_age:
                # Skip stories that are too old
                continue
            yield (data["ups"], data["title"], age_in_hours)

    def _yield_story(self, ups: int, title: str, age_in_hours: int) -> Iterator[str]:
        story_lines = 0
        age_in_hours_str = f"{age_in_hours}h"
        left_col = [
            f"{age_in_hours_str:>{UPS_WIDTH}}",
            f"{round(ups / 1000):>{UPS_WIDTH-1},}k",
        ]

        wrapped_lines = wrap(title, self.title_width)
        line_count = len(wrapped_lines)

        for idx, line in enumerate(wrapped_lines):
            left = left_col.pop() if left_col else " " * UPS_WIDTH
            if idx == 0:
                SEPERATOR = f" {TOP_SEP} "
            elif idx == line_count - 1 or idx == self.max_story_lines - 1:
                SEPERATOR = f" {BOTTOM_SEP} "
            else:
                SEPERATOR = f" {SEP} "

            formatted_line = f"{left}{SEPERATOR}{line}"

            story_lines += 1
            if story_lines == self.max_story_lines:
                # Reached max story lines, check if we need to cut off the last word
                if idx == len(wrapped_lines) - 1:
                    # It's the last line, so we just yield
                    yield formatted_line
                else:
                    # We need to remove the last word potentially
                    line = wrap(line, self.title_width - 2)[0]
                    yield f"{left}{SEPERATOR}{line}.."
                break

            yield formatted_line

    def get_lines(self) -> Iterator[str]:
        lines = 0

        for ups, title, age_in_hours in self._get_source():
            for story_line in self._yield_story(ups, title, age_in_hours):
                yield story_line
                lines += 1
                if lines == self.max_lines:
                    return  # Reached max lines
