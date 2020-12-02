<template>
  <div class="container">
    <!-- dev test -->
    <a-input placeholder="用户名" v-model="credentials.username"></a-input>
    <a-input placeholder="密码" v-model="credentials.password"></a-input>
    <a-button type="primary" @click="loginBtnHdl">登录</a-button>
    <!-- dev test -->
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    name: '',
    data() {
      return {
        credentials: {
          username: 'DogAdmin',
          password: '1145141919810'
        }
      }
    },
    methods: {
      ...mapActions(['login']),

      loginBtnHdl() {
        // this.$router.push('/')
        this.login(this.credentials)
      }
    }
  }
</script>

<style lang="scss" scoped>
  
</style>