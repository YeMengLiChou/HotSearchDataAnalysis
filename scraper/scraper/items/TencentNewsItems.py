import dataclasses


@dataclasses.dataclass
class TencentNewsHotSearchItem:
    title: str
    rank: int
    hot_num: int
    category: list[str]
    publish_timestamp: int
    tags: list[str]
    praise_nums: int
    comment_nums: int
    node: str