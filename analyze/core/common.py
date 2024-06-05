import jieba
from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as fn
from pyspark.sql.types import ArrayType, StringType

with open("./core/hit_stopwords.txt", mode="r", encoding="utf-8") as f:
    stopwords = f.read().split("\n")


"""
前端查询某个时间段的排行榜
1. 通过 rowKey 查找到最近的时间点，然后拿到整个排行榜
2. 点击某个热搜，然后查询该热搜词条的相关信息
"""


def _common_trending_analyze(df: DataFrame) -> DataFrame:
    """
    通用 item 的趋势数据，只有 rank 和 hot_num 基本信息
    :param df:
    :return:

    +------+---------------+-------------+--------+--------+--------+
    |title |start_timestamp|end_timestamp|duration|summary |trending|
    +------+---------------+-------------+--------+--------+--------+
    """
    trending_df = (
        df.groupby("title")
        .agg(
            fn.array_distinct(
                fn.collect_list(fn.struct("rank", "hot_num", "timestamp"))
            ).alias("trending")
        )
        .select(
            "title",
            "trending",
        )
    )

    result_df = trending_df.join(_common_analyze(df), "title")

    return result_df


def _common_analyze(df: DataFrame) -> DataFrame:
    """
    通用分析
    :param df:
    :return:
    """

    result_df = df.groupby("title").agg(
        fn.min("timestamp").alias("start_timestamp"),
        fn.max("timestamp").alias("end_timestamp"),
        fn.max("hot_num").alias("max_hot_num"),
        fn.min("hot_num").alias("min_hot_num"),
        fn.avg("hot_num").alias("avg_hot_num"),
        fn.max("rank").alias("max_rank"),
        fn.min("rank").alias("min_rank"),
    )

    return result_df


@fn.udf(returnType=ArrayType(StringType()))
def jieba_cut(text):
    """
    jieba分词
    :param text:
    :return:
    """
    words = jieba.lcut(text)
    filter_words = [word for word in words if word not in stopwords and len(word) > 1]
    return filter_words


def word_segment_analyze(df: DataFrame) -> DataFrame:
    """
    分词分析
    :param df:
    :return:
    """
    result_df = (
        df
        .withColumn("words", jieba_cut("title"))
        .select("words", "timestamp", "hot_num")
        .withColumn("word", fn.explode("words"))
        .select("word", "timestamp", "hot_num")
        .groupby("timestamp")
        .agg(
            fn.collect_list(fn.struct("word", "hot_num")).alias("words")
        ).select("timestamp", "words")
    )
    return result_df
