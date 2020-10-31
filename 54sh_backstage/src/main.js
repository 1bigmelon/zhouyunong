import Vue from 'vue'
import App from './App.vue'

// plugins
import Axios from './plugins/axios'
import API from './plugins/api'

// dependencies
import Vuex from 'vuex'
import Router from './router/router'
import {
  Layout, Message, Menu, Icon, Avatar, Dropdown
} from 'ant-design-vue'

Vue.prototype.$axios = Axios
Vue.prototype.$api = API

// antdv config
Vue.use(Layout).use(Message).use(Menu).use(Icon).use(Avatar)
   .use(Dropdown)

Vue.use(Vuex)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: Router
}).$mount('#app')
