from config.config import get_settings
from scraper.run import start


def __start_scrape():
    """
    启动爬虫
    :return:
    """
    spider_name = get_settings("scrapy.spider_name")
    settings_path = get_settings("scrapy.settings_path")
    if not spider_name or not isinstance(spider_name, str):
        raise ValueError("`scrapy.spider_name` must not be None and must be str")

    if not settings_path or not isinstance(settings_path, str):
        raise ValueError("`scrapy.module_path` must not be None and must be str")

    start(spider_name=spider_name, settings_path=settings_path)


if __name__ == "__main__":
    # TODO: 定时运行
    if not (interval := get_settings("scrapy.scrapy_start_interval")) or not isinstance(
        interval, int
    ):
        raise ValueError(
            "`scrapy.scrapy_start_interval` must not be None and must be int"
        )

    pass
