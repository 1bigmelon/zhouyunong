import { Axios } from '@/plugins/axios'

export default {
  newCategory(category) {
    return Axios.post('/div/new', category)
  },
  viewCategory() {
    return Axios.get('div/ls')
  }
}
