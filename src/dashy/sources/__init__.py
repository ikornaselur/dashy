from typing import Iterator


class Source:
    max_lines: int
    max_width: int

    def __init__(self, max_lines: int, max_width: int) -> None:
        self.max_lines = max_lines
        self.max_width = max_width

    def get_lines(self) -> Iterator[str]:
        raise NotImplementedError()
