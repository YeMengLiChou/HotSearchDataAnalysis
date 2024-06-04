import happybase
from pyspark.sql import Row
from analyze.sinks.foreach import ForeachWriter
from utils import hbase_utils


class TrendingDataForeachWriter(ForeachWriter):
    """
    爬取源数据写入
    """

    def __init__(self):
        hbase_utils.create_table("trend", {"data": {}})
        self.batch: happybase.Batch | None = None

    def open(self, partition_id: int, epoch_id: int) -> bool:
        self.batch = hbase_utils.get_table("trend").batch(batch_size=1000)
        return True

    def process_row(self, row: Row):
        """
        rowKey设计：时间戳+apiType,
        column family
        :param row:
        :return:
        """
        # row_key = f"{}"
        # row_key = str(row.timestamp) + ":" + str(row.api_type) + ":"
        # self.batch.put(row=row_key, data={"data:trend": str(row.asDict())})
        pass

    def close(self, error):
        if self.batch:
            self.batch.send()
            self.batch = None
