<template>
    <div class="header-container">
      <el-image :src="this.url" class="icon"></el-image>
    </div>
</template>
<script lang="ts">
import Img from "../assets/icon.png"
export default {
  data(){
    return {
      url: Img
    }
  }
}
</script>
<style scoped>
.icon{
  height: 40px;
}
</style>
