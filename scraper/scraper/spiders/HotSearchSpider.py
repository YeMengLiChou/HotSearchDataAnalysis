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
        # 澎湃
        elif api_type == PengPainHotSearchApiRequest.type.value:
            item = parse.parse_pengpai_hot_search(response.text, api_type)
        # 今日头条
        elif api_type == TouTiaoHotSearchApiRequest.type.value:
            item = parse.parse_toutiao_hot_search(response.text, api_type)
        # 搜狗
        elif api_type == SougouHotSearchApiRequest.type.value:
            item = parse.parse_sougou_hot_search(response.text, api_type)
        # 抖音
        elif api_type == DouyinHotSearchApiRequest.type.value:
            item = parse.parse_douyin_hot_search(response.text, api_type)
        # bilibili
        elif api_type == BilibiliHotSearchApiRequest.type.value:
            item = parse.parse_bilibili_hot_search(response.text, api_type)
        # 快手
        elif api_type == KuaiShouHotSearchApiRequest.type.value:
            item = parse.parse_kuaishou_hot_search(response.text, api_type)
        # 腾讯新闻
        elif api_type == TencentNewsHotSearchApiRequest.type.value:
            item = parse.parse_tencent_news_hot_search(response.text, api_type)
        else:
            raise RuntimeError("你丫的忘记判断了！")

        yield item
