import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box
} from '@mui/material'
import { usersApi } from '../api/api'
import { format } from 'date-fns'

const SavedArticles = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSavedArticles()
  }, [])

  const fetchSavedArticles = async () => {
    try {
      const response = await usersApi.getSavedArticles()
      setArticles(response.data.articles)
    } catch (error) {
      console.error('Failed to fetch saved articles:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <Typography>Loading...</Typography>

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Saved Articles
      </Typography>
      {articles.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          No saved articles yet
        </Typography>
      ) : (
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {articles.map((article) => (
            <Grid item xs={12} md={6} key={article.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {article.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {article.excerpt}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {article.published_at
                      ? format(new Date(article.published_at), 'MMM d, yyyy')
                      : 'Draft'}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" component={Link} to={`/news/${article.id}`}>
                    Read More
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
}

export default SavedArticles

