import json

import happybase
from pyspark.sql import Row

from analyze.sinks.foreach import ForeachWriter
from utils import hbase_utils


class WordCutForeachWriter(ForeachWriter):
    """
    分词写入

    """

    def __reduce__(self):
        return self.__class__, (self.api_type,)

    def __init__(self, api_type: int):
        self.api_type = api_type
        hbase_utils.create_table(
            table_name="hot_search_word", column_family={"word": {}}
        )
        self.batch: happybase.Batch = hbase_utils.get_table("hot_search_word").batch(
            batch_size=10000
        )

    def open(self, partition_id: int, epoch_id: int) -> bool:
        return True

    def process_row(self, row: Row):
        """
        rowKey设计：时间戳+apiType
        :param row:
        :return:
        """
        row_key = f"{self.api_type}:{row.timestamp}"
        self.batch.put(
            row_key,
            {
                "word:words": json.dumps(row.asDict(recursive=True)["words"], ensure_ascii=False),
                "word:timestamp": str(row.timestamp),
            },
        )

    def close(self, error):
        if self.batch:
            self.batch.send()
            self.batch = None

    def __del__(self):
        if self.batch:
            self.batch.send()
            self.batch = None
