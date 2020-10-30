import Vue from 'vue'
import VueRouter from 'vue-router'

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
      return '/index'
    }
  },
  {
    path: '/index',
    component: () => import('../pages/index.vue')
  },
  {
    path: '/login',
    component: () => import('../pages/login.vue')
  }
]

const routerConfig = {
  mode: 'history',
  routes: routes,
  base: '/mgnt'
}

let router = new VueRouter(routerConfig)

export default router