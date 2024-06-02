<script setup>
import HotDataList from "@/components/HotDataList.vue";
import {ref} from "vue";
const myDate = ref("")
const getDate = (val)=>{
  myDate.value = val.date
}
</script>

<template>
  <div class="weibo-common">
    weibo
    <HotDataList @sendDate="getDate"/>
  </div>

</template>

<style scoped>
.weibo-common{
  color: white;
}
</style>
