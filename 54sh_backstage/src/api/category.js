import { Axios } from '@/plugins/axios'

export default {
  newCategory(category) {
    return Axios.post('/div/new', category)
  },
  getAllCategories() {
    return Axios.get('div/ls')
  }
}
