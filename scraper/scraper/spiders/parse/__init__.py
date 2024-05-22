from .WeiboParse import (
    parse_hot_search as parse_weibo_hot_search,
    parse_entertainment_hot_search as parse_weibo_entertainment,
    parse_news_hot_search as parse_weibo_news
)
from .BaiduParse import parse_hot_search as parse_baidu_hot_search

__all__ = [
    "parse_weibo_hot_search",
    "parse_weibo_entertainment",
    "parse_weibo_news",
    "parse_baidu_hot_search"
]
