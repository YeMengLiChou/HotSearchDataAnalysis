from lxml import etree

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import xpath, time_utils


def parse_hot_search(html_text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析百度的网页内容
    :param html_text:
    :param api_type:
    :return:
    """

    result_items: list[CommonHotSearchItem] = []

    html = etree.HTML(html_text, etree.HTMLParser())
    items_container = html.xpath(
        "//div[contains(@class, 'container-bg_')]/div[@style='margin-bottom:20px']/div"
    )
    for item in items_container:
        hot_num = int(
            xpath.first(item, ".//div[contains(@class, 'hot-index_')]/text()").strip()
        )
        title = xpath.first(item, ".//div[@class='c-single-text-ellipsis']/text()").strip()
        summary = xpath.first(item, ".//div[contains(@class, 'hot-desc_')]/text()").strip()

        try:
            rank = int(
                xpath.first(item, ".//div[contains(@class, 'c-index-bg')]/text()").strip()
            )
        except:
            rank = 0

        result_items.append(
            CommonHotSearchItem(
                title=title,
                summary=summary,
                hot_num=hot_num,
                rank=rank,
            )
        )

    return HotSearchItem(
        api_type=api_type.value,
        data=result_items,
        timestamp=time_utils.now_timestamp(),
    )
