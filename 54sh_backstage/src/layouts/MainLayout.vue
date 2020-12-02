<template>
  <div class="container">
    <div class="side-bar-box">
      <div class="side-bar-header">
        <div class="title-box">
          <i class="icon"></i>
          <span>升华网管理后台</span>
        </div>
      </div>
      <div class="side-bar">
        <div id="article-manage">
          <div class="side-bar-title">
            <span>文章管理</span>
          </div>
          <div class="side-bar-item">
            <MenuItem></MenuItem>
          </div>
        </div>
      </div>
    </div>
    <div class="main">
      <div class="header-box">

      </div>
      <div class="content-box">

      </div>
    </div>
  </div>
</template>

<script>
import MenuItem from '../components/MenuItem'

export default {
  name: 'MainLayout',
  data() {
    return {

    }
  },
  components: {
    MenuItem
  }
}
</script>

<style lang="scss" scoped>
  $side-bar-width: 15rem;

  .container {
    height: 100%;
    width: 100%;
    display: flex;

    .side-bar-box {
      height: 100%;
      width: $side-bar-width;

      .side-bar-header {
        height: 3.8rem;
        width: 100%;
        background-color: rgb(127, 99, 244);
        box-shadow: 0 0 .5px .5px rgb(127, 99, 244);
        display: flex;
        justify-content: center;
        align-items: center;

        .title-box {
          $icon-size: 2.2rem;
          display: flex;

          .icon {
            height: $icon-size;
            width: $icon-size;
            background-image: url('../assets/logo.png');
            background-size: contain;
            vertical-align: middle;
          }

          span {
            color: white;
            height: $icon-size;
            display: inline-flex;
            align-items: center;
            margin-left: .5rem;

            &:nth-child(2) {
              font-size: 1.1rem;
            }
          }
        }
      }

      .side-bar {
        height: calc(100% - 4rem);
        width: 100%;
        padding-top: .5rem;

        .side-bar-title {
          height: 2.5rem;
          display: flex;
          align-items: center;

          span {
            margin-left: 1.8rem;
            color: rgb(174, 173, 177);
            font-size: .8rem;
          }
        }
      }
    }
    
    .main {
      height: 100%;
      width: 100%;
      z-index: -1;

      .header-box {
        height: 3.8rem;
        width: 100%;
      }

      .content-box {
        height: calc(100% - 4rem);
        width: 100%;
        background-color: rgb(243, 247, 250);
      }
    }
  }

  // @font-face {
  //   font-family: 'Hiragino';
  //   src: url(../assets/fonts/HiraginoSansGB.ttf);
  // }
</style>