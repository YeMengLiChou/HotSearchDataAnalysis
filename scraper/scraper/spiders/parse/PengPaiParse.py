import json

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.PengpaiItems import PengPaiHotSearchItem
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析澎湃新闻返回的 json 数据
    :param text:
    :param api_type:
    :return:
    """
    result_items: list[PengPaiHotSearchItem] = []

    response = json.loads(text)
    data = response["data"]
    hot_news = data["hotNews"]
    idx = 0
    for item in hot_news:
        idx += 1

        result_items.append(
            PengPaiHotSearchItem(
                title=item["name"],
                publish_timestamp=int(item["pubTimeLong"]),
                tags=[tag["tag"] for tag in item.get("tagList", [])],
                praise_nums=int(item["praiseTimes"]),
                comment_nums=int(item["interactionNum"]),
                node=item["nodeInfo"]["name"],
                rank=idx,
            )
        )

    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
