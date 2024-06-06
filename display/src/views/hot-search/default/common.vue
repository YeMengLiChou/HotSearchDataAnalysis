<script setup lang="ts">
import ChartWordCloud from "../../../components/charts/ChartWordCloud.vue";
<<<<<<< HEAD
import { onMounted, reactive, ref } from "vue";
import HotDataList from "@/components/charts/HotDataList.vue";
import {
  ApiType,
  WordCloudHotNumItem,
  getHotSearchOriginData,
  getWordCloudHotNum
} from "@/api/anaylze";
=======
import {onMounted, reactive, ref} from "vue";
import HotDataList from "@/components/charts/HotDataList.vue";
import { ApiType, getHotSearchOriginData,getTrendingData } from "@/api/anaylze";
>>>>>>> refs/remotes/origin/feat-display
import { integer } from "vue-types";
import { ElMessage } from "element-plus";
defineOptions({
  name: "common"
});

const props = defineProps({
  // api 类型参数
  apiType: {
    type: Number,
    default: 0,
    required: false
  }
});

// 分析数据
const state = ref({
  chartOptions: {
    series: [
      {
        gridSize: 20,
        data: []
      }
    ]
  }
});

const queryTime = ref(0);



const getDate = (val) => {
  queryTime.value = parseInt(val.date);
  console.log(queryTime.value);
  queryData(queryTime.value, queryTime.value + 86400000);
  queryWordCut(queryTime.value, queryTime.value + 86400000);
};

// 数据列表
const dataList = ref(null);
onMounted(()=>{
  queryData(new Date().setHours(0, 0, 0, 0), new Date().setHours(0, 0, 0, 0) + 86400000);
})
const queryData = (start: any, end: any) => {
  console.log(start, end);
  getHotSearchOriginData(props.apiType, start, end)
    .then(res => {
      dataList.value = res.data;
    })
    .catch(err => {
      console.log(err);
    });
};

type Item = {
  name: string;
  value: number;
};

const transformWordCloud = (data: WordCloudHotNumItem[]) => {
  const items: Array<Item> = [];
  data.forEach(item => {
    item.words.forEach(item1 => {
      items.push({
        name: item1.word,
        value: item1.hot_num
      });
    });
  });
  return {
    chartOptions: {
      series: [
        {
          gridSize: 20,
          data: items
        }
      ]
    }
  };
};

// 请求分词数据
const queryWordCut = (start: number, end: number) => {
  getWordCloudHotNum(props.apiType, start, end)
    .then(res => {
      if (res.code == 200) {
        console.log(res.data);
        state.value = transformWordCloud(res.data);
      } else {
        ElMessage({
          message: res.msg,
          type: "error"
        });
      }
    })
    .catch(err => {
      console.log(err);
      ElMessage({
        message: err,
        type: "error"
      });
    });
};
</script>

<template>
  <div>
    <div class="weibo-common">
      <HotDataList @sendDate="getDate" :data="dataList" :api-type="props.apiType"/>
    </div>
    <div class="blank" />
    <ChartWordCloud
      :options="state.chartOptions"
      class="chart-cloud"
    ></ChartWordCloud>
  </div>
</template>

<style scoped lang="scss">
.chart-cloud {
  height: 50%;
  width: 50%;
}
.blank {
  height: 50px;
  width: 100%;
}
</style>
