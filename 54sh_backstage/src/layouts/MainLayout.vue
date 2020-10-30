<!--
 * @FileDescription: 主要布局组件
 * @Author: wangsz12
 * @Date: 10.30 22.47
 * @LastEditors: wangz12
 * @LastEditTime: 10.30 22.47
 -->

<template>
  <div class="container">
    <a-layout>
      <a-layout-header style="background-color: pink;">
        header
      </a-layout-header>
      <a-layout>
        <a-layout-sider style="background-color: lightblue;">
          sidebar
        </a-layout-sider>
        <a-layout-content style="background-color: lightgreen;">
          content
        </a-layout-content>
      </a-layout>
      <a-layout-footer style="background-color: lightyellow;">
        footer
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script>
  export default {
    name: 'MainLayout',
    data() {
      return {
        
      }
    }
  }
</script>

<style lang="scss" scoped>
  
</style>