<script setup lang="ts">
import ChartWordCloud from "../../../components/charts/ChartWordCloud.vue"
import {reactive, ref} from "vue";
import HotDataList from "@/components/charts/HotDataList.vue";
import {http} from "@/utils/http";
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
  state.chartOptions.series =
    {
      ...state.chartOptions.series,

    }
}

const queryData = (start:any,end:any)=>{
  const param = {
    start:start,
    end:end
  }
  http.request("get","/api/hot/1",param).then(res=>{
    console.log(res)
  }).catch(err=>{
    console.log(err)
  })
}

const dataList = reactive({
  data:[
      {
        title:'热搜词1',key:'1',id:'1',
        data:[
          {
            smooth: true,
            name: '政治',
            data: [820, 932, 901, 934, 1290, 1330, 1320],
            type: 'line'
          },
          {
            smooth: true,
            name: '科技',
            data: [120, 532, 301, 634, 1190, 1830, 2320],
            type: 'line'
          }
        ]
      },
      {
        title:'热搜词2',key:'2',id:'2',
        data:[
          {
            smooth: true,
            name: '政治',
            data: [820, 932, 901, 934, 1290, 1330, 1320],
            type: 'line'
          },
          {
            smooth: true,
            name: '科技',
            data: [120, 532, 301, 634, 1190, 1830, 2320],
            type: 'line'
          }
        ]
      }
    ]
})
</script>

<template>
  <div>
    <div class="weibo-common">
      <HotDataList @sendDate="getDate" :data="dataList.data" />
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
