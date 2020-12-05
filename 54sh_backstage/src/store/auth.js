import context from '../main'

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
  login({ commit }, credentials) {
    commit('setIsLogin', true)
    return context.$api.login(credentials)
      .then((res) => {
        console.log('res: ', res);
        if (res.data.status) {
          localStorage.setItem('token', res.data.data.token)
          const { id, name, last_ip } = res.data.data.user
          commit('setUserInfo', {
            id,
            name,
            IP: last_ip
          })
          context.$router.push('/index')
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