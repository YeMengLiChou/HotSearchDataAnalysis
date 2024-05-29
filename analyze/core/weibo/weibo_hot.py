from pyspark.sql import DataFrame
from pyspark.sql import functions as fn
from analyze import schemas


def parse(df: DataFrame) -> DataFrame:
    """"
    保证 ``df`` 的 ``api_type`` 字段为
    """
    df = df.withColumn(
        "json", fn.from_json("data", schema=schemas.HotSearchItemSchema)
    ).select("json", "timestamp")
