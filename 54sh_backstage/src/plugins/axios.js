import axios from 'axios'
import router from '@/router/router'

/**
 * TODO 配置baseURL
 */
export const baseURL = 'http://kyaru.dy1c.top:5000/api/v1'

export const Axios = axios.create({
  baseURL: baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 配置请求拦截器
Axios.interceptors.request.use((req) => {
  const token = localStorage.getItem('token')
  if (token) {
    req.headers.Authorization = token
  }

  return req
}, (err) => {
  return Promise.reject(err)
})

// 配置响应拦截器
Axios.interceptors.response.use((res) => {
  if (res.headers.Authorization) {
    localStorage.setItem('token', res.headers.Authorization)
  }

  if (res.data.status !== true) {
    return Promise.reject(res)
  }

  return res
}, (err) => {
  if (err.message.startsWith('timeout')) {
    err.message = '请求超时，请检查网络'
  }
  if (err.message.endsWith('401')) {
    err.message = '身份已过期，请重新登录'
    router.push('/login')
  }

  return Promise.reject(err)
})

export default {
  install(Vue) {
    Object.defineProperty(Vue.prototype, '$axios', { value: Axios })
  }
}
