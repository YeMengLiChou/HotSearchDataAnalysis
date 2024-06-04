from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as fn
from analyze import schemas
from analyze.sinks.console import batch_to_console
from analyze.core.common import _common_trending_analyze


def analyze(df: DataFrame) -> DataFrame:
    """
    百度热搜分析
    +----+------+--------+-------+----------+
    |rank|title |summary |hot_num|timestamp |
    +----+------+--------+-------+----------+

    """

    # batch_to_console(_common_trending_analyze(df), row=100)
    pass