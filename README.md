# 热点热搜数据分析
Kafka + Scrapy + Redis：爬虫部分实现

# Usage
1. 创建虚拟环境，安装所需依赖 `pip install -r ./config/requirement.txt`
2. 修改项目配置文件 `./config/settings.toml`


# Branch
- `feat-scrape`：爬虫部分实现

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

