from flask import Flask
from flask import request

from backend.dto.result import ApiResult
from constants.scrapy import ApiType
from utils import hbase_utils

app = Flask(__name__)


@app.get("/hot/")
def get_hot_data():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{start_time}:{ApiType.Baidu.value}", columns=["items:data"]):
        data.append(cell)
    return ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__
