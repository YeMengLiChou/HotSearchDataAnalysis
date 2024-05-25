import abc
from typing import Optional, Callable, Union

import scrapy

from constants.scrapy import ApiType, ResponseMetaField


class ApiRequest(abc.ABC):
    """
    Api 请求基类，规定一些字段
    """

    method: str
    """
    请求方法
    """

    url: str
    """
    请求 url
    """

    cookies: Optional[dict] = None
    """
    Cookies
    """

    accept: Optional[str] = "application/json; charset=utf-8"
    """
    请求内容需要为 application/json
    """

    headers: dict = {}
    """
    特定请求头
    """

    type: ApiType
    """
    Api 所属的类型
    """

    def get_scrapy_request(
        self,
        callback: Optional[Callable] = None,
        headers: Optional[dict] = None,
        body: Optional[Union[bytes, str]] = None,
        meta: Optional[dict] = None,
        priority: int = 0,
        dont_filter: bool = True,
        errback: Optional[Callable] = None,
    ) -> scrapy.Request:
        """
        生成对应的api
        :param callback:
        :param headers:
        :param body:
        :param meta:
        :param priority:
        :param dont_filter:
        :param errback:
        :return:
        """
        # 更新 content-type
        if self.accept:
            if headers is None:
                headers = {}
            headers["Accept"] = self.accept

        # 更新请求头
        if headers:
            headers.update(self.headers)

        # 添加所属类型
        meta = meta or {}
        meta.setdefault(ResponseMetaField.type.value, self.type.value)

        return scrapy.Request(
            url=self.url,
            method=self.method,
            callback=callback,
            headers=headers,
            body=body,
            cookies=self.cookies,
            meta=meta,
            priority=priority,
            dont_filter=dont_filter,
            errback=errback,
        )


class WeiBoHotSearchApiRequest(ApiRequest):
    """
    微博热搜榜
    """

    method = "GET"

    url = "https://weibo.com/ajax/side/hotSearch"

    type = ApiType.WeiBoHotSearch


class WeiBoEntertainmentApiRequest(ApiRequest):
    """
    微博文娱榜
    """

    method = "GET"

    url = "https://weibo.com/ajax/statuses/entertainment"

    cookies = {
        'SUB': '_2AkMRdsEcf8NxqwFRmfsQzW7iZIp3zw7EieKnKjDHJRMxHRl-yT9kqmoztRB6Ovbv8yRr5hGC5vVlQR3I5u37TIvYCgsZ'
    }

    type = ApiType.WeiBoEntertainment


class WeiBoNewsApiRequest(ApiRequest):
    """
    微博要闻榜
    """

    method = "GET"

    url = "https://weibo.com/ajax/statuses/news"

    cookies = {
        'SUB': '_2AkMRdsEcf8NxqwFRmfsQzW7iZIp3zw7EieKnKjDHJRMxHRl-yT9kqmoztRB6Ovbv8yRr5hGC5vVlQR3I5u37TIvYCgsZ'
    }

    type = ApiType.WeiBoNews


class BaiduHotSearchApiRequest(ApiRequest):
    """
    百度热搜榜
    """

    method = "GET"

    url = "https://top.baidu.com/board?tab=realtime"

    accept = None

    type = ApiType.Baidu


class ZhihuHotSearchApiRequest(ApiRequest):
    """
    知乎热搜榜
    """

    method = "GET"

    url = "https://www.zhihu.com/billboard"

    accept = None

    type = ApiType.Zhihu


class PengPainHotSearchApiRequest(ApiRequest):
    """
    澎湃热搜榜
    """

    method = "GET"

    url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"

    accept = None

    type = ApiType.PengPai


class TouTiaoHotSearchApiRequest(ApiRequest):
    """
    头条热搜榜
    """

    method = "GET"

    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"

    type = ApiType.TouTiao


class SougouHotSearchApiRequest(ApiRequest):
    """
    搜狗热搜榜
    """

    method = "GET"

    url = "https://go.ie.sogou.com/hot_ranks"

    type = ApiType.Sougou


class T360HotSearchApiRequest(ApiRequest):
    """
    360热搜榜
    """

    method = "GET"

    url = "https://trends.so.com/top/realtime"

    type = ApiType.T360


class DouyinHotSearchApiRequest(ApiRequest):
    """
    抖音热搜榜
    """

    method = "GET"

    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"

    headers = {"Referer": "https://www.douyin.com/hot"}

    type = ApiType.Douyin


class BilibiliHotSearchApiRequest(ApiRequest):
    """
    哔哩哔哩热搜榜
    """

    method = "GET"

    url = "https://api.bilibili.com/x/web-interface/wbi/search/square?limit=50&platform=web"

    type = ApiType.Bilibili


class KuaiShouHotSearchApiRequest(ApiRequest):
    """
    快手热搜榜
    """

    method = "GET"

    url = "https://www.kuaishou.com/?isHome=1"

    accept = None

    type = ApiType.KuaiShou


class TencentNewsHotSearchApiRequest(ApiRequest):
    """
    腾讯新闻热搜榜
    """

    method = "GET"

    url = ("https://i.news.qq.com/gw/event/pc_hot_ranking_list?ids_hash=&offset=0&page_size=50&appver=15.5_qqnews_7.1"
           ".60&rank_id=hot")

    accept = None

    type = ApiType.TencentNews


all_apis = [
    WeiBoHotSearchApiRequest,
    WeiBoEntertainmentApiRequest,
    WeiBoNewsApiRequest,
    BaiduHotSearchApiRequest,
    ZhihuHotSearchApiRequest,
    PengPainHotSearchApiRequest,
    TouTiaoHotSearchApiRequest,
    SougouHotSearchApiRequest,
    # T360HotSearchApiRequest,
    DouyinHotSearchApiRequest,
    BilibiliHotSearchApiRequest,
    KuaiShouHotSearchApiRequest,
    TencentNewsHotSearchApiRequest,
]
