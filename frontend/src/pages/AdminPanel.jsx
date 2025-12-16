import React, { useState, useEffect } from 'react'
import {
  Typography,
  Box,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material'
import { adminApi } from '../api/api'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

const AdminPanel = () => {
  const { isAdmin, isEditor } = useAuth()
  const navigate = useNavigate()
  const [tab, setTab] = useState(0)
  const [articles, setArticles] = useState([])
  const [users, setUsers] = useState([])
  const [editDialog, setEditDialog] = useState({ open: false, article: null })

  useEffect(() => {
    if (!isEditor) {
      navigate('/')
      return
    }
    fetchArticles()
    if (isAdmin) {
      fetchUsers()
    }
  }, [isEditor, isAdmin])

  const fetchArticles = async () => {
    try {
      const response = await adminApi.listArticles({ page: 1, limit: 50 })
      setArticles(response.data.articles)
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await adminApi.listUsers({ page: 1, limit: 50 })
      setUsers(response.data.users)
    } catch (error) {
      console.error('Failed to fetch users:', error)
    }
  }

  const handleUpdateArticle = async () => {
    try {
      await adminApi.updateArticle(editDialog.article.id, editDialog.article)
      setEditDialog({ open: false, article: null })
      fetchArticles()
    } catch (error) {
      console.error('Failed to update article:', error)
    }
  }

  const handleDeleteArticle = async (id) => {
    if (!window.confirm('Are you sure you want to delete this article?')) return
    try {
      await adminApi.deleteArticle(id)
      fetchArticles()
    } catch (error) {
      console.error('Failed to delete article:', error)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Admin Panel
      </Typography>
      <Tabs value={tab} onChange={(e, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab label="Articles" />
        {isAdmin && <Tab label="Users" />}
      </Tabs>

      {tab === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Author</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {articles.map((article) => (
                <TableRow key={article.id}>
                  <TableCell>{article.title}</TableCell>
                  <TableCell>{article.status}</TableCell>
                  <TableCell>{article.author_id}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      onClick={() => setEditDialog({ open: true, article })}
                    >
                      Edit
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDeleteArticle(article.id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {tab === 1 && isAdmin && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Username</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Role</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.role}</TableCell>
                  <TableCell>{user.is_active ? 'Active' : 'Inactive'}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      onClick={async () => {
                        await adminApi.toggleUserActive(user.id)
                        fetchUsers()
                      }}
                    >
                      Toggle Active
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Dialog
        open={editDialog.open}
        onClose={() => setEditDialog({ open: false, article: null })}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Article</DialogTitle>
        <DialogContent>
          {editDialog.article && (
            <Box sx={{ pt: 2 }}>
              <TextField
                fullWidth
                label="Title"
                value={editDialog.article.title}
                onChange={(e) =>
                  setEditDialog({
                    ...editDialog,
                    article: { ...editDialog.article, title: e.target.value }
                  })
                }
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                multiline
                rows={10}
                label="Content"
                value={editDialog.article.content}
                onChange={(e) =>
                  setEditDialog({
                    ...editDialog,
                    article: { ...editDialog.article, content: e.target.value }
                  })
                }
                sx={{ mb: 2 }}
              />
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Status</InputLabel>
                <Select
                  value={editDialog.article.status}
                  label="Status"
                  onChange={(e) =>
                    setEditDialog({
                      ...editDialog,
                      article: { ...editDialog.article, status: e.target.value }
                    })
                  }
                >
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="published">Published</MenuItem>
                  <MenuItem value="archived">Archived</MenuItem>
                </Select>
              </FormControl>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialog({ open: false, article: null })}>
            Cancel
          </Button>
          <Button onClick={handleUpdateArticle} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default AdminPanel

