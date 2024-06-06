<script lang="ts" setup>
import { reactive, ref, onMounted, watch, nextTick, toRaw } from "vue";
import { defineEmits } from "vue";
import HeatCurveEntry from "@/components/HeatCurveEntry.vue";
import * as echarts from "echarts/core";
import { getTrendingData } from "@/api/anaylze";

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

const endValue = ref("")

const sendDate = () => {
  let params = {
    startDate: value2.value,
    endDate: endValue.value,
  };
  emits("sendDate", params);
};


let listData = ref([]);
watch(
  () => props.data,
  async () => {
    await nextTick();
    const data = toRaw(props.data);
    listData.value = data[0].data;
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

function DrawCategory(data: any, len: number) {
  // 词云
  for (let i = 1; i <= len; i++) {
    console.log(data[i - 1].data, len);
    let myChart = echarts.init(document.getElementById("chart-" + i));
    const option = {
      legend: {
        data: ["政治", "科技"],
        left: "center",
        bottom: 5
      },
      xAxis: {
        type: "category",
        data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
      },
      yAxis: {
        type: "value"
      },
      grid: {
        left: "3%",
        right: "7%",
        bottom: "7%",
        containLabel: true
      },
      series: data[i - 1].data
    };
    myChart.setOption(option);
  }
  for (let i = 1; i <= len; i++) {
    console.log(data[i - 1].data, len);
    let myChart = echarts.init(document.getElementById("-chart-" + i));
    const option = {
      legend: {
        data: ["政治", "科技"],
        left: "center",
        bottom: 5
      },
      xAxis: {
        type: "category",
        data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
      },
      yAxis: {
        type: "value"
      },
      grid: {
        left: "3%",
        right: "7%",
        bottom: "7%",
        containLabel: true
      },
      series: data[i - 1].data
    };
    myChart.setOption(option);
  }
}
const activeNames = ref(["0"]); // 初始时，没有面板打开
const isPanelOneActive = ref(false); // 跟踪面板一是否真正渲染了内容
const handleCollapseChange = val => {
  if (val.includes("1") && !isPanelOneActive.value) {
    console.log(val + "打开");
  }
};
const value2 = ref<Date>(new Date(2024, 5, 6, 0, 0, 0));
const defaultTime = ref<Date>(new Date(2024, 5, 6, 0, 0, 0));
</script>

<template>
  <div class="common-list">
    <div class="query-time-table">
      <div class="date-picker">
        <el-date-picker
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
        />
      </div>
    </div>
    <el-collapse accordion @change="handleCollapseChange">
      <el-collapse-item v-for="i in listData">
        <template #title>
          <div class="hot-list-item-id">{{ i.rank + 1 }}</div>
          <div>{{ i.title }}</div>
        </template>
        <div class="hot-list-item-info">
          <div :id="`chart-${i.id}`" class="chart"></div>
          <div :id="`-chart-${i.id}`" class="chart"></div>
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
