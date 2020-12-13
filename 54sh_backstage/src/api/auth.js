import context from '../main'

export default {
  login(credentials) {
    return context.$axios.post('/auth/signin', credentials)
  }
}