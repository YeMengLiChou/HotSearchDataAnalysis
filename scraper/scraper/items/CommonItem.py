import dataclasses


@dataclasses.dataclass
class CommonHotSearchItem:
    """
    通用的热搜item
    """
    rank: int
    title: str
    summary: str
    hot_num: int
