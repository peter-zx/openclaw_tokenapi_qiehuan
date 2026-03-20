/**
 * API 调用封装
 */
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:9131/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => config,
  error => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.message
    return Promise.reject(new Error(message))
  }
)

// API 方法
export const api = {
  // 获取配置状态
  getConfig: () => apiClient.get('/config'),

  // 切换模型
  switchModel: (data) => apiClient.post('/switch', data),

  // 保存模型
  saveModel: (data) => apiClient.post('/save', data),

  // 删除模型
  deleteModel: (data) => apiClient.post('/delete', data),

  // 获取提供商列表
  getProviders: () => apiClient.get('/providers'),

  // 控制网关
  controlGateway: (action) => apiClient.post('/gateway/control', { action }),

  // 更新 API Key
  updateApiKey: (data) => apiClient.post('/provider/apikey', data)
}

export default api
