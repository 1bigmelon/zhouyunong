import { Axios } from '@/plugins/axios'

export default {
  createTag(tagInfo) {
    return Axios.post('tag/new', tagInfo)
  },
  getAllTags() {
    return Axios.get('tag/ls')
  }
}
