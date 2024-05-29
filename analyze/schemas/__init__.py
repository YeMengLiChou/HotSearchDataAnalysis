from pyspark.sql.types import *


HotSearchItemSchema = StructType(
    [
        StructField("api_type", IntegerType(), False),
        StructField("data", ArrayType(StringType()), False),
        StructField("timestamp", LongType(), True),
    ]
)


CommonHotSearchItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("title", StringType(), False),
        StructField("summary", StringType(), False),
        StructField("hot_num", LongType(), False),
    ]
)

CommonHotSearchNoValueItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("title", StringType(), False),
    ]
)

DouyinHotSearchItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("word", StringType(), False),
        StructField("hot_num", LongType(), False),
        StructField("event_timestamp", LongType(), False),
    ]
)

PengpaiHotSearchItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("title", StringType(), False),
        StructField("publish_timestamp", LongType(), False),
        StructField("tags", ArrayType(StringType()), False),
        StructField("praise_nums", LongType(), False),
        StructField("comment_nums", LongType(), False),
        StructField("node", StringType(), False),
    ]
)


TencentNewsHotSearchItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("title", StringType(), False),
        StructField("publish_timestamp", LongType(), False),
        StructField("source", StringType(), False),
        StructField("hot_num", LongType(), False),
        StructField("comment_nums", LongType(), False),
        StructField("read_nums", LongType(), False),
        StructField("summary", StringType(), False),
    ]
)


WeiBoHotSearchItemSchema = StructType(
    [
        StructField("rank", IntegerType(), False),
        StructField("note", StringType(), False),
        StructField("category", ArrayType(StringType()), False),
        StructField("raw_hot", LongType(), False),
        StructField("num", LongType(), False),
        StructField("onboard_time", LongType(), False),
        StructField("star_name", ArrayType(StringType()), False),
        StructField("is_new", IntegerType(), False),
        StructField("is_hot", IntegerType(), False),
        StructField("is_gov", IntegerType(), False),
    ]
)

WeiboEntertainmentItemSchema = StructType(
    [
        StructField("grade", StringType(), False),
        StructField("note", StringType(), False),
        StructField("onboard_time", LongType(), False),
        StructField("circle_hot", LongType(), False),
        StructField("hot_num", LongType(), False),
        StructField("category", ArrayType(StringType()), False),
        StructField("star_name", ArrayType(StringType()), False),
        StructField("rank", IntegerType(), False),
        StructField("is_new", IntegerType(), False),
        StructField("is_hot", IntegerType(), False),
    ]
)


WeiboNewsItemSchema = StructType(
    [
        StructField("summary", StringType(), False),
        StructField("topic", StringType(), False),
        StructField("rank", IntegerType(), False),
        StructField("mention", IntegerType(), False),
        StructField("read", IntegerType(), False),
        StructField("claim", StringType(), False),
        StructField("category", ArrayType(StringType()), False),
    ]
)
