const state = {
  selectedItemName: 'index',
  contentTitle: ''
}

const mutations = {
  setSelectedItemName(state, newVal) {
    state.selectedItemName = newVal
  },
  setContentTitle(state, newVal) {
    state.contentTitle = newVal
  }
}

const actions = {
  setSelectedItemName({ commit }, newVal) {
    commit('setSelectedItemName', newVal)
  },
  setContentTitle({ commit }, newVal) {
    commit('setContentTitle', newVal)
  }
}

export default {
  state,
  mutations,
  actions
}