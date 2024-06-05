import json

import happybase
from pyspark.sql import Row
from analyze.sinks.foreach import ForeachWriter
from utils import hbase_utils


class TrendingDataForeachWriter(ForeachWriter):
    """
    爬取源数据写入
    """

    def __reduce__(self):
        return self.__class__, (self.api_type,)

    def __init__(self, api_type: int):
        self.api_type = api_type
        hbase_utils.create_table(
            table_name="hot_search_trend", column_family={"analyze": {}, "trending": {}}
        )
        self.batch: happybase.Batch = hbase_utils.get_table("hot_search_trend").batch(
            batch_size=10000
        )

    def open(self, partition_id: int, epoch_id: int) -> bool:
        return True

    def process_row(self, row: Row):
        """
        rowKey设计：时间戳 apiType:title:start_timestamp,
        column family
        :param row:
        :return:
        """
        row_key = f"{self.api_type}:{row.title}:{row.start_timestamp}"
        self.batch.put(
            row=row_key,
            data={
                "analyze:start_timestamp": str(row.start_timestamp),
                "analyze:end_timestamp": str(row.end_timestamp),
                "analyze:max_hot_num": str(row.max_hot_num),
                "analyze:avg_hot_num": str(row.avg_hot_num),
                "analyze:min_hot_num": str(row.min_hot_num),
                "analyze:max_rank": str(row.max_rank),
                "analyze:min _rank": str(row.min_rank),
                "trending:list": json.dumps(row.trending, ensure_ascii=False),
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
