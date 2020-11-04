import Vue from 'vue'
import VueRouter from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 屏蔽反复点击同一路由时的报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: () => {
      /**
       * TODO 验证token合法性
       * 合法转至index
       * 过期转至login
       */
      return '/login'
    }
  },
  {
    path: '/index',
    component: () => import('../layouts/MainLayout'),
    children: [
      {
        path: '',
        component: () => import('../pages/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('../pages/login')
  },
  {
    path: '/article',
    component: () => import('../layouts/MainLayout'),
    children: [
      {
        path: 'newArticle',
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
})

router.afterEach(() => {
  NProgress.done()
})

export default router