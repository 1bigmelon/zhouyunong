import { Axios } from '@/plugins/axios'

export default {
  createUser(userInfo) {
    return Axios.post('/user/new', userInfo)
  },
  getUserInfo(username) {
    // eslint-disable-next-line camelcase
    return Axios.post('/user/info', { user_id: username })
  },
  getUsersByPageNum(page) {
    return Axios.get(`/user/ls?page=${page}`)
  },
  disableUser(id) {
    return Axios.post('/user/disable', { id })
  },
  enableUser(id) {
    return Axios.post('/user/chinfo', {
      id,
      status: true
    })
  },
  changeUserInfo(userInfo) {
    return Axios.post('/user/chinfo', userInfo)
  },
  searchUsers(criteria) {
    return Axios.post('/user/search', criteria)
  }
}
