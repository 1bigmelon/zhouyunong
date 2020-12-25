import { Axios } from '@/plugins/axios'

export default {
  getAllOrgs() {
    return Axios.get('/org/ls')
  }
}
