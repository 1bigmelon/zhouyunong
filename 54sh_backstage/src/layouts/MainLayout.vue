<template>
  <div class="container">
    <div class="side-bar-header">
      <div class="title-box">
        <i class="icon"></i>
        <span>升华网管理后台</span>
      </div>
    </div>
    <aside class="side-bar-box">
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
              name="review"
              to="/article/review"
            />
            <menu-item
              text="文章管理"
              icon="container"
              name="manageArticle"
              to="/article/manage"
            />
            <menu-item
              text="投稿管理"
              icon="inbox"
              name="manageContribution"
              to="/article/contribution"
            />
          </div>
        </div>
        <div v-if="userInfo.auth >= 4" class="divider"></div>
        <div v-if="userInfo.auth >= 4" id="category-manage">
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
              text="分类管理"
              icon="appstore"
              name="manageCategory"
              to="/category/manage"
            />
          </div>
        </div>
        <div v-if="userInfo.auth >= 4" class="divider"></div>
        <div v-if="userInfo.auth >= 4" id="tag-manage">
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
              text="标签管理"
              icon="tags"
              name="manageTag"
              to="/tag/manage"
            />
          </div>
        </div>
        <div v-if="userInfo.auth >= 4" class="divider"></div>
        <div v-if="userInfo.auth >= 4" id="system-manage">
          <div class="side-bar-title">
            <span>人员管理</span>
          </div>
          <div>
            <menu-item
              text="新建用户"
              icon="user-add"
              name="newUser"
              to="/user/new"
            />
            <menu-item
              text="用户管理"
              icon="team"
              name="manageUser"
              to="/user/manage"
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
              @click="logout"
            />
          </div>
        </div>
      </div>
    </aside>
    <header class="header-box">
      <div class="fold-box">
        <a-icon type="menu-fold" class="fold" title="收起侧栏" @click="foldSideBar" />
        <span style="color: red;">←这个还没做</span>
      </div>
      <div class="user-box">
        <div class="dropdown-box">
          <div class="info-box">
            <a-avatar icon="user" />
            <span style="cursor: default;">{{ userInfo.name }}</span>
            <a-icon type="caret-down" style="font-size: .8rem;" />
          </div>
          <div class="dropdown">
            <div class="dropdown-item">
              <div class="dropdown-content" @click="logout">
                <a-icon type="export" />
                <span>退出登录</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <main ref="page" class="content-box">
      <div v-if="showTitleBar" class="content-title">
        <span>{{ contentTitle }}</span>
      </div>
      <div class="page-box">
        <div class="page">
          <router-view></router-view>
        </div>
        <div class="copyright">
          <span>2020 &copy; 升华工作室</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import MenuItem from '../components/MenuItem.vue'

export default {
  name: 'MainLayout',
  components: {
    'menu-item': MenuItem
  },
  data() {
    return {
      showTitleBar: true
    }
  },
  computed: {
    ...mapState([
      'selectedItemName',
      'contentTitle',
      'userInfo'
    ])
  },
  watch: {
    selectedItemName(newVal) {
      this.showTitleBar = (newVal !== 'index')
    },
    contentTitle() {
      this.$refs.page.scrollTop = 0
    }
  },
  mounted() {
    this.showTitleBar = (this.selectedItemName !== 'index')

    if (window.performance.navigation.type !== 1) {
      this.verifyToken()
        .catch(() => {
          this.$message.error('身份已过期，请重新登录')
          this.$router.push('/login')
        })
    }
  },
  methods: {
    ...mapActions(['verifyToken']),

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
      this.$message.success('已退出登录')
    },
    foldSideBar() {

    }
  }
}
</script>

<style lang="scss" scoped>
  $side-bar-width: 13.5rem;
  $header-height: 3.8rem;

  .container {
    height: max-content;
    min-height: 100%;
    // height: 100%;
    width: 100%;
    display: flex;
    background-color: rgb(243, 247, 250);

    .divider {
      height: 1px;
      width: 85%;
      background-color: rgb(236, 236, 236);
      margin: .8rem auto .4rem auto;
    }

    .side-bar-header {
      height: $header-height;
      width: $side-bar-width;
      background-color: $theme-color;
      box-shadow: 0 0 .5px .5px $theme-color;
      display: flex;
      justify-content: center;
      align-items: center;
      position: fixed;
      z-index: 999;

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

    .side-bar-box {
      height: calc(100% - 3.8rem);
      width: $side-bar-width;
      position: fixed;
      top: $header-height;
      overflow: auto;
      background-color: #fff;
      z-index: 999;
      box-shadow: 0 0 .2px .2px rgb(0, 0, 0, 0.1);

      &::-webkit-scrollbar-track,
      &::-webkit-scrollbar,
      &::-webkit-scrollbar-thumb {
        display: none;
      }

      .side-bar {
        height: calc(max-content - 4rem);
        width: 100%;
        padding: {
          top: .5rem;
          bottom: 1rem;
        }
        z-index: 999;

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

    .header-box {
      height: $header-height;
      width: calc(100% - 13rem);
      display: flex;
      align-items: center;
      position: fixed;
      left: $side-bar-width;
      background-color: #fff;
      z-index: 999;
      box-shadow: 0 0 .2px .2px rgb(0, 0, 0, 0.1);

      .fold-box {
        position: absolute;
        left: 1.5rem;
        display: flex;
        align-items: center;

        .fold {
          font-size: 1.1rem;
          transition: all .3s ease;

          &:hover {
            color: $theme-color;
            cursor: pointer;
            transform: scale(1.1);
            transition: all .3s ease;
          }
        }
      }

      .user-box {
        display: flex;
        align-items: center;
        position: absolute;
        right: 2rem;
        top: 1rem;
        min-width: 10rem;

        .dropdown-box {
          font-size: 1rem;
          width: 100%;
          position: relative;

          .info-box {
            display: flex;
            align-items: center;
            justify-content: center;
            padding-bottom: .5rem;

            span:nth-child(2) {
              height: 100%;
              padding-left: .8rem;
              padding-right: .5rem;
              line-height: 1.9rem;
            }
          }

          &:hover .dropdown {
            display: block;
            animation: dropdown-list .3s ease;
          }

          .dropdown {
            width: 100%;
            background-color: #FFF;
            border-radius: 7px;
            box-shadow: 1px 1.5px 10px -5px $theme-color;
            padding: .5rem 0;
            display: none;

            .dropdown-item {
              height: 2rem;
              display: flex;
              align-items: center;
              transition: background-color linear .15s;

              &:hover {
                background-color: rgb(242, 240, 254);
                transition: background-color linear .15s;
                cursor: pointer;
                color: $theme-color;
              }

              .dropdown-content {
                margin-left: 1.5rem;
                font-size: .9rem;

                span {
                  padding-left: 1rem;
                }
              }
            }
          }
        }
      }
    }

    .content-box {
      height: calc(100% - 3.8rem);
      width: calc(100% - 13.5rem);
      position: fixed;
      right: 0;
      bottom: 0;
      overflow: {
        x: hidden;
        y: auto;
      }

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

      .page-box {
        width: 100%;
        padding: 2rem;

        .copyright {
          text-align: center;
          color: rgb(150, 150, 150);
          margin-top: 1.5rem;
        }
      }
    }
  }

  @keyframes dropdown-list {
    from {
      transform: translateY(-7px);
      opacity: 0;
    }

    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>
