import json
from typing import List

import scrapy
from scrapy.http import Response

from constants.scrapy import ApiType
from scraper.scraper.items import HotSearchItem
from scraper.scraper.items import WeiBoItems
from utils import time_utils


def parse_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析微博热搜榜的响应
    :param api_type:
    :param text:  response.text
    :return:
    """

    body = json.loads(text)
    data = body["data"]
    result_items: List[WeiBoItems.WeiboHotSearchItem] = []

    # 当前的热搜
    realtime: list = data["realtime"]
    for item in realtime:
        # 去掉广告
        if item.get("is_ad", 0) == 1:
            continue
        if (star_name := item["star_name"]) == {}:
            star_name = []
        result_items.append(
            WeiBoItems.WeiboHotSearchItem(
                # 排名
                rank=item["rank"],
                # 文字
                note=item["note"].replace("#", ""),
                # 类别
                category=item["category"].split(","),
                # 生热度（真实热度）
                raw_hot=item["raw_hot"],
                # 显示的热度
                num=item["num"],
                # 上榜时间
                onboard_time=item["onboard_time"],
                # 明星名称
                star_name=star_name,
                # 是否新上榜
                is_new=item.get("is_new", 0),
                # 是否很“热”
                is_hot=item.get("is_hot", 0),
                # 是否为政府
                is_gov=item.get("is_gov", 0),
            )
        )
    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )


def parse_entertainment_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析娱乐热搜榜的响应
    :param api_type:
    :param text:  response.text
    :return:
    """

    body = json.loads(text)
    data = body["data"]
    result_items: List[WeiBoItems.WeiboEntertainmentItem] = []

    band_list: list = data["band_list"]
    for item in band_list:
        if (star_name := item["star_name"]) == {}:
            star_name = []
        result_items.append(
            WeiBoItems.WeiboEntertainmentItem(
                grade=item["grade"],
                note=item["note"].replace("#", ""),
                onboard_time=item["onboard_time"],
                circle_hot=item["circle_hot"],
                hot_num=item["hot_num"],
                category=item["category"].split(","),
                star_name=star_name,
                rank=item["hot_rank_position"],
                is_hot=item.get("is_hot", 0),
                is_new=item.get("is_new", 0),
            )
        )

    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )


def parse_news_hot_search(text: str, api_type: ApiType) -> HotSearchItem:
    """
    解析微博要闻榜的响应
    :param api_type:
    :param text:  response.text
    :return:
    """

    body = json.loads(text)
    data = body["data"]
    result_items: List[WeiBoItems.WeiboNewsItem] = []

    band_list: list = data["band_list"]
    for item in band_list:
        cates: list[str] = []
        for text in item["category"].split("|"):
            if not text.isdigit():
                cates.append(text)
        result_items.append(
            WeiBoItems.WeiboNewsItem(
                summary=item["summary"],
                topic=item["topic"],
                rank=item["rank"],
                mention=item["mention"],
                read=item["read"],
                claim=item["claim"],
                category=cates,
            )
        )
    return HotSearchItem(
        api_type=api_type.value, data=result_items, timestamp=time_utils.now_timestamp()
    )
