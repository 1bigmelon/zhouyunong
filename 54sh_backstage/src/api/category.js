import { Axios } from '@/plugins/axios'

export default {
  createCategory(categoryInfo) {
    return Axios.post('/div/new', categoryInfo)
  },
  getAllCategories() {
    return Axios.get('/div/ls')
  },
  getCategoriesByPageNum(page) {
    return Axios.get(`/div/ls?page=${page}`)
  },
  getCategoryInfo(id) {
    return Axios.post('/div/info', { id })
  },
  disableCategory(id) {
    return Axios.post('/div/modify', {
      id,
      status: false
    })
  },
  enableCategory(id) {
    return Axios.post('/div/modify', {
      id,
      status: true
    })
  },
  changeCategoryInfo(categoryInfo) {
    return Axios.post('/div/modify', categoryInfo)
  },
  searchCategory(categoryInfo) {
    return Axios.post('/div/search', categoryInfo)
  }
}
