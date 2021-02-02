import { Axios } from '@/plugins/axios'

export default {
  createOrg(orgInfo) {
    return Axios.post('/org/new', orgInfo)
  },
  getAllOrgs() {
    return Axios.get('/org/ls')
  },
  getOrgsByPageNum(page) {
    return Axios.get(`/org/ls?page=${page}`)
  },
  getOrgInfo(id) {
    return Axios.post(`/org/info`, { id })
  },
  disableOrg(id) {
    return Axios.post('/org/modify', {
      id,
      status: false
    })
  },
  enableOrg(id) {
    return Axios.post('/org/modify', {
      id,
      status: true
    })
  },
  changeOrgInfo(orgInfo) {
    return Axios.post('/org/modify', orgInfo)
  },
  searchOrg(orgInfo) {
    return Axios.post('/org/search', orgInfo)
  }
}
