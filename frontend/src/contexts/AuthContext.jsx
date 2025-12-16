import React, { createContext, useState, useEffect, useContext } from 'react'
import axios from 'axios'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(null)

  // Initialize auth on mount - check localStorage for existing token
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedToken = localStorage.getItem('token')
        console.log('🔄 Initializing auth, token found:', !!storedToken)
        
        if (storedToken) {
          // Set token in state first
          setToken(storedToken)
          
          // Set axios default header for all requests immediately
          axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
          console.log('✅ Token set in axios headers')
          
          // Small delay to ensure headers are set before making request
          await new Promise(resolve => setTimeout(resolve, 100))
          
          // Fetch current user to verify token is valid
          await fetchCurrentUser(storedToken)
        } else {
          // No token found, user is not logged in
          console.log('ℹ️ No token found, user not logged in')
          setLoading(false)
        }
      } catch (error) {
        console.error('❌ Auth initialization error:', error)
        setLoading(false)
      }
    }
    
    initializeAuth()
    
    // Listen for invalid token events from API interceptor
    const handleInvalidToken = (event) => {
      console.log('⚠️ Received invalid token event, clearing auth state')
      localStorage.removeItem('token')
      setToken(null)
      setUser(null)
      delete axios.defaults.headers.common['Authorization']
    }
    
    window.addEventListener('auth:invalid-token', handleInvalidToken)
    
    // Cleanup
    return () => {
      window.removeEventListener('auth:invalid-token', handleInvalidToken)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const fetchCurrentUser = async (tokenToUse = null) => {
    try {
      const token = tokenToUse || localStorage.getItem('token')
      
      if (!token) {
        console.log('No token found in localStorage')
        setLoading(false)
        return
      }
      
      console.log('Attempting to fetch user with token:', token.substring(0, 20) + '...')
      
      // Ensure token is set in axios headers before making request
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      const response = await axios.get('/api/auth/me')
      
      if (response.data && response.data.user) {
        setUser(response.data.user)
        setToken(token)
        console.log('✅ User authenticated successfully:', response.data.user.username)
      } else {
        console.warn('Invalid response format from /api/auth/me:', response.data)
      }
    } catch (error) {
      console.error('❌ Failed to fetch user:', error)
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message
      })
      
      // Only clear token if it's a 401 (unauthorized) error from the auth endpoint
      // This means the token is definitely invalid/expired
      if (error.response?.status === 401) {
        const errorMessage = error.response?.data?.error || ''
        
        // Only clear if it's a clear authentication error, not other issues
        if (errorMessage.includes('token') || errorMessage.includes('expired') || errorMessage.includes('invalid')) {
          console.log('⚠️ Token invalid/expired (401), clearing auth state')
          localStorage.removeItem('token')
          setToken(null)
          setUser(null)
          delete axios.defaults.headers.common['Authorization']
        } else {
          console.log('⚠️ 401 error but keeping token - might be temporary:', errorMessage)
          // Keep token - might be a temporary backend issue
        }
      } else if (error.response?.status === 403) {
        console.log('⚠️ Access forbidden (403), but keeping token')
        // Don't clear token for 403, just don't set user
      } else if (!error.response) {
        console.log('⚠️ Network error (no response), keeping token:', error.message)
        // Network error - don't clear token, might be temporary
      } else {
        console.log('⚠️ Other error, keeping token:', error.response.status, error.message)
        // Other errors - don't clear token
      }
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      const { access_token, user } = response.data
      
      // Store token in localStorage for persistence
      localStorage.setItem('token', access_token)
      
      // Update state
      setToken(access_token)
      setUser(user)
      
      // Set axios default header for all future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      console.log('Login successful, token stored')
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/api/auth/register', userData)
      const { access_token, user } = response.data
      
      // Store token in localStorage for persistence
      localStorage.setItem('token', access_token)
      
      // Update state
      setToken(access_token)
      setUser(user)
      
      // Set axios default header for all future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      console.log('Registration successful, token stored')
      return { success: true }
    } catch (error) {
      console.error('Registration error:', error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    // Clear localStorage
    localStorage.removeItem('token')
    
    // Clear state
    setToken(null)
    setUser(null)
    
    // Remove axios header
    delete axios.defaults.headers.common['Authorization']
    
    console.log('Logged out, token cleared')
  }

  const updateUserProfile = (updatedUser) => {
    setUser((prev) => ({
      ...(prev || {}),
      ...updatedUser
    }))
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUserProfile,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    isEditor: user?.role === 'editor' || user?.role === 'admin'
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

