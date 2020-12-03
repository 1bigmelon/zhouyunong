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
        <menu-item
          text="首页"
          icon="home"
          name="index"
          to="/index"
        />
        <div class="divider"></div>
        <div id="article-manage">
          <div class="side-bar-title">
            <span>文章管理</span>
          </div>
          <div>
            <menu-item
              text="新建文章"
              icon="form"
              name="newArticle"
              to="/article/new"
            />
            <menu-item
              text="文章审核"
              icon="audit"
              name="reviewArticle"
              to="/article/review"
            />
            <menu-item
              text="文章管理"
              icon="container"
              name="manageArticle"
              to="/article/manage"
            />
          </div>
        </div>
        <div class="divider"></div>
        <div id="category-manage">
          <div class="side-bar-title">
            <span>分类管理</span>
          </div>
          <div>
            <menu-item
              text="新建分类"
              icon="bars"
              name="newCategory"
              to="/category/new"
            />
            <menu-item
              text="查看分类"
              icon="appstore"
              name="manageCategory"
              to="/category/manage"
            />
          </div>
        </div>
        <div class="divider"></div>
        <div id="tag-manage">
          <div class="side-bar-title">
            <span>标签管理</span>
          </div>
          <div>
            <menu-item
              text="新建标签"
              icon="tag"
              name="newTag"
              to="/tag/new"
            />
            <menu-item
              text="查看标签"
              icon="appstore"
              name="manageTag"
              to="/tag/manage"
            />
          </div>
        </div>
        <div class="divider"></div>
        <div id="system-manage">
          <div class="side-bar-title">
            <span>系统管理</span>
          </div>
          <div>
            <menu-item
              text="人员管理"
              icon="team"
              name="personnel"
              to="/system/personnel"
            />
          </div>
        </div>
        <div class="divider"></div>
        <div id="logout">
          <div class="side-bar-title">
            <span>操作</span>
          </div>
          <div>
            <menu-item
              text="退出登录"
              icon="export"
              name="logout"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="main">
      <div class="header-box">
        <div class="fold-box">
          <a-icon type="menu-fold" style="font-size: 1.1rem;"/>
        </div>
        <div class="user-box">
          <a-avatar icon="user"/>
          <span>测试名字</span>
          <a-icon type="caret-down"/>
        </div>
      </div>
      <div class="content-box">
        <div class="content-title" v-if="ifShowTitleBar">
          <span>{{ contentTitle }}</span>
        </div>
        <div class="content">  
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import MenuItem from '../components/MenuItem.vue'

export default {
  name: 'MainLayout',
  data() {
    return {
      ifShowTitleBar: true
    }
  },
  methods: {
  },
  components: {
    'menu-item': MenuItem
  },
  computed: {
    ...mapState(['selectedItemName', 'contentTitle'])
  },
  watch: {
    selectedItemName(newVal) {
      this.ifShowTitleBar = (newVal !== 'index')
    }
  },
  mounted() {
    this.ifShowTitleBar = (this.selectedItemName !== 'index')
  }
}
</script>

<style lang="scss" scoped>
  $side-bar-width: 15rem;

  .container {
    height: max-content;
    min-height: 100%;
    // height: 100%;
    width: 100%;
    display: flex;

    .divider {
      height: 1px;
      width: 85%;
      background-color: rgb(236, 236, 236);
      margin: .8rem auto .4rem auto;
    }

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
          height: 2rem;
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
      min-height: 100%;
      width: 100%;
      z-index: -1;

      .header-box {
        height: 3.8rem;
        width: 100%;
        display: flex;
        align-items: center;
        position: relative;

        .user-box {
          height: 2rem;
          width: 10rem;
          display: flex;
          align-items: center;
          position: absolute;
          right: 1rem;

          span:nth-child(2) {
            height: 100%;
            font-size: 1rem;
            padding-left: .8rem;
            padding-right: .5rem;
            line-height: 1.9rem;
          }
        }

        .fold-box {
          position: absolute;
          left: 1.5rem;
          display: flex;
          align-items: center;
        }
      }

      .content-box {
        height: calc(100% - 4rem);
        width: 100%;
        background-color: rgb(243, 247, 250);

        .content-title {
          height: 3rem;
          width: 100%;
          background-color: rgb(232, 231, 249);
          display: flex;
          align-items: center;
          padding-left: 1.5rem;
          color: rgb(115, 97, 211);
          font-size: 1.1rem;
        }

        .content {
          min-height: calc(100% - 3rem);
          width: 100%;
          padding: 1rem 1rem;
        }
      }
    }
  }

  // @font-face {
  //   font-family: 'Hiragino';
  //   src: url(../assets/fonts/HiraginoSansGB.ttf);
  // }
</style>