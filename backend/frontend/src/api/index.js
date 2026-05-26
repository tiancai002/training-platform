import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      } else {
        ElMessage.error(data.detail || '请求失败')
      }
    }
    return Promise.reject(error)
  }
)

export default api

// Auth APIs
export const authApi = {
  login: (data) => api.post('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/me', data),
  getActivity: () => api.get('/auth/me/activity?days=7')
}

// Question Bank APIs
export const questionApi = {
  getBanks: (params) => api.get('/question/banks', { params }),
  getQuestions: (params) => api.get('/question/questions', { params }),
  practice: (data) => api.post('/question/practice', data),
  submitPractice: (data) => api.post('/question/practice/submit', data),
  getWrongBook: () => api.get('/question/wrong-book'),
  getDaily: (params) => api.get('/question/daily', { params }),
  getStats: () => api.get('/question/stats')
}

// Course APIs
export const courseApi = {
  getList: (params) => api.get('/course/list', { params }),
  getDetail: (id) => api.get(`/course/${id}`)
}

// Order APIs
export const orderApi = {
  create: (data) => api.post('/order/create', data),
  getList: () => api.get('/order/list'),
  getDetail: (id) => api.get(`/order/${id}`)
}

// Community APIs
export const communityApi = {
  getCategories: () => api.get('/community/categories'),
  getPosts: (params) => api.get('/community/posts', { params }),
  createPost: (data) => api.post('/community/posts/create', data),
  getPost: (id) => api.get(`/community/posts/${id}`),
  likePost: (id) => api.post(`/community/posts/${id}/like`),
  addComment: (id, data) => api.post(`/community/posts/${id}/comment`, data)
}
