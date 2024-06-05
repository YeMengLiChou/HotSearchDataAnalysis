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

    if table_name.encode("utf-8") not in _conn.tables():
        _conn.create_table(table_name, column_family)
    else:
        if cover:
            _conn.delete_table(table_name, disable=True)
            _conn.create_table(table_name, column_family)


def delete_table(table_name: str):
    """
    删除表
    :param table_name:
    :return:
    """
    if table_name in _conn.tables():
        _conn.delete_table(table_name, disable=True)


def put(table_name: str, row_key: str, data: dict):
    """
    插入数据
    :param data:
    :param table_name:
    :param row_key:
    :return:
    """
    table = _conn.table(table_name)
    table.put(row=row_key, data=data)


def get_table(table_name: str) -> happybase.Table:
    return _conn.table(table_name)


if __name__ == "__main__":
    print(_conn.tables())
    # _conn.create_table("test1", {"cf1": {}, "cf2": {}})
    # # create_table("test", ["cf1", "cf2"])
    # put(
    #     "test1",
    #     "123",
    #     {"cf1:a": "haha"}
    # )
    # # put(
    # #     "scraped",
    # #     "1716657002576:4",
    # #     {"items:data": "{'api_type': 4, 'data': [], 'timestamp': 1716657002576}"},
    # # )
    # # print(_conn.table("test").families())
    # table = _conn.table("test1")
    # for item in table.scan():
    #     print(item)
