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

const routes = [
  {
    path: '/',
    name: 'base'
  },
  {
    path: '/index',
    component: () => import('../layouts/MainLayout'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('../pages/index')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../pages/login')
  },
  {
    path: '/article',
    component: () => import('../layouts/MainLayout'),
    children: [
      {
        path: 'newArticle',
        name: 'newArticle',
        component: () => import('../pages/article/newArticle')
      }
    ]
  },
  {
    path: '/tag',
    component: () => import('../layouts/MainLayout'),
    children: [
      {
        path: 'newTag',
        component: () => import ('../pages/tag/newTag')
      }
    ]
  }
]

const routerConfig = {
  mode: 'history',
  routes: routes,
  base: '/manage'
}

let router = new VueRouter(routerConfig)

const breadcrumbNames = {
  'index': '主页',
  'article': '文章管理',
  'newArticle': '新建文章',
  'tag': '标签管理',
  'newTag': '新建标签'
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

    // 获取url分段数组
    let breadcrumbs = to.fullPath.split('/')
    breadcrumbs.shift()
    
    let breadcrumbRoutes = []
    for (let item in breadcrumbNames) {
      if (breadcrumbs.includes(item)) {
        breadcrumbRoutes.push({ breadcrumbName: breadcrumbNames[item] })
      }
    }
    router.app.$options.store.dispatch('setBreadcrumbs', breadcrumbRoutes)
    next()
  }
})

router.afterEach(() => {
  NProgress.done()
})

export default router