import Vue from 'vue'
import App from './App.vue'

// plugins
import axiosConfig from './plugins/axios'
import APIConfig from './plugins/api'
Vue.use(axiosConfig)
Vue.use(APIConfig)

// dependencies
import Vuex from 'vuex'
import store from './store/index'
Vue.use(Vuex)
import router from './router/router'

// ant design vue
import {
  Message, Icon, Avatar, Input, Button,
  Table, Tag, Tooltip, Form, Select,
  Modal, Alert, Popconfirm, Pagination, ConfigProvider,
  Spin
} from 'ant-design-vue'
Vue.use(Icon).use(Avatar).use(Input).use(Button).use(Table)
  .use(Tag).use(Tooltip).use(Form).use(Select).use(Modal)
  .use(Alert).use(Popconfirm).use(Pagination).use(ConfigProvider)
  .use(Spin)

Vue.prototype.$message = Message
Vue.prototype.$form = Form
Vue.prototype.$modal = Modal

Vue.config.productionTip = false

export default new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')
