<template>
  <div class="container">
    <!-- dev test -->
      <!-- <div style="height: 1500px; width: 200px; background-color: pink;">
        这个div用来测试滚动条
      </div> -->
    <!-- dev test -->
    <div class="data-box">
      <data-box icon="file-text" title="文章总数量" :value="1564"/>
      <data-box icon="cloud" title="已发布数量" :value="432"/>
      <data-box icon="file-protect" title="待二审数量" :value="745"/>
      <data-box icon="audit" title="待终审数量" :value="545"/>
      <data-box icon="cloud-upload" title="待发布数量" :value="976"/>
      <data-box icon="delete" title="回收站数量" :value="15"/>
    </div>
  </div>
</template>

<script>
import DataBox from '../components/DataBox.vue'

export default {
  name: 'index',
  data() {
    return {
      
    }
  },
  components: {
    'data-box': DataBox
  }
}
</script>

<style lang="scss" scoped>
  .container {
    height: 100%;
    width: 100%;
    
    .data-box {
      width: 100%;
      display: flex;
      justify-content: space-around;
    }
  }
</style>