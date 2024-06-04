# 热点热搜数据分析
Kafka + Scrapy + Redis：爬虫部分实现

# Usage
1. 创建虚拟环境，安装所需依赖 `pip install -r ./config/requirement.txt`
2. 修改项目配置文件 `./config/settings.toml`


# Branch
- `feat-scrape`：爬虫部分实现
- `feat-analyze` 数据分析部分实现

# 爬虫运行

爬取到的数据将会发送到 `config/settings.toml` 文件中定义的 Kafka服务器中
- `scrapy.kafka.topic` 是发送的目标Topic
- `kafka.*` 是Kafka服务配置

统计数据可以通过 `redis` 查看，分别记录了每个类别的爬取次数以及上次爬取的时间
- `hot_search:api:count:<category>` 爬取次数
- `hot_search:api:time:<category>` 上次爬取时间
相关 redis 配置在 `config/settings.toml` 文件

## Linux环境
使用 `crontab` 设置定时任务
项目根目录下 `time.cron` 里面就是定时任务的配置

```bash
crontab -u <your-user> <project-dir>/time.cron
```

或者添加到你的对应文件中：

```cronexp
*/10 * * * * /bin/bash -C '<your-path>/HotSearchDataAnalysis/exec.sh'
```
----


# 数据分析
使用 Spark 3.5.1 和 scala 2.13 版本

## Spark 
### Windows 环境
Spark 配置好，不需要 Hadoop 配置，需要创建文件夹 `xxx/hadoop/bin`，并下载随便一个版本的 `winutils.exe` 放置在该目录下

在 `config/settings.toml` 文件中指定 `spark.home` 和 `spark.hadoop_home`

---

## Hbase
`happybase` 依赖的 `thriftpy2` 如果在 window 环境下无法安装，显示 required Visual C++ greater than 14.0 ...;

那么需要先下载 visual studio 2019 build tools, 然后选中 c++ 桌面开发安装（可能需要重启）；

完成后再安装；

-----



