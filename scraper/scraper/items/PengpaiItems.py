import dataclasses


@dataclasses.dataclass
class PengPaiHotSearchItem:
    title: str

    publish_timestamp: int

    tags: list[str]

    praise_nums: int
    """
    点赞数量
    """

    comment_nums: int
    """
    评论数量
    """

    node: str
    """
    所处节点
    """

    rank: int
    """
    排名
    """
