import { Axios } from '@/plugins/axios'

export default {
  login(credentials) {
    return Axios.post('/auth/signin', credentials)
  },
  verifyToken() {
    return Axios.get('/auth/verify')
  }
}
