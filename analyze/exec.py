from pyspark.sql import DataFrame

from analyze import schemas
from config.config import get_settings
from constants.scrapy import ApiType
from utils.spark_utils import SparkUtils
from pyspark.sql import functions as func


def get_kafka_source():
    """
    读取配置拿到 streaming
    """
    host = get_settings("kafka.host")
    port = get_settings("kafka.port")
    kafka_server = f"{host}:{port}"
    topic = get_settings("kafka.spark.topic", None)
    session = SparkUtils.get_spark_sql_session("analyse")
    return SparkUtils.get_kafka_source(session, kafka_server, topics=[topic]).load()


def transform_to_json(df: DataFrame) -> DataFrame:
    """
    将数据转换为json
    """
    return (
        df.selectExpr("CAST(value AS STRING)")
        .withColumn(
            "json",
            col=func.from_json("value", schema=schemas.HotSearchItemSchema),
        )
        .select(func.col("json"))
    )


def dispatcher(df: DataFrame):
    weibo_hot_df = df.filter(func.col("json.api_type") == ApiType.WeiBoHotSearch.value)

    # weibo_entertainment_df = df.filter(
    #     func.col("json.api_type") == ApiType.WeiBoEntertainment.value
    # )
    # weibo_news_df = df.filter(func.col("json.api_type") == ApiType.WeiBoNews.value)
    # baidu_hot_df = df.filter(func.col("json.api_type") == ApiType.Baidu.value)




