from typing import List
from typing_extensions import TypedDict


class ChildData(TypedDict):
    title: str
    ups: int


class ChildrenItem(TypedDict):
    kind: str
    data: ChildData


class Data(TypedDict):
    children: List[ChildrenItem]


class WorldNews(TypedDict):
    kind: str
    data: Data
