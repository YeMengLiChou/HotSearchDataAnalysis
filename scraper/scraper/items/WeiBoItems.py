from dataclasses import dataclass


@dataclass
class WeiboHotSearchItem:
    """
    微博热搜榜的 item
    """

    rank: int
    note: str
    category: list[str]
    raw_hot: int
    num: int
    onboard_time: int
    star_name: list[str]
    is_new: int
    is_hot: int
    is_gov: int


@dataclass
class WeiboEntertainmentItem:
    """
    微博文娱榜的 item
    """

    grade: str
    note: str
    onboard_time: int
    circle_hot: int
    hot_num: int
    category: list[str]
    star_name: list[str]
    rank: int
    is_new: int
    is_hot: int


@dataclass
class WeiboNewsItem:
    """
    微博要闻棒的 item
    """

    summary: str
    topic: str
    rank: int
    mention: int
    read: int
    claim: str
    category: list[str]
