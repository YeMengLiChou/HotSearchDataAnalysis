from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as fn

from analyze.core.common import jieba_cut
from analyze.sinks.console import batch_to_console
from analyze.sinks.trending import TrendingDataForeachWriter
from analyze.sinks.wordcut import WordCutForeachWriter
from analyze.sinks.typed import WeiBoCategoryDataForeachWriter
from constants.scrapy import ApiType


__trending_sink = TrendingDataForeachWriter(api_type=ApiType.WeiBoHotSearch.value)
__word_sink = WordCutForeachWriter(api_type=ApiType.WeiBoHotSearch.value)
__category_sink = WeiBoCategoryDataForeachWriter()


def analyze(df: DataFrame):
    """ "
    保证 ``df`` 的 ``api_type`` 字段为 ApiType.WeiboHot

    ``df`` 格式:
    +----+----+---------+-------+---+------------+---------+------+------+------+---------+
    |rank|note|category |raw_hot|num|onboard_time|star_name|is_new|is_hot|is_gov|timestamp|
    +----+----+---------+-------+---+------------+---------+------+------+------+---------+

    """

    window_spec = Window.partitionBy("note").orderBy("timestamp")

    #  变化趋势
    trending_df = (
        df.withColumn("max_timestamp", fn.max("timestamp").over(window_spec))
        .groupby("note")
        .agg(
            fn.array_distinct(
                fn.collect_list(
                    fn.struct("timestamp", "rank", fn.col("num").alias("hot_num"))
                )
            ).alias(
                "trending"
            ),  # 将处理的结果收集为一个列表
        )
        .select("note", "trending")
    )

    data_df = (
        df.groupby("note")
        .agg(
            fn.min("onboard_time").alias("start_timestamp"),
            fn.max("timestamp").alias("end_timestamp"),
            fn.max("num").alias("max_hot_num"),
            fn.min("num").alias("min_hot_num"),
            fn.avg("num").alias("avg_hot_num"),
            fn.max("rank").alias("max_rank"),
            fn.min("rank").alias("min_rank"),
        )
        .select(
            "note",
            "start_timestamp",
            "end_timestamp",
            "max_hot_num",
            "avg_hot_num",
            "min_hot_num",
            "max_rank",
            "min_rank",
        )
    )

    result_df = data_df.join(trending_df, "note").withColumnRenamed("note", "title")
    result_df.foreach(__trending_sink.process_row)
    batch_to_console(result_df)

    word_df = word_segment_analyze(df)
    word_df.foreach(__word_sink.process_row)
    batch_to_console(word_df)

    typed_df = analyze_type(df)

    typed_df.foreach(__category_sink.process_row)
    batch_to_console(typed_df, row=100)


"""
词频统计：
1. 给某个时间段，需要统计该时间段上的所有词
2. 分词后，需要将词与时间戳关联起来，
3. 查询时就是时间段内的所有词统计出次数
"""


def word_segment_analyze(df: DataFrame):
    """
    分词
    :param df:
    :return:
    """
    df = (
        df.withColumnRenamed(existing="note", new="title")
        .withColumn("words", jieba_cut("title"))
        .withColumn("word", fn.explode("words"))
        .select("timestamp", "word", fn.col("num").alias("hot_num"))
        .groupby("timestamp")
        .agg(
            fn.array_distinct(fn.collect_list(fn.struct("word", "hot_num"))).alias(
                "words"
            ),
        )
        .select("words", "timestamp")
    )
    return df


def analyze_type(df: DataFrame) -> DataFrame:
    """
    分析类别,
    :param df:
    :return:
    """
    result_df = (
        df.withColumnRenamed(existing="num", new="hot_num")
        .withColumn("category", fn.explode("category"))
        .groupby("category", "timestamp")
        .agg(fn.collect_list(fn.struct("hot_num", "rank")).alias("values"))
        .select(
            "category", "timestamp", "values", fn.array_size("values").alias("count")
        )
    )
    return result_df
