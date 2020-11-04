const state = {
  breadcrumbs: []
}

const mutations = {
  setBreadcrumbs(state, newBreadcrumb) {
    state.breadcrumbs = newBreadcrumb
  }
}

const actions = {
  setBreadcrumbs({ commit }, newBreadcrumb) {
    commit('setBreadcrumbs', newBreadcrumb)
  }
}

export default {
  state,
  mutations,
  actions
}