const state = {
  selectedItemName: 'index',
  contentTitle: '',
  isSideBarFolded: false
}

const mutations = {
  setSelectedItemName(state, newVal) {
    state.selectedItemName = newVal
  },
  setContentTitle(state, newVal) {
    state.contentTitle = newVal
  },
  setIsSideBarFolded(state, newVal) {
    state.isSideBarFolded = newVal
  }
}

const actions = {
  setSelectedItemName({ commit }, newSelectedItemName) {
    commit('setSelectedItemName', newSelectedItemName)
  },
  setContentTitle({ commit }, newContentTitle) {
    commit('setContentTitle', newContentTitle)
  },
  setIsSideBarFolded({ commit }, newIsSideBarFolded) {
    commit('setIsSideBarFolded', newIsSideBarFolded)
  }
}

export default {
  state,
  mutations,
  actions
}
