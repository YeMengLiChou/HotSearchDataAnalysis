<script setup>
import HotDataList from "@/components/HotDataList.vue";
import ChartWordCloud from "@/components/ChartWordCloud.vue";
import {ref,reactive,onMounted} from "vue";
const myDate = ref("")
const getDate = (val)=>{
  myDate.value = val.date
}
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

onMounted(() => {})
</script>

<template>
  <div class="weibo-common">
    weibo
    <HotDataList @sendDate="getDate"/>
  </div>
  <div class="blank" />
    <ChartWordCloud :options="state.chartOptions" class="chart-cloud"></ChartWordCloud>
</template>

<style scoped>
.weibo-common{
  color: white;
}
.blank{
  height: 20px;
  width: 100%;
}
</style>
