import json
from typing import Any

import requests
from requests import Response

from scraper.api import *


def send_request(api: ApiRequest) -> Response:
    """
    发送请求
    :param api: 见 [scraper.api] 部分
    :return:
    """
    scrapy_request = api.get_scrapy_request()
    headers = scrapy_request.headers
    # 将请求头转换一下
    gen_headers = {}
    for k, v in headers.items():
        if isinstance(v, list):
            v = ";".join([x.decode() for x in v])
        gen_headers[k] = v

    gen_headers["User-Agent"] = (
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
    )
    return requests.request(
        method=scrapy_request.method,
        url=scrapy_request.url,
        headers=gen_headers,
        cookies=scrapy_request.cookies,
        data=scrapy_request.body,
        timeout=5,
    )


def print_json(obj: Any):
    """
    以 json 的格式输出
    :param obj:
    :return:
    """
    print(json.dumps(obj, ensure_ascii=False, indent=4, default=lambda x: x.__dict__))


def test_parse_baidu():
    from scraper.scraper.spiders.parse.BaiduParse import parse_hot_search

    print_json(
        parse_hot_search(
            html_text=send_request(BaiduHotSearchApiRequest()).text,
            api_type=ApiType.Baidu,
        )
    )


def test_parse_weibo_hot():
    from scraper.scraper.spiders.parse.WeiboParse import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(WeiBoHotSearchApiRequest()).text,
            api_type=ApiType.WeiBoHotSearch,
        )
    )


def test_parse_weibo_news():
    """
    测试 Weibo 要闻热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.WeiboParse import parse_news_hot_search

    print_json(
        parse_news_hot_search(
            text=send_request(WeiBoNewsApiRequest()).text,
            api_type=ApiType.WeiBoNews,
        )
    )


def test_parse_zhihu():
    """
    测试知乎热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.ZhihuParse import parse_hot_search

    print_json(
        parse_hot_search(
            html_text=send_request(ZhihuHotSearchApiRequest()).text,
            api_type=ApiType.Zhihu,
        )
    )


def test_parse_weibo_entertainment():
    """
    测试 Weibo 娱乐热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.WeiboParse import parse_entertainment_hot_search

    print_json(
        parse_entertainment_hot_search(
            text=send_request(WeiBoEntertainmentApiRequest()).text,
            api_type=ApiType.WeiBoEntertainment,
        )
    )


def test_parse_bilibili():
    """
    测试 Bilibili 热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.BilibiliParse import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(BilibiliHotSearchApiRequest()).text,
            api_type=ApiType.Bilibili,
        )
    )


def test_parse_jinritoutiao():
    """
    测试 今日头条 热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.JInRiTouTiaoParse import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(TouTiaoHotSearchApiRequest()).text,
            api_type=ApiType.TouTiao,
        )
    )


def test_parse_kuaishou():
    """
    测试快手热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.KuaiShouParse import parse_hot_search

    print_json(
        parse_hot_search(
            html_text=send_request(KuaiShouHotSearchApiRequest()).text,
            api_type=ApiType.KuaiShou,
        )
    )


def test_parse_pengpai():
    """
    测试彭拍热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.PengPaiParse import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(PengPainHotSearchApiRequest()).text,
            api_type=ApiType.PengPai,
        )
    )


def test_parse_tencent():
    """
    测试腾讯热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.TencentNewsItems import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(TencentNewsHotSearchApiRequest()).text,
            api_type=ApiType.TencentNews,
        )
    )


def test_parse_sougou():
    """
    测试搜狗热搜响应
    :return:
    """
    from scraper.scraper.spiders.parse.SougouParse import parse_hot_search

    print_json(
        parse_hot_search(
            text=send_request(SougouHotSearchApiRequest()).text,
            api_type=ApiType.Sougou,
        )
    )


if __name__ == "__main__":
    test_parse_baidu()
    test_parse_weibo_hot()
    test_parse_weibo_news()
    test_parse_zhihu()
    test_parse_weibo_entertainment()
    test_parse_bilibili()
    test_parse_jinritoutiao()
    test_parse_kuaishou()
    test_parse_pengpai()
    test_parse_tencent()
    test_parse_sougou()

    # from scraper.api import all_apis
    # for api in all_apis:
    #     print_json(
    #
    #     )
