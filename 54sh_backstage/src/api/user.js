import { Axios } from '@/plugins/axios'

export default {
  createUser(userInfo) {
    return Axios.post('/user/new', userInfo)
  },
  getAllUsers() {
    return Axios.get('/user/ls')
  }
}
