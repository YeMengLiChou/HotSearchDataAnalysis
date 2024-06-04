import happybase
from pyspark.sql import Row

from analyze.sinks.foreach import ForeachWriter


class WordCutForeachWriter(ForeachWriter):
    """
    分词写入

    """

    def __init__(self):
        self.batch: happybase.Batch | None = None

    def open(self, partition_id: int, epoch_id: int) -> bool:
        return True

    def process_row(self, row: Row):
        """
        rowKey设计：时间戳+apiType
        :param row:
        :return:
        """

    def close(self, error):
        pass
