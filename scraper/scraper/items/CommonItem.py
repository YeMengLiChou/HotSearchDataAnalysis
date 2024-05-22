import dataclasses


@dataclasses.dataclass
class BaiduHotSearchItem:
    rank: int
    title: str
    