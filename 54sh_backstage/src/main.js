import Vue from 'vue'
import App from './App.vue'

// plugins
import axiosConfig from './plugins/axios'
import APIConfig from './plugins/api'
Vue.use(axiosConfig)
   .use(APIConfig)

// dependencies
import Vuex from 'vuex'
import store from './store/index'
Vue.use(Vuex)
import router from './router/router'

// ant design vue
import {
  Message, Icon, Avatar, Input, Button
} from 'ant-design-vue'
Vue.use(Icon).use(Avatar).use(Input).use(Button)

Vue.prototype.$message = Message

// MainLayout
import shLayout from './layouts/MainLayout'
Vue.component('sh-layout', shLayout)

Vue.config.productionTip = false

export default new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')
