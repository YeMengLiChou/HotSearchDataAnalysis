from pyspark.sql import DataFrame

from analyze.core.common import _common_trending_analyze, word_segment_analyze
from analyze.sinks.console import batch_to_console
from analyze.sinks.trending import TrendingDataForeachWriter
from analyze.sinks.wordcut import WordCutForeachWriter
from constants.scrapy import ApiType

__trending_sink = TrendingDataForeachWriter(api_type=ApiType.Zhihu.value)
__word_cut_sink = WordCutForeachWriter(api_type=ApiType.Zhihu.value)


def analyze(df: DataFrame):
    """
    知乎热搜分析
    """
    result_df = _common_trending_analyze(df)
    result_df.foreach(__trending_sink.process_row)
    batch_to_console(result_df, row=10)

    word_df = word_segment_analyze(df)
    word_df.foreach(__word_cut_sink.process_row)
    batch_to_console(word_df, row=10)
