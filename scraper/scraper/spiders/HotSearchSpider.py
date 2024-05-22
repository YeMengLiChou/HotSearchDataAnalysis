from typing import Iterable, Any

from scrapy import Request
from scrapy.http import Response

from scraper.api import *
from scraper.scraper.items import HotSearchItem
from scraper.scraper.spiders import parse


class HotSearchSpider(scrapy.Spider):
    name = "hot search"

    def start_requests(self) -> Iterable[Request]:
        apis = all_apis
        return [api.get_scrapy_request(callback=self.parse) for api in apis]

    def parse(self, response: Response, **kwargs: Any) -> HotSearchItem:
        api_type = response.meta[ResponseMetaField.type.value]
        item: HotSearchItem
        # 热搜榜
        if api_type == WeiBoHotSearchApiRequest.type.value:
            item = parse.parse_weibo_hot_search(response.text, api_type)
        # 娱乐榜
        elif api_type == WeiBoEntertainmentApiRequest.type.value:
            item = parse.parse_weibo_entertainment(response.text, api_type)
        # 要闻棒
        elif api_type == WeiBoNewsApiRequest.type.value:
            item = parse.parse_weibo_news(response.text, api_type)
        # 百度
        elif api_type == BaiduHotSearchApiRequest.type.value:
            item = parse.parse_baidu_hot_search(response.text, api_type)
        # 知乎
        elif api_type == ZhihuHotSearchApiRequest.type.value:
            item = parse.parse_zhihu_hot_search(response.text, api_type)
        yield item
