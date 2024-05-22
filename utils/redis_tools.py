import datetime
import logging
import threading
from typing import Union
from config.config import settings
import redis
from redis import Redis

logger = logging.getLogger(__name__)

_client: Union[Redis, None] = None

_lock = threading.Lock()

if not _client:
    with _lock:
        if not _client:
            _client = redis.Redis(
                host=getattr(settings, "redis.host", "localhost"),
                port=getattr(settings, "redis.port", 6379),
                db=getattr(settings, "redis.db", 0),
                decode_responses=True,
            )

# ========================== KEY CONSTANTS ========================= #
KEY_API_RECORD_PREFIX = "hot_search:api"


# ======================== TOOLS FUNCTIONS ========================= #


def _get_api_count_key(api_type: str) -> str:
    return f"{KEY_API_RECORD_PREFIX}:count:{api_type}"


def _get_api_time_key(api_type: str) -> str:
    return f"{KEY_API_RECORD_PREFIX}:time:{api_type}"


def update_api_scraped(api_type: str, timestamp: int):
    _client.incrby(_get_api_count_key(api_type), 1)
    _client.set(_get_api_time_key(api_type), timestamp)


def parse_timestamp(timestamp: int) -> str:
    """
    将毫秒级时间戳解析为 YY-MM-DD 格式
    :param timestamp: 毫秒级时间戳
    :return: 格式化的字符串
    """
    time = datetime.datetime.fromtimestamp(timestamp / 1000)
    # 时间转换为字符串到每秒
    return time.strftime("%Y-%m-%d:%H:%M:%S")


def get_api_information(api_type: str) -> dict:
    """
    获取 API 类型的统计信息
    :param api_type: API 类型
    :return: 统计信息
    """
    count = int(_client.get(_get_api_count_key(api_type)) or "0")
    time = int(_client.get(_get_api_time_key(api_type)) or "0")
    return {
        "count": count,
        "time": parse_timestamp(time),
    }
