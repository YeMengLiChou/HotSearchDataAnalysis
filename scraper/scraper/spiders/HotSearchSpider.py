import logging
from typing import Any

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.http import Response

from scraper.api import *
from scraper.scraper.items import HotSearchItem
from scraper.scraper.spiders import parse
from utils import redis_tools


class HotSearchSpider(scrapy.Spider):
    name = "hot search"

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        crawler.signals.connect(
            receiver=spider.closed_spider, signal=signals.spider_closed
        )
        return spider

    def start_requests(self):
        yield from [api().get_scrapy_request(callback=self.parse) for api in all_apis]
        # yield all_apis[0]().get_scrapy_request(callback=self.parse)
        # yield from [
        #     WeiBoHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     WeiBoNewsApiRequest().get_scrapy_request(callback=self.parse),
        #     WeiBoEntertainmentApiRequest().get_scrapy_request(callback=self.parse),
        #     BaiduHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     ZhihuHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     PengPainHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     TencentNewsHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     SougouHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     BilibiliHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     KuaiShouHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     T360HotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     TouTiaoHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        #     DouyinHotSearchApiRequest().get_scrapy_request(callback=self.parse),
        # ]

    def parse(self, response: Response, **kwargs: Any) -> HotSearchItem:
        api_type = ApiType(response.meta[ResponseMetaField.type.value])
        item: HotSearchItem
        # 热搜榜
        if api_type == WeiBoHotSearchApiRequest.type:
            item = parse.parse_weibo_hot_search(response.text, api_type)
        # 娱乐榜
        elif api_type == WeiBoEntertainmentApiRequest.type:
            item = parse.parse_weibo_entertainment(response.text, api_type)
        # 要闻棒
        elif api_type == WeiBoNewsApiRequest.type:
            item = parse.parse_weibo_news(response.text, api_type)
        # 百度
        elif api_type == BaiduHotSearchApiRequest.type:
            item = parse.parse_baidu_hot_search(response.text, api_type)
        # 知乎
        elif api_type == ZhihuHotSearchApiRequest.type:
            item = parse.parse_zhihu_hot_search(response.text, api_type)
        # 澎湃
        elif api_type == PengPainHotSearchApiRequest.type:
            item = parse.parse_pengpai_hot_search(response.text, api_type)
        # 今日头条
        elif api_type == TouTiaoHotSearchApiRequest.type:
            item = parse.parse_toutiao_hot_search(response.text, api_type)
        # 搜狗
        elif api_type == SougouHotSearchApiRequest.type:
            item = parse.parse_sougou_hot_search(response.text, api_type)
        # 抖音
        elif api_type == DouyinHotSearchApiRequest.type:
            item = parse.parse_douyin_hot_search(response.text, api_type)
        # bilibili
        elif api_type == BilibiliHotSearchApiRequest.type:
            item = parse.parse_bilibili_hot_search(response.text, api_type)
        # 快手
        elif api_type == KuaiShouHotSearchApiRequest.type:
            item = parse.parse_kuaishou_hot_search(response.text, api_type)
        # 腾讯新闻
        elif api_type == TencentNewsHotSearchApiRequest.type:
            item = parse.parse_tencent_news_hot_search(response.text, api_type)
        else:
            logging.error(f"{api_type} - {api_type.name} not implemented yet!")
            raise RuntimeError("你丫的忘记判断了！")

        yield item

    def closed_spider(self, spider: scrapy.Spider) -> None:
        content = "Scraper redis status:\n"
        for api_type in ApiType:
            res = redis_tools.get_api_information(api_type.name)
            content += f"{api_type.name}: {res['time']} - {res['count']}\n"
        spider.logger.warning(content)
