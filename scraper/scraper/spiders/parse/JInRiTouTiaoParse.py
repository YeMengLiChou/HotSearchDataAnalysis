import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 今日头条 返回的 json 数据

    :param text:
    :param api_type:
    :return:
    """
    result_items: list[CommonHotSearchItem] = []
    response = json.loads(text)
    data = response['data']

    idx = 0
    for item in data:
        idx += 1
        result_items.append(CommonHotSearchItem(
            title=item['title'],
            rank=idx,
            summary="",
            hot_num=int(item['HotValue'])
        ))

    return HotSearchItem(
        api_type=api_type.value,
        data=result_items,
        timestamp=time_utils.now_timestamp()
    )