<script setup lang="ts">
import * as echarts from 'echarts/core';
import { GridComponent } from 'echarts/components';
import { ScatterChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import {onMounted, ref} from "vue";
import merge from "lodash/merge";
echarts.use([GridComponent, ScatterChart, CanvasRenderer, UniversalTransition]);

const props = withDefaults(
    defineProps<{
      options: any
    }>(),
    {},
)
const defaultSeries = [
  {
    smooth: true,
    type: 'line',
    data: []
  }
]
let seriesData = props.options.series || defaultSeries;

function DrawCategory() {
  // 词云
  let mychart = echarts.init(document.querySelector("#chart-category"))
  // let mychart = echarts.init(document.getElementById("chart-category")) // 可以设置主题色'dark'
  mychart.setOption({

    grid: {
      left: '3%',
      right: '7%',
      bottom: '7%',
      containLabel: true
    },
    brush: {},
    legend:{},
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: seriesData
  })
}

onMounted(() => {
  DrawCategory()
})
</script>

<template>
  <div id="chart-category"></div>
</template>

<style scoped>
#chart-category{
  width: 400px;
  height: 400px;
  background-color: white;
  margin: 0 auto;
}
</style>
