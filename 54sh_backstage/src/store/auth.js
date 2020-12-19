/* eslint-disable camelcase */
import context from '@/main'

const roleMap = {
  '一审': 1,
  '二审': 2,
  '终审': 3,
  '管理员': 4
}

const state = {
  userInfo: {},
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
        if (!res.data.status) {
          return Promise.reject(res.data.msg)
        }
        const userInfo = res.data.data.user
        Object.assign(userInfo, { auth: roleMap[res.data.data.user.role] })
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
        localStorage.setItem('token', res.data.data.token)
        commit('setUserInfo', userInfo)
      })
      .catch((err) => {
        return Promise.reject(err?.message)
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
