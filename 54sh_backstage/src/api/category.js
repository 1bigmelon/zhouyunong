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
  }
}
