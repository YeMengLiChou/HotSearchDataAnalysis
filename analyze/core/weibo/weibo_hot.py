from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as fn

from analyze.core.common import jieba_cut
from analyze.sinks.console import batch_to_console

"""
1. 上榜持续时间 max(timestamp - onboard_time)
2. 这段时间的排名+热度变化 -> rank hot timestamp
3. 某个分类上的热搜 -> category note
4. 明星上榜次数 -> star

"""


def analyze(df: DataFrame) -> DataFrame:
    """ "
    保证 ``df`` 的 ``api_type`` 字段为 ApiType.WeiboHot

    ``df`` 格式:
    +----+----+---------+-------+---+------------+---------+------+------+------+---------+
    |rank|note|category |raw_hot|num|onboard_time|star_name|is_new|is_hot|is_gov|timestamp|
    +----+----+---------+-------+---+------------+---------+------+------+------+---------+

    """
    # TODO 源数据写入 hbase

    # df.select("")

    word_segment_analyze(df)
    return

    window_spec = Window.partitionBy("note").orderBy("timestamp")

    #  变化趋势
    trending_df = (
        df.withColumn("max_timestamp", fn.max("timestamp").over(window_spec))
        .withColumn(
            "duration",
            fn.col("max_timestamp") - fn.col("onboard_time"),
        )
        .groupby("note")
        .agg(
            fn.array_distinct(
                fn.collect_list(
                    fn.struct(
                        "timestamp", "rank", "raw_hot", fn.col("num").alias("hot_num")
                    )
                )
            ).alias(
                "trending"
            ),  # 将处理的结果收集为一个列表
        )
        .select("note", "trending")
    )

    data_df = (
        df.groupby("note", "category")
        .agg(
            fn.min("onboard_time").alias("start_timestamp"),
            fn.max("timestamp").alias("end_timestamp"),
            fn.max("num").alias("max_hot_num"),
            fn.min("num").alias("min_hot_num"),
            fn.max("rank").alias("max_rank"),
            fn.min("rank").alias("min_rank"),
            fn.max("raw_hot").alias("max_raw_hot"),
            fn.min("raw_hot").alias("min_raw_hot"),
        )
        .select(
            "note",
            "category",
            "start_timestamp",
            "end_timestamp",
            "max_hot_num",
            "min_hot_num",
            "max_raw_hot",
            "min_raw_hot",
            "max_rank",
            "min_rank",
        )
    )

    result_df = data_df.join(trending_df, "note")
    batch_to_console(
        result_df,
    )
    """
    result_df 格式
    +----+---------+---------------+-------------+-----------+-----------+-----------+-----------+--------+--------+---------+
    |note|category |start_timestamp|end_timestamp|max_hot_num|min_hot_num|max_raw_hot|min_raw_hot|max_rank|min_rank|trending |
    +----+---------+---------------+-------------+-----------+-----------+-----------+-----------+--------+--------+---------+
    """

    return result_df


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
        df.withColumn("note", fn.regexp_replace("note", r"[^\u4e00-\u9fa5]", ""))
        .withColumn("words", jieba_cut("note"))
        .withColumn("words", fn.explode("words"))
        .select("timestamp", "words", "rank", "num", "raw_hot")
        .orderBy("raw_hot")
    )
    batch_to_console(df, row=100)
