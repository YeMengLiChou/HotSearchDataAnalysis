import dataclasses
from typing import TypeVar

T = TypeVar("T")


@dataclasses.dataclass
class HotSearchItem:
    """
    热搜 Item
    """

    api_type: int
    """
    所属类型
    """

    data: list[T]
    """
    热搜内容
    """

    timestamp: int
    """
    爬取时间，可以认为是当前时间点的热搜
    """