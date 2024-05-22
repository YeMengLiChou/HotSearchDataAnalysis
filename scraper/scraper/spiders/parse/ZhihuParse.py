import json
import re

from lxml import etree

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import time_utils, xpath


def parse_hot_search(html_text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析知乎热搜网页
    :param html_text:
    :param api_type:
    :return:
    """
    result_items: list[CommonHotSearchItem] = []

    html = etree.HTML(html_text, etree.HTMLParser())

    js_data = xpath.first(html, "//script[@id='js-initialData']/text()")
    json_data = json.loads(js_data)

    hot_list = json_data["initialState"]["topstory"]["hotList"]

    idx = 0
    for item in hot_list:
        idx += 1
        item = item["target"]

        hot_num_str = item["metricsArea"]["text"]
        # 正则匹配
        match = re.match(r"(\d+)", hot_num_str)
        hot_num = int(match.group(1))
        if "万" in hot_num_str:
            hot_num *= 10000

        result_items.append(
            CommonHotSearchItem(
                title=item["titleArea"]["text"],
                summary=item["excerptArea"]["text"],
                rank=idx,
                hot_num=hot_num,
            )
        )

    return HotSearchItem(
        api_type=api_type.value,
        data=result_items,
        timestamp=time_utils.now_timestamp(),
    )
