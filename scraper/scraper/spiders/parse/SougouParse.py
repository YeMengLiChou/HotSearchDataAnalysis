import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 搜狗热搜 的 json 数据
    :param text:
    :param api_type:
    :return:
    """
    result_items: list[CommonHotSearchItem] = []

    response = json.loads(text)
    data = response["data"]

    for item in data:
        item = item["attributes"]
        result_items.append(
            CommonHotSearchItem(
                title=item["title"], rank=item["rank"], hot_num=item["num"], summary=""
            )
        )

    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
