import dataclasses


@dataclasses.dataclass
class CommonHotSearchItem:
    """
    通用的热搜item
    """
    rank: int
    """
    排名
    """

    title: str
    """
    标题
    """
    summary: str
    """
    概要
    """

    hot_num: int
    """
    热度
    """