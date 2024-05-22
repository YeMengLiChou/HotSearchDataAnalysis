import re

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items.CommonItem import CommonHotSearchItem
from utils import time_utils

PATTERN = re.compile(
    r'"VisionHotRankItem:\S+?":\{"rank":(\d+),\S+?"name":"(\S+?)",\S+?"'
    r'hotValue":"(\d+(?:.\d+)?万?)",\S+?"__typename":"VisionHotRankItem"}'
)

def parse_hot_search(html_text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析 快手 网页上的热搜数据
    :param html_text:
    :param api_type:
    :return:
    """

    result_items: list[CommonHotSearchItem] = []

    html_text = html_text.replace(" ", "").replace("\n", "")
    for item in PATTERN.findall(html_text):
        hot_num_str = item[3]
        if "万" in hot_num_str:
            hot_num_str = hot_num_str.replace("万", "")
            hot_num = int(hot_num_str) * 10_000
        else:
            hot_num = int(hot_num_str)

        result_items.append(
            CommonHotSearchItem(
                rank=int(item[1]), title=item[2], hot_num=hot_num, summary=""
            )
        )

    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
