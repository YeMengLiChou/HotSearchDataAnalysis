from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from pyspark.sql.streaming import StreamingQuery, DataStreamReader
from pyspark.sql import DataFrameReader


class SparkUtils:

    @staticmethod
    def get_spark_sql_session(app_name: str, log_level: str = "WARN") -> SparkSession:
        """
        返回 SparkSession
        """
        session = (
            SparkSession.builder.appName(app_name)
            .config(
                "spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0",
            )  # 配置所需要的依赖包
            # .config('spark.sql.streaming.statefulOperator.checkCorrectness.enabled', False)
            # .config("spark.streaming.kafka.maxRatePerPartition", 3000)  # 每个进程每秒最多从kafka读取的数据条数
            .config(
                "spark.streaming.kafka.consumer.cache.enabled", False
            )  # 禁用UninterruptibleThread
            .master("local[*]")
            .getOrCreate()
        )
        session.sparkContext.setLogLevel(log_level)
        return session

    @staticmethod
    def get_kafka_streaming(
        session: SparkSession,
        kafka_server: str,
        topics: list[str],
        starting_offsets: str | list[str] = "earliest",
    ) -> DataStreamReader:
        """
        获取 kafka 的 streaming

        :param starting_offsets: 开始读取的偏移量
        :param session
        :param kafka_server
        :param topics
        :return 返回对应的 ``DataStreamReader``
        """
        topic = ".".join(topics)
        if isinstance(starting_offsets, list):
            starting_offsets = str(
                {topics[i]: str(starting_offsets[i]) for i in range(len(topics))}
            )
        kafka_options = {
            "kafka.bootstrap.servers": kafka_server,
            "subscribe": topic,
            "startingOffsets": starting_offsets,
            "endingOffsets": "latest",
        }
        return session.readStream.format("kafka").options(**kafka_options)

    @staticmethod
    def get_kafka_source(
        session: SparkSession,
        kafka_server: str,
        topics: list[str],
        starting_offsets: str | list[str] = "earliest",
    ) -> DataFrameReader:
        """
        获取 kafka 的数据源，不是 Streaming

        :param starting_offsets:
        :param session
        :param kafka_server
        :param topics
        :return 返回对应的 ``DataStreamReader``
        """
        topic = ".".join(topics)
        if isinstance(starting_offsets, list):
            starting_offsets = str(
                {topics[i]: str(starting_offsets[i]) for i in range(len(topics))}
            )
        return (
            session.read.format("kafka")
            .option("kafka.bootstrap.servers", kafka_server)
            .option("subscribe", topic)
            .option("startingOffsets", starting_offsets)
        )

    @staticmethod
    def send_to_kafka(
        df: DataFrame,
        topic_name: str,
        _id: str,
        kafka_server: str,
        output_mode: str = "append",
    ) -> StreamingQuery:
        """
        将数据发送到kafka指定的主题中

        :param df:
        :param topic_name:  发送的主题
        :param _id：
        :param kafka_server: 发送的kafka服务器
        :param output_mode: 输出模式
        :return:
        """
        return (
            df.select(to_json(struct("*")).alias("value"))
            .writeStream.outputMode(output_mode)  # 有新数据则发送
            .format("kafka")
            .option("kafka.bootstrap.servers", kafka_server)
            .option("topic", f"{topic_name}")
            .option("checkpointLocation", f"logs/checkpoints/{topic_name}/{_id}")
            .start()
        )
