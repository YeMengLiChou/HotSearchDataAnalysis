import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.DouyinItems import DouyinHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析抖音热榜返回的数据
    :param text:
    :param api_type:
    :return:
    """
    result_items: list[DouyinHotSearchItem] = []
    data = json.loads(text)["data"]

    word_list = data["word_list"]
    for item in word_list:
        result_items.append(
            DouyinHotSearchItem(
                rank=item["position"],
                word=item["word"],
                hot_num=item["hot_value"],
                event_timestamp=item["event_time"],
            )
        )
    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
