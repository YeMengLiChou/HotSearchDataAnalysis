import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.TencentNewsItems import TencentNewsHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 腾讯新闻 返回的数据
    :param text:
    :param api_type:
    :return:
    """
    result_list: list[TencentNewsHotSearchItem] = []

    response = json.loads(text)
    news_list = response["idlist"][0]["newslist"]
    for item in news_list:
        if item["picShowType"] == 0:
            continue

        title = item["hotEvent"]["title"]
        timestamp = item["timestamp"]
        abstract = item.get("abstract", "")
        source = item.get("source", "")
        read_count = item.get("readCount", -1)
        comment_count = item.get("comments", -1)
        rank = item["ranking"]
        hot_num = item["hotEvent"]["hotScore"]
        result_list.append(
            TencentNewsHotSearchItem(
                title=title,
                publish_timestamp=timestamp,
                summary=abstract,
                source=source,
                read_nums=read_count,
                comment_nums=comment_count,
                rank=rank,
                hot_num=hot_num,
            )
        )

    return HotSearchItem(
        api_type=api_type.value, data=result_list, timestamp=time_utils.now_timestamp()
    )
