import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  Typography,
  Box,
  Paper,
  Button,
  TextField,
  IconButton,
  Divider,
  Chip
} from '@mui/material'
import { Favorite, Bookmark, Send } from '@mui/icons-material'
import { newsApi, commentsApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'
import { format } from 'date-fns'

const ArticleDetail = () => {
  const { id } = useParams()
  const { isAuthenticated } = useAuth()
  const [article, setArticle] = useState(null)
  const [comments, setComments] = useState([])
  const [commentText, setCommentText] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (id) {
      fetchArticle()
      fetchComments()
    } else {
      setError('Invalid article ID')
      setLoading(false)
    }
  }, [id])

  const fetchArticle = async () => {
    try {
      setLoading(true)
      setError(null)
      console.log('Fetching article with ID:', id, 'Type:', typeof id)
      
      const articleId = parseInt(id, 10)
      if (isNaN(articleId)) {
        throw new Error('Invalid article ID')
      }
      
      const response = await newsApi.getArticle(articleId)
      console.log('Article response:', response.data)
      
      if (response && response.data) {
        if (response.data.article) {
          setArticle(response.data.article)
          console.log('Article loaded successfully:', response.data.article.title)
        } else if (response.data.error) {
          console.error('API returned error:', response.data.error)
          setError(response.data.error)
          setArticle(null)
        } else {
          console.error('Invalid response format - no article or error:', response.data)
          setError('Invalid response from server')
          setArticle(null)
        }
      } else {
        console.error('Invalid response - no data:', response)
        setError('No data received from server')
        setArticle(null)
      }
    } catch (error) {
      console.error('Failed to fetch article:', error)
      console.error('Error response:', error.response?.data)
      console.error('Error status:', error.response?.status)
      console.error('Error message:', error.message)
      
      if (error.response?.status === 404) {
        setError('Article not found')
      } else if (error.response?.status === 403) {
        setError('Premium subscription required to view this article')
      } else if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
        setError('Cannot connect to server. Please make sure the backend is running on port 5001.')
      } else {
        const errorMsg = error.response?.data?.error || error.message || 'Failed to load article'
        setError(errorMsg)
        console.error('Full error object:', error)
        console.error('Error config:', error.config)
        console.error('Error request URL:', error.config?.url)
        console.error('Error response data:', JSON.stringify(error.response?.data, null, 2))
      }
      setArticle(null)
    } finally {
      setLoading(false)
    }
  }

  const fetchComments = async () => {
    try {
      const response = await commentsApi.getComments(id)
      setComments(response.data.comments)
    } catch (error) {
      console.error('Failed to fetch comments:', error)
    }
  }

  const handleSubmitComment = async () => {
    if (!commentText.trim()) return
    
    try {
      await commentsApi.createComment(id, commentText)
      setCommentText('')
      fetchComments()
    } catch (error) {
      console.error('Failed to post comment:', error)
      alert('Failed to post comment')
    }
  }

  const handleLike = async () => {
    if (!isAuthenticated) {
      alert('Please login to like articles')
      return
    }
    try {
      const response = await newsApi.likeArticle(id)
      const isLiked = response.data?.liked || false
      const currentCount = article.likes_count || 0
      
      // Update article immediately
      setArticle(prevArticle => ({
        ...prevArticle,
        is_liked: isLiked,
        likes_count: isLiked ? currentCount + 1 : Math.max(0, currentCount - 1)
      }))
    } catch (error) {
      console.error('Failed to like article:', error)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to like article. Please try again.'
      alert(errorMsg)
    }
  }

  const handleSave = async () => {
    if (!isAuthenticated) {
      alert('Please login to save articles')
      return
    }
    try {
      const response = await newsApi.saveArticle(id)
      const isSaved = response.data?.saved || false
      
      // Update article immediately
      setArticle(prevArticle => ({
        ...prevArticle,
        is_saved: isSaved
      }))
    } catch (error) {
      console.error('Failed to save article:', error)
      const errorMsg = error.response?.data?.error || error.message || 'Failed to save article. Please try again.'
      alert(errorMsg)
    }
  }

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Typography>Loading...</Typography>
      </Box>
    )
  }
  
  if (!article && !loading) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Typography variant="h5" gutterBottom color="error">
          {error || 'Article not found'}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {error === 'Premium subscription required to view this article' 
            ? 'This article is available for premium subscribers only.'
            : "The article you're looking for doesn't exist or has been removed."}
        </Typography>
        <Button component={Link} to="/" variant="contained" sx={{ mt: 2 }}>
          Back to Home
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Paper sx={{ p: 4, mb: 4 }}>
        <Box sx={{ mb: 2 }}>
          {article.is_breaking && (
            <Chip label="BREAKING" color="error" size="small" sx={{ mr: 1 }} />
          )}
          {article.is_premium && (
            <Chip label="PREMIUM" color="warning" size="small" />
          )}
        </Box>
        <Typography variant="h3" component="h1" gutterBottom>
          {article.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          By {article.author?.username || 'Unknown'} •{' '}
          {article.published_at
            ? format(new Date(article.published_at), 'MMMM d, yyyy')
            : 'Draft'}
        </Typography>
        <Box sx={{ mt: 2, mb: 3, display: 'flex', gap: 2, alignItems: 'center' }}>
          {isAuthenticated ? (
            <>
              <IconButton 
                onClick={handleLike}
                sx={{
                  color: article.is_liked ? 'error.main' : 'text.secondary',
                  '&:hover': {
                    color: 'error.main'
                  }
                }}
              >
                <Favorite sx={{ fill: article.is_liked ? 'currentColor' : 'none', stroke: 'currentColor', strokeWidth: 1.5 }} />
              </IconButton>
              <Typography variant="body2" sx={{ mr: 1 }}>
                {article.likes_count || 0}
              </Typography>
              <IconButton 
                onClick={handleSave}
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
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Favorite sx={{ color: 'text.secondary' }} /> 
              <Typography variant="body2">{article.likes_count}</Typography>
            </Box>
          )}
          <Typography variant="body2" sx={{ ml: 1 }}>
            {article.views_count} views
          </Typography>
        </Box>
        <Divider sx={{ my: 3 }} />
        <Typography variant="body1" paragraph sx={{ whiteSpace: 'pre-wrap' }}>
          {article.content}
        </Typography>
      </Paper>

      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Comments ({comments.length})
        </Typography>
        
        {isAuthenticated ? (
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              multiline
              rows={3}
              placeholder="Write a comment..."
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              startIcon={<Send />}
              onClick={handleSubmitComment}
            >
              Post Comment
            </Button>
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Please login to comment
          </Typography>
        )}

        <Divider sx={{ my: 2 }} />

        {comments.map((comment) => (
          <Box key={comment.id} sx={{ mb: 3 }}>
            <Typography variant="subtitle2" fontWeight="bold">
              {comment.username}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {format(new Date(comment.created_at), 'MMM d, yyyy h:mm a')}
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              {comment.content}
            </Typography>
            {comment.replies && comment.replies.length > 0 && (
              <Box sx={{ ml: 4, mt: 2 }}>
                {comment.replies.map((reply) => (
                  <Box key={reply.id} sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {reply.username}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(reply.created_at), 'MMM d, yyyy h:mm a')}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {reply.content}
                    </Typography>
                  </Box>
                ))}
              </Box>
            )}
            <Divider sx={{ mt: 2 }} />
          </Box>
        ))}
      </Paper>
    </Box>
  )
}

export default ArticleDetail

