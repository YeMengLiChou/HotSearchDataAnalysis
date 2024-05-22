import dataclasses


@dataclasses.dataclass
class DouyinHotSearchItem:
    rank: int
    word: str
    hot_num: int
    event_timestamp: int