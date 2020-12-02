import context from '../main'

const state = {
  userInfo: {
    id: '',
    name: '',
    username: ''
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
        if (res.data.status) {
          localStorage.setItem('token', res.data.data.token)
          const { id, name, user_id } = res.data.data.user
          commit('setUserInfo', {
            id,
            name,
            username: user_id
          })
          context.$router.push('/index')
        }
      })
  }
}

export default {
  state,
  mutations,
  actions
}