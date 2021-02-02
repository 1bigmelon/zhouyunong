import auth from '@/api/auth'
import org from '@/api/org'
import user from '@/api/user'
import category from '@/api/category'
import tag from '@/api/tag'

const Repository = {
  ...auth,
  ...org,
  ...user,
  ...category,
  ...tag
}

export default {
  install(Vue) {
    Object.defineProperty(Vue.prototype, '$api', { value: Repository })
  }
}
