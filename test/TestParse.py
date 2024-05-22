import json
from typing import Any

import requests
from requests import Response

from scraper.api import *


def send_request(api: ApiRequest) -> Response:
    scrapy_request = api.get_scrapy_request()
    return requests.request(
        method=scrapy_request.method,
        url=scrapy_request.url,
        headers=scrapy_request.headers,
        cookies=scrapy_request.cookies,
        data=scrapy_request.body,
        timeout=5,
    )


def print_json(obj: Any):
    print(json.dumps(obj, ensure_ascii=False, indent=4, default=lambda x: x.__dict__))


def test_parse_baidu():
    from scraper.scraper.spiders.parse.BaiduParse import parse_hot_search

    print_json(
        parse_hot_search(
            html_text=send_request(BaiduHotSearchApiRequest()).text,
            api_type=ApiType.Baidu,
        )
    )


if __name__ == "__main__":
    test_parse_baidu()
