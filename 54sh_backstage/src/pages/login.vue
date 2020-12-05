<template>
  <div class="container">
    <div class="login-box">
      <div class="title-box">
        <span>升华网管理后台登录</span>
      </div>
      <div class="input-box">
        <input type="text" required class="input" title="" v-model="credentials.username" />
        <a-icon type="user" class="prefix-icon" />
        <div class="underline"></div>
        <label>用户名</label>
      </div>
      <div class="input-box">
        <input type="password" required class="input" title="" v-model="credentials.password" />
        <a-icon type="key" class="prefix-icon" />
        <div class="underline"></div>
        <label>密码</label>
      </div>
      <div class="login-btn-box">
        <a-button type="primary" :loading="logining" class="login-btn" @click="loginBtnHdl">登录</a-button>
      </div>
      <div class="copyright">
        <span>2020 © 升华工作室</span>
      </div>
    </div>
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
        },
        logining: false
      }
    },
    methods: {
      ...mapActions(['login']),

      loginBtnHdl() {
        if (this.credentials.username === '') {
          this.$message.error('请输入用户名')
          return
        }
        if (this.credentials.password === '') {
          this.$message.error('请输入密码')
          return
        }
        
        this.logining = true
        this.login(this.credentials)
          .then(() => {
            this.$message.success('登录成功')
          })
          .catch((err) => {
            this.$message.error(err.data.msg)
          })
          .finally(() => {
            this.logining = false
          })
      }
    }
  }
</script>

<style lang="scss" scoped>
  .container {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    .login-box {
      width: 30rem;
      border-radius: 8px;
      box-shadow: 1px 1px 10px -2px rgba(0, 0, 0, 0.4);
      padding: 2rem 4rem;

      .title-box {
        height: 3rem;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

        span {
          font-size: 1.7rem;
          font-weight: bold;
        }
      }

      .input-box {
        height: 3rem;
        width: 100%;
        position: relative;
        margin-top: 2.5rem;

        .input {
          height: 100%;
          width: 100%;
          border: none;
          border-bottom: 2px solid silver;
          padding: 1rem 2.7rem;
          font-size: 1.2rem;
          outline: none;

          &:focus, &:valid {
            border-bottom-color: $theme-color;
            box-shadow: none;

            & ~ label {
              transform: translate(-2.5rem, -2rem);
              font-size: 1.1rem;
              color: $theme-color;
            }

            & ~ .underline:before {
              transform: scaleX(1);
            }
          }
        }

        label {
          position: absolute;
          bottom: .8rem;
          left: 2.7rem;
          color: grey;
          pointer-events: none;
          font-size: 1.1rem;
          transition: all .3s ease;
        }

        .underline {
          position: absolute;
          bottom: 0;
          height: 2px;
          width: 100%;

          &:before {
            content: "";
            position: absolute;
            height: 100%;
            width: 100%;
            background-color: $theme-color;
            transform: scaleX(0);
            transition: transform .3s ease;
          }
        }

        .prefix-icon {
          position: absolute;
          bottom: 1rem;
          left: .8rem;
          font-size: 1.1rem;
        }
      }

      .login-btn-box {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 3.5rem;
        margin-bottom: 2.5rem;

        .login-btn {
          height: 2.8rem;
          width: 10rem;
          font-size: 1.2rem;
        }
      }

      .copyright {
        text-align: center;
        font-size: .9rem;
        color: grey;
      }
    }
  }
</style>