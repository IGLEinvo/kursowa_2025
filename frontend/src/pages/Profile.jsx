import React, { useState, useEffect } from 'react'
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Divider,
  Alert
} from '@mui/material'
import { usersApi, subscriptionsApi, preferencesApi, newsApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'

const Profile = () => {
  const { user: authUser, updateUserProfile } = useAuth()
  const [user, setUser] = useState(null)
  const [subscription, setSubscription] = useState(null)
  const [categories, setCategories] = useState([])
  const [favoriteCategories, setFavoriteCategories] = useState([])
  const [formData, setFormData] = useState({
    username: authUser?.username || '',
    first_name: authUser?.first_name || '',
    last_name: authUser?.last_name || ''
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  useEffect(() => {
    // When component mounts or auth user changes, prefill form and refresh data from API
    if (authUser) {
      setFormData((prev) => ({
        ...prev,
        username: authUser.username || '',
        first_name: authUser.first_name || '',
        last_name: authUser.last_name || ''
      }))
    }

    fetchProfile()
    fetchSubscription()
    fetchCategories()
    fetchFavoriteCategories()
  }, [authUser])

  const fetchProfile = async () => {
    try {
      // Check if user is authenticated before making request
      if (!authUser) {
        setLoading(false)
        return
      }
      
      const response = await usersApi.getProfile()
      setUser(response.data.user)
      setFormData({
        username: response.data.user.username,
        first_name: response.data.user.first_name || '',
        last_name: response.data.user.last_name || ''
      })
    } catch (error) {
      console.error('Failed to fetch profile:', error)
      if (error.response?.status === 401) {
        console.error('Unauthorized - token may be invalid or expired')
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchSubscription = async () => {
    try {
      // Check if user is authenticated before making request
      if (!authUser) {
        return
      }
      
      const response = await subscriptionsApi.getUserSubscription()
      setSubscription(response.data.subscription)
    } catch (error) {
      console.error('Failed to fetch subscription:', error)
      if (error.response?.status === 401) {
        console.error('Unauthorized - token may be invalid or expired')
      }
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await newsApi.getCategories()
      setCategories(response.data.categories || [])
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const fetchFavoriteCategories = async () => {
    try {
      if (!authUser) return
      
      const response = await preferencesApi.getFavoriteCategories()
      console.log('Favorite categories response:', response.data)
      
      // The API returns { favorite_categories: [...], count: N }
      // Each favorite is a category object with id field
      const favorites = response.data?.favorite_categories || []
      const favoriteIds = favorites
        .map(f => {
          // Extract category ID from the response
          if (typeof f === 'object' && f !== null) {
            return f.id || f.category_id
          }
          return null
        })
        .filter(id => id !== undefined && id !== null && id !== '')
      
      console.log('Loaded favorite category IDs:', favoriteIds)
      console.log('Total categories:', categories.length)
      setFavoriteCategories(favoriteIds)
    } catch (error) {
      console.error('Failed to fetch favorite categories:', error)
      console.error('Error details:', error.response?.data)
      setFavoriteCategories([])
    }
  }

  const handleCategoryToggle = async (categoryId) => {
    try {
      const isFavorite = favoriteCategories.includes(categoryId)
      console.log(`Toggling category ${categoryId}, currently favorite: ${isFavorite}`)
      
      if (isFavorite) {
        const response = await preferencesApi.removeFavoriteCategory(categoryId)
        console.log('Remove favorite response:', response.data)
        setFavoriteCategories(prev => {
          const updated = prev.filter(id => id !== categoryId)
          console.log('Removed favorite, new list:', updated)
          return updated
        })
      } else {
        const response = await preferencesApi.addFavoriteCategory(categoryId)
        console.log('Add favorite response:', response.data)
        setFavoriteCategories(prev => {
          const updated = [...prev, categoryId]
          console.log('Added favorite, new list:', updated)
          return updated
        })
      }
    } catch (error) {
      console.error('Failed to update favorite category:', error)
      console.error('Error response:', error.response)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to update favorite category'
      alert(errorMsg)
      
      // If 422 error, it might be a validation issue - check token
      if (error.response?.status === 422) {
        console.error('422 Validation Error - Token might be invalid. Please try logging in again.')
      }
    }
  }

  const handleUpdate = async () => {
    try {
      setError(null)
      setSuccess(null)
      
      const response = await usersApi.updateProfile(formData)
      const updatedUser = response.data.user

      // Update local state
      setUser(updatedUser)
      setFormData({
        username: updatedUser.username,
        first_name: updatedUser.first_name || '',
        last_name: updatedUser.last_name || ''
      })

      // Update global auth state so navbar and other parts reflect changes
      updateUserProfile(updatedUser)

      setSuccess('Profile updated successfully!')
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      console.error('Failed to update profile:', error)
      const errorMsg = error.response?.data?.error || 'Failed to update profile'
      setError(errorMsg)
      setTimeout(() => setError(null), 5000)
    }
  }

  if (loading) return <Typography>Loading...</Typography>

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <Paper sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Profile Settings
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mt: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mt: 2 }} onClose={() => setSuccess(null)}>
              {success}
            </Alert>
          )}
          <Box sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            />
            <TextField
              fullWidth
              label="Email"
              margin="normal"
              value={user?.email || authUser?.email || ''}
              disabled
            />
            <TextField
              fullWidth
              label="First Name"
              margin="normal"
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            />
            <TextField
              fullWidth
              label="Last Name"
              margin="normal"
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            />
            <Button
              variant="contained"
              onClick={handleUpdate}
              sx={{ mt: 2 }}
            >
              Update Profile
            </Button>
          </Box>
          
          <Divider sx={{ my: 4 }} />
          
          <Typography variant="h5" gutterBottom>
            Favorite Categories
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Select your favorite categories to personalize your news feed and get better recommendations.
          </Typography>
          <FormGroup>
            {categories.length === 0 ? (
              <Typography variant="body2" color="text.secondary">
                Loading categories...
              </Typography>
            ) : (
              categories.map((category) => {
                const isChecked = favoriteCategories.includes(category.id)
                return (
                  <FormControlLabel
                    key={category.id}
                    control={
                      <Checkbox
                        checked={isChecked}
                        onChange={() => handleCategoryToggle(category.id)}
                      />
                    }
                    label={category.name}
                  />
                )
              })
            )}
          </FormGroup>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Subscription
            </Typography>
            {subscription ? (
              <Box>
                <Typography variant="body1">
                  {subscription.tier_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Expires: {new Date(subscription.end_date).toLocaleDateString()}
                </Typography>
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No active subscription
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  )
}

export default Profile

