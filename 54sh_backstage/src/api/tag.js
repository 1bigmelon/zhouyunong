import { Axios } from '@/plugins/axios'

export default {
  createTag(tagInfo) {
    return Axios.post('/tag/new', tagInfo)
  },
  getAllTags() {
    return Axios.get('/tag/ls')
  },
  getTagsByPageNum(page) {
    return Axios.get(`/tag/ls?page=${page}`)
  },
  getTagInfo(id) {
    return Axios.post('/tag/info', { id })
  },
  disableTag(id) {
    return Axios.post('/tag/modify', {
      id,
      status: false
    })
  },
  enableTag(id) {
    return Axios.post('/tag/modify', {
      id,
      status: true
    })
  },
  changeTagInfo(tagInfo) {
    return Axios.post('/tag/modify', tagInfo)
  },
  searchTag(tagInfo) {
    return Axios.post('/tag/search', tagInfo)
  }
}
