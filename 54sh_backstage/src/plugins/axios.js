import axios from 'axios'

/**
 * TODO 配置baseURL
 */
export const baseURL = 'http://47.115.90.131:10079/api/vi'

export const Axios = axios.create({
  baseURL: baseURL,
  timeout: 10000
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
  if (err.response.status === 401) {

    /**
     * TODO 返回到登录界面
     */

  }

  return Promise.reject(err.response.data)
})

export default {
  install(Vue) {
    Object.defineProperty(Vue.prototype, '$axios', { value: Axios })
  }
}