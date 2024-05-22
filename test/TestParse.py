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
    gen_headers = {}
    for k, v in headers.items():
        if isinstance(v, list):
            v = ";".join([x.decode() for x in v])
        gen_headers[k] = v

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


if __name__ == "__main__":
    # test_parse_baidu()
    test_parse_weibo_hot()
