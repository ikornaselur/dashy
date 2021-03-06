from typing import List
from typing_extensions import TypedDict


class ChildData(TypedDict):
    created_utc: int
    title: str
    ups: int


class ChildrenItem(TypedDict):
    kind: str
    data: ChildData


class PostData(TypedDict):
    children: List[ChildrenItem]


class Posts(TypedDict):
    kind: str
    data: PostData
