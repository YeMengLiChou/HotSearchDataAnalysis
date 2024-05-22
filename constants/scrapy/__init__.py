from enum import Enum


class ResponseMetaField(Enum):
    """
    响应数据 meta 的字段

    """

    data = "ResponseData"
    """
    响应数据
    """

    type = "ApiType"
    """
    所属类型
    """

    scrape_timestamp = "ScrapeTimestamp"
    """
    爬取的时间
    """


class ApiType(Enum):
    """
    Api 的类型，用于 kafka中区分数据
    """

    WeiBoHotSearch = 1
    """
    微博热搜榜
    """

    WeiBoEntertainment = 2
    """
    微博要闻榜
    """

    WeiBoNews = 3
    """
    微博要闻榜
    """

    Baidu = 4
    """
    百度热搜
    """

    Zhihu = 5
    """
    知乎热搜
    """

    PengPai = 6
    """
    澎湃热搜
    """

    TouTiao = 7
    """
    今日头条
    """

    Sougou = 8
    """
    搜狗热搜
    """

    Douyin = 9
    """
    抖音热搜
    """

    Bilibili = 10
    """
    哔哩哔哩热搜
    """

    KuaiShou = 11
    """
    快手热搜
    """

    TencentNews = 12
    """
    腾讯新闻热搜
    """

    T360 = 13
    """
    360 热搜
    """

    @staticmethod
    def get_name_by_value(api_type: int) -> str:
        for k, v in ApiType.__members__.items():
            if v.value == api_type:
                return k
