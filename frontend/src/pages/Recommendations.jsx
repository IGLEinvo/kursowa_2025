import React, { useState, useEffect } from 'react'
import {
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip,
  IconButton,
  Alert,
  CircularProgress
} from '@mui/material'
import { Refresh } from '@mui/icons-material'
import { Link, useLocation } from 'react-router-dom'
import { Favorite, Bookmark } from '@mui/icons-material'
import { newsApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'
import { format } from 'date-fns'

const Recommendations = () => {
  const { isAuthenticated } = useAuth()
  const location = useLocation()
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (isAuthenticated) {
      fetchRecommendations()
    } else {
      setError('Please login to see personalized recommendations')
      setLoading(false)
    }
    // Refresh when route changes (user navigates to this page)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated, location.pathname])

  const fetchRecommendations = async () => {
    try {
      setLoading(true)
      setError(null)
      console.log('Fetching recommendations...')
      const response = await newsApi.getRecommended(10)
      console.log('Recommendations response:', response.data)
      
      if (response.data && response.data.articles) {
        setArticles(response.data.articles)
        console.log('Articles loaded:', response.data.articles.length)
        if (response.data.articles.length === 0) {
          setError('No recommendations available yet. Start reading and liking articles!')
        }
      } else {
        console.warn('Unexpected response format:', response.data)
        setArticles([])
        setError('No recommendations available yet.')
      }
    } catch (error) {
      console.error('Failed to fetch recommendations:', error)
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      })
      
      // Handle 401 errors - token invalid/expired
      if (error.response?.status === 401) {
        const errorMsg = error.response?.data?.error || 'Your session has expired. Please login again.'
        setError(errorMsg)
        // The API interceptor will clear the token and dispatch event
        // AuthContext will handle the redirect
      } else {
        const errorMsg = error.response?.data?.error || error.message || 'Failed to load recommendations'
        setError(errorMsg)
      }
      setArticles([])
    } finally {
      setLoading(false)
    }
  }

  const handleLike = async (articleId) => {
    if (!isAuthenticated) {
      alert('Please login to like articles')
      return
    }
    try {
      const response = await newsApi.likeArticle(articleId)
      const isLiked = response.data?.liked || false
      
      // Update the article in the list immediately
      setArticles(prevArticles => 
        prevArticles.map(article => {
          if (article.id === articleId) {
            const currentCount = article.likes_count || 0
            return {
              ...article,
              is_liked: isLiked,
              likes_count: isLiked ? currentCount + 1 : Math.max(0, currentCount - 1)
            }
          }
          return article
        })
      )
    } catch (error) {
      console.error('Failed to like article:', error)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to like article. Please try again.'
      alert(errorMsg)
    }
  }

  const handleSave = async (articleId) => {
    if (!isAuthenticated) {
      alert('Please login to save articles')
      return
    }
    try {
      const response = await newsApi.saveArticle(articleId)
      const isSaved = response.data?.saved || false
      
      // Update the article in the list immediately
      setArticles(prevArticles => 
        prevArticles.map(article => {
          if (article.id === articleId) {
            return {
              ...article,
              is_saved: isSaved
            }
          }
          return article
        })
      )
    } catch (error) {
      console.error('Failed to save article:', error)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to save article. Please try again.'
      alert(errorMsg)
    }
  }

  if (!isAuthenticated) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Alert severity="info" sx={{ mb: 2 }}>
          Please login to see personalized recommendations based on your interests and reading history.
        </Alert>
      </Box>
    )
  }

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Typography>Loading recommendations...</Typography>
      </Box>
    )
  }

  if (error && articles.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={fetchRecommendations}>
          Try Again
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Personalized Recommendations
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Articles tailored to your interests based on your views, likes, and favorite categories.
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={loading ? <CircularProgress size={20} /> : <Refresh />}
          onClick={fetchRecommendations}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>
      
      {error && (
        <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {articles.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6" gutterBottom>
            No recommendations yet
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Start reading articles and liking them to get personalized recommendations!
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {articles.map((article) => (
            <Grid item xs={12} md={6} lg={4} key={article.id}>
              <Card sx={{ position: 'relative' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', gap: 1, mb: 1, flexWrap: 'wrap' }}>
                    {article.is_breaking && (
                      <Chip label="BREAKING" color="error" size="small" />
                    )}
                    {article.is_premium && (
                      <Chip label="PREMIUM" color="warning" size="small" />
                    )}
                  </Box>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {article.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {article.excerpt}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {article.author?.username || 'Unknown'} •{' '}
                    {article.published_at
                      ? format(new Date(article.published_at), 'MMM d, yyyy')
                      : 'Draft'}
                  </Typography>
                  <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                    <Typography variant="caption">
                      👁️ {article.views_count}
                    </Typography>
                    <Typography variant="caption">
                      ❤️ {article.likes_count}
                    </Typography>
                  </Box>
                </CardContent>
                <CardActions>
                  <Button size="small" component={Link} to={`/news/${article.id}`}>
                    Read More
                  </Button>
                  {isAuthenticated && (
                    <>
                      <IconButton
                        size="small"
                        onClick={() => handleLike(article.id)}
                        sx={{
                          color: article.is_liked ? 'error.main' : 'text.secondary',
                          '&:hover': {
                            color: 'error.main'
                          }
                        }}
                      >
                        <Favorite sx={{ fill: article.is_liked ? 'currentColor' : 'none', stroke: 'currentColor', strokeWidth: 1.5 }} />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleSave(article.id)}
                        sx={{
                          color: article.is_saved ? 'primary.main' : 'text.secondary',
                          '&:hover': {
                            color: 'primary.main'
                          }
                        }}
                      >
                        <Bookmark sx={{ fill: article.is_saved ? 'currentColor' : 'none', stroke: 'currentColor', strokeWidth: 1.5 }} />
                      </IconButton>
                    </>
                  )}
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
}

export default Recommendations
