from typing import Union

import happybase
from config.config import get_settings

from threading import Lock

_lock = Lock()

with _lock:
    _conn = happybase.Connection(
        host=get_settings("hbase.host"),
        port=get_settings("hbase.port"),
        autoconnect=False,
    )
    _conn.open()


def __conn() -> happybase.Connection:
    global _conn
    if not _conn.transport.is_open():
        with _lock:
            _conn = happybase.Connection(
                host=get_settings("hbase.host"),
                port=get_settings("hbase.port"),
                autoconnect=False,
            )
            _conn.open()
    return _conn


def create_table(
        table_name: str,
        column_family: Union[dict[str, dict], list[str]],
        cover: bool = False,
):
    """
    创建表
    :param cover:
    :param table_name:
    :param column_family: {cf: 配置dict}
    :return:
    """
    if isinstance(column_family, list):
        column_family = {cf: {} for cf in column_family}

    if table_name.encode("utf-8") not in __conn().tables():
        __conn().create_table(table_name, column_family)
    else:
        if cover:
            __conn().delete_table(table_name, disable=True)
            __conn().create_table(table_name, column_family)


def delete_table(table_name: str):
    """
    删除表
    :param table_name:
    :return:
    """
    if table_name in __conn().tables():
        __conn().delete_table(table_name, disable=True)


def put(table_name: str, row_key: str, data: dict):
    """
    插入数据
    :param data:
    :param table_name:
    :param row_key:
    :return:
    """
    table = __conn().table(table_name)
    table.put(row=row_key, data=data)


def get_table(table_name: str) -> happybase.Table:
    return __conn().table(table_name)


if __name__ == "__main__":
    print(__conn().tables())
