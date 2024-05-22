import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import (
    CommonHotSearchNoValueItem,
)
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 bilibili 返回的热搜 json 数据

    :param text:
    :param api_type:
    :return:
    """

    result_items: list[CommonHotSearchNoValueItem] = []
    data = json.loads(text)["data"]["trending"]["list"]
    idx = 0
    for item in data:
        idx += 1
        result_items.append(
            CommonHotSearchNoValueItem(
                rank=idx,
                title=item["show_name"],
            )
        )
    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
