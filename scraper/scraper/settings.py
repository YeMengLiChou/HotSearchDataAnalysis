import logging
from config.config import get_settings


BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = False

# 最大并发数
CONCURRENT_REQUESTS = get_settings("scrapy.settings.CONCURRENT_REQUESTS", 16)

# 下载延时
DOWNLOAD_DELAY = get_settings("scrapy.settings.DOWNLOAD_DELAY", 0)

# 下载超时30
DOWNLOAD_TIMEOUT = get_settings("scrapy.settings.DOWNLOAD_TIMEOUT", 30)

# 对用一个响应的最大处理item数
CONCURRENT_ITEMS = get_settings("scrapy.settings.CONCURRENT_ITEMS", 100)

# 对同一个域名的最大并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = get_settings(
    "scrapy.settings.CONCURRENT_REQUESTS_PER_DOMAIN", 16
)

# 重试次数
RETRY_TIMES = get_settings("scrapy.settings.RETRY_TIMES", 3)

# 最大线程池大小
REACTOR_THREADPOOL_MAXSIZE = get_settings(
    "scrapy.settings.REACTOR_THREADPOOL_MAXSIZE", 10
)

# url长度限制
URLLENGTH_LIMIT = 3000


SPIDER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES = {
    "scraper.downloadmiddlewares.UserAgentMiddleware": 100,
}

ITEM_PIPELINES = {
    "scraper.pipelines.SendKafkaPipeline": 300,  # 发送到 kafka
}


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = logging.getLevelName(get_settings("scrapy.log.LOG_LEVEL", "INFO"))

LOG_FILE = get_settings("scrapy.log.LOG_FILE", None)

# size / time
LOG_FILE_TYPE = get_settings("scrapy.log.LOG_FILE_TYPE", "time")

# 最大保留个数
LOG_FILE_BACKUP_COUNT = get_settings("scrapy.log.LOG_FILE_BACKUP_COUNT", 10)

# 最大文件大小，当 ``LOG_FILE_TYPE`` 设置为 size 生效
LOG_FILE_MAX_BYTES = get_settings("scrapy.log.LOG_FILE_MAX_BYTES", 1024 * 1024 * 10)

# 生成文件间隔，单位为 ``LOG_FILE_ROTATION``，当 ``LOG_FILE_TYPE`` 设置为 time 生效
LOG_FILE_INTERVAL = get_settings("scrapy.log.LOG_FILE_INTERVAL", 1)

# 日志文件生成间隔单位：second / minute / hour / day /
LOG_FILE_ROTATION_UNIT = get_settings("scrapy.log.LOG_FILE_ROTATION_UNIT", "hour")

# 自动调节
AUTOTHROTTLE_ENABLED = get_settings("scrapy.settings.AUTOTHROTTLE_ENABLED", False)

# 下载延迟
AUTOTHROTTLE_START_DELAY = get_settings("scrapy.settings.AUTOTHROTTLE_START_DELAY", 5)

# 最大延迟
AUTOTHROTTLE_MAX_DELAY = get_settings("scrapy.settings.AUTOTHROTTLE_MAX_DELAY", 60)

REDIRECT_ENABLED = get_settings("scrapy.settings.REDIRECT_ENABLED", True)