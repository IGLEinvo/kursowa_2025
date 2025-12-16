/** API service for backend communication */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
};

export const userAPI = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data) => api.put('/users/me', data),
  getUser: (id) => api.get(`/users/${id}`),
};

export const articleAPI = {
  getArticles: (params) => api.get('/articles', { params }),
  getArticle: (id) => api.get(`/articles/${id}`),
  createArticle: (data) => api.post('/articles', data),
  updateArticle: (id, data) => api.put(`/articles/${id}`, data),
  deleteArticle: (id) => api.delete(`/articles/${id}`),
  publishArticle: (id) => api.post(`/articles/${id}/publish`),
  searchArticles: (params) => api.get('/articles/search', { params }),
  getTrending: (limit = 10) => api.get('/articles/trending', { params: { limit } }),
  getRecommendations: (limit = 10) => api.get('/articles/recommendations', { params: { limit } }),
};

export const commentAPI = {
  getArticleComments: (articleId) => api.get(`/comments/article/${articleId}`),
  createComment: (data) => api.post('/comments', data),
  updateComment: (id, data) => api.put(`/comments/${id}`, data),
  deleteComment: (id) => api.delete(`/comments/${id}`),
};

export const notificationAPI = {
  getNotifications: (params) => api.get('/notifications', { params }),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
  markAllAsRead: () => api.put('/notifications/read-all'),
};

export const adminAPI = {
  getUsers: (params) => api.get('/admin/users', { params }),
  getArticles: (params) => api.get('/admin/articles', { params }),
  getCategories: () => api.get('/admin/categories'),
  createCategory: (data) => api.post('/admin/categories', data),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
};

export default api;




