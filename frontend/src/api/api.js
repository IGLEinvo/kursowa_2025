import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('API Request:', config.method?.toUpperCase(), config.url)
  return config
})

// Add response interceptor for debugging and error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    return response
  },
  (error) => {
    const status = error.response?.status
    const data = error.response?.data
    console.error('API Error:', error.config?.url, status, data || error.message)
    
    // Handle 401 errors - token invalid/expired
    if (status === 401) {
      const errorMsg = data?.error || 'Unauthorized'
      console.error('401 Unauthorized - Token may be invalid or expired:', errorMsg)
      
      // Clear token if it's a token-related error (but skip for /auth/me endpoint to avoid loops)
      const isAuthEndpoint = error.config?.url?.includes('/auth/me')
      if (!isAuthEndpoint && (errorMsg.toLowerCase().includes('token') || 
          errorMsg.toLowerCase().includes('expired') || 
          errorMsg.toLowerCase().includes('invalid') ||
          errorMsg.toLowerCase().includes('authorization'))) {
        console.warn('Clearing invalid token from localStorage')
        localStorage.removeItem('token')
        delete api.defaults.headers.common['Authorization']
        
        // Dispatch event to notify AuthContext to clear user state
        window.dispatchEvent(new CustomEvent('auth:invalid-token', { detail: { error: errorMsg } }))
      }
    }
    
    // Handle 422 validation errors specifically
    if (status === 422) {
      console.error('422 Validation Error Details:', data)
      // If it's a JWT error, suggest re-login
      if (data?.error && (data.error.includes('token') || data.error.includes('Token'))) {
        console.error('Token validation failed - user may need to re-login')
      }
    }
    
    // Handle 401 errors - token might be expired or invalid
    if (error.response?.status === 401) {
      // Don't clear token here - let AuthContext handle it
      console.warn('401 Unauthorized - token may be expired')
    }
    
    return Promise.reject(error)
  }
)

// News API
export const newsApi = {
  getNews: (params) => api.get('/news', { params }),
  getArticle: (id) => api.get(`/news/${id}`),
  searchNews: (query, page = 1) => api.get('/news/search', { params: { q: query, page } }),
  getCategories: () => api.get('/news/categories'),
  getRecommended: (limit = 10) => api.get('/news/recommended', { params: { limit } }),
  likeArticle: (id) => api.post(`/news/${id}/like`),
  saveArticle: (id) => api.post(`/news/${id}/save`)
}

// Auth API
export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (data) => api.post('/auth/register', data),
  getCurrentUser: () => api.get('/auth/me')
}

// Comments API
export const commentsApi = {
  getComments: (articleId) => api.get(`/comments/articles/${articleId}/comments`),
  createComment: (articleId, content, parentId = null) => 
    api.post(`/comments/articles/${articleId}/comments`, { content, parent_id: parentId })
}

// Subscriptions API
export const subscriptionsApi = {
  getUserSubscription: () => api.get('/subscriptions'),
  getTiers: () => api.get('/subscriptions/tiers'),
  createSubscription: (tierId) => api.post('/subscriptions', { tier_id: tierId })
}

// Notifications API
export const notificationsApi = {
  getNotifications: (params) => api.get('/notifications', { params }),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
  getPreferences: () => api.get('/notifications/preferences'),
  updatePreferences: (prefs) => api.put('/notifications/preferences', prefs)
}

// Users API
export const usersApi = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  getSavedArticles: (page = 1) => api.get('/users/saved', { params: { page } }),
  followAuthor: (authorId) => api.post(`/users/authors/${authorId}/follow`),
  unfollowAuthor: (authorId) => api.post(`/users/authors/${authorId}/unfollow`)
}

// Admin API
export const adminApi = {
  listArticles: (params) => api.get('/admin/articles', { params }),
  updateArticle: (id, data) => api.put(`/admin/articles/${id}`, data),
  deleteArticle: (id) => api.delete(`/admin/articles/${id}`),
  createCategory: (data) => api.post('/admin/categories', data),
  updateCategory: (id, data) => api.put(`/admin/categories/${id}`, data),
  listUsers: (params) => api.get('/admin/users', { params }),
  toggleUserActive: (id) => api.put(`/admin/users/${id}/toggle-active`)
}

// Preferences API
export const preferencesApi = {
  getFavoriteCategories: () => api.get('/preferences/categories'),
  addFavoriteCategory: (categoryId) => api.post('/preferences/categories', { category_id: categoryId }),
  removeFavoriteCategory: (categoryId) => api.delete(`/preferences/categories/${categoryId}`),
  updateFavoriteCategories: (categoryIds) => api.post('/preferences/categories/bulk', { category_ids: categoryIds })
}

export default api

