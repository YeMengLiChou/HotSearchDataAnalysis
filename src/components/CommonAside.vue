<template>
  <div class="aside-menu">
    <el-switch v-model="isCollapse" class="switch">
      <template #active-action>
        <span class="custom-active-action">T</span>
      </template>
      <template #inactive-action>
        <span class="custom-inactive-action">F</span>
      </template>
    </el-switch>
    <el-menu
        :default-active="activeIndex"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        @select="handleSelect"
        background-color="1F2339"
        active-text-color="#fff"
        text-color="#8D8F9A"
        :router="true"
    >
      <el-menu-item index="/default">
        <el-icon><document/></el-icon>
        <span>默认</span>
      </el-menu-item>
      <el-menu-item index="/weiboPage">
        <el-icon><icon-menu /></el-icon>
        <span>微博</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
  Document,
  Menu as IconMenu
} from '@element-plus/icons-vue'
const activeIndex = ref('/default')
const isCollapse = ref(true)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleSelect= (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  height: 100vh;
  overflow: hidden;
}
.el-menu-vertical-demo{
  height: 100vh;
  overflow: hidden;
}
.switch{
  position: absolute;
  left: 50%;
  transform: translate(-50%);
}
--el-switch-on-color{
  background-color: #1F2339;
}
</style>
