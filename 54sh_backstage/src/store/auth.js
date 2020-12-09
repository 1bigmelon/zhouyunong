/* eslint-disable camelcase */
import context from '@/main'

const state = {
  userInfo: {
    id: '',
    name: '',
    IP: ''
  },
  isLogin: false
}

const mutations = {
  setUserInfo(state, newUserInfo) {
    state.userInfo = newUserInfo
  },
  setIsLogin(state, newIsLogin) {
    state.isLogin = newIsLogin
  }
}

const actions = {
  setUserInfo({ commit }, newVal) {
    commit('setUserInfo', newVal)
  },
  login({ commit }, credentials) {
    commit('setIsLogin', true)
    return context.$api.login(credentials)
      .then((res) => {
        if (res.data.status) {
          localStorage.setItem('token', res.data.data.token)
          const { id, name, last_ip } = res.data.data.user
          const userInfo = { id, name, IP: last_ip }
          localStorage.setItem('userInfo', JSON.stringify(userInfo))
          commit('setUserInfo', userInfo)
          return Promise.resolve(res)
        }
        else {
          return Promise.reject(res.data.msg)
        }
      })
      .catch((err) => {
        return Promise.reject(err)
      })
  },
  verifyToken() {
    return context.$api.verifyToken()
      .then((res) => {
        if (res.data.status) {
          return Promise.resolve(res)
        }
        else {
          return Promise.reject(res.data.msg)
        }
      })
      .catch((err) => {
        return Promise.reject(err)
      })
  }
}

export default {
  state,
  mutations,
  actions
}
