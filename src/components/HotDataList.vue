<script lang="ts" setup>
import { ref } from 'vue'
import {defineEmits} from 'vue'
const emits = defineEmits(['sendDate'])
const size = ref<'default' | 'large' | 'small'>('default')

const value2 = ref('')
const sendDate= () => {
  let params = {
    date:value2.value
  }
  emits('sendDate', params)
}

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
interface Tree {
  label: string
  children?: Tree[]
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
    <el-collapse accordion>
      <el-collapse-item v-for="i in list" >
        <template #title>
          <div class="hot-list-item-id">{{i.id}}</div>
          <div> {{i.title}}</div>
        </template>
        <div class="hot-list-item-info">
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
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
</style>
