#!/bin/bash

bash "kafka-mirror-maker.sh --consumer.config ./consumer.properties --producer.config producer.properties --include hot_1 "