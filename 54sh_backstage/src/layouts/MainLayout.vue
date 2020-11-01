<!--
 * @FileDescription: 主要布局组件
 * @Author: wangsz12
 * @Date: 10.30 22.47
 * @LastEditors: wangz12
 * @LastEditTime: 11.1 00.20
 -->

<template>
  <div class="container">
    <a-layout>
      <a-layout-header class="header">
        <span class="logo" @click="$router.push('/index')">
          <span>中南大学升华网管理系统</span>
          <span>{{ systemName }}</span>
        </span>
        <span class="user-info">
          <a-avatar icon="user" style="margin-right: .5rem;"/>
          <a-dropdown>
            <span>{{ username }} <a-icon type="caret-down" style="transform: scale(0.8);"/> </span>
            <a-menu slot="overlay">
              <a-menu-item @click="logout()">
                <a-icon type="export" />
                <span>注销</span>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </span>
      </a-layout-header>
      <a-layout class="main-container">
        <a-layout-sider class="sider">
          <a-menu class="menu" mode="inline" theme="dark">
            <a-sub-menu key="article">
              <template slot="title">
                <a-icon type="file-text"/>
                <span>文章管理</span>
              </template>
              <a-menu-item key="newArticle" @click="newArticle">
                <a-icon type="form" />
                <span>新建文稿</span>
              </a-menu-item>
              <a-menu-item key="reviewArticle">
                <a-icon type="audit" />
                <span>文稿审核</span>
              </a-menu-item>
              <a-menu-item key="articleManage">
                <a-icon type="container" />
                <span>文稿管理</span>
              </a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="class">
              <template slot="title">
                <a-icon type="bars"/>
                <span>分类管理</span>
              </template>
              <a-menu-item key="newClass">
                <a-icon type="form" />
                <span>新建分类</span>
              </a-menu-item>
              <a-menu-item key="showClass">
                <a-icon type="appstore" />
                <span>查看分类</span>
              </a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="tags">
              <template slot="title">
                <a-icon type="tags"/>
                <span>标签管理</span>
              </template>
              <a-menu-item key="newTag">
                <a-icon type="form" />
                <span>新建标签</span>
              </a-menu-item>
              <a-menu-item key="showTag">
                <a-icon type="appstore" />
                <span>查看标签</span>
              </a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="system">
              <template slot="title">
                <a-icon type="setting"/>
                <span>系统管理</span>
              </template>
              <a-menu-item key="personnel">
                <a-icon type="team" />
                <span>人员管理</span>
              </a-menu-item>
            </a-sub-menu>
            <a-menu-item key="logout" @click="logout" selectable="false">
              <a-icon type="export" />
              <span>注销</span>
            </a-menu-item>
          </a-menu>
        </a-layout-sider>
        <a-layout-content class="content">
          <router-view></router-view>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
  export default {
    name: 'MainLayout',
    data() {
      return {
        systemName: '审稿后台',
        username: 'ABC'
      }
    },
    methods: {
      newArticle() {
        this.$router.push('/article/new')
      },
      logout() {
        localStorage.removeItem('token')
        this.$router.push('/login')
      }
    }
  }
</script>

<style lang="scss" scoped>
  .header {
    background-color: rgba(20, 120, 226, .9);
    // background-image: linear-gradient(to right, rgb(20, 120, 226), rgb(46, 114, 187));
    position: fixed;
    z-index: 1;
    width: 100%;

    span {
      color: white;
      user-select: none;
      -moz-user-select: none;
      -webkit-user-select: none;
    }

    .logo {
      &:hover {
        cursor: pointer;
      }

      span {
        &:nth-child(1) {
          font-size: 1.3rem;
        }

        &:nth-child(2) {
          padding-left: 0.5rem;
          font-size: 1rem;
        }
      }
    }

    .user-info {
      width: fit-content;
      padding-left: 1rem;
      float: right;

      span {
        vertical-align: middle;
        font-size: 1rem;
      }
    }
  }

  .main-container {
    margin-top: 4rem;
    margin-left: 200px;

    .sider {
      overflow: auto;
      height: 100vh;
      position: fixed;
      left: 0;
      user-select: none;
      -moz-user-select: none;
      -webkit-user-select: none;
    }

    .content {
      background-color: lightgreen;
      height: 100%;
      width: 100%;
      overflow: initial;
    }
  }
</style>