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

    items = html.xpath("//a[@class='HotList-item']")
    for item in items:
        rank = int(
            xpath.first(
                item, ".//div[@class='HotList-itemIndex HotList-itemIndexHot']/text()"
            ).strip()
        )

        title: str = xpath.first(
            item, ".//div[@class='HotList-itemTitle']/text()"
        ).strip()
        desc: str = xpath.first(
            item, ".//div[@class='HotList-itemExcerpt']/text()"
        ).strip()

        hot_num_str: str = xpath.first(
            item, ".//div[@class='HotList-itemMetrics']/text()"
        ).strip()
        # 正则匹配
        match = re.match(r"(\d+)", hot_num_str)
        hot_num = int(match.group(1))
        if "万" in hot_num_str:
            hot_num *= 10000

    return HotSearchItem(
        api_type=api_type.value,
        data=result_items,
        timestamp=time_utils.now_timestamp(),
    )
