<script setup lang="ts">
import ChartWordCloud from "../../../components/charts/ChartWordCloud.vue"
import {reactive, ref} from "vue";
import HotDataList from "@/components/charts/HotDataList.vue";
import {ApiType, getHotSearchOriginData} from "@/api/anaylze";
import {integer} from "vue-types";
defineOptions({
  name: 'default'
})
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
const queryTime = ref("")
const getDate = (val)=>{
  queryTime.value = val.date
  console.log(queryTime.value)
  queryData(queryTime.value,queryTime.value+86400000)

}
let dataList = ref(null)

const queryData = (start:any,end:any)=>{
  console.log(start,end)
  getHotSearchOriginData(ApiType.WeiBoHotSearch,start,end).then(res=>{

    dataList.value = res.data
    console.log(dataList.value)
  }).catch(err=>{
    console.log(err)
  })
}


</script>

<template>
  <div>
    <div class="weibo-common">
      <HotDataList @sendDate="getDate" :data="dataList" />
    </div>
    <div class="blank" />
    <ChartWordCloud :options="state.chartOptions" class="chart-cloud"></ChartWordCloud>
  </div>
</template>

<style scoped lang="scss">
.chart-cloud{
  height: 50%;
  width: 50%;
}
.blank{
  height: 50px;
  width: 100%;
}
</style>
