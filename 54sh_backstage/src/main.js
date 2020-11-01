import Vue from 'vue'
import App from './App.vue'

// plugins
import axiosConfig from './plugins/axios'
import APIConfig from './plugins/api'
Vue.use(axiosConfig)
   .use(APIConfig)

// dependencies
import Vuex from 'vuex'
import Router from './router/router'
Vue.use(Vuex)

// ant design vue
import {
  Layout, Message, Menu, Icon, Avatar, Dropdown, Button
} from 'ant-design-vue'
Vue.use(Layout).use(Message).use(Menu).use(Icon).use(Avatar)
   .use(Dropdown).use(Button)

// MainLayout
import shLayout from './layouts/MainLayout'
Vue.component('sh-layout', shLayout)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: Router
}).$mount('#app')
