import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Navbar from './components/Layout/Navbar'
import Home from './pages/Home'
import ArticleDetail from './pages/ArticleDetail'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import SavedArticles from './pages/SavedArticles'
import AdminPanel from './pages/AdminPanel'
import Recommendations from './pages/Recommendations'
import Subscription from './pages/Subscription'
import { Container, Box, CircularProgress, Typography } from '@mui/material'

function AppContent() {
  const { loading } = useAuth()

  // Show loading screen while checking authentication
  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          gap: 2
        }}
      >
        <CircularProgress />
        <Typography variant="body2" color="text.secondary">
          Loading...
        </Typography>
      </Box>
    )
  }

  return (
    <>
      <Navbar />
      <Container maxWidth="xl" sx={{ mt: { xs: 2, sm: 4 }, mb: 4, px: { xs: 2, sm: 3 } }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news/:id" element={<ArticleDetail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/saved" element={<SavedArticles />} />
          <Route path="/subscription" element={<Subscription />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
    </>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

