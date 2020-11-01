import authAPI from '../api/auth'

const Repository = {
  ...authAPI
}

export default {
  install(Vue) {
    Object.defineProperty(Vue.prototype, '$api', { value: Repository })
  }
}