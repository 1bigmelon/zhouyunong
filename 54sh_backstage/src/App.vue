<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: '',
  data() {
    return {

    }
  },
  mounted() {
    console.log('document.body.clientHeight: ', document.body.clientHeight)
    console.log('document.body.clientWidth: ', document.body.clientWidth)

    if (localStorage.getItem('userInfo')) {
      this.setUserInfo(JSON.parse(localStorage.getItem('userInfo')))
    }
  },
  methods: {
    ...mapActions(['setUserInfo'])
  }
}
</script>

<style lang="scss">
  #app {
    height: 100%;
    width: 100%;
  }

  .ant-table-tbody > tr > td {
    padding: 0 .3rem;
    height: 4rem;
  }
</style>
