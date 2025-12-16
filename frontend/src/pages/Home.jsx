import React, { useState, useEffect } from 'react'
import {
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  IconButton,
  CircularProgress
} from '@mui/material'
import { Link } from 'react-router-dom'
import { Favorite, Bookmark } from '@mui/icons-material'
import { newsApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'
import { format } from 'date-fns'

const Home = () => {
  const { isAuthenticated } = useAuth()
  const [articles, setArticles] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [categoriesLoading, setCategoriesLoading] = useState(true)

  // Initialize: reset filters and fetch categories on page load
  useEffect(() => {
    // Reset all filters on page load
    setSelectedCategory('')
    setSearchQuery('')
    setArticles([])
    
    // Fetch categories first
    setCategoriesLoading(true)
    fetchCategories().then(() => {
      setCategoriesLoading(false)
      // Fetch news after categories are loaded
      fetchNews()
    }).catch(() => {
      setCategoriesLoading(false)
      // Still try to fetch news even if categories fail
      fetchNews()
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Fetch news when category selection changes
  useEffect(() => {
    // Only fetch if categories have finished loading (or if no category selected)
    if (!categoriesLoading) {
      fetchNews()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCategory])

  const fetchCategories = async () => {
    try {
      const response = await newsApi.getCategories()
      if (response.data && response.data.categories) {
        setCategories(response.data.categories)
        console.log('Categories loaded:', response.data.categories.length)
        return true
      } else {
        console.error('Invalid response format:', response.data)
        setCategories([])
        return false
      }
    } catch (error) {
      console.error('Failed to fetch categories:', error)
      console.error('Error details:', error.response?.data || error.message)
      // Set empty array on error to prevent UI issues
      setCategories([])
      return false
    }
  }

  const fetchNews = async () => {
    try {
      setLoading(true)
      const params = { page: 1, limit: 20 }
      
      // Only filter by category if we have categories loaded and a valid selection
      if (selectedCategory && categories.length > 0) {
        const category = categories.find(c => c.slug === selectedCategory || c.id === selectedCategory)
        if (category) {
          params.category_id = category.id
        } else {
          // Invalid category selection, reset it
          console.warn('Invalid category selected, resetting filter')
          setSelectedCategory('')
        }
      }
      
      const response = await newsApi.getNews(params)
      if (response.data && response.data.articles) {
        setArticles(response.data.articles)
        console.log('Articles loaded:', response.data.articles.length)
      } else {
        console.error('Invalid response format:', response.data)
        setArticles([])
      }
    } catch (error) {
      console.error('Failed to fetch news:', error)
      console.error('Error details:', error.response?.data || error.message)
      setArticles([])
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchNews()
      return
    }
    
    try {
      setLoading(true)
      const response = await newsApi.searchNews(searchQuery)
      setArticles(response.data.articles)
    } catch (error) {
      console.error('Search failed:', error)
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
      console.log('Liking article:', articleId)
      const response = await newsApi.likeArticle(articleId)
      console.log('Like response:', response.data)
      
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
      console.error('Error response:', error.response)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to like article. Please try again.'
      
      // If 422 error, it might be a validation issue - check token
      if (error.response?.status === 422) {
        console.error('422 Validation Error - Token might be invalid. Please try logging in again.')
        alert('Your session may have expired. Please refresh the page and try again.')
        return
      }
      
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

  return (
    <Box>
      {/* Hero Section with Search */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: 4,
          p: 6,
          mb: 6,
          color: 'white',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        }}
      >
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: 700, mb: 2, textAlign: 'center' }}
        >
          Discover Latest News
        </Typography>
        <Typography
          variant="h6"
          sx={{ mb: 4, textAlign: 'center', opacity: 0.9, fontWeight: 400 }}
        >
          Stay informed with the most relevant stories from around the world
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', maxWidth: 900, mx: 'auto' }}>
          <TextField
            placeholder="Search articles, authors, topics..."
            variant="outlined"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            sx={{
              flexGrow: 1,
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              borderRadius: 3,
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  border: 'none',
                },
                '&:hover fieldset': {
                  border: 'none',
                },
                '&.Mui-focused fieldset': {
                  border: '2px solid rgba(255,255,255,0.5)',
                },
              },
            }}
            InputProps={{
              sx: { py: 1, px: 2 },
            }}
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            sx={{
              px: 4,
              py: 1.5,
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              backdropFilter: 'blur(10px)',
              color: 'white',
              fontWeight: 600,
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.3)',
              },
            }}
          >
            Search
          </Button>
          <FormControl
            sx={{
              minWidth: 200,
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              borderRadius: 3,
            }}
            disabled={categoriesLoading}
          >
            <InputLabel>Category</InputLabel>
            <Select
              value={selectedCategory}
              label="Category"
              onChange={(e) => setSelectedCategory(e.target.value)}
              sx={{
                '& .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  border: 'none',
                },
              }}
            >
              <MenuItem value="">All Categories</MenuItem>
              {categories.map((cat) => (
                <MenuItem key={cat.id} value={cat.slug}>
                  {cat.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Box>

      {loading ? (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            py: 8,
          }}
        >
          <CircularProgress size={60} thickness={4} />
          <Typography variant="h6" sx={{ mt: 3, color: 'text.secondary' }}>
            Loading articles...
          </Typography>
        </Box>
      ) : articles.length === 0 ? (
        <Box
          sx={{
            textAlign: 'center',
            py: 8,
            px: 3,
            borderRadius: 4,
            backgroundColor: 'background.paper',
            boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
          }}
        >
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
            No articles found
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500, mx: 'auto' }}>
            {selectedCategory
              ? `No articles in this category. Try selecting a different category.`
              : 'No articles available at the moment. Check back later for updates!'}
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={4}>
          {articles.map((article) => (
            <Grid item xs={12} sm={6} lg={4} key={article.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  overflow: 'hidden',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 40px rgba(0,0,0,0.15)',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1, pb: 1 }}>
                  <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                    {article.is_breaking && (
                      <Chip
                        label="BREAKING"
                        color="error"
                        size="small"
                        sx={{ fontWeight: 600, borderRadius: 2 }}
                      />
                    )}
                    {article.is_premium && (
                      <Chip
                        label="PREMIUM"
                        color="warning"
                        size="small"
                        sx={{ fontWeight: 600, borderRadius: 2 }}
                      />
                    )}
                  </Box>
                  <Typography
                    variant="h6"
                    component="h2"
                    gutterBottom
                    sx={{
                      fontWeight: 600,
                      mb: 2,
                      lineHeight: 1.3,
                      color: 'text.primary',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                    }}
                  >
                    {article.title}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    paragraph
                    sx={{
                      mb: 2,
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                      lineHeight: 1.6,
                    }}
                  >
                    {article.excerpt}
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      mb: 2,
                      flexWrap: 'wrap',
                      gap: 1,
                    }}
                  >
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ fontWeight: 500 }}
                    >
                      {article.author?.username || 'Unknown'} •{' '}
                      {article.published_at
                        ? format(new Date(article.published_at), 'MMM d, yyyy')
                        : 'Draft'}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Typography
                        variant="caption"
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
                      >
                        👁️ {article.views_count || 0}
                      </Typography>
                      <Typography
                        variant="caption"
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
                      >
                        ❤️ {article.likes_count || 0}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
                <CardActions
                  sx={{
                    px: 2,
                    pb: 2,
                    pt: 1,
                    justifyContent: 'space-between',
                    borderTop: '1px solid',
                    borderColor: 'divider',
                  }}
                >
                  <Button
                    component={Link}
                    to={`/news/${article.id}`}
                    variant="contained"
                    size="small"
                    sx={{
                      textTransform: 'none',
                      fontWeight: 600,
                      borderRadius: 2,
                      px: 3,
                    }}
                  >
                    Read More
                  </Button>
                  {isAuthenticated && (
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleLike(article.id)}
                        sx={{
                          color: article.is_liked ? 'error.main' : 'text.secondary',
                          '&:hover': {
                            color: 'error.main',
                            backgroundColor: 'error.light',
                            backgroundColor: 'rgba(234, 67, 53, 0.1)',
                          },
                        }}
                      >
                        <Favorite
                          sx={{
                            fill: article.is_liked ? 'currentColor' : 'none',
                            stroke: 'currentColor',
                            strokeWidth: 1.5,
                          }}
                        />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleSave(article.id)}
                        sx={{
                          color: article.is_saved ? 'primary.main' : 'text.secondary',
                          '&:hover': {
                            color: 'primary.main',
                            backgroundColor: 'rgba(26, 115, 232, 0.1)',
                          },
                        }}
                      >
                        <Bookmark
                          sx={{
                            fill: article.is_saved ? 'currentColor' : 'none',
                            stroke: 'currentColor',
                            strokeWidth: 1.5,
                          }}
                        />
                      </IconButton>
                    </Box>
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

export default Home

