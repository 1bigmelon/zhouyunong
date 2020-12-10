<template>
  <div class="container">
    <aside class="side-bar-box">
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
            <menu-item
              text="查看投稿"
              icon="inbox"
              name="manageContribution"
              to="/article/contribution"
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
            <span>人员管理</span>
          </div>
          <div>
            <menu-item
              text="新建用户"
              icon="user"
              name="newUser"
              to="/user/new"
            />
            <menu-item
              text="查看用户"
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
    <div class="main">
      <header class="header-box">
        <div class="fold-box">
          <a-icon type="menu-fold" style="font-size: 1.1rem;" />
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
      <main class="content-box">
        <div v-if="showTitleBar" class="content-title">
          <span>{{ contentTitle }}</span>
        </div>
        <div class="content">
          <router-view></router-view>
        </div>
      </main>
    </div>
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
    }
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
        background-color: $theme-color;
        box-shadow: 0 0 .5px .5px $theme-color;
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
        padding-bottom: 1rem;

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

      .header-box {
        height: 3.8rem;
        width: 100%;
        display: flex;
        align-items: center;
        position: relative;

        .user-box {
          display: flex;
          align-items: center;
          position: absolute;
          right: 2rem;
          top: 1rem;

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
          padding: 2rem;
        }
      }
    }
  }
</style>
