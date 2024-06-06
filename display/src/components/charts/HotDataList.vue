<script lang="ts" setup>
import { reactive, ref, onMounted, watch, nextTick, toRaw } from "vue";
import { defineEmits } from "vue";
import HeatCurveEntry from "@/components/HeatCurveEntry.vue";
import * as echarts from "echarts/core";
import { getTrendingData } from "@/api/anaylze";
import { timestamp } from "@vueuse/core";
import analyze from "@/router/modules/views/analyze";

const emits = defineEmits(["sendDate"]);
const size = ref<"default" | "large" | "small">("default");
const props = defineProps({
  data: {
    type: Object,
    default: {}
  },
  apiType: {
    type: Number,
    default: 0,
    required: false
  }
});

const endValue = ref("");

const sendDate = () => {
  let params = {
    startDate: value1.value[0].getTime(),
    endDate: value1.value[1].getTime()
  };
  emits("sendDate", params);
};

let listData = ref([]);
watch(
  () => props.data,
  async () => {
    await nextTick();
    const data = toRaw(props.data);
    console.log(data.length)
    listData.value = data[data.length-1].data;
    // console.log(data[0].data)
    for (const dataKey in data[0].data) {
      console.log(data[0].data[dataKey]); // 获取title
    }

    if (props.data) {
      DrawCategory(props.data, props.data.length);
    }
  }
);

const shortcuts = [
  {
    text: "今天",
    value: new Date()
  },
  {
    text: "昨天",
    value: () => {
      const date = new Date();
      date.setTime(date.getTime() - 3600 * 1000 * 24);
      return date;
    }
  },
  {
    text: "一周前",
    value: () => {
      const date = new Date();
      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
      return date;
    }
  }
];

const disabledDate = (time: Date) => {
  return time.getTime() > Date.now();
};

interface Tree {
  label: string;
  children?: Tree[];
}

function DrawCategory(data: any, val: any) {
  // 词云
  console.log(data.transformedHotData);
  console.log(data.transformedRankData);
  let myChart = echarts.init(document.getElementById("chart-" + val));
  const option = {
    xAxis: {
      type: "category"
    },
    yAxis: {
      type: "value"
    },
    title: {
      text: "热度趋势图"
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        label: {
          backgroundColor: "#6a7985"
        }
      }
    },
    grid: {
      left: "3%",
      right: "7%",
      bottom: "7%",
      containLabel: true
    },
    series: {
      type: "line",
      smooth: 1,
      symbol: "none",
      lineStyle: {
        color: "#5470C6",
        width: 1
      },
      data: data.transformedHotData
    }
  };
  myChart.setOption(option);
  let myChart2 = echarts.init(document.getElementById("-chart-" + val));
  const option2 = {
    xAxis: {
      type: "category"
    },
    yAxis: {
      type: "value",
      inverse: true
    },
    title: {
      text: "排名趋势图"
    },

    grid: {
      left: "3%",
      right: "7%",
      bottom: "7%",
      containLabel: true
    },

    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        label: {
          backgroundColor: "#6a7985"
        }
      }
    },
    series: {
      type: "line",
      smooth: 1,
      symbol: "none",
      lineStyle: {
        color: "#5470C6",
        width: 1
      },
      data: data.transformedRankData
    }
  };
  myChart2.setOption(option2);
}
type rankData = {
  timestamp: number;
  rank: number;
};
type hotData = {
  timestamp: number;
  hot_num: number;
};
const formattedDate = (timestamp: number) => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

  return `${year}年${month}月${day}日 ${hours}:${minutes}`;
};

type Item = {
  timestamp: number;
  hot_num: number;
  rank: number;
};

type TranformedItem = {
  avg_hot_num: number;
  min_hot_num: number;
  max_hot_num: number;
  min_rank: number;
  max_rank: number;
  duration: string;
};

const analyzedItem = ref<TranformedItem>(null);

const transformWordCloud = (data: Item[]) => {
  const rankItems: Array<rankData> = [];
  const hotItems: Array<hotData> = [];

  data.forEach(item => {
    rankItems.push({
      timestamp: formattedDate(item.timestamp),
      rank: item.rank
    });
    hotItems.push({
      timestamp: formattedDate(item.timestamp),
      hot_num: item.hot_num
    });
  });
  const transformedRankData: Array<Array<number>> = rankItems.map(item => [
    item.timestamp,
    item.rank
  ]);
  const transformedHotData: Array<Array<number>> = hotItems.map(item => [
    item.timestamp,
    item.hot_num
  ]);
  return {
    transformedRankData,
    transformedHotData
  };
};
const activeNames = ref(["0"]); // 初始时，没有面板打开
const isPanelOneActive = ref(false); // 跟踪面板一是否真正渲染了内容
const handleCollapseChange = val => {
  if (val != "" && !isPanelOneActive.value) {
    // console.log(val+"打开")
    const pData = listData[val];
    let parts = val.split("-");
    console.log(parts);
    // let endDate = endValue.value;
    // if (endDate > new Date().getTime()) {
    //   endDate = new Date().getTime();
    // }

    getTrendingData(
      props.apiType,
      parts[0],
      value1.value[0].getTime(),
      value1.value[1].getTime()
    )
      .then(res => {
        if (res.data.length > 0) {
          const data = res.data[0];
          const trending_list = data.trending_list;

          let output = transformWordCloud(trending_list);

          let maxTime = 0;
          let minTime = 999999999999999999;
          trending_list.forEach(item => {
            maxTime = Math.max(maxTime, item.timestamp);
            minTime = Math.min(minTime, item.timestamp);
          });

          const duration = maxTime - minTime;
          // 计算总分钟数
          const totalMinutes = Math.floor(duration / (1000 * 60));

          // 分离出小时和分钟部分
          const hours = Math.floor(totalMinutes / 60);
          let minutes = totalMinutes % 60; // 使用取余运算得到剩余的分钟数

          analyzedItem.value = {
            max_hot_num: data.max_hot_num,
            min_hot_num: data.min_hot_num,
            avg_hot_num: data.avg_hot_num,
            max_rank: data.max_rank,
            min_rank: data.min_rank,
            duration: `${hours}小时${minutes}分钟`
          };

          console.log(output);
          DrawCategory(output, val);
        }
      })
      .catch(err => {
        console.log(err);
      });
  }
};

const curDate = new Date();
curDate.setDate(curDate.getDate() - 1);
const value1 = ref<[Date, Date]>([curDate, new Date()]);

// const value2 = ref<Date>(new Date(2024, 5, 6, 0, 0, 0));
// const defaultTime = ref<Date>(new Date(2024, 5, 6, 0, 0, 0));
</script>

<template>
  <div class="common-list">
    <div class="query-time-table">
      <div class="date-picker">
        <div class="block">
          <span class="demonstration">选择时间</span>
          <el-date-picker
            v-model="value1"
            type="datetimerange"
            range-separator="To"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            :disabled-date="disabledDate"
            @change="sendDate"
          />
        </div>

        <!-- <el-date-picker
          format="YYYY/MM/DD"
          value-format="x"
          :default-time="defaultTime"
          v-model="value2"
          type="date"
          placeholder="选择热搜开始日期"
          :disabled-date="disabledDate"
          :shortcuts="shortcuts"
          @change="sendDate"
          :size="size"
        />

        <el-date-picker
          format="YYYY/MM/DD"
          value-format="x"
          :default-time="defaultTime"
          v-model="endValue"
          type="date"
          placeholder="选择热搜结束日期"
          :disabled-date="disabledDate"
          :shortcuts="shortcuts"
          @change="sendDate"
          :size="size"
        /> -->
      </div>
    </div>
    <el-collapse accordion @change="handleCollapseChange">
      <el-collapse-item
        v-for="i in listData"
        :name="i.title + '-' + i.time"
        :key="i.time"
      >
        <template v-if="analyzedItem != null">
          <el-descriptions class="margin-top" :column="3" border>
            <el-descriptions-item label="榜上最高热度">{{
              analyzedItem.max_hot_num
            }}</el-descriptions-item>
            <el-descriptions-item label="榜上最低热度">{{
              analyzedItem.min_hot_num
            }}</el-descriptions-item>
            <el-descriptions-item label="榜上平均热度">{{
              analyzedItem.avg_hot_num
            }}</el-descriptions-item>
            <el-descriptions-item label="榜上最高排名">{{
              analyzedItem.min_rank
            }}</el-descriptions-item>
            <el-descriptions-item label="榜上最低排名">{{
              analyzedItem.max_rank
            }}</el-descriptions-item>
            <el-descriptions-item label="在榜持续时间">{{
              analyzedItem.duration
            }}</el-descriptions-item>
          </el-descriptions>
        </template>

        <template #title>
          <div class="hot-list-item-id" v-if="i.rank>0">{{ i.rank }}</div>
          <div class="hot-list-item-id" v-if="i.rank<=0">置顶</div>
          <div>{{ i.title }}</div>
        </template>
        <div class="hot-list-item-info">
          <div :id="`chart-${i.title + '-' + i.time}`" class="chart"></div>
          <div :id="`-chart-${i.title + '-' + i.time}`" class="chart"></div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<style scoped>
.common-list {
  text-align: center;
}
.date-picker {
  margin-left: 20px;
}
.hot-list-item-id {
  color: red;
  font-size: 12px;
  font-weight: bold;
  margin-right: 15px;
  margin-left: 15px;
}
.hot-list-item-info {
  margin: 15px;
  display: flex;
  justify-content: center;
}
.chart {
  height: 60vh;
  width: 60vh;
}
</style>
