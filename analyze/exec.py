import os

from pyspark.sql import Row

from analyze.sinks.scraped import ScrapedForeachWriter
from config.config import get_settings

if home := get_settings("spark.home"):
    os.environ["SPARK_HOME"] = home
    os.environ["HADOOP_HOME"] = get_settings("spark.hadoop_home")
    os.environ["PYSPARK_PYTHON"] = "python"

from pyspark.sql import DataFrame
from analyze import schemas
from constants.scrapy import ApiType
from utils.spark_utils import SparkUtils
from pyspark.sql import functions as func
from analyze import core
from utils import redis_tools


def get_kafka_source():
    """
    读取配置拿到 streaming
    """
    host = get_settings("kafka.host")
    port = get_settings("kafka.port")
    kafka_server = f"{host}:{port}"
    topic = get_settings("spark.kafka.topic")
    session = SparkUtils.get_spark_sql_session("analyse", log_level="ERROR")
    return SparkUtils.get_kafka_source(
        session,
        kafka_server,
        topics=[topic],
        starting_offsets="earliest"
        # starting_offsets=redis_tools.get_kafka_offset(topic),
    ).load()


def save_kafka_offset(row: Row):
    offset = row["offset"]
    topic = row["topic"]
    redis_tools.update_kafka_offset(topic, offset)


def transform_to_json(df: DataFrame) -> DataFrame:
    """
    将数据转换为json
    """
    # df.foreach(save_kafka_offset)
    return (
        df.selectExpr("CAST(value AS STRING)")
        .withColumn(
            "json",
            func.from_json("value", schema=schemas.HotSearchItemSchema),
        )
        .select("json.*")  # api_type data timestamp
    )


def filter_by_api_type(df: DataFrame, api_type: int, schema) -> DataFrame:
    """
    根据 api_type 过滤，并转换为 json
    """
    return (
        df.filter(func.col("api_type") == api_type)
        .drop("api_type")  # data timestamp
        .withColumn("json", func.explode("data"))  # data json timestamp
        .withColumn(
            "data", func.from_json("json", schema=schema)
        )  # data json timestamp
        .select("data.*", "timestamp")  # data.* timestamp
    )


def dispatcher(df: DataFrame):
    # 元数据写入 hbase
    df.foreach(ScrapedForeachWriter().process_row)

    # 微博热搜榜
    core.analyze_wei_hot_df(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.WeiBoHotSearch.value,
            schema=schemas.WeiBoHotSearchItemSchema,
        )
    )

    # 百度热搜
    core.analyze_baidu_df(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.Baidu.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )

    # 知乎热搜
    core.analyze_zhihu_df(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.Zhihu.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )

    # 澎湃热搜
    core.analyze_peng_pai_df(
        df=filter_by_api_type(
            df=source,
            api_type=ApiType.PengPai.value,
            schema=schemas.PengpaiHotSearchItemSchema,
        )
    )

    # 今日头条热搜
    core.analyze_tou_tiao(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.TouTiao.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )

    # 搜狗
    core.analyze_sougou(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.Sougou.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )

    # 抖音
    core.analyze_douyin(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.Douyin.value,
            schema=schemas.DouyinHotSearchItemSchema,
        )
    )

    # bilibili
    core.analyze_bilibili(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.Bilibili.value,
            schema=schemas.CommonHotSearchNoValueItemSchema,
        )
    )

    # 快手
    core.analyze_kuaishou(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.KuaiShou.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )

    # 腾讯新闻
    core.analyze_tencent_news(
        df=filter_by_api_type(
            df=df,
            api_type=ApiType.TencentNews.value,
            schema=schemas.CommonHotSearchItemSchema,
        )
    )


def start_spark():
    source = transform_to_json(get_kafka_source())
    dispatcher(source)


if __name__ == "__main__":
    start_spark()
