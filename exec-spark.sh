#!/bin/bash
PROJECT_DIR="/home/ecs-user/project/HotSearchDataAnalysis"
LOGFILE="$PROJECT_DIR/logs/exce-spark.log"
exec >> $LOGFILE 2>&1
# 输出当前时间
cd $PROJECT_DIR
echo "start spark: `date`"
source $PROJECT_DIR/venv/bin/activate
$PROJECT_DIR/venv/bin/python $PROJECT_DIR/analyze/exec.py

