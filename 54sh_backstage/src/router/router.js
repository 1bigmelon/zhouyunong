import Vue from 'vue'
import VueRouter from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { Message } from 'ant-design-vue'

// 屏蔽反复点击同一路由时的报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

import { routes } from './routerMap'

const routerConfig = {
  mode: 'history',
  routes: routes,
  base: '/manage'
}

const router = new VueRouter(routerConfig)

const contentTitleMap = {
  'index': '主页',
  'newArticle': '新建文章',
  'review': '文章审核',
  'manageArticle': '文章管理',
  'newCategory': '新建分类',
  'manageCategory': '查看分类',
  'newTag': '新建标签',
  'manageTag': '查看标签',
  'newUser': '新建用户',
  'manageUser': '用户管理',

}

router.beforeEach((to, from, next) => {
  NProgress.start()

  if (to.name === 'login') {
    next()
  }
  else {
    // 判断token合法性
    /**
     * TODO 判断token合法性
     */
    if (localStorage.getItem('token')) {
      next()
    }
    else {
      if (to.name !== 'base') {
        Message.error('身份已过期，请重新登录')
      }
      next('/login')
    }

    router.app.$options.store.dispatch('setContentTitle', contentTitleMap[to.name])
    router.app.$options.store.dispatch('setSelectedItemName', to.name)
    next()
  }
})

router.afterEach(() => {
  window.scrollTo(0, 0)
  NProgress.done()
})

export default router
