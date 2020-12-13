import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// stores
import Universal from './universal'
import Auth from './auth'

export default new Vuex.Store({
  state: {
    ...Universal.state,
    ...Auth.state
  },
  mutations: {
    ...Universal.mutations,
    ...Auth.mutations
  },
  actions: {
    ...Universal.actions,
    ...Auth.actions
  }
})