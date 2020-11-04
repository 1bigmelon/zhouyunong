import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// stores
import Universal from './universal'

export default new Vuex.Store({
  state: {
    ...Universal.state
  },
  mutations: {
    ...Universal.mutations
  },
  actions: {
    ...Universal.actions
  }
})