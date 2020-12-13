import { Axios } from '@/plugins/axios'

export default {
  newTag(tag) {
    return Axios.post('tag/new', tag)
  },
  viewTag() {
    return Axios.get('tag/ls')
  }
}
