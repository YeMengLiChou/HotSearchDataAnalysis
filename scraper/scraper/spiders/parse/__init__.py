from .WeiboParse import (
    parse_hot_search as parse_weibo_hot_search,
    parse_entertainment_hot_search as parse_weibo_entertainment,
    parse_news_hot_search as parse_weibo_news
)
from .BaiduParse import parse_hot_search as parse_baidu_hot_search
from .ZhihuParse import parse_hot_search as parse_zhihu_hot_search
from .PengPaiParse import parse_hot_search as parse_pengpai_hot_search

__all__ = [
    "parse_weibo_hot_search",
    "parse_weibo_entertainment",
    "parse_weibo_news",
    "parse_baidu_hot_search",
    "parse_zhihu_hot_search",
    "parse_pengpai_hot_search",

]
