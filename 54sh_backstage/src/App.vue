<template>
  <a-config-provider :locale="zhCN">
    <div id="app">
      <router-view v-if="isRouterAlive"></router-view>
    </div>
  </a-config-provider>
</template>

<script>
import { mapActions } from 'vuex'
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'

export default {
  name: '',
  provide() {
    return {
      refresh: this.refresh
    }
  },
  data() {
    return {
      isRouterAlive: true,
      zhCN
    }
  },
  mounted() {
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

  .ant-table-thead > tr > th {
    font-weight: bold;
  }

  .index-list-box .ant-table-tbody > tr > td {
    padding: 0 .3rem;
    height: 4rem;
  }

  .user-list-box, .tag-list-box {
    .ant-table-tbody > tr > td {
      padding: 0 .3rem;
      height: 2.8rem;
    }
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
