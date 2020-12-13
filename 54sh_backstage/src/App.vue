<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: '',
    data() {
      return {
        
      }
    },
    mounted() {
      console.log('document.body.clientHeight: ', document.body.clientHeight);
      console.log('document.body.clientWidth: ', document.body.clientWidth);
    }
  }
</script>

<style lang="scss">
  #app {
    height: 100%;
    width: 100%;
  }
</style>