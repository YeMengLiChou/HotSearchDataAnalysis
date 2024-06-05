<script lang="ts" setup>
import {reactive, ref,onMounted} from 'vue'
import {defineEmits} from 'vue'
import HeatCurveEntry from "@/components/HeatCurveEntry.vue";
import * as echarts from "echarts/core";
const emits = defineEmits(['sendDate'])
const size = ref<'default' | 'large' | 'small'>('default')

const value2 = ref('')
const sendDate= () => {
  let params = {
    date:value2.value
  }
  emits('sendDate', params)
}
const testData = [
  {
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
onMounted(() =>{
  DrawCategory(testData,2)
})
const shortcuts = [
  {
    text: '今天',
    value: new Date(),
  },
  {
    text: '昨天',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24)
      return date
    },
  },
  {
    text: '一周前',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
      return date
    },
  },
]

const disabledDate = (time: Date) => {
  return time.getTime() > Date.now()
}
const list = [
  {title:'热搜词1',key:'1',id:'1'},
  {title:'热搜词2',key:'2',id:'2'},
  {title:'热搜词3',key:'3',id:'3'},
  {title:'热搜词4',key:'4',id:'4'},
  {title:'热搜词5',key:'5',id:'5'},
]

const state = ({
  chartOptions:{
    legend:{
      data:["政治","科技"],
      left: 'center',
      bottom: 5
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    }
  }
})
interface Tree {
  label: string
  children?: Tree[]
}
function DrawCategory(data,len) {
  // 词云
  for (let i = 1; i <= len; i++){
    console.log(data[i-1].data,len)
    let mychart = echarts.init(document.getElementById("chart-"+i))
    mychart.setOption({
      legend:{
        data:["政治","科技"],
        left: 'center',
        bottom: 5
      },
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      grid: {
        left: '3%',
        right: '7%',
        bottom: '7%',
        containLabel: true
      },
      series:data[i-1].data
    })
  }
}

</script>

<template>
  <div class="common-list">
    <div class="query-time-table">
      <div class="date-picker">
        <el-date-picker
          v-model="value2"
          type="date"
          placeholder="选择热搜日期"
          :disabled-date="disabledDate"
          :shortcuts="shortcuts"
          @change="sendDate"
          :size="size"/>
      </div>
    </div>
    <el-collapse accordion >
      <el-collapse-item v-for="i in list" >
        <template #title>
          <div class="hot-list-item-id">{{i.id}}</div>
          <div> {{i.title}}</div>
        </template>
        <div class="hot-list-item-info" >
          <div :id="`chart-${i.id}`" class="chart"></div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<style scoped>
.common-list{
  text-align: center;
}
.date-picker{
  margin-left: 20px;
}
.hot-list-item-id{
  color: red;
  font-size: 12px;
  font-weight: bold;
  margin-right: 15px;
  margin-left: 15px;
}
.hot-list-item-info{
  margin: 15px;
}
.chart{
  height: 400px;
  width: 400px;
}
</style>
