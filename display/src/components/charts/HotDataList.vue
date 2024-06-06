<script lang="ts" setup>
import {reactive, ref, onMounted, watch} from 'vue'
import {defineEmits} from 'vue'
import HeatCurveEntry from "@/components/HeatCurveEntry.vue";
import * as echarts from "echarts/core";
const emits = defineEmits(['sendDate'])
const size = ref<'default' | 'large' | 'small'>('default')
const props = defineProps({
  data:{
    type:Object,
    default: {}
  }
})

const value2 = ref('')
const sendDate= () => {
  let params = {
    date:value2.value
  }
  emits('sendDate', params)
}
const data = props.data

onMounted(() =>{
  DrawCategory(data,data.length)
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

interface Tree {
  label: string
  children?: Tree[]
}
function DrawCategory(data:any,len:number) {
  // 词云
  for (let i = 1; i <= len; i++){
    console.log(data[i-1].data,len)
    let myChart = echarts.init(document.getElementById("chart-"+i))
    const option = {
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
    }
    myChart.setOption(option)
  }
  for (let i = 1; i <= len; i++){
    console.log(data[i-1].data,len)
    let myChart = echarts.init(document.getElementById("-chart-"+i))
    const option = {
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
    }
    myChart.setOption(option)
  }
}

</script>

<template>
  {{data}}
  <div class="common-list">
    <div class="query-time-table">
      <div class="date-picker">
        <el-date-picker
          format="YYYY/MM/DD"
          value-format="x"
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
      <el-collapse-item v-for="i in data"  >
        <template #title>
          <div class="hot-list-item-id">{{i.rank}}</div>
          <div> {{i.title}}</div>
        </template>
        <div class="hot-list-item-info" >
          <div :id="`chart-${i.id}`" class="chart"></div>
          <div :id="`-chart-${i.id}`" class="chart"> </div>
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
  display: flex;
  justify-content: center;
}
.chart{
  height: 60vh;
  width: 60vh;
}
</style>
