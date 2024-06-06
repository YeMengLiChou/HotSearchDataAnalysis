<script setup>
import HotDataList from "@/components/HotDataList.vue";
import ChartWordCloud from "@/components/ChartWordCloud.vue";
import ChartScatter from "@/components/ChartScatter.vue";
import {ref,reactive,onMounted} from "vue";
const myDate = ref("")
const getDate = (val)=>{
  myDate.value = val.date
}
// 词云的数据
const state = reactive({
  chartOptions:{
    series:[
      {
        gridSize: 20,
        data:[
          {name: '娜娜米', value: 30},
          {name: '五条悟',value: 30},
          { name: '狗卷', value: 28 },
          { name: 'Shoto', value: 28 },
          { name: 'Vox', value: 25 },
          { name: "Aza", value: 23 },
          { name: 'Mysta', value: 20 },
          { name: 'Uki', value: 18 },
          { name: 'Luca', value: 15 },
          { name: 'Shu', value: 10 },
          { name: 'Ike', value: 10 },
          { name: "Fulgun", value: 10 }
        ]
      }
    ]
  }
})
// 分类散点图数据
const state2 = reactive({
  chartOptions:{
    legend:{
      data:["政治","科技"],
      left: 'center',
      bottom: 5
    },
    series:[
      {
        name:'政治',
        data:[
          [1.05, 3.33],
          [4.05, 4.96],
          [6.03, 7.24],
          [12.0, 6.26],
          [12.0, 8.84],
          [7.08, 5.82],
          [5.02, 5.68]
        ],
        type: 'scatter'
      },
      {
        name:'科技',
        data:[
          [10.0, 8.04],
          [8.07, 6.95],
          [4.05, 4.96],
          [6.03, 7.24],
          [12.0, 6.26],
          [12.0, 8.84],
          [7.08, 5.82]
        ],
        type: 'scatter'
      }
    ]
  }
})

onMounted(() => {})
</script>

<template>
  <div class="weibo-common">
    <HotDataList @sendDate="getDate"/>
  </div>
  <div class="blank" />
    <chart-scatter :options="state2.chartOptions"/>
  <div class="blank" />
    <ChartWordCloud :options="state.chartOptions" class="chart-cloud"></ChartWordCloud>

</template>

<style scoped>
.weibo-common{
  color: white;
}
.blank{
  height: 50px;
  width: 100%;
}
</style>
