<script>
import CommonHeader from '@/components/CommonHeader.vue'
import CommonAside from '@/components/CommonAside.vue'
import CommonTag from '@/components/CommonTag.vue'
export default {
  data() {
    return {

    };
  },
  components:{
    CommonHeader,
    CommonAside,
    CommonTag
  },
  mounted() {
  } ,
  methods:{

  }
}
</script>
<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header"> <common-header/> </el-header>
      <el-container style="max-height: 100vh">
        <el-aside class="aside"><CommonAside/></el-aside>
        <el-main class="main"><router-view/></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.aside{
  background-color: #1F2339;
  width: fit-content;
  height: 100vh;
  overflow: hidden;
}
.main{
  background-color: #081023
}
.header{
  background-color: #1F2339;
  padding: 10px;
}
</style>
