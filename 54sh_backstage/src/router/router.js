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
        path: 'new',
        component: () => import('../pages/article/newArticle')
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

router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router