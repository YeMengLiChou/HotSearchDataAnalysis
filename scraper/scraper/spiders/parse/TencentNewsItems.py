import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 腾讯新闻 返回的数据
    :param text:
    :param api_type:
    :return:
    """
    result_list: list[CommonHotSearchItem] = []

    response = json.loads(text)
    news_list = response['idlist'][0]['newslist']
    for item in news_list:
        if item['picShowType'] == 0:
            continue

        title = item['hotEvent']['title']
        timestamp = item['timestamp']
        abstract = item['abstract']
        source = item['source']
        read_count = item['readCount']
        comment_count = item['comments']
        rank = item['ranking']
        hot_num = item['hotEvent']['hotScore']


    return HotSearchItem(
        api_type=api_type.value, data=result_list, timestamp=time_utils.now_timestamp()
    )
