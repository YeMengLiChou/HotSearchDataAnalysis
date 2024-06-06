<script setup lang='ts'>
import { ApiType } from '@/api/anaylze';
import Common from '../default/common.vue';
import { ref } from 'vue';

defineOptions({
  name: 'toutiao'
})

const type = ref(ApiType.TouTiao)

</script>

<template>
  <div>
    <Common :apiType="type"/>
  </div>
</template>

<style lang='css' scoped>

</style>
