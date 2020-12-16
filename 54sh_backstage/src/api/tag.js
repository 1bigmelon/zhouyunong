import { Axios } from '@/plugins/axios'

export default {
  newTag(tag) {
    return Axios.post('tag/new', tag)
  },
  getAllTags() {
    return Axios.get('tag/ls')
  }
}
