import Vue from 'vue'
import App from './App.vue'

// plugins
import Axios from './plugins/axios'
import API from './plugins/api'

// dependencies
import Vuex from 'vuex'
import Router from './router/router'
import {
  Layout
} from 'ant-design-vue'

Vue.prototype.$axios = Axios
Vue.prototype.$api = API

// antdv config
Vue.use(Layout)

Vue.use(Vuex)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router: Router
}).$mount('#app')
