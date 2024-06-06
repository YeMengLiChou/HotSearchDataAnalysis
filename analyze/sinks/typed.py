import json

import happybase
from pyspark.sql import Row
from analyze.sinks.foreach import ForeachWriter
from utils import hbase_utils


class WeiBoCategoryDataForeachWriter(ForeachWriter):
    """
    微博的类别数据写入
    """

    def __reduce__(self):
        return self.__class__, ()

    def __init__(self):
        hbase_utils.create_table(
            table_name="hot_search_weibo_category",
            column_family={"data": {}, "analyze": {}},
        )
        self.batch: happybase.Batch = hbase_utils.get_table(
            "hot_search_weibo_category"
        ).batch(batch_size=10000)

    def open(self, partition_id: int, epoch_id: int) -> bool:
        return True

    def process_row(self, row: Row):
        """
        rowKey设计：时间戳 apiType:title:start_timestamp,
        column family
        :param row:
        :return:
        """
        row_key = f"{row.timestamp}:{row.category}"
        self.batch.put(
            row=row_key,
            data={
                "data:category": row.category,
                "data:timestamp": str(row.timestamp),
                "analyze:list": json.dumps(row.values),
                "analyze:count": str(row.count),
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
