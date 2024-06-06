from flask import Flask, jsonify
from flask import request

from backend.dto.result import ApiResult
from constants.scrapy import ApiType
from utils import hbase_utils
import json

app = Flask(__name__)


def decode_dict(value: dict[bytes, bytes]) -> dict:
    result = dict()
    for key, value in value.items():
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        if isinstance(value, dict):
            value = decode_dict(value)
        result[key.decode('utf-8')] = value
    return result


@app.get("/hot/<int:api_type>")
def get_hot_data(api_type):
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    try:
        # 尝试将api_type转换为枚举类型
        api_enum = ApiType(api_type)
    except ValueError:
        # 如果转换失败，则返回一个包含错误信息的ApiResult对象
        response_data = ApiResult(
            code=200,
            msg=f"不存在该类型的热搜: {api_type}",
            data=None
        ).__dict__

        # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=200,
            mimetype='application/json'
        )

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{api_enum.value}:{start_time}",
                           row_stop=f"{api_enum.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]
        # 获取rowkey中的时间
        # item['time'] = row_key.split(":")[1]
        # item['data'] = item_data
        item['data'] = item_data
        app.logger.info(f"{item}")

        data.append(item)

    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 百度热搜
@app.get("/hot/baidu")
def get_hot_baidu():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.Baidu.value}:{start_time}",
                           row_stop=f"{ApiType.Baidu.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构, 把获取到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前15条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:16]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d["hot_num"],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": ApiType.Baidu.value,  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 微博热搜
@app.get("/hot/weibo")
def get_hot_weibo():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.WeiBoHotSearch.value}:{start_time}",
                           row_stop=f"{ApiType.WeiBoHotSearch.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:16]:
            transformed_data.append({
                "title": d["note"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d["num"],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 微博要闻热搜
@app.get("/hot/weibo-news")
def get_hot_weibo_news():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.WeiBoNews.value}:{start_time}",
                           row_stop=f"{ApiType.WeiBoNews.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["topic"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d["read"],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 微博娱乐热搜
@app.get("/hot/weibo-entertainment")
def get_hot_weibo_entertainment():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.WeiBoEntertainment.value}:{start_time}",
                           row_stop=f"{ApiType.WeiBoEntertainment.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["note"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d["hot_num"],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 知乎热搜
@app.get("/hot/zhihu")
def get_hot_zhihu():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.Zhihu.value}:{start_time}",
                           row_stop=f"{ApiType.Zhihu.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d["hot_num"],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 澎湃新闻热搜
@app.get("/hot/pengpai")
def get_hot_pengpai():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.PengPai.value}:{start_time}",
                           row_stop=f"{ApiType.PengPai.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": '',
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 头条热搜
@app.get("/hot/toutiao")
def get_hot_toutiao():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.TouTiao.value}:{start_time}",
                           row_stop=f"{ApiType.TouTiao.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d['hot_num'],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 搜狗热搜
@app.get("/hot/sougou")
def get_hot_sougou():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.Sougou.value}:{start_time}",
                           row_stop=f"{ApiType.Sougou.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d['hot_num'],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 抖音热搜
@app.get("/hot/douyin")
def get_hot_douyin():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.Douyin.value}:{start_time}",
                           row_stop=f"{ApiType.Douyin.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["word"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d['hot_num'],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# Bilibili热搜
@app.get("/hot/bilibili")
def get_hot_bilibili():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.Bilibili.value}:{start_time}",
                           row_stop=f"{ApiType.Bilibili.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:15]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": '',
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 快手热搜
@app.get("/hot/kuaishou")
def get_hot_kuaishou():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.KuaiShou.value}:{start_time}",
                           row_stop=f"{ApiType.KuaiShou.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:16]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d['hot_num'],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


# 腾讯热搜
@app.get("/hot/tencent")
def get_hot_tencent():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    # 从hbase读取
    table = hbase_utils.get_table("scraped")
    data = []
    for cell in table.scan(row_start=f"{ApiType.TencentNews.value}:{start_time}",
                           row_stop=f"{ApiType.TencentNews.value}:{end_time}",
                           columns=["items:data"]):
        row_key = cell[0].decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell[1])

        # 将字符串形式的JSON数据转换为Python对象
        # 解析row_data中特定字段的JSON字符串，移除单引号以兼容JSON格式
        item = json.loads(row_data["items:data"].replace("'", ""))

        # 将item中'data'字段的每个字符串元素转换为Python对象
        # 通过列表推导式对item['data']中的每个JSON字符串进行解析
        item_data = [json.loads(x) for x in item['data']]

        # 重新构造每个条目的数据结构,把得到的数据 转为前端所需要的格式
        transformed_data = []
        # 在前11条信息中提取数据 转为前端所需要的格式,返回前11条是因为,对于百度的接口来说,第一条数据是置顶的
        for d in item_data[:16]:
            transformed_data.append({
                "title": d["title"],
                "rank": d["rank"],
                "time": item["timestamp"],
                "hot_num": [{
                    "num": d['hot_num'],
                    "time": item["timestamp"]  # 使用外部的时间戳
                }]
            })

        # 构造每个平台的数据结构
        platform_data = {
            "platform": item["api_type"],  # 添加平台信息
            "time": item["timestamp"],
            "data": transformed_data
        }

        data.append(platform_data)
    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


@app.get("/word-cloud-hot-num/<int:api_type>")
def get_word_cloud(api_type: int):
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    try:
        # 尝试将api_type转换为枚举类型
        api_enum = ApiType(api_type)
    except ValueError:
        # 如果转换失败，则返回一个包含错误信息的ApiResult对象
        response_data = ApiResult(
            code=200,
            msg=f"不存在该类型的平台: {api_type}",
            data=None
        ).__dict__
        # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=200,
            mimetype='application/json'
        )

    # 从hbase读取
    table = hbase_utils.get_table("hot_search_word")
    data = []
    word_dict = {}

    for key, cell in table.scan(row_start=f"{api_enum.value}:{start_time}",
                                row_stop=f"{api_enum.value}:{end_time}",
                                columns=["word:words", "word:timestamp"]):
        row_key = key.decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell)
        words = json.loads(row_data["word:words"])
        timestamp = row_data["word:timestamp"]

        if timestamp not in word_dict:
            word_dict[timestamp] = {}

        for word_info in words:
            word = word_info['word']
            hot_num = word_info.get('hot_num', 0)
            if word in word_dict[timestamp]:
                word_dict[timestamp][word] += hot_num
            else:
                word_dict[timestamp][word] = hot_num

    for timestamp, words in word_dict.items():
        word_list = [{'word': word, 'hot_num': hot_num} for word, hot_num in words.items()]
        data.append({
            'timestamp': timestamp,
            'words': word_list
        })

    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


@app.get("/word-cloud-num/<int:api_type>")
def get_word_cloud_num(api_type: int):
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    try:
        # 尝试将api_type转换为枚举类型
        api_enum = ApiType(api_type)
    except ValueError:
        # 如果转换失败，则返回一个包含错误信息的ApiResult对象
        response_data = ApiResult(
            code=200,
            msg=f"不存在该类型的分词数据: {api_type}",
            data=None
        ).__dict__

        # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=200,
            mimetype='application/json'
        )

    # 从hbase读取
    table = hbase_utils.get_table("hot_search_word")
    word_frequency = {}

    for key, cell in table.scan(row_start=f"{api_enum.value}:{start_time}",
                                row_stop=f"{api_enum.value}:{end_time}",
                                columns=["word:words", "word:timestamp"]):
        row_data: dict = decode_dict(cell)
        timestamp = row_data["word:timestamp"]
        words = json.loads(row_data["word:words"])

        if timestamp not in word_frequency:
            word_frequency[timestamp] = {}

        for word_info in words:
            word = word_info['word']
            word_frequency[timestamp][word] = word_frequency[timestamp].get(word, 0) + 1

    # 构建响应数据并对words按出现频率排序
    data = []
    for timestamp, words in word_frequency.items():
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        sorted_word_list = [{'word': word, 'num': frequency} for word, frequency in sorted_words]
        data.append({'timestamp': timestamp, 'words': sorted_word_list})

    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


@app.get("/trending-data/<int:api_type>")
def get_trending_data(api_type: int):
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    app.logger.info(f"start={start_time}, end={end_time}")

    try:
        # 尝试将api_type转换为枚举类型
        api_enum = ApiType(api_type)
    except ValueError:
        # 如果转换失败，则返回一个包含错误信息的ApiResult对象
        response_data = ApiResult(
            code=200,
            msg=f"不存在该类型的热搜: {api_type}",
            data=None
        ).__dict__

        # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=200,
            mimetype='application/json'
        )

    # 从hbase读取
    table = hbase_utils.get_table("hot_search_trend")
    data = []

    for key, cell in table.scan(row_start=f"{api_enum.value}:{start_time}",
                                row_stop=f"{api_enum.value}:{end_time}",
                                columns=[
                                    "analyze:start_timestamp",
                                    "analyze:end_timestamp",
                                    "analyze:max_hot_num",
                                    "analyze:avg_hot_num",
                                    "analyze:min_hot_num",
                                    "analyze:max_rank",
                                    "analyze:min _rank",
                                    "trending:list"
                                ]):
        row_key = key.decode('utf-8')

        # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
        row_data: dict = decode_dict(cell)
        trending_list = json.loads(row_data["trending:list"])

        item = {
            "title": row_key.split(":")[1],
            "start_timestamp": row_data["analyze:start_timestamp"],
            "end_timestamp": row_data["analyze:end_timestamp"],
            "max_hot_num": float(row_data["analyze:max_hot_num"]),
            "avg_hot_num": float(row_data["analyze:avg_hot_num"]),
            "min_hot_num": float(row_data["analyze:min_hot_num"]),
            "max_rank": int(row_data["analyze:max_rank"]),
            "min_rank": int(row_data["analyze:min _rank"]),
            "trending_list": trending_list
        }

        app.logger.info(f"{item}")
        data.append(item)

    response_data = ApiResult(
        code=200,
        msg="success",
        data=data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )


@app.get("/weibo-category-data")
def get_weibo_category_data():
    # 从 url 读取参数
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    category = request.args.get("category")
    app.logger.info(f"start={start_time}, end={end_time}, category={category}")

    # 参数验证
    if not start_time or not end_time:
        response_data = ApiResult(
            code=400,
            msg="缺少必要的参数: start, end ",
            data=None
        ).__dict__

        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=400,
            mimetype='application/json'
        )

    # 从hbase读取
    table = hbase_utils.get_table("hot_search_weibo_category")
    data = []

    try:
        for key, cell in table.scan(row_start=f"{start_time}:{category}",
                                    row_stop=f"{end_time}:{category}",
                                    columns=[
                                        "data:category",
                                        "data:timestamp",
                                        "analyze:list",
                                        "analyze:count"
                                    ]):
            row_key = key.decode('utf-8')

            # 解码单元格数据，将其转换为字典格式，以便后续处理和使用
            row_data: dict = decode_dict(cell)
            analyze_list = json.loads(row_data["analyze:list"])

            try:
                count = int(row_data["analyze:count"])
            except ValueError as ve:
                app.logger.error(f"Invalid count value for row {row_key}: {row_data['analyze:count']}")
                count = None

            item = {
                "category": row_data["data:category"],
                "timestamp": row_data["data:timestamp"],
                "values": analyze_list,
                "count": count,
            }

            app.logger.info(f"{item}")
            data.append(item)
    except Exception as e:
        app.logger.error(f"Error reading from HBase: {str(e)}")
        response_data = ApiResult(
            code=500,
            msg="Error reading data from HBase",
            data=None
        ).__dict__

        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=500,
            mimetype='application/json'
        )

    # 合并数据
    merged_data = {}
    for item in data:
        category = item['category']
        for value in item['values']:
            hotness = value[0]
            if category not in merged_data:
                merged_data[category] = 0
            merged_data[category] += hotness

    # 排序并计算排名
    sorted_data = sorted(merged_data.items(), key=lambda x: x[1], reverse=True)
    result_data = []
    for rank, (category, total_hotness) in enumerate(sorted_data, start=1):
        result_data.append({
            "category": category,
            "values": [total_hotness, rank]
        })

    response_data = ApiResult(
        code=200,
        msg="success",
        data=result_data
    ).__dict__

    # 使用 ensure_ascii=False 和 indent 来生成格式化的 JSON 响应
    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),
        status=200,
        mimetype='application/json'
    )
