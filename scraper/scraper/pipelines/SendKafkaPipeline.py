import logging

from scrapy.crawler import Crawler
from scrapy.statscollectors import StatsCollector

from constants.scrapy import ApiType

# from utils import kafka_tools
from constants.scrapy.Items import HotSearchItemConstant
from scraper.scraper.items import HotSearchItem
from utils import redis_tools

logger = logging.getLogger(__name__)


class SendKafkaPipeline:
    """
    将 item 发送到 指定的 kafka中
    """

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        obj = cls(crawler.stats)
        return obj

    def __init__(self, stats: StatsCollector):
        self.stats = stats

    def process_item(self, item: HotSearchItem, spider):
        # 将 item 发送给 kafka
        try:
            logger.debug(item)
            # kafka_tools.send_item_to_kafka(item, immediate=True)
            logger.info(f"{ApiType(item.api_type).name}: Success")
            redis_tools.update_api_scraped(ApiType(item.api_type).name, item.timestamp)
        except Exception as e:
            logger.error(f"{ApiType(item.api_type).name}: Error")
            logger.error(e)
