import dataclasses


@dataclasses.dataclass
class TencentNewsHotSearchItem:
    title: str
    rank: int
    hot_num: int
    source: str
    publish_timestamp: int
    comment_nums: int
    read_nums: int
    summary: str
