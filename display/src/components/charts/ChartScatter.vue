<script setup lang="ts">
import * as echarts from 'echarts/core';
import { GridComponent } from 'echarts/components';
import { ScatterChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import {onMounted, ref} from "vue";
import merge from "lodash/merge";
import { useECharts } from '@pureadmin/utils';
echarts.use([GridComponent, ScatterChart, CanvasRenderer, UniversalTransition]);

const props = withDefaults(
    defineProps<{
      options: any
    }>(),
    {},
)
const defaultSeries = [
  {
  symbolSize: 10,
  type: 'scatter',
  data: []
  },
  {
    symbolSize: 10,
    type: 'scatter',
    data: []
  }
]
let seriesData = props.options.series || defaultSeries;

const chartScatter = ref()
const { setOptions } = useECharts(chartScatter)
function DrawScatter() {
  // 词云
  // let mychart = echarts.init(document.getElementById("chart-scatter")) // 可以设置主题色'dark'
  setOptions({
    grid: {
      left: '3%',
      right: '7%',
      bottom: '7%',
      containLabel: true
    },
    brush: {},
    legend:{},
    tooltip: {
      // trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.7)',
      showDelay: 1,
      formatter: function (params) {
        if (params.value.length > 1) {
          return (
              params.seriesName +
              ' :<br/>' +
              '热度: ' +
              params.value[0] +
              '<br/>' +
              '日期: ' +
              params.value[1]
          );
        } else {
          return (
              params.seriesName +
              ' :<br/>' +
              params.name +
              ' : ' +
              params.value +
              'kg '
          );
        }
      },
      axisPointer: {
        show: true,
        type: 'cross',
        lineStyle: {
          type: 'dashed',
          width: 1
        }
      }
    },
    xAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        show: false
      }
    },
    series: seriesData
  })
}

onMounted(() => {
  DrawScatter()
})
</script>

<template>
  <div id="chart-scatter" ref="chartScatter"></div>
</template>

<style scoped>
#chart-scatter{
  width: 50%;
  height: 50%;
  background-color: white;
  margin: 0 auto;
}
</style>
