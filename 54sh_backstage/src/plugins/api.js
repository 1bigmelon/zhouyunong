import authAPI from '@/api/auth'
import orgAPI from '@/api/org'
import userAPI from '@/api/user'

const Repository = {
  ...authAPI,
  ...orgAPI,
  ...userAPI
}

export default {
  install(Vue) {
    Object.defineProperty(Vue.prototype, '$api', { value: Repository })
  }
}
