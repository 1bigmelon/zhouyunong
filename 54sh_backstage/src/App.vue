<template>
  <div id="app">
    <router-view v-if="isRouterAlive"></router-view>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: '',
  provide() {
    return {
      refresh: this.refresh
    }
  },
  data() {
    return {
      isRouterAlive: true
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
    ...mapActions(['setUserInfo']),

    refresh() {
      this.isRouterAlive = false
      this.$nextTick(() => {
        this.isRouterAlive = true
      })
    }
  }
}
</script>

<style lang="scss">
  html {
    overflow: hidden;
  }

  #app {
    height: 100%;
    width: 100%;
  }

  .index-list-box .ant-table-tbody > tr > td {
    padding: 0 .3rem;
    height: 4rem;
  }

  .user-list-box .ant-table-tbody > tr > td {
    padding: 0 .3rem;
    height: 2.8rem;
  }

  .button-color-green {
    background-color: #52C41A;
    border-color: #52C41A;
    color: white;

    &:hover, &:focus {
      background-color: #73d13d;
      border-color: #73d13d;
      color: white;
    }

    &:active, &.active {
      background-color: #389e0d;
      border-color: #389e0d;
      color: white;
    }
  }

  @font-face {
    font-family: 'OpenSans';
    src: url(./assets/fonts/OpenSans-Regular.ttf);
  }
</style>
