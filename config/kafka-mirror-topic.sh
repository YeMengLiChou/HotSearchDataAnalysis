#!/bin/bash
# 用于从服务器端同步数据到本地
bash "kafka-mirror-maker.sh --consumer.config ./consumer.properties --producer.config producer.properties --include hot_1 "